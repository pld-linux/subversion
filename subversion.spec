# TODO:
# - remove net_client_only and add db bcond (then without apache and
#   without db => net_client_only - spec will be more simpler, I think)
#
# Conditional build:
%bcond_with	net_client_only			# build only net client
%bcond_without	python				# build without python bindings (broken)
%bcond_without	perl				# build without perl bindings
%bcond_without	apache				# build without apache support (webdav, etc)
#
%{!?with_net_client_only:%include	/usr/lib/rpm/macros.perl}
%define	apxs	/usr/sbin/apxs
%define	pdir	SVN
%define	pnam	_Core
Summary:	A Concurrent Versioning system similar to but better than CVS
Summary(pl.UTF-8):	System kontroli wersji podobny, ale lepszy, niż CVS
Summary(pt_BR.UTF-8):	Sistema de versionamento concorrente
Name:		subversion
Version:	1.4.6
Release:	2
License:	Apache/BSD Style
Group:		Development/Version Control
Source0:	http://subversion.tigris.org/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	32786fe2f322982c0567346de18f6460
Source1:	%{name}-dav_svn.conf
Source2:	%{name}-authz_svn.conf
Source3:	%{name}-svnserve.init
Source4:	%{name}-svnserve.sysconfig
Source5:	%{name}-convert-typemaps-to-ifdef.py
Patch0:		%{name}-home_etc.patch
Patch1:		%{name}-DESTDIR.patch
Patch2:		%{name}-neon.patch
Patch3:		%{name}-python_bindings.patch
Patch4:		%{name}-swig.patch
URL:		http://subversion.tigris.org/
%if %{with net_client_only}
%global apache_modules_api 0
%else
%{?with_apache:BuildRequires:	apache-devel >= 2.2.0-8}
BuildRequires:	automake
BuildRequires:	db-devel >= 4.1.25
BuildRequires:	rpmbuild(macros) >= 1.268
%if %{with perl}
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	swig-perl >= 1.3.24
%endif
%endif
BuildRequires:	apr-devel >= 1:1.0.0
BuildRequires:	apr-util-devel >= 1:1.2.8-3
BuildRequires:	autoconf >= 2.59
BuildRequires:	bison
BuildRequires:	expat-devel
BuildRequires:	gettext-devel
BuildRequires:	libtool >= 1.4-9
BuildRequires:	neon-devel >= 0.26.0
BuildRequires:	python >= 2.2
BuildRequires:	python-modules >= 2.2
%if %{with python}
BuildRequires:	python-devel >= 2.2
BuildRequires:	sed >= 4.0
BuildRequires:	swig-python >= 1.3.24
%endif
BuildRequires:	texinfo
BuildRequires:	which
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir		%{_libdir}/svn
%define		apacheconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)/conf.d
%define		apachelibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)

%description
The goal of the Subversion project is to build a version control
system that is a compelling replacement for CVS in the open source
community.

Our goals are:
- All current CVS features.
- Directories, renames, and file meta-data are versioned.
- Symbolic links, etc, are supported
- Commits are truly atomic.
- Branching and tagging are cheap (constant time) operations
- Repeated merges are handled gracefully
- Support for plug-in client side diff programs
- Natively client/server
- Client/server protocol sends diffs in both directions
- Costs are proportional to change size, not project size
- Internationalization
- Progressive multi-lingual support

%description -l pl.UTF-8
Celem projektu Subversion jest stworzenie systemu kontroli wersji jako
zamiennika dla CVS.

Cele projektu to:
- Wszystkie aktualne możliwości CVS.
- Katalogi, zmiany nazw oraz metadane plików są wersjonowane.
- Obsługa dowiązań symbolicznych itp.
- Commity są w pełni atomowe.
- Branchowanie oraz tagowanie są tanimi (stałymi w czasie) operacjami.
- Dobra obsługa powtarzanego łączenia (merge).
- Obsługa wtyczek diff po stronie klienta.
- Natywny klient/serwer.
- Klient/Serwer przesyłają diffy w obu kierunkach.
- Koszty proporcjonalne do rozmiaru zmiany, a nie rozmiaru projektu.
- Internacjonalizacja.
- Postępujące wsparcie dla wielu języków.

%description -l pt_BR.UTF-8
O objetivo do projeto Subversion é construir um sistema de controle de
versões que seja um substituto para o CVS (Concurrent Versioning
System) na comunidade opensource, fornecendo grandes melhorias.

%package libs
Summary:	Subversion libraries and modules
Summary(pl.UTF-8):	Biblioteka subversion oraz ładowalne moduły
Group:		Libraries
Requires:	neon >= 0.26.0
Obsoletes:	libsubversion0

%description libs
Subversion libraries and modules.

%description libs -l pl.UTF-8
Biblioteka subversion oraz ładowalne moduły.

%package devel
Summary:	Header files and develpment documentation for subversion
Summary(pl.UTF-8):	Pliki nagłówkowe i dokumetacja do subversion
Summary(pt_BR.UTF-8):	Arquivos de desenvolvimento para o Subversion
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	apr-util-devel >= 1:1.0.0
Requires:	neon-devel >= 0.26.0
Obsoletes:	libsubversion0-devel

%description devel
Header files and develpment documentation for subversion.

%description devel -l pl.UTF-8
Pliki nagłówkowe i dokumetacja do subversion.

%description devel -l pt_BR.UTF-8
Este pacote provê os arquivos necessários para desenvolvedores
interagirem com o Subversion.

%package static
Summary:	Static subversion library
Summary(pl.UTF-8):	Biblioteka statyczna subversion
Summary(pt_BR.UTF-8):	Sistema de versionamento concorrente
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}
Obsoletes:	libsubversion0-static-devel

%description static
Static subversion library.

%description static -l pl.UTF-8
Biblioteka statyczna subversion.

%description static -l pt_BR.UTF-8
Este pacote provê um cliente estático do subversion.

%package svnserve
Summary:	Subversion svnserve
Summary(pl.UTF-8):	Subversion svnserve
Group:		Networking/Daemons
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name} = %{version}-%{release}
Requires:	rc-scripts

%description svnserve
Subversion svnserve server.

%description svnserve -l pl.UTF-8
Serwer subversion svnserve.

%package tools
Summary:	Subversion tools and scripts
Summary(pl.UTF-8):	Narzędzia oraz skrypty dla subversion
Summary(pt_BR.UTF-8):	Módulos python para acessar os recursos do Subversion
Group:		Applications
%pyrequires_eq	python
Requires:	%{name} = %{version}-%{release}
Requires:	python-rcsparse >= 0.1-0.20031026.0
Requires:	python-subversion = %{version}

%description tools
Subversion tools and scripts.

%description tools -l pl.UTF-8
Narzędzia oraz skrypty dla subversion.

%package -n bash-completion-subversion
Summary:	bash completion for subversion
Summary(pl.UTF-8):	Dopełnienia basha dla subversion
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion
Conflicts:	%{name}-tools <= 1.1.0-0.rc6.1

%description -n bash-completion-subversion
Bash completion for subversion.

%description -n bash-completion-subversion -l pl.UTF-8
Dopełnienia basha dla subversion.

%package -n python-subversion
Summary:	Subversion python bindings
Summary(pl.UTF-8):	Dowiązania do subversion dla pythona
Summary(pt_BR.UTF-8):	Módulos python para acessar os recursos do Subversion
Group:		Development/Languages/Python
%pyrequires_eq	python
Requires:	%{name}-libs = %{version}-%{release}
Obsoletes:	subversion-python

%description -n python-subversion
Subversion python bindings.

%description -n python-subversion -l pl.UTF-8
Dowiązania do subversion dla pythona.

%description -n python-subversion -l pt_BR.UTF-8
Módulos python para acessar os recursos do Subversion.

%package -n perl-subversion
Summary:	Subversion perl bindings
Summary(pl.UTF-8):	Dowiązania do subversion dla perla
Summary(pt_BR.UTF-8):	Módulos perl para acessar os recursos do Subversion
Group:		Development/Languages/Perl
Requires:	%{name}-libs = %{version}-%{release}
Obsoletes:	subversion-perl

%description -n perl-subversion
Subversion perl bindings.

%description -n perl-subversion -l pl.UTF-8
Dowiązania do subversion dla perl.

%description -n perl-subversion -l pt_BR.UTF-8
Módulos perl para acessar os recursos do Subversion.

%package -n apache-mod_dav_svn
Summary:	Apache module: Subversion Server
Summary(pl.UTF-8):	Moduł apache: Serwer Subversion
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}
Requires:	apache(modules-api) = %apache_modules_api
Requires:	apache-mod_dav

%description -n apache-mod_dav_svn
Apache module: Subversion Server.

%description -n apache-mod_dav_svn -l pl.UTF-8
Moduł apache: Serwer Subversion.

%package -n apache-mod_authz_svn
Summary:	Apache module: Subversion Server - path-based authorization
Summary(pl.UTF-8):	Moduł apache: autoryzacja na podstawie ścieżki dla serwera Subversion
Group:		Networking/Daemons
Requires:	apache(modules-api) = %apache_modules_api
Requires:	apache-mod_dav_svn = %{version}-%{release}

%description -n apache-mod_authz_svn
Apache module: Subversion Server - path-based authorization.

%description -n apache-mod_authz_svn -l pl.UTF-8
Moduł apache: autoryzacja na podstawie ścieżki dla serwera Subversion.

%prep
%setup -q
rm -rf apr apr-util neon
%patch0 -p0
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
rm subversion/bindings/swig/proxy/*.swg 
cd subversion/bindings/swig && python "%{SOURCE5}" && cd ../../..
cp -f /usr/share/automake/config.sub ac-helpers
chmod +x ./autogen.sh && ./autogen.sh

# don't enable dso - currently it's broken
%configure \
	--with-editor=vi \
	--with-zlib \
	--with-python=%{_bindir}/python \
	--with-perl5=%{_bindir}/perl \
%if %{with net_client_only}
	--without-apache \
	--without-swig \
	--without-apxs \
	--without-berkeley-db \
%else
	--disable-dso \
	--disable-mod-activation \
%if %{with apache}
	--with-apxs=%{_sbindir}/apxs \
%else
	--without-apache \
	--without-apxs \
	--with-berkeley-db=%{_includedir}/db4:%{_libdir} \
%endif
%if !%{with python} && !%{with perl}
	--without-swig \
%endif
%endif
	--with-neon=%{_prefix} \
	--disable-neon-version-check \
	--with-apr=%{_bindir}/apr-1-config \
	--with-apr-util=%{_bindir}/apu-1-config

%{__make} -j1

%if !%{with net_client_only}
# python
%if %{with python}
%{__make} swig-py \
	swig_pydir=%{py_sitedir}/libsvn \
	swig_pydir_extra=%{py_sitedir}/svn
%endif
# perl
%if %{with perl}
%{__make} swig-pl-lib
odir=$(pwd)
cd subversion/bindings/swig/perl/native
%{__perl} Makefile.PL INSTALLDIRS=vendor
%{__make}
cd $odir
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig,bash_completion.d} \
	$RPM_BUILD_ROOT{%{apacheconfdir},%{apachelibdir},%{_infodir}} \
	$RPM_BUILD_ROOT%{_examplesdir}/{%{name}-%{version},python-%{name}-%{version}} \
	$RPM_BUILD_ROOT/home/services/subversion{,/repos}

%{__make} install -j1 \
%if !%{with net_client_only} && %{with python}
	install-swig-py \
%endif
	APACHE_LIBEXECDIR="$(%{_sbindir}/apxs -q LIBEXECDIR)" \
	DESTDIR=$RPM_BUILD_ROOT \
	swig_pydir=%{py_sitedir}/libsvn \
	swig_pydir_extra=%{py_sitedir}/svn

%if !%{with net_client_only} && %{with perl}
%{__make} install-swig-pl-lib \
	DESTDIR=$RPM_BUILD_ROOT
odir=$(pwd)
cd subversion/bindings/swig/perl/native
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=$RPM_BUILD_ROOT%{_prefix} \
	LIBDIR=$RPM_BUILD_ROOT%{_libdir}
cd $odir
%endif

%if %{with apache}
install %{SOURCE1} $RPM_BUILD_ROOT%{apacheconfdir}/65_mod_dav_svn.conf
install %{SOURCE2} $RPM_BUILD_ROOT%{apacheconfdir}/66_mod_authz_svn.conf
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/svnserve
install %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/svnserve
%endif

%if !%{with net_client_only}
install tools/backup/hot-backup.py $RPM_BUILD_ROOT%{_bindir}/svn-hot-backup
%if %{with python}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
find $RPM_BUILD_ROOT%{py_sitedir} -name "*.py" -o -name "*.a" -o -name "*.la" | xargs rm -f
install tools/examples/*.py $RPM_BUILD_ROOT%{_examplesdir}/python-%{name}-%{version}
%endif
%endif

install tools/client-side/bash_completion $RPM_BUILD_ROOT/etc/bash_completion.d/%{name}
install tools/examples/*.c $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%find_lang %{name}

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*swig*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post devel	-p	/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun devel	-p	/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig
%post   -n python-subversion -p /sbin/ldconfig
%postun -n perl-subversion -p /sbin/ldconfig

%post svnserve
/sbin/chkconfig --add svnserve
%service svnserve restart "svnserve daemon"

%preun svnserve
if [ "$1" = "0" ]; then
	%service svnserve stop
	/sbin/chkconfig --del svnserve
fi

%post -n apache-mod_dav_svn
%service -q httpd restart

%preun -n apache-mod_dav_svn
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc BUGS CHANGES COPYING INSTALL README
%doc doc/*/*.html
%doc tools/hook-scripts/*.{pl,py,example}
%doc tools/hook-scripts/mailer/*.{py,example}
%doc tools/xslt/*
%attr(755,root,root) %{_bindir}/svn*
%exclude %{_bindir}/svnserve
%if !%{with net_client_only}
%exclude %{_bindir}/svn-hot-backup
%endif
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%exclude %{_mandir}/man?/svnserve*

%files libs -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*
%if %{with perl} || %{with python}
%exclude %{_libdir}/lib*_swig_*.so.*
%endif

%files devel
%defattr(644,root,root,755)
%{_includedir}/%{name}*
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%if %{with perl} || %{with python}
%exclude %{_libdir}/lib*_swig_*.so
%endif
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%if !%{with net_client_only}
%files svnserve
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/svnserve
%{_mandir}/man?/svnserve*
%dir /home/services/subversion
%dir /home/services/subversion/repos
%if %{with apache}
%attr(754,root,root) /etc/rc.d/init.d/svnserve
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/svnserve
%endif

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/svn-hot-backup

%files -n bash-completion-subversion
%defattr(644,root,root,755)
/etc/bash_completion.d/%{name}

%if %{with python}
%files -n python-subversion
%defattr(644,root,root,755)
%doc tools/backup/*.py tools/examples/*.py
%dir %{py_sitedir}/svn
%dir %{py_sitedir}/libsvn
%{py_sitedir}/svn/*.py[co]
%{py_sitedir}/libsvn/*.py[co]
%attr(755,root,root) %{py_sitedir}/libsvn/*.so
%{_examplesdir}/python-%{name}-%{version}
%attr(755,root,root) %{_libdir}/lib*_swig_py*.so*
%endif

%if %{with perl}
%files -n perl-subversion
%defattr(644,root,root,755)
%{perl_vendorarch}/SVN
%dir %{perl_vendorarch}/auto/SVN
%dir %{perl_vendorarch}/auto/SVN/*
%attr(755,root,root) %{perl_vendorarch}/auto/SVN/*/*.so
%{perl_vendorarch}/auto/SVN/*/*.bs
%{_mandir}/man3/*.3pm*
%attr(755,root,root) %{_libdir}/lib*_swig_perl*.so*
%endif

%if %{with apache}
%files -n apache-mod_dav_svn
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{apacheconfdir}/*_mod_dav_svn.conf
%attr(755,root,root) %{apachelibdir}/mod_dav_svn.so

%files -n apache-mod_authz_svn
%defattr(644,root,root,755)
%doc subversion/mod_authz_svn/INSTALL
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{apacheconfdir}/*_mod_authz_svn.conf
%attr(755,root,root) %{apachelibdir}/mod_authz_svn.so
%endif

%endif # net_client_only
