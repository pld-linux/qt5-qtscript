#
# Conditional build:
%bcond_without	examples	# examples packaging
%bcond_without	doc		# Documentation
%bcond_without	qm		# QM translations

%define		orgname		qtscript
%define		qtbase_ver	%{version}
%define		qttools_ver	%{version}
Summary:	The Qt5 Script libraries
Summary(pl.UTF-8):	Biblioteki Qt5 Script
Name:		qt5-%{orgname}
Version:	5.14.1
Release:	1
License:	LGPL v2.1 with Digia Qt LGPL Exception v1.1 or GPL v3.0
Group:		Libraries
Source0:	http://download.qt.io/official_releases/qt/5.14/%{version}/submodules/%{orgname}-everywhere-src-%{version}.tar.xz
# Source0-md5:	37a5b232f8c319c330f5882c0b8d5142
Source1:	http://download.qt.io/official_releases/qt/5.14/%{version}/submodules/qttranslations-everywhere-src-%{version}.tar.xz
# Source1-md5:	ef18bbad424173c3211c2ce0f4074485
URL:		http://www.qt.io/
BuildRequires:	OpenGL-devel
BuildRequires:	Qt5Core-devel >= %{qtbase_ver}
BuildRequires:	Qt5Gui-devel >= %{qtbase_ver}
BuildRequires:	Qt5Widgets-devel >= %{qtbase_ver}
%if %{with examples}
BuildRequires:	Qt5UiTools-devel >= %{qttools_ver}
%endif
%if %{with doc}
BuildRequires:	qt5-assistant >= %{qttools_ver}
%endif
BuildRequires:	qt5-build >= %{qtbase_ver}
%{?with_qm:BuildRequires:	qt5-linguist >= %{qttools_ver}}
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
Summary:	The Qt5 Script library
Summary(pl.UTF-8):	Biblioteka Qt5 Script
Group:		Libraries
Requires:	Qt5Core >= %{qtbase_ver}
Obsoletes:	qt5-qtscript

%description -n Qt5Script
Qt5 Script library provides classes for making Qt 5 applications
scriptable.

%description -n Qt5Script -l pl.UTF-8
Biblioteka Qt5 Script dostarcza klasy pozwalające na oskryptowanie
aplikacji Qt 5.

%package -n Qt5Script-devel
Summary:	Qt5 Script library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 Script - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt5Core-devel >= %{qtbase_ver}
Requires:	Qt5Script = %{version}-%{release}
Obsoletes:	qt5-qtscript-devel

%description -n Qt5Script-devel
Qt5 Script library - development files.

%description -n Qt5Script-devel -l pl.UTF-8
Biblioteka Qt5 Script - pliki programistyczne.

%package -n Qt5ScriptTools
Summary:	The Qt5 ScriptTools libraries
Summary(pl.UTF-8):	Biblioteki Qt5 ScriptTools
Group:		Libraries
Requires:	Qt5Gui >= %{qtbase_ver}
Requires:	Qt5Script = %{version}-%{release}
Requires:	Qt5Widgets >= %{qtbase_ver}

%description -n Qt5ScriptTools
Qt5 ScriptTools library provides additional components for
applications that use Qt5 Script.

%description -n Qt5ScriptTools -l pl.UTF-8
Biblioteki Qt5 ScriptTools dostarczaja dodatkowe komponenty dla
aplikacji wykorzystujących bibliotekę Qt5 Script.

%package -n Qt5ScriptTools-devel
Summary:	Qt5 ScriptTools library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 ScriptTools - pliki programistyczne
Group:		Development/Libraries
Requires:	OpenGL-devel
Requires:	Qt5Gui-devel >= %{qtbase_ver}
Requires:	Qt5Script-devel = %{version}-%{release}
Requires:	Qt5ScriptTools = %{version}-%{release}
Requires:	Qt5Widgets-devel >= %{qtbase_ver}

%description -n Qt5ScriptTools-devel
Qt5 ScriptTools library - development files.

%description -n Qt5ScriptTools-devel -l pl.UTF-8
Biblioteka Qt5 ScriptTools - pliki programistyczne.

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
%setup -q -n %{orgname}-everywhere-src-%{version} %{?with_qm:-a1}

%build
qmake-qt5
%{__make}
%{?with_doc:%{__make} doc}s

%if %{with qm}
cd qttranslations-everywhere-src-%{version}
qmake-qt5
%{__make}
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%if %{with doc}
%{__make} install_docs \
	INSTALL_ROOT=$RPM_BUILD_ROOT
%endif

%if %{with qm}
%{__make} -C qttranslations-everywhere-src-%{version} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT
# keep only qtscript
%{__rm} $RPM_BUILD_ROOT%{_datadir}/qt5/translations/{assistant,designer,linguist,qt,qtbase,qtconnectivity,qtdeclarative,qtlocation,qtmultimedia,qtquickcontrols,qtquickcontrols2,qtserialport,qtwebengine,qtwebsockets,qtxmlpatterns}_*.qm
%endif

# kill unnecessary -L%{_libdir} from *.la, *.prl, *.pc
%{__sed} -i -e "s,-L%{_libdir} \?,,g" \
	$RPM_BUILD_ROOT%{_libdir}/*.{la,prl} \
	$RPM_BUILD_ROOT%{_pkgconfigdir}/*.pc

# useless symlinks
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.so.5.??
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

# find_lang --with-qm supports only PLD qt3/qt4 specific %{_datadir}/locale/*/LC_MESSAGES layout
find_qt5_qm()
{
	name="$1"
	find $RPM_BUILD_ROOT%{_datadir}/qt5/translations -name "${name}_*.qm" | \
		sed -e "s:^$RPM_BUILD_ROOT::" \
		    -e 's:\(.*/'$name'_\)\([a-z][a-z][a-z]\?\)\(_[A-Z][A-Z]\)\?\(\.qm\)$:%lang(\2\3) \1\2\3\4:'
}

echo '%defattr(644,root,root,755)' > qtscript.lang
%if %{with qm}
find_qt5_qm qtscript >> qtscript.lang
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n Qt5Script -p /sbin/ldconfig
%postun	-n Qt5Script -p /sbin/ldconfig

%post	-n Qt5ScriptTools -p /sbin/ldconfig
%postun	-n Qt5ScriptTools -p /sbin/ldconfig

%files -n Qt5Script -f qtscript.lang
%defattr(644,root,root,755)
%doc LICENSE.GPL3-EXCEPT dist/changes-*
%attr(755,root,root) %{_libdir}/libQt5Script.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Script.so.5

%files -n Qt5Script-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5Script.so
%{_libdir}/libQt5Script.prl
%{_includedir}/qt5/QtScript
%{_pkgconfigdir}/Qt5Script.pc
%{_libdir}/cmake/Qt5Script
%{qt5dir}/mkspecs/modules/qt_lib_script.pri
%{qt5dir}/mkspecs/modules/qt_lib_script_private.pri

%files -n Qt5ScriptTools
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5ScriptTools.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5ScriptTools.so.5

%files -n Qt5ScriptTools-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5ScriptTools.so
%{_libdir}/libQt5ScriptTools.prl
%{_includedir}/qt5/QtScriptTools
%{_pkgconfigdir}/Qt5ScriptTools.pc
%{_libdir}/cmake/Qt5ScriptTools
%{qt5dir}/mkspecs/modules/qt_lib_scripttools.pri
%{qt5dir}/mkspecs/modules/qt_lib_scripttools_private.pri

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtscript
%{_docdir}/qt5-doc/qtscripttools

%files doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtscript.qch
%{_docdir}/qt5-doc/qtscripttools.qch
%endif

%if %{with examples}
%files examples -f examples.files
%defattr(644,root,root,755)
# XXX: dir shared with qt5-qtbase-examples
%dir %{_examplesdir}/qt5
%endif
