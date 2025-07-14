#
# Conditional build:
%bcond_without	libunwind	# libunwind support
%bcond_without	static_libs	# static library
%bcond_without	tests		# gtest/gmock based tests [recheck: signalhandler_unittest broken on x32 as of 0.4.0]

%ifarch %{ix86} %{x8664} x32 %{arm} hppa ia64 mips ppc ppc64 sh
%undefine	with_libunwind
%endif
Summary:	A C++ application logging library
Summary(pl.UTF-8):	Biblioteka do logowania dla aplikacji w C++
Name:		glog
Version:	0.6.0
Release:	2
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/google/glog/releases
Source0:	https://github.com/google/glog/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	c98a6068bc9b8ad9cebaca625ca73aa2
Patch0:		avoid-inline-asm.patch
URL:		https://github.com/google/glog
BuildRequires:	cmake >= 3.16
BuildRequires:	gflags-devel >= 2.2.2
BuildRequires:	libstdc++-devel
%if %{with libunwind}
BuildRequires:	libunwind-devel
%endif
BuildRequires:	pkgconfig
%if %{with tests}
BuildRequires:	gmock-devel >= 1.10.0
BuildRequires:	gtest-devel
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Google glog is a library that implements application-level logging.
This library provides logging APIs based on C++-style streams and
various helper macros.

%description -l pl.UTF-8
Google glog to biblioteka implementująca logowanie na poziomie
aplikacji. Zapewnia API do logowania oparte na strumieniach w stylu
C++ oraz różne makra pomocnicze

%package devel
Summary:	Development files for glog library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki glog
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gflags-devel >= 2.2.2
Requires:	libstdc++-devel

%description devel
This package contains the header files for developing applications
that use glog library.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia aplikacji
wykorzystujących bibliotekę glog.

%package static
Summary:	Static glog library
Summary(pl.UTF-8):	Statyczna biblioteka glog
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static glog library.

%description static -l pl.UTF-8
Statyczna biblioteka glog.

%prep
%setup -q
%patch -P0 -p1

%build
%if %{with static_libs}
%cmake -B build-static \
	-DBUILD_SHARED_LIBS=OFF \
	%{!?with_tests:-DWITH_GTEST=OFF} \
	%{!?with_libunwind:-DWITH_UNWIND=OFF}

%{__make} -C build-static
%endif

%cmake -B build \
	%{!?with_tests:-DWITH_GTEST=OFF} \
	%{!?with_libunwind:-DWITH_UNWIND=OFF}

%{__make} -C build

%if %{with tests}
%{__make} -C build test
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} -C build-static install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog README.rst
%attr(755,root,root) %{_libdir}/libglog.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libglog.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libglog.so
%{_includedir}/glog
%{_pkgconfigdir}/libglog.pc
%{_libdir}/cmake/glog

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libglog.a
%endif
