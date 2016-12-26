#
# Conditional build:
%bcond_without	tests	# gtest/gmock based tests

Summary:	A C++ application logging library
Summary(pl.UTF-8):	Biblioteka do logowania dla aplikacji w C++
Name:		glog
Version:	0.3.4
Release:	5
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/google/glog/releases
Source0:	https://github.com/google/glog/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	df92e05c9d02504fb96674bc776a41cb
Patch0:		%{name}-gflags.patch
Patch1:		avoid-inline-asm.patch
Patch2:		gcc5.patch
URL:		https://github.com/google/glog
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
BuildRequires:	gflags-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	pkgconfig
%if %{with tests}
BuildRequires:	gmock-devel
BuildRequires:	gtest-devel
%endif
%ifarch %{ix86} %{x8664} arm hppa ia64 mips ppc ppc64 sh
BuildRequires:	libunwind-devel
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
Requires:	gflags-devel
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
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%if %{with tests}
install -d gmock
cd gmock
%cmake $(pkg-config --variable=srcdir gmock) \
	-DBUILD_SHARED_LIBS=OFF
%{__make}
cd ..
LDFLAGS="%{rpmldflags} -L$(pwd)/gmock"
%endif
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure

%{__make}

%if %{with tests}
%{__make} check
%endif

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
%doc AUTHORS COPYING ChangeLog README
%attr(755,root,root) %{_libdir}/libglog.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libglog.so.0

%files devel
%defattr(644,root,root,755)
%doc doc/designstyle.css doc/glog.html
%attr(755,root,root) %{_libdir}/libglog.so
%{_includedir}/glog
%{_pkgconfigdir}/libglog.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libglog.a
