#
# Conditional build:
%bcond_with	internal_neon		# build with internal neon
%bcond_with	net_client_only		# build only net client
#	
%include        /usr/lib/rpm/macros.python
Summary:	A Concurrent Versioning system similar to but better than CVS
Summary(pl):	System kontroli wersji podobny, ale lepszy, ni¿ CVS
Summary(pt_BR):	Sistema de versionamento concorrente
Name:		subversion
Version:	0.33.0
Release:	0.1
License:	Apache/BSD Style
Group:		Development/Version Control
Source0:	http://svn.collab.net/tarballs/%{name}-%{version}.tar.gz
# Source0-md5:	938b452b50d02eeb72b50c344b34d8de
Source1:	%{name}-dav_svn.conf
Source2:	%{name}-authz_svn.conf
URL:		http://subversion.tigris.org/
%if %{with net_client_only}
%global apache_modules_api 0
%else
BuildRequires:	apache-devel >= 2.0.47-0.6
BuildRequires:  db-devel >= 4.1.25
BuildRequires:  rpmbuild(macros) >= 1.120
BuildRequires:  swig >= 1.3.17
BuildRequires:  swig-python >= 1.3.17
%endif
BuildRequires:	apr-devel >= 1:0.9.5
BuildRequires:	apr-util-devel >= 1:0.9.5
BuildRequires:	autoconf >= 2.53
BuildRequires:	bison
BuildRequires:	docbook-style-xsl >= 1.56
BuildRequires:	expat-devel
BuildRequires:	libtool >= 1.4-9
BuildRequires:	libxslt-progs
%{!?with_internal_neon:BuildRequires:	neon-devel >= 0.24.1}
BuildRequires:  python >= 2.2
BuildRequires:  rpm-pythonprov >= 4.0.2-50
BuildRequires:	texinfo
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_apachelibdir	/usr/lib/apache
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
- Wszystkie aktualne mo¿liwo¶ci CVS.
- Katalogi, zmiany nazw oraz meta-dane plików s± wersjonowane.
- Wsparcie dla linków symbolicznych itp.
- Commity s± w pe³ni atomowe.
- Branchowanie oraz tagowanie s± tanimi (sta³ymi w czasie) operacjami.
- Powtarzaj±ce merge.
- Wsparcie dla pluginów diff'a po stronie klienta.
- Natywny klient/serwer.
- Klient/Serwer przesy³aj± diffy w obu kierunkach.
- Koszty proporcjonalne do rozmiaru zmiany, a nie rozmiaru projektu.
- Internacjonalizacja.
- Postêpuj±ce wsparcie dla wielu jêzyków.

%description -l pt_BR
O objetivo do projeto Subversion é construir um sistema de controle de
versões que seja um substituto para o CVS (Concurrent Versioning
System) na comunidade opensource, fornecendo grandes melhorias.

%package libs
Summary:	Subversion libraries and modules
Summary(pl):	Biblioteka subversion oraz ³adowalne modu³y
Group:		Libraries
Obsoletes:	libsubversion0

%description libs
Subversion libraries and modules.

%description libs -l pl
Biblioteka subversion oraz ³adowalne modu³y.

%package devel
Summary:	Header files and develpment documentation for subversion
Summary(pl):	Pliki nag³ówkowe i dokumetacja do subversion
Summary(pt_BR):	Arquivos de desenvolvimento para o Subversion
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}
Obsoletes:	libsubversion0-devel

%description devel
Header files and develpment documentation for subversion.

%description devel -l pl
Pliki nag³ówkowe i dokumetacja do subversion.

%description devel -l pt_BR
Este pacote provê os arquivos necessários para desenvolvedores
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
Este pacote provê um cliente estático do subversion.

%package tools
Summary:	Subversion tools and scripts
Summary(pl):	Narzêdzia oraz skrypty dla subversion
Summary(pt_BR):	Módulos python para acessar os recursos do Subversion
Group:		Applications
%pyrequires_eq	python
Requires:	python-rcsparse >= 0.1-0.20031026.0
Requires:	python-subversion = %{version}

%description tools
Subversion tools and scripts.

%description tools -l pl
Narzêdzia oraz skrypty dla subversion.


%package -n python-subversion
Summary:	Subversion python bindings
Summary(pl):	Dowi±zania do subversion dla pythona
Summary(pt_BR):	Módulos python para acessar os recursos do Subversion
Group:		Development/Languages/Python
%pyrequires_eq	python
Obsoletes:	subversion-python

%description -n python-subversion
Subversion python bindings.

%description -n python-subversion -l pl
Dowi±zania do subversion dla pythona.

%description -n python-subversion -l pt_BR
Módulos python para acessar os recursos do Subversion.

%package -n apache-mod_dav_svn
Summary:	Apache module: Subversion Server
Summary(pl):	Modu³ apache: Serwer Subversion
Group:		Networking/Daemons
Requires:	apache >= 2.0.47
Requires:	apache(modules-api) = %{apache_modules_api}
Requires:	apache-mod_dav

%description -n apache-mod_dav_svn
Apache module: Subversion Server.

%description -n apache-mod_dav_svn -l pl
Modu³ apache: Serwer Subversion.

%package -n apache-mod_authz_svn
Summary:	Apache module: Subversion Server - path-based authorization
Summary(pl):	Modu³ apache: autoryzacja na podstawie ¶cie¿ki dla serwera Subversion
Group:		Networking/Daemons
Requires:	apache-mod_dav_svn = %{version}
Requires:	apache >= 2.0.47
Requires:	apache(modules-api) = %{apache_modules_api}

%description -n apache-mod_authz_svn
Apache module: Subversion Server - path-based authorization.

%description -n apache-mod_authz_svn -l pl
Modu³ apache: autoryzacja na podstawie ¶cie¿ki dla serwera Subversion.

%prep
%setup -q

%build
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
%{__make} swig-py \
	swig_pydir=%{py_sitedir}/libsvn \
	swig_pydir_extra=%{py_sitedir}/svn
%endif

# build documentation; build process for documentation is severely
# braindamaged -- authors suggests to untar docbook distribution in
# build directory, hence the hack here
%{__make} -C doc/book all-html \
	XSL_DIR=/usr/share/sgml/docbook/xsl-stylesheets/

# prepare for %%doc below
mv -f doc/book/book/html-chunk svn-handbook
mkdir svn-handbook/images/
cp -f doc/book/book/images/*.png svn-handbook/images/

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/httpd/httpd.conf,%{_apachelibdir},%{_infodir}}

%{__make} install \
	LC_ALL=C \
	%{!?with_net_client_only:install-swig-py} \
	DESTDIR=$RPM_BUILD_ROOT \
	swig_pydir=%{py_sitedir}/libsvn \
	swig_pydir_extra=%{py_sitedir}/svn

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/httpd.conf/65_mod_dav_svn.conf
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/httpd.conf/66_mod_authz_svn.conf
install doc/programmer/design/*.info* $RPM_BUILD_ROOT%{_infodir}/

%if ! %{with net_client_only}
install tools/cvs2svn/cvs2svn.py	$RPM_BUILD_ROOT%{_bindir}/cvs2svn
install tools/cvs2svn/cvs2svn.1		$RPM_BUILD_ROOT%{_mandir}/man1
cp tools/cvs2svn/README tools/cvs2svn/README.cvs2svn

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post devel
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun devel
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

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
%attr(755,root,root) %{_bindir}/svn*
#%exclude %{_bindir}/svn-config
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%{?with_internal_neon:%exclude %{_mandir}/man1/neon*}

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/%{name}*
#%attr(755,root,root) %{_bindir}/svn-config
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_infodir}/svn*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%if ! %{with net_client_only}
%files tools
%defattr(644,root,root,755)
%doc tools/cvs2svn/README*
%attr(755,root,root) %{_bindir}/cvs*
%{_mandir}/man1/cvs*

%files -n python-subversion
%defattr(644,root,root,755)
%doc tools/backup/*.py tools/examples/*.py
%dir %{py_sitedir}/svn
%dir %{py_sitedir}/libsvn
%{py_sitedir}/svn/*.py[co]
%{py_sitedir}/libsvn/*.py[co]
%attr(755,root,root) %{py_sitedir}/libsvn/*.so

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
