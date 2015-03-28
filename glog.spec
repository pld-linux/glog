#
# Conditional build:
%bcond_without	tests	# gtest/gmock based tests

Summary:	A C++ application logging library
Summary(pl.UTF-8):	Biblioteka do logowania dla aplikacji w C++
Name:		glog
Version:	0.3.3
Release:	3
License:	BSD
Group:		Libraries
#Source0Download: http://code.google.com/p/google-glog/downloads/list
Source0:	http://google-glog.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	a6fd2c22f8996846e34c763422717c18
Patch0:		%{name}-gflags.patch
Patch1:		avoid-inline-asm.patch
URL:		http://code.google.com/p/google-glog
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
BuildRequires:	gflags-devel
%if %{with tests}
BuildRequires:	gmock-devel
BuildRequires:	gtest-devel
%endif
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
%ifarch %{ix86} %{x8664} arm hppa ia64 mips ppc ppc64 sh
BuildRequires:	libunwind-devel
%endif
BuildRequires:	pkgconfig
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
