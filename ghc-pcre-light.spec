#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	pcre-light
Summary:	A library for Perl 5 compatible regular expressions
Summary(pl.UTF-8):	Biblioteka wyrażeń regularnych zgodnych z Perlem 5
Name:		ghc-%{pkgname}
Version:	0.4.1.0
Release:	1
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/pcre-light
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	b2998e2841561c04d93cea443aae6ad1
URL:		http://hackage.haskell.org/package/pcre-light
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 3
BuildRequires:	ghc-base <= 5
BuildRequires:	ghc-bytestring >= 0.9
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-base-prof >= 3
BuildRequires:	ghc-base-prof <= 5
BuildRequires:	ghc-bytestring-prof >= 0.9
%endif
BuildRequires:	pcre-devel
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-base >= 3
Requires:	ghc-base <= 5
Requires:	ghc-bytestring >= 0.9
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
A small, efficient and portable regex library for Perl 5 compatible
regular expressions.

%description -l pl.UTF-8
Mała, wydajna i przenośna biblioteka wyrażeń regularnych zgodnych z
Perlem 5.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 3
Requires:	ghc-base-prof <= 5
Requires:	ghc-bytestring-prof >= 0.9

%description prof
Profiling %{pkgname} library for GHC. Should be installed when GHC's
profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%package doc
Summary:	HTML documentation for ghc %{pkgname} package
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}
Group:		Documentation

%description doc
HTML documentation for ghc %{pkgname} package.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.lhs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs build
runhaskell Setup.lhs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.lhs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/html %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSpcre-light-%{version}-*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSpcre-light-%{version}-*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSpcre-light-%{version}-*_p.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Regex
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Regex/PCRE
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Regex/PCRE/Light.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Regex/PCRE/Light.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Regex/PCRE/Light
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Regex/PCRE/Light/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Regex/PCRE/Light/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSpcre-light-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Regex/PCRE/Light.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Regex/PCRE/Light/*.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
