# TODO:
# - more BRs
# - cleanup

%define		orgname		qtscript
Summary:	The Qt5 Script
Name:		qt5-%{orgname}
Version:	5.3.0
Release:	0.2
License:	LGPL v2.1 or GPL v3.0
Group:		X11/Libraries
Source0:	http://download.qt-project.org/official_releases/qt/5.3/%{version}/submodules/%{orgname}-opensource-src-%{version}.tar.xz
# Source0-md5:	4f755c8810946246adcfbaa74fafae62
URL:		http://qt-project.org/
BuildRequires:	Qt5Core-devel = %{version}
BuildRequires:	qt5-assistant = %{version}
BuildRequires:	rpmbuild(macros) >= 1.654
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreqdep	libGL.so.1 libGLU.so.1
%define		_noautostrip	'.*_debug\\.so*'

%define		specflags	-fno-strict-aliasing
%define		_qtdir		%{_libdir}/qt5

%description
Qt5 Script libraries.

%package -n Qt5Script
Summary:	The Qt5 Script
Group:		X11/Libraries

%description -n Qt5Script
Qt5 Script libraries.

%package -n Qt5Script-devel
Summary:	The Qt5 Script - development files
Group:		X11/Development/Libraries
Requires:	Qt5Script = %{version}-%{release}

%description -n Qt5Script-devel
Qt5 Script - development files.

%package doc
Summary:	The Qt5 Script - docs
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc
Qt5 Script - documentation.

%package examples
Summary:	Qt5 Script examples
Group:		X11/Development/Libraries
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description examples
Qt5 Script - examples.

%prep
%setup -q -n %{orgname}-opensource-src-%{version}

%build
qmake-qt5
%{__make}
%{__make} docs

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%{__make} install_docs \
	INSTALL_ROOT=$RPM_BUILD_ROOT

# Prepare some files list
ifecho() {
	RESULT=`echo $RPM_BUILD_ROOT$2 2>/dev/null`
	[ "$RESULT" == "" ] && return # XXX this is never true due $RPM_BUILD_ROOT being set
	r=`echo $RESULT | awk '{ print $1 }'`

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

echo "%defattr(644,root,root,755)" > examples.files
ifecho examples %{_examplesdir}/qt5
for f in `find $RPM_BUILD_ROOT%{_examplesdir}/qt5 -printf "%%P "`; do
	ifecho examples %{_examplesdir}/qt5/$f
done

%clean
rm -rf $RPM_BUILD_ROOT

%post -n Qt5Script	-p /sbin/ldconfig
%postun -n Qt5Script	-p /sbin/ldconfig

%files -n Qt5Script
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libQt5Script.so.?
%attr(755,root,root) %{_libdir}/libQt5Script.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5ScriptTools.so.?
%attr(755,root,root) %{_libdir}/libQt5ScriptTools.so.*.*

%files -n Qt5Script-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5Script.so
%attr(755,root,root) %{_libdir}/libQt5ScriptTools.so
%{_libdir}/libQt5Script.la
%{_libdir}/libQt5ScriptTools.la
%{_libdir}/libQt5Script.prl
%{_libdir}/libQt5ScriptTools.prl
%{_libdir}/cmake/Qt5Script
%{_libdir}/cmake/Qt5ScriptTools
%{_includedir}/qt5/QtScript
%{_includedir}/qt5/QtScriptTools
%{_pkgconfigdir}/*.pc
%{_qtdir}/mkspecs

%files doc
%defattr(644,root,root,755)
%{_docdir}/qt5-doc

%files examples -f examples.files
