Summary:	A C++ application logging library
Name:		glog
Version:	0.3.3
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://google-glog.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	a6fd2c22f8996846e34c763422717c18
URL:		http://code.google.com/p/google-glog
BuildRequires:	autoconf
BuildRequires:	libstdc++-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Google glog is a library that implements application-level logging.
This library provides logging APIs based on C++-style streams and
various helper macros.

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
%{__autoconf}
%configure \
	--disable-static

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libglog.la
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog COPYING README
%attr(755,root,root) %{_libdir}/libglog.so.*.*.*
%ghost %{_libdir}/libglog.so.0

%files devel
%defattr(644,root,root,755)
%doc doc/designstyle.css doc/glog.html
%{_libdir}/libglog.so
%{_pkgconfigdir}/libglog.pc
%dir %{_includedir}/glog
%{_includedir}/glog/*
