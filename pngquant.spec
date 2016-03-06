#
# Conditional build:
%bcond_without	static_libs	# static library
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
Version:	2.6.0
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://pngquant.org/releases.html
Source0:	https://pngquant.org/%{name}-%{version}-src.tar.gz
# Source0-md5:	54df683f87cd5bfc15b3c2764419c957
Patch0:		%{name}-shared.patch
URL:		https://pngquant.org/
%{?with_openmp:BuildRequires:	gcc >= 6:4.2}
%{?with_openmp:BuildRequires:	libgomp-devel}
%{?with_lcms:BuildRequires:	lcms2-devel >= 2}
BuildRequires:	libpng-devel
BuildRequires:	pkgconfig
BuildRequires:	zlib-devel
Requires:	libimagequant = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PNG converter and lossy image compressor.

%description -l pl.UTF-8
Konwerter i stratny kompresor dla plików PNG.

%package -n libimagequant
Summary:	Image Quantization library
Summary(pl.UTF-8):	Biblioteka do kwantyzacji obrazów
Group:		Libraries
URL:		https://pngquant.org/lib/

%description -n libimagequant
Image Quantization library.

%description -n libimagequant -l pl.UTF-8
Biblioteka do kwantyzacji obrazów.

%package -n libimagequant-devel
Summary:	Header files for libimagequant library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libimagequant
Group:		Development/Libraries
URL:		https://pngquant.org/lib/
Requires:	libimagequant = %{version}-%{release}

%description -n libimagequant-devel
Header files for libimagequant library.

%description -n libimagequant-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libimagequant.

%package -n libimagequant-static
Summary:	Static libimagequant library
Summary(pl.UTF-8):	Statyczna biblioteka libimagequant
Group:		Development/Libraries
URL:		https://pngquant.org/lib/
Requires:	libimagequant-devel = %{version}-%{release}

%description -n libimagequant-static
Static libimagequant library.

%description -n libimagequant-static -l pl.UTF-8
Statyczna biblioteka libimagequant.

%prep
%setup -q
%patch0 -p1

%build
# not autoconf configure
./configure \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} %{rpmcppflags}" \
	LDFLAGS="%{rpmldflags}" \
	--prefix=%{_prefix} \
	%{?with_sse:--enable-sse} \
	%{?with_lcms:--with-lcms2} \
	%{?with_openmp:--with-openmp}

%{__make} -C lib %{!?with_static_libs:shared}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# not covered by make install
cp -a lib/libimagequant.so* $RPM_BUILD_ROOT%{_libdir}
%if %{with static_libs}
cp -p lib/libimagequant.a $RPM_BUILD_ROOT%{_libdir}
%endif
cp -p lib/libimagequant.h $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n libimagequant -p /sbin/ldconfig
%postun	-n libimagequant -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG COPYRIGHT README.md
%attr(755,root,root) %{_bindir}/pngquant
%{_mandir}/man1/pngquant.1*

%files -n libimagequant
%defattr(644,root,root,755)
%doc lib/{COPYRIGHT,MANUAL.md}
%attr(755,root,root) %{_libdir}/libimagequant.so.0

%files -n libimagequant-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libimagequant.so
%{_includedir}/libimagequant.h

%if %{with static_libs}
%files -n libimagequant-static
%defattr(644,root,root,755)
%{_libdir}/libimagequant.a
%endif
