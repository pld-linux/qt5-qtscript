#
# Conditional build:
%bcond_without	qch	# documentation in QCH format

%define		orgname		qtscript
%define		qtbase_ver	%{version}
%define		qttools_ver	%{version}
Summary:	The Qt5 Script libraries
Summary(pl.UTF-8):	Biblioteki Qt5 Script
Name:		qt5-%{orgname}
Version:	5.3.0
Release:	1
License:	LGPL v2.1 with Digia Qt LGPL Exception v1.1 or GPL v3.0
Group:		Libraries
Source0:	http://download.qt-project.org/official_releases/qt/5.3/%{version}/submodules/%{orgname}-opensource-src-%{version}.tar.xz
# Source0-md5:	4f755c8810946246adcfbaa74fafae62
URL:		http://qt-project.org/
BuildRequires:	OpenGL-devel
BuildRequires:	Qt5Core-devel >= %{qtbase_ver}
BuildRequires:	Qt5Gui-devel >= %{qtbase_ver}
BuildRequires:	Qt5Widgets-devel >= %{qtbase_ver}
%if %{with qch}
BuildRequires:	qt5-assistant = %{qttools_ver}
%endif
BuildRequires:	qt5-build >= %{qtbase_ver}
BuildRequires:	qt5-qmake >= %{qtbase_ver}
BuildRequires:	rpmbuild(macros) >= 1.654
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-strict-aliasing
%define		qt5dir		%{_libdir}/qt5

%description
Qt is a cross-platform application and UI framework. Using Qt, you can
write web-enabled applications once and deploy them across desktop,
mobile and embedded systems without rewriting the source code.

This package contains Qt5 Script libraries.

%description -l pl.UTF-8
Qt to wieloplatformowy szkielet aplikacji i interfejsów użytkownika.
Przy użyciu Qt można pisać aplikacje powiązane z WWW i wdrażać je w
systemach biurkowych, przenośnych i wbudowanych bez przepisywania kodu
źródłowego.

Ten pakiet zawiera biblioteki Qt5 Script.

%package -n Qt5Script
Summary:	The Qt5 Script libraries
Summary(pl.UTF-8):	Biblioteki Qt5 Script
Group:		Libraries
Requires:	Qt5Core >= %{qtbase_ver}
Requires:	Qt5Gui >= %{qtbase_ver}
Requires:	Qt5Widgets >= %{qtbase_ver}
Obsoletes:	qt5-qtscript

%description -n Qt5Script
Qt5 Script libraries provide classes for making Qt 5 applications
scriptable.

%description -n Qt5Script -l pl.UTF_8
Biblioteki Qt5 Script dostarczają klasy pozwalające na oskryptowanie
aplikacji Qt 5.

%package -n Qt5Script-devel
Summary:	Qt5 Script libraries - development files
Summary(pl.UTF-8):	Biblioteki Qt5 Script - pliki programistyczne
Group:		Development/Libraries
Requires:	OpenGL-devel
Requires:	Qt5Core-devel >= %{qtbase_ver}
Requires:	Qt5Gui-devel >= %{qtbase_ver}
Requires:	Qt5Script = %{version}-%{release}
Requires:	Qt5Widgets-devel >= %{qtbase_ver}
Obsoletes:	qt5-qtscript-devel

%description -n Qt5Script-devel
Qt5 Script libraries - development files.

%description -n Qt5Script-devel -l pl.UTF-8
Biblioteki Qt5 Script - pliki programistyczne.

%package doc
Summary:	Qt5 Script documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do bibliotek Qt5 Script w formacie HTML
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc
Qt5 Script documentation in HTML format.

%description doc -l pl.UTF-8
Dokumentacja do bibliotek Qt5 Script w formacie HTML.

%package doc-qch
Summary:	Qt5 Script documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do bibliotek Qt5 Script w formacie QCH
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc-qch
Qt5 Script documentation in QCH format.

%description doc-qch -l pl.UTF-8
Dokumentacja do bibliotek Qt5 Script w formacie QCH.

%package examples
Summary:	Qt5 Script examples
Summary(pl.UTF-8):	Przykłady do bibliotek Qt5 Script
Group:		X11/Development/Libraries
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description examples
Qt5 Script examples.

%description examples -l pl.UTF-8
Przykłady do bibliotek Qt5 Script.

%prep
%setup -q -n %{orgname}-opensource-src-%{version}

%build
qmake-qt5
%{__make}
%{__make} %{!?with_qch:html_}docs

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%{__make} install_%{!?with_qch:html_}docs \
	INSTALL_ROOT=$RPM_BUILD_ROOT

# kill unnecessary -L%{_libdir} from *.la, *.prl, *.pc
%{__sed} -i -e "s,-L%{_libdir} \?,,g" \
	$RPM_BUILD_ROOT%{_libdir}/*.{la,prl} \
	$RPM_BUILD_ROOT%{_pkgconfigdir}/*.pc

# useless symlinks
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.so.5.?
# actually drop *.la, follow policy of not packaging them when *.pc exist
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.la

# Prepare some files list
ifecho() {
	r="$RPM_BUILD_ROOT$2"
	if [ -d "$r" ]; then
		echo "%%dir $2" >> $1.files
	elif [ -x "$r" ] ; then
		echo "%%attr(755,root,root) $2" >> $1.files
	elif [ -f "$r" ]; then
		echo "$2" >> $1.files
	else
		echo "Error generation $1 files list!"
		echo "$r: no such file or directory!"
		return 1
	fi
}
ifecho_tree() {
	ifecho $1 $2
	for f in `find $RPM_BUILD_ROOT$2 -printf "%%P "`; do
		ifecho $1 $2/$f
	done
}

echo "%defattr(644,root,root,755)" > examples.files
ifecho_tree examples %{_examplesdir}/qt5/script

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n Qt5Script -p /sbin/ldconfig
%postun	-n Qt5Script -p /sbin/ldconfig

%files -n Qt5Script
%defattr(644,root,root,755)
%doc LGPL_EXCEPTION.txt dist/changes-*
%attr(755,root,root) %{_libdir}/libQt5Script.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Script.so.5
%attr(755,root,root) %{_libdir}/libQt5ScriptTools.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5ScriptTools.so.5

%files -n Qt5Script-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5Script.so
%attr(755,root,root) %{_libdir}/libQt5ScriptTools.so
%{_libdir}/libQt5Script.prl
%{_libdir}/libQt5ScriptTools.prl
%{_includedir}/qt5/QtScript
%{_includedir}/qt5/QtScriptTools
%{_pkgconfigdir}/Qt5Script.pc
%{_pkgconfigdir}/Qt5ScriptTools.pc
%{_libdir}/cmake/Qt5Script
%{_libdir}/cmake/Qt5ScriptTools
%{qt5dir}/mkspecs/modules/qt_lib_script.pri
%{qt5dir}/mkspecs/modules/qt_lib_script_private.pri
%{qt5dir}/mkspecs/modules/qt_lib_scripttools.pri
%{qt5dir}/mkspecs/modules/qt_lib_scripttools_private.pri

%files doc
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtscript
%{_docdir}/qt5-doc/qtscripttools

%if %{with qch}
%files doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtscript.qch
%{_docdir}/qt5-doc/qtscripttools.qch
%endif

%files examples -f examples.files
%defattr(644,root,root,755)
# XXX: dir shared with qt5-qtbase-examples
%dir %{_examplesdir}/qt5
