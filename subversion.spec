#
# Conditional build:
%bcond_with	internal_neon		# build with internal neon
%bcond_with	net_client_only		# build only net client
#	
%include	/usr/lib/rpm/macros.python
%{!?with_net_client_only:%include	/usr/lib/rpm/macros.perl}
Summary:	A Concurrent Versioning system similar to but better than CVS
Summary(pl):	System kontroli wersji podobny, ale lepszy, ni� CVS
Summary(pt_BR):	Sistema de versionamento concorrente
Name:		subversion
Version:	1.0.4
Release:	1
License:	Apache/BSD Style
Group:		Development/Version Control
Source0:	http://subversion.tigris.org/tarballs/%{name}-%{version}.tar.bz2
# Source0-md5:	313bd03f353683de7561eadf477f7612
Source1:	%{name}-dav_svn.conf
Source2:	%{name}-authz_svn.conf
Source3:	%{name}-svnserve.init
Source4:	%{name}-svnserve.sysconfig
#Patch0:		%{name}-svnlook.patch
#Patch1:		%{name}-hot_backup_num.patch
URL:		http://subversion.tigris.org/
%if %{with net_client_only}
%global apache_modules_api 0
%else
BuildRequires:	automake
BuildRequires:	apache-devel >= 2.0.47-0.6
BuildRequires:	db-devel >= 4.1.25
BuildRequires:	rpmbuild(macros) >= 1.120
BuildRequires:	swig >= 1.3.19
BuildRequires:	swig-python >= 1.3.19
BuildRequires:	swig-perl >= 1.3.19
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
%endif
BuildRequires:	apr-devel >= 1:0.9.5
BuildRequires:	apr-util-devel >= 1:0.9.5
BuildRequires:	autoconf >= 2.59
BuildRequires:	bison
BuildRequires:	docbook-style-xsl >= 1.56
BuildRequires:	expat-devel
BuildRequires:	libtool >= 1.4-9
BuildRequires:	libxslt-progs
%{!?with_internal_neon:BuildRequires:	neon-devel >= 0.24.6}
BuildRequires:	python-devel >= 2.2
BuildRequires:	rpm-pythonprov >= 4.0.2-50
BuildRequires:	texinfo
BuildRequires:	which
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_apachelibdir	/usr/%{_lib}/apache
%define		_libexecdir	%{_libdir}/svn

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

%description -l pl
Celem projektu Subversion jest stworzenie systemu kontroli wersji jako
zamiennika dla CVS.

Cele projektu to:
- Wszystkie aktualne mo�liwo�ci CVS.
- Katalogi, zmiany nazw oraz meta-dane plik�w s� wersjonowane.
- Wsparcie dla link�w symbolicznych itp.
- Commity s� w pe�ni atomowe.
- Branchowanie oraz tagowanie s� tanimi (sta�ymi w czasie) operacjami.
- Powtarzaj�ce merge.
- Wsparcie dla plugin�w diff'a po stronie klienta.
- Natywny klient/serwer.
- Klient/Serwer przesy�aj� diffy w obu kierunkach.
- Koszty proporcjonalne do rozmiaru zmiany, a nie rozmiaru projektu.
- Internacjonalizacja.
- Post�puj�ce wsparcie dla wielu j�zyk�w.

%description -l pt_BR
O objetivo do projeto Subversion � construir um sistema de controle de
vers�es que seja um substituto para o CVS (Concurrent Versioning
System) na comunidade opensource, fornecendo grandes melhorias.

%package libs
Summary:	Subversion libraries and modules
Summary(pl):	Biblioteka subversion oraz �adowalne modu�y
Group:		Libraries
Obsoletes:	libsubversion0
%{!?with_internal_neon:Requires:	neon >= 0.24.6}

%description libs
Subversion libraries and modules.

%description libs -l pl
Biblioteka subversion oraz �adowalne modu�y.

%package devel
Summary:	Header files and develpment documentation for subversion
Summary(pl):	Pliki nag��wkowe i dokumetacja do subversion
Summary(pt_BR):	Arquivos de desenvolvimento para o Subversion
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	apr-util-devel >= 1:0.9.5
%{!?with_internal_neon:Requires:	neon-devel >= 0.24.6}
Obsoletes:	libsubversion0-devel

%description devel
Header files and develpment documentation for subversion.

%description devel -l pl
Pliki nag��wkowe i dokumetacja do subversion.

%description devel -l pt_BR
Este pacote prov� os arquivos necess�rios para desenvolvedores
interagirem com o Subversion.

%package static
Summary:	Static subversion library
Summary(pl):	Biblioteka statyczna subversion
Summary(pt_BR):	Sistema de versionamento concorrente
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}
Obsoletes:	libsubversion0-static-devel

%description static
Static subversion library.

%description static -l pl
Biblioteka statyczna subversion.

%description static -l pt_BR
Este pacote prov� um cliente est�tico do subversion.

%package svnserve
Summary:	Subversion svnserve
Summary(pl):	Subversion svnserve
Group:		Networking/Daemons
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name} = %{version}-%{release}

%description svnserve
Subversion svnserve server.

%description svnserve -l pl
Serwer subversion svnserve.

%package tools
Summary:	Subversion tools and scripts
Summary(pl):	Narz�dzia oraz skrypty dla subversion
Summary(pt_BR):	M�dulos python para acessar os recursos do Subversion
Group:		Applications
%pyrequires_eq	python
Requires:	python-rcsparse >= 0.1-0.20031026.0
Requires:	python-subversion = %{version}
Requires:	%{name} = %{version}-%{release}

%description tools
Subversion tools and scripts.

%description tools -l pl
Narz�dzia oraz skrypty dla subversion.

%package -n python-subversion
Summary:	Subversion python bindings
Summary(pl):	Dowi�zania do subversion dla pythona
Summary(pt_BR):	M�dulos python para acessar os recursos do Subversion
Group:		Development/Languages/Python
%pyrequires_eq	python
Obsoletes:	subversion-python
Requires:	%{name}-libs = %{version}-%{release}

%description -n python-subversion
Subversion python bindings.

%description -n python-subversion -l pl
Dowi�zania do subversion dla pythona.

%description -n python-subversion -l pt_BR
M�dulos python para acessar os recursos do Subversion.

%package -n perl-subversion
Summary:	Subversion perl bindings
Summary(pl):	Dowi�zania do subversion dla perla
Summary(pt_BR):	M�dulos perl para acessar os recursos do Subversion
Group:		Development/Languages/Perl
Obsoletes:	subversion-perl
Requires:	%{name}-libs = %{version}-%{release}

%description -n perl-subversion
Subversion perl bindings.

%description -n perl-subversion -l pl
Dowi�zania do subversion dla perl.

%description -n perl-subversion -l pt_BR
M�dulos perl para acessar os recursos do Subversion.

%package -n apache-mod_dav_svn
Summary:	Apache module: Subversion Server
Summary(pl):	Modu� apache: Serwer Subversion
Group:		Networking/Daemons
Requires:	apache >= 2.0.47
Requires:	apache(modules-api) = %{apache_modules_api}
Requires:	apache-mod_dav
Requires:	%{name} = %{version}-%{release}

%description -n apache-mod_dav_svn
Apache module: Subversion Server.

%description -n apache-mod_dav_svn -l pl
Modu� apache: Serwer Subversion.

%package -n apache-mod_authz_svn
Summary:	Apache module: Subversion Server - path-based authorization
Summary(pl):	Modu� apache: autoryzacja na podstawie �cie�ki dla serwera Subversion
Group:		Networking/Daemons
Requires:	apache-mod_dav_svn = %{version}-%{release}
Requires:	apache >= 2.0.47
Requires:	apache(modules-api) = %{apache_modules_api}

%description -n apache-mod_authz_svn
Apache module: Subversion Server - path-based authorization.

%description -n apache-mod_authz_svn -l pl
Modu� apache: autoryzacja na podstawie �cie�ki dla serwera Subversion.

%prep
%setup -q
#%patch0 -p0
#%patch1 -p1

rm -rf apr-util{,/xml/expat}/autom4te.cache

%build
cp -f /usr/share/automake/config.sub ac-helpers
chmod +x ./autogen.sh && ./autogen.sh

# don't enable dso - currently it's broken
%configure \
%if %{with net_client_only}
	--without-apache \
	--without-swig \
	--without-apxs \
	--without-berkeley-db \
%else
	--disable-dso \
	--disable-mod-activation \
	--with-apxs=%{_sbindir}/apxs \
	--with-berkeley-db=%{_includedir}/db4:%{_libdir} \
%endif
	%{!?with_internal_neon:--with-neon=%{_prefix}} \
	--with-apr=%{_bindir}/apr-config \
	--with-apr-util=%{_bindir}/apu-config

%{__make}

%if ! %{with net_client_only}
# python
%{__make} swig-py \
	swig_pydir=%{py_sitedir}/libsvn \
	swig_pydir_extra=%{py_sitedir}/svn
# perl
bdir=$(pwd)
%{__make} install-swig-pl-lib \
	LC_ALL=C \
	DESTDIR=${bdir}/swig-pl-lib-buildroot
%{__make}
cd subversion/bindings/swig/perl
env APR_CONFIG=%{_bindir}/apr-config \
    APU_CONFIG=%{_bindir}/apu-config \
	%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
env LIBRARY_PATH=${bdir}/swig-pl-lib-buildroot%{_libdir} %{__make}
cd ../../../../
%endif

# build documentation; build process for documentation is severely
# braindamaged -- authors suggests to untar docbook distribution in
# build directory, hence the hack here
ln -s /usr/share/sgml/docbook/xsl-stylesheets doc/book/tools/xsl
%{__make} -C doc/book all-html

# prepare for %%doc below
mv -f doc/book/book/html-chunk svn-handbook
mkdir svn-handbook/images/
cp -f doc/book/book/images/*.png svn-handbook/images/

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig,bash_completion.d} \
	$RPM_BUILD_ROOT{%{_sysconfdir}/httpd/httpd.conf,%{_apachelibdir},%{_infodir}} \
	$RPM_BUILD_ROOT%{_examplesdir}/{%{name}-%{version},python-%{name}-%{version}}

%{__make} install \
	LC_ALL=C \
	%{!?with_net_client_only:install-swig-py} \
	DESTDIR=$RPM_BUILD_ROOT \
	swig_pydir=%{py_sitedir}/libsvn \
	swig_pydir_extra=%{py_sitedir}/svn

%if ! %{with net_client_only}
%{__make} install-swig-pl-lib \
	LC_ALL=C \
	DESTDIR=$RPM_BUILD_ROOT
%{__make} -C subversion/bindings/swig/perl install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/httpd.conf/65_mod_dav_svn.conf
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/httpd.conf/66_mod_authz_svn.conf
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/svnserve
install %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/svnserve
install doc/programmer/design/*.info* $RPM_BUILD_ROOT%{_infodir}/

%if ! %{with net_client_only}
install tools/backup/hot-backup.py $RPM_BUILD_ROOT%{_bindir}/svn-hot-backup

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
find $RPM_BUILD_ROOT%{py_sitedir} -name "*.py" -o -name "*.a" -o -name "*.la" | xargs rm -f
install tools/examples/*.py $RPM_BUILD_ROOT%{_examplesdir}/python-%{name}-%{version}
%endif

install tools/client-side/bash_completion $RPM_BUILD_ROOT/etc/bash_completion.d/%{name}
install tools/examples/*.c $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post devel
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun devel
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post svnserve
if [ -f /var/lock/subsys/svnserve ]; then
	/etc/rc.d/init.d/svnserve restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/svnserve start\" to start subversion svnserve daemon."
fi

%preun svnserve
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/svnserve ]; then
		/etc/rc.d/init.d/svnserve restart 1>&2
	fi
fi

%post -n apache-mod_dav_svn
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/httpd start\" to start apache http daemon."
fi

%preun -n apache-mod_dav_svn
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc BUGS CHANGES COPYING INSTALL README
%doc svn-handbook doc/book/misc-docs/misc-docs.html
%doc tools/hook-scripts/*.{pl,py,example}
%doc tools/hook-scripts/mailer/*.{py,example}
%doc tools/xslt/*
%attr(755,root,root) %{_bindir}/svn*
%exclude %{_bindir}/svnserve
%exclude %{_bindir}/svn-hot-backup
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%exclude %{_mandir}/man?/svnserve*
%{?with_internal_neon:%exclude %{_mandir}/man1/neon*}

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/%{name}*
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_infodir}/svn*
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%if ! %{with net_client_only}
%files svnserve
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/svnserve
%{_mandir}/man?/svnserve*
%attr(754,root,root) /etc/rc.d/init.d/svnserve
%attr(640,root,root) %config(noreplace) %verify(not mtime md5 size) /etc/sysconfig/svnserve

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/svn-hot-backup
/etc/bash_completion.d/%{name}

%files -n python-subversion
%defattr(644,root,root,755)
%doc tools/backup/*.py tools/examples/*.py
%dir %{py_sitedir}/svn
%dir %{py_sitedir}/libsvn
%{py_sitedir}/svn/*.py[co]
%{py_sitedir}/libsvn/*.py[co]
%attr(755,root,root) %{py_sitedir}/libsvn/*.so
%{_examplesdir}/python-%{name}-%{version}

%files -n perl-subversion
%defattr(644,root,root,755)
%{perl_vendorarch}/SVN
%dir %{perl_vendorarch}/auto/SVN
%dir %{perl_vendorarch}/auto/SVN/*
%attr(755,root,root) %{perl_vendorarch}/auto/SVN/*/*.so
%{perl_vendorarch}/auto/SVN/*/*.bs
%{_mandir}/man3/*.3pm*

%files -n apache-mod_dav_svn
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/httpd/httpd.conf/*_mod_dav_svn.conf
%attr(755,root,root) %{_apachelibdir}/mod_dav_svn.so

%files -n apache-mod_authz_svn
%defattr(644,root,root,755)
%doc subversion/mod_authz_svn/INSTALL
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/httpd/httpd.conf/*_mod_authz_svn.conf
%attr(755,root,root) %{_apachelibdir}/mod_authz_svn.so
%endif
