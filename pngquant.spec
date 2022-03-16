#
# Conditional build:
%bcond_without	openmp		# OpenMP support
%bcond_without	lcms		# LCMS support
%bcond_with	sse		# SSE instructions
#
%ifarch pentium3 pentium4 %{x8664} x32
%define	with_sse	1
%endif
Summary:	PNG converter and lossy image compressor
Summary(pl.UTF-8):	Konwerter i stratny kompresor dla plików PNG
Name:		pngquant
Version:	2.17.0
Release:	1
# some original code was on MIT-like license
License:	GPL v3+ with MIT parts or commercial
Group:		Libraries
#Source0Download: https://pngquant.org/releases.html
Source0:	https://pngquant.org/%{name}-%{version}-src.tar.gz
# Source0-md5:	e18dd9cc2114c28f85b04b376512c267
URL:		https://pngquant.org/
%{?with_openmp:BuildRequires:	gcc >= 6:4.2}
%{?with_openmp:BuildRequires:	libgomp-devel}
%{?with_lcms:BuildRequires:	lcms2-devel >= 2}
BuildRequires:	libimagequant-devel >= 2.17
BuildRequires:	libpng-devel
BuildRequires:	pkgconfig
BuildRequires:	zlib-devel
Requires:	libimagequant >= 2.17
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PNG converter and lossy image compressor.

%description -l pl.UTF-8
Konwerter i stratny kompresor dla plików PNG.

%prep
%setup -q

%build
# not autoconf configure
./configure \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} %{rpmcppflags}" \
	LDFLAGS="%{rpmldflags}" \
	--prefix=%{_prefix} \
	%{__enable_disable sse} \
	%{?with_lcms:--with-lcms2} \
	--with-libimagequant \
	%{?with_openmp:--with-openmp}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG COPYRIGHT README.md
%attr(755,root,root) %{_bindir}/pngquant
%{_mandir}/man1/pngquant.1*
