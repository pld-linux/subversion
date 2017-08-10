#
# Conditional build:
%bcond_with	net_client_only		# build only net client
%bcond_without	swig			# disable bindings generation with Swig
%bcond_without	python			# build without Python bindings (broken)
%bcond_without	csvn			# build Python csvn bindings
%bcond_without	perl			# build without Perl bindings
%bcond_without	ruby			# build without Ruby bindings
%bcond_without	apache			# build without Apache support (webdav, etc)
%bcond_without	java			# build without javahl support (Java high-level bindings)
%bcond_with	tests			# don't perform "make check"
%bcond_without	kwallet			# build without kde4 wallet support
%bcond_without	kde			# build without kde4 support (alias for kwallet)
%bcond_without	gnome			# build without gnome keyring support
%bcond_without	db			# disable Subversion Berkeley DB based filesystem library
%bcond_with	db6			# allow BDB6 (not tested by upstream, released on AGPL)

# for AC: --without csvn,gnome,java,kde,ruby

%if %{with net_client_only}
%undefine	with_apache
%undefine	with_db
%undefine	with_swig
%undefine	with_java
%undefine	with_csvn
%undefine	with_gnome
%undefine	with_kde
%endif

%if %{without swig}
%undefine	with_perl
%undefine	with_python
%undefine	with_ruby
%endif

%if %{without kde}
%undefine	with_kwallet
%endif

%if %{without python} && %{without perl} && %{without ruby}
%undefine	with_swig
%endif

%define	apxs	/usr/sbin/apxs
%define	pdir	SVN
%define	pnam	_Core

%{?with_perl:%include	/usr/lib/rpm/macros.perl}
Summary:	A Concurrent Versioning system similar to but better than CVS
Summary(pl.UTF-8):	System kontroli wersji podobny, ale lepszy, niż CVS
Summary(pt_BR.UTF-8):	Sistema de versionamento concorrente
Name:		subversion
Version:	1.9.7
Release:	1
License:	Apache v2.0
Group:		Development/Version Control
Source0:	http://www.apache.org/dist/subversion/%{name}-%{version}.tar.bz2
# Source0-md5:	05b0c677681073920f938c1f322e0be2
Source1:	%{name}-dav_svn.conf
Source2:	%{name}-authz_svn.conf
Source3:	%{name}-svnserve.init
Source4:	%{name}-svnserve.sysconfig
# current subversion tarball has correct *.swg files
# but after regeneration these are broken again, so
# we still need this script
Source5:	%{name}-convert-typemaps-to-ifdef.py
Patch0:		%{name}-home_etc.patch
Patch1:		%{name}-DESTDIR.patch
Patch2:		%{name}-ruby-datadir-path.patch
Patch3:		%{name}-tests.patch
Patch4:		x32-libdir.patch
URL:		http://subversion.apache.org/
%{?with_apache:BuildRequires:	apache-devel >= 2.4.14}
BuildRequires:	apr-devel >= 1:1.3
BuildRequires:	apr-util-devel >= 1:1.3
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	cyrus-sasl-devel
%if %{with kwallet} || %{with gnome}
BuildRequires:	dbus-devel
%endif
%{!?with_db6:BuildRequires:	db-devel < 6}
BuildRequires:	db-devel >= 4.1.25
BuildRequires:	expat-devel
BuildRequires:	gettext-tools
%{?with_gnome:BuildRequires:	glib2-devel >= 2.0}
%{?with_kwallet:BuildRequires:	kde4-kdelibs-devel}
%{?with_gnome:BuildRequires:	libgnome-keyring-devel}
BuildRequires:	libmagic-devel
BuildRequires:	libtool >= 1.4-9
BuildRequires:	pkgconfig
%{?with_csvn:BuildRequires:	python-ctypesgen}
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.656
BuildRequires:	sed >= 4.0
BuildRequires:	serf-devel >= 1.3.4
BuildRequires:	sqlite3-devel >= 3.7.12
BuildRequires:	texinfo
BuildRequires:	which
%if %{with java}
BuildRequires:	jdk >= 1.5
BuildRequires:	libstdc++-devel
%endif
%if %{with perl}
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	swig-perl >= 1.3.24
%endif
%if %{with python}
BuildRequires:	python-devel >= 1:2.4
BuildRequires:	swig-python >= 1.3.24
%endif
%if %{with ruby}
BuildRequires:	rpm-rubyprov
BuildRequires:	ruby-devel >= 1:1.8.2
BuildRequires:	ruby-irb
BuildRequires:	ruby-rubygems
BuildRequires:	swig-ruby >= 1.3.24
%endif
Requires:	%{name}-libs = %{version}-%{release}
%requires_ge	sqlite3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir		%{_libdir}/svn
%define		apacheconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)/conf.d
%define		apachelibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)

%define		skip_post_check_so	libsvn_swig_py-1.so.* libsvn_swig_perl-1.so.* libsvn_fs_x-1.so.*

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
Requires:	apr >= 1:1.3
Requires:	apr-util >= 1:1.3
Requires:	serf >= 1.3.4
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
Requires:	apr-util-devel >= 1:1.3
Requires:	serf-devel >= 1.3.4
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
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/lib/rpm/user_group.sh
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(pre):	/usr/sbin/usermod
Requires:	%{name} = %{version}-%{release}
Requires:	rc-scripts
Provides:	group(svn)
Provides:	user(svn)

%description svnserve
Subversion svnserve server.

%description svnserve -l pl.UTF-8
Serwer subversion svnserve.

%package tools
Summary:	Subversion tools and scripts
Summary(pl.UTF-8):	Narzędzia oraz skrypty dla subversion
Summary(pt_BR.UTF-8):	Módulos python para acessar os recursos do Subversion
Group:		Applications
Requires:	%{name} = %{version}-%{release}
Requires:	python
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
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n bash-completion-subversion
Bash completion for subversion.

%description -n bash-completion-subversion -l pl.UTF-8
Dopełnienia basha dla subversion.

%package -n java-subversion
Summary:	Subversion Java bindings
Summary(pl.UTF-8):	Dowiązania do Subversion dla Javy
Group:		Development/Languages/Java
Requires:	%{name}-libs = %{version}-%{release}

%description -n java-subversion
This is a set of Java classes which provide the functionality of
subversion-libs, the Subversion libraries. It is useful if you want
to, for example, write a Java class that manipulates a Subversion
repository or working copy. See the 'subversion' package for more
information.

%description -n java-subversion -l pl.UTF-8
Ten pakiet zawiera zestaw klas Javy udostępniających funkcjonalność
subversion-libs, czyli bibliotek Subversion. Jest przydatny przy
pisaniu klas Javy np. modyfikujących repozytorium Subversion lub kopię
roboczą. Więcej informacji w pakiecie subversion.

%package -n python-subversion
Summary:	Subversion Python bindings
Summary(pl.UTF-8):	Dowiązania do Subversion dla Pythona
Summary(pt_BR.UTF-8):	Módulos Python para acessar os recursos do Subversion
Group:		Development/Languages/Python
Requires:	%{name}-libs = %{version}-%{release}
Requires:	python
Obsoletes:	subversion-python

%description -n python-subversion
Subversion Python bindings.

%description -n python-subversion -l pl.UTF-8
Dowiązania do Subversion dla Pythona.

%description -n python-subversion -l pt_BR.UTF-8
Módulos Python para acessar os recursos do Subversion.

%package -n python-csvn
Summary:	CTypes Subversion Python bindings
Summary(pl.UTF-8):	Dowiązania do Subversion dla Pythona
Summary(pt_BR.UTF-8):	Módulos Python para acessar os recursos do Subversion
Group:		Development/Languages/Python
Requires:	%{name}-libs = %{version}-%{release}
Requires:	python

%description -n python-csvn
Subversion CTypes Python bindings.

%description -n python-csvn -l pl.UTF-8
Dowiązania do Subversion dla Pythona używające CTypes.

%description -n python-csvn -l pt_BR.UTF-8
Módulos Python para acessar os recursos do Subversion.

%package -n perl-subversion
Summary:	Subversion Perl bindings
Summary(pl.UTF-8):	Dowiązania do Subversion dla Perla
Summary(pt_BR.UTF-8):	Módulos Perl para acessar os recursos do Subversion
Group:		Development/Languages/Perl
Requires:	%{name}-libs = %{version}-%{release}
Obsoletes:	subversion-perl

%description -n perl-subversion
Subversion Perl bindings.

%description -n perl-subversion -l pl.UTF-8
Dowiązania do Subversion dla Perla.

%description -n perl-subversion -l pt_BR.UTF-8
Módulos Perl para acessar os recursos do Subversion.

%package -n ruby-subversion
Summary:	Subversion Ruby bindings
Summary(pl.UTF-8):	Dowiązania do Subversion dla języka Ruby
Summary(pt_BR.UTF-8):	Módulos Ruby para acessar os recursos do Subversion
Group:		Development/Languages
Requires:	%{name}-libs = %{version}-%{release}
Obsoletes:	subversion-ruby

%description -n ruby-subversion
Subversion Ruby bindings.

%description -n ruby-subversion -l pl.UTF-8
Dowiązania do Subversion dla języka Ruby.

%description -n ruby-subversion -l pt_BR.UTF-8
Módulos Ruby para acessar os recursos do Subversion.

%package -n apache-mod_dav_svn
Summary:	Apache module: Subversion Server
Summary(pl.UTF-8):	Moduł Apache'a: serwer Subversion
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}
Requires:	apache(modules-api) = %apache_modules_api
Requires:	apache-mod_dav

%description -n apache-mod_dav_svn
Apache module: Subversion Server.

%description -n apache-mod_dav_svn -l pl.UTF-8
Moduł Apache'a: serwer Subversion.

%package -n apache-mod_authz_svn
Summary:	Apache module: Subversion Server - path-based authorization
Summary(pl.UTF-8):	Moduł Apache'a: autoryzacja na podstawie ścieżki dla serwera Subversion
Group:		Networking/Daemons
Requires:	%{name}-libs = %{version}-%{release}
Requires:	apache(modules-api) = %apache_modules_api
Requires:	apache-mod_dav_svn = %{version}-%{release}

%description -n apache-mod_authz_svn
Apache module: Subversion Server - path-based authorization.

%description -n apache-mod_authz_svn -l pl.UTF-8
Moduł Apache'a: autoryzacja na podstawie ścieżki dla serwera
Subversion.

%package -n apache-mod_dontdothat_svn
Summary:	Apache module: Allows you to block specific svn requests
Summary(pl.UTF-8):	Moduł Apache'a pozwalający na blokowanie pewnych zapytań svn
Group:		Networking/Daemons
Requires:	%{name}-libs = %{version}-%{release}
Requires:	apache(modules-api) = %apache_modules_api
Requires:	apache-mod_dav_svn = %{version}-%{release}

%description -n apache-mod_dontdothat_svn
Apache module: Allows you to block specific svn requests.

%description -n apache-mod_dontdothat_svn -l pl.UTF-8
Moduł Apache'a pozwalający na blokowanie pewnych zapytań svn.

%package -n gnome-keyring-subversion
Summary:	GNOME Keyring authentication provider for Subversion
Summary(pl.UTF-8):	Moduł uwierzytelniający GNOME Keyring dla Subversion
Group:		X11/Applications
Requires:	%{name}-libs = %{version}-%{release}

%description -n gnome-keyring-subversion
Authentication provider module for Subversion which allows SVN client
to authenticate using GNOME Keyring.

%description -n gnome-keyring-subversion -l pl.UTF-8
Moduł uwierzytelniający dla Subversion pozwalający klientom SVN
uwierzytelniać się przy użyciu mechanizmu GNOME Keyring.

%package -n kde4-kwallet-subversion
Summary:	KDE Wallet authentication provider for Subversion
Summary(pl.UTF-8):	Moduł uwierzytelniający dla Subversion wykorzystujący Portfel KDE
Group:		X11/Applications
Requires:	%{name}-libs = %{version}-%{release}

%description -n kde4-kwallet-subversion
Authentication provider module for Subversion which allows SVN client
to authenticate using KDE Wallet.

%description -n kde4-kwallet-subversion -l pl.UTF-8
Moduł uwierzytelniający dla Subversion pozwalający klientom SVN
uwierzytelniać się przy użyciu Portfela KDE.

%prep
%setup -q
%patch0 -p0
%patch1 -p1
%patch2 -p0
%patch3 -p1
%patch4 -p1

sed -i -e 's#serf_prefix/lib#serf_prefix/%{_lib}#g' build/ac-macros/serf.m4

%build
# disabled regeneration - subversion 1.6.13 is not ready for swig 2.0.x
#%{__rm} subversion/bindings/swig/proxy/*.swg
#cd subversion/bindings/swig && python "%{SOURCE5}" && cd ../../..
chmod +x ./autogen.sh && ./autogen.sh
%{__libtoolize}
%configure \
	--with-editor=vi \
	--with-zlib=%{_libdir} \
	--disable-runtime-module-search \
	--disable-mod-activation \
%if %{with db}
	--with-berkeley-db="db.h:%{_includedir}:%{_libdir}:db" \
	%{?with_db6:--enable-bdb6} \
%else
	--without-berkeley-db \
%endif
%if %{with apache}
	--with-apache-libexecdir="$(%{_sbindir}/apxs -q LIBEXECDIR)" \
	--with-apxs=%{_sbindir}/apxs \
%else
	--without-apxs \
%endif
%if %{without swig}
	--without-swig \
%endif
%if %{with ruby}
	svn_cv_ruby_sitedir_libsuffix="" \
	svn_cv_ruby_sitedir_archsuffix="" \
	--with-ruby-sitedir=%{ruby_vendorarchdir} \
%else
	ac_cv_path_RUBY=none \
%endif
%if %{with csvn}
	--with-ctypesgen=%{_bindir}/ctypesgen.py \
%endif
%if %{with java}
	--enable-javahl \
	--with-jdk="%{java_home}" \
	--without-jikes \
%else
	--disable-javahl \
%endif
	--with-serf=%{_prefix} \
	--with-apr=%{_bindir}/apr-1-config \
	--with-apr-util=%{_bindir}/apu-1-config \
%if %{with kwallet}
	--with-kwallet \
%endif
%if %{with gnome}
	--with-gnome-keyring
%endif

%{__make} -j1

%{__make} tools

%if %{with csvn}
# Python ctypes bindings
%{__make} ctypes-python
%endif
%if %{with python}
# Python swig bindings
%{__make} swig-py \
	swig_pydir=%{py_sitedir}/libsvn \
	swig_pydir_extra=%{py_sitedir}/svn
%endif
%if %{with perl}
# Perl swig bindings
%{__make} -j1 swig-pl-lib
cd subversion/bindings/swig/perl/native
%{__perl} Makefile.PL INSTALLDIRS=vendor
%{__make} -j1
cd -
%endif
%if %{with java}
%{__make} -j1 javahl \
	javahl_javadir="%{_javadir}"
%endif
# ruby
%if %{with ruby}
%{__make} swig-rb
%endif

%if %{with tests}
%{__make} -j1 check
%if %{with csvn}
%{__make} -j1 check-ctypes-python
%endif
%if %{with python}
%{__make} -j1 check-swig-py
%endif
%if %{with perl}
%{__make} -j1 check-swig-pl
%endif
%if %{with ruby}
# disabled, see https://bugs.launchpad.net/pld-linux/+bug/734340
#%{__make} check-swig-rb
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig,bash_completion.d} \
	$RPM_BUILD_ROOT{%{apacheconfdir},%{apachelibdir},%{_infodir}} \
	$RPM_BUILD_ROOT%{_examplesdir}/{%{name}-%{version},python-%{name}-%{version}} \
	$RPM_BUILD_ROOT%{_sysconfdir}/%{name} \
	$RPM_BUILD_ROOT/home/services/subversion{,/repos}

%{__make} -j1 install \
	pkgconfig_dir=%{_pkgconfigdir} \
	toolsdir=%{_bindir} \
	DESTDIR=$RPM_BUILD_ROOT \
	APACHE_LIBEXECDIR="$(%{_sbindir}/apxs -q LIBEXECDIR)" \
%if %{with java}
	install-javahl \
	javahl_javadir="%{_javadir}" \
%endif
%if %{with python}
	install-swig-py \
	swig_pydir=%{py_sitedir}/libsvn \
	swig_pydir_extra=%{py_sitedir}/svn \
%endif
	install-tools

%if %{with csvn}
# manually execute install-ctypes-python target
cd subversion/bindings/ctypes-python
%py_install
cd ../../..
%endif

%if %{with ruby}
%{__make} -j1 install-swig-rb install-swig-rb-doc \
	SWIG_RB_RI_DATADIR=$RPM_BUILD_ROOT%{ruby_ridir} \
	DESTDIR=$RPM_BUILD_ROOT

# not our package
%{__rm} -r $RPM_BUILD_ROOT%{ruby_ridir}/OptionParser
%{__rm} -r $RPM_BUILD_ROOT%{ruby_ridir}/Time
%if "%{ruby_abi}" >= "2.0"
%{__rm} -r $RPM_BUILD_ROOT%{ruby_ridir}/File
%endif
%{__rm} $RPM_BUILD_ROOT%{ruby_ridir}/cache.ri
%{__rm} $RPM_BUILD_ROOT%{ruby_ridir}/created.rid
%endif

%if %{with perl}
%{__make} install-swig-pl-lib \
	DESTDIR=$RPM_BUILD_ROOT
%{__make} -C subversion/bindings/swig/perl/native install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=$RPM_BUILD_ROOT%{_prefix} \
	LIBDIR=$RPM_BUILD_ROOT%{_libdir}
%endif

%if %{with apache}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{apacheconfdir}/65_mod_dav_svn.conf
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{apacheconfdir}/66_mod_authz_svn.conf
cp -p %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/svnserve
install -p %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/svnserve
%endif

%if %{without net_client_only}
install -p tools/backup/hot-backup.py $RPM_BUILD_ROOT%{_bindir}/svn-hot-backup
%endif

# rename not to conflict with standard packages. (are these needed at all?)
%{__mv} $RPM_BUILD_ROOT%{_bindir}/{,svn}diff
%{__mv} $RPM_BUILD_ROOT%{_bindir}/{,svn}diff3
%{__mv} $RPM_BUILD_ROOT%{_bindir}/{,svn}diff4

%if %{with python} || %{with csvn}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean
%endif
%if %{with python}
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/libsvn/*.la
# .a created on ac only
%{__rm} -f $RPM_BUILD_ROOT%{py_sitedir}/libsvn/*.a
cp -p tools/examples/*.py $RPM_BUILD_ROOT%{_examplesdir}/python-%{name}-%{version}
%endif

cp -p tools/client-side/bash_completion $RPM_BUILD_ROOT/etc/bash_completion.d/%{name}
cp -p tools/examples/*.c $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%if %{with java}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libsvnjavahl*.{la,a}
%endif
%if %{with swig}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libsvn_swig*.{la,a}
%if %{with ruby}
%{__rm} $RPM_BUILD_ROOT%{ruby_vendorarchdir}/svn/ext/*.la
%endif
%endif
%if %{with gnome} || %{with kwallet}
# dlopened by soname (libsvn_auth_*-1.so.0)
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libsvn_auth_*-1.{so,la,a}
%endif

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre svnserve
%groupadd -g 86 svn
%useradd -u 180 -d /home/services/subversion -c "Subversion svnserve" -g svn svn

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post	devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%post	-n java-subversion -p /sbin/ldconfig
%postun	-n java-subversion -p /sbin/ldconfig

%post	-n perl-subversion -p /sbin/ldconfig
%postun	-n perl-subversion -p /sbin/ldconfig

%post	-n python-subversion -p /sbin/ldconfig
%postun	-n python-subversion -p /sbin/ldconfig

%post	-n ruby-subversion -p /sbin/ldconfig
%postun	-n ruby-subversion -p /sbin/ldconfig

%post	-n gnome-keyring-subversion -p /sbin/ldconfig
%postun	-n gnome-keyring-subversion -p /sbin/ldconfig

%post	-n kde4-kwallet-subversion -p /sbin/ldconfig
%postun	-n kde4-kwallet-subversion -p /sbin/ldconfig

%post svnserve
/sbin/chkconfig --add svnserve
%service svnserve restart "svnserve daemon"

%preun svnserve
if [ "$1" = "0" ]; then
	%service svnserve stop
	/sbin/chkconfig --del svnserve
fi

%postun svnserve
if [ "$1" = "0" ]; then
	%userremove svn
	%groupremove svn
fi

%post -n apache-mod_dav_svn
%service -q httpd restart

%postun -n apache-mod_dav_svn
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%post -n apache-mod_authz_svn
%service -q httpd restart

%postun -n apache-mod_authz_svn
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%post -n apache-mod_dontdothat_svn
%service -q httpd restart

%postun -n apache-mod_dontdothat_svn
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc BUGS CHANGES INSTALL README
%doc doc/*/*.html
%doc tools/hook-scripts/*.{pl,py,example}
%doc tools/hook-scripts/mailer/*.{py,example}
%doc tools/xslt/*
%attr(755,root,root) %{_bindir}/svn
%attr(755,root,root) %{_bindir}/svnadmin
%attr(755,root,root) %{_bindir}/svndumpfilter
%attr(755,root,root) %{_bindir}/svnlook
%attr(755,root,root) %{_bindir}/svnmucc
%attr(755,root,root) %{_bindir}/svnrdump
%attr(755,root,root) %{_bindir}/svnsync
%attr(755,root,root) %{_bindir}/svnversion
%{_mandir}/man1/svn.1*
%{_mandir}/man1/svnadmin.1*
%{_mandir}/man1/svndumpfilter.1*
%{_mandir}/man1/svnrdump.1*
%{_mandir}/man1/svnlook.1*
%{_mandir}/man1/svnmucc.1*
%{_mandir}/man1/svnsync.1*
%{_mandir}/man1/svnversion.1*

%files libs -f %{name}.lang
%defattr(644,root,root,755)
%dir %{_sysconfdir}/%{name}
%attr(755,root,root) %{_libdir}/libsvn_client-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsvn_client-1.so.0
%attr(755,root,root) %{_libdir}/libsvn_delta-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsvn_delta-1.so.0
%attr(755,root,root) %{_libdir}/libsvn_diff-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsvn_diff-1.so.0
%attr(755,root,root) %{_libdir}/libsvn_fs-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsvn_fs-1.so.0
%if %{without net_client_only}
%attr(755,root,root) %{_libdir}/libsvn_fs_base-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsvn_fs_base-1.so.0
%endif
%attr(755,root,root) %{_libdir}/libsvn_fs_fs-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsvn_fs_fs-1.so.0
%attr(755,root,root) %{_libdir}/libsvn_fs_util-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsvn_fs_util-1.so.0
%attr(755,root,root) %{_libdir}/libsvn_fs_x-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsvn_fs_x-1.so.0
%attr(755,root,root) %{_libdir}/libsvn_ra-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsvn_ra-1.so.0
%attr(755,root,root) %{_libdir}/libsvn_ra_local-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsvn_ra_local-1.so.0
%attr(755,root,root) %{_libdir}/libsvn_ra_serf-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsvn_ra_serf-1.so.0
%attr(755,root,root) %{_libdir}/libsvn_ra_svn-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsvn_ra_svn-1.so.0
%attr(755,root,root) %{_libdir}/libsvn_repos-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsvn_repos-1.so.0
%attr(755,root,root) %{_libdir}/libsvn_subr-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsvn_subr-1.so.0
%attr(755,root,root) %{_libdir}/libsvn_wc-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsvn_wc-1.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsvn_client-1.so
%attr(755,root,root) %{_libdir}/libsvn_delta-1.so
%attr(755,root,root) %{_libdir}/libsvn_diff-1.so
%attr(755,root,root) %{_libdir}/libsvn_fs-1.so
%if %{without net_client_only}
%attr(755,root,root) %{_libdir}/libsvn_fs_base-1.so
%endif
%attr(755,root,root) %{_libdir}/libsvn_fs_fs-1.so
%attr(755,root,root) %{_libdir}/libsvn_fs_util-1.so
%attr(755,root,root) %{_libdir}/libsvn_fs_x-1.so
%attr(755,root,root) %{_libdir}/libsvn_ra-1.so
%attr(755,root,root) %{_libdir}/libsvn_ra_local-1.so
%attr(755,root,root) %{_libdir}/libsvn_ra_serf-1.so
%attr(755,root,root) %{_libdir}/libsvn_ra_svn-1.so
%attr(755,root,root) %{_libdir}/libsvn_repos-1.so
%attr(755,root,root) %{_libdir}/libsvn_subr-1.so
%attr(755,root,root) %{_libdir}/libsvn_wc-1.so
%{_libdir}/libsvn_client-1.la
%{_libdir}/libsvn_delta-1.la
%{_libdir}/libsvn_diff-1.la
%{_libdir}/libsvn_fs-1.la
%if %{without net_client_only}
%{_libdir}/libsvn_fs_base-1.la
%endif
%{_libdir}/libsvn_fs_fs-1.la
%{_libdir}/libsvn_fs_util-1.la
%{_libdir}/libsvn_fs_x-1.la
%{_libdir}/libsvn_ra-1.la
%{_libdir}/libsvn_ra_local-1.la
%{_libdir}/libsvn_ra_serf-1.la
%{_libdir}/libsvn_ra_svn-1.la
%{_libdir}/libsvn_repos-1.la
%{_libdir}/libsvn_subr-1.la
%{_libdir}/libsvn_wc-1.la
%if %{with gnome}
# only for feature check, linking will fail (no libsvn_auth_gnome_keyring.so)
%{_pkgconfigdir}/libsvn_auth_gnome_keyring.pc
%endif
%if %{with kwallet}
# only for feature check, linking will fail (no libsvn_auth_kwallet.so)
%{_pkgconfigdir}/libsvn_auth_kwallet.pc
%endif
%{_pkgconfigdir}/libsvn_client.pc
%{_pkgconfigdir}/libsvn_delta.pc
%{_pkgconfigdir}/libsvn_diff.pc
%{_pkgconfigdir}/libsvn_fs.pc
%if %{without net_client_only}
%{_pkgconfigdir}/libsvn_fs_base.pc
%endif
%{_pkgconfigdir}/libsvn_fs_fs.pc
%{_pkgconfigdir}/libsvn_fs_util.pc
%{_pkgconfigdir}/libsvn_fs_x.pc
%{_pkgconfigdir}/libsvn_ra.pc
%{_pkgconfigdir}/libsvn_ra_local.pc
%{_pkgconfigdir}/libsvn_ra_serf.pc
%{_pkgconfigdir}/libsvn_ra_svn.pc
%{_pkgconfigdir}/libsvn_repos.pc
%{_pkgconfigdir}/libsvn_subr.pc
%{_pkgconfigdir}/libsvn_wc.pc
%{_includedir}/%{name}-1
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/libsvn_client-1.a
%{_libdir}/libsvn_delta-1.a
%{_libdir}/libsvn_diff-1.a
%{_libdir}/libsvn_fs-1.a
%if %{without net_client_only}
%{_libdir}/libsvn_fs_base-1.a
%endif
%{_libdir}/libsvn_fs_fs-1.a
%{_libdir}/libsvn_fs_util-1.a
%{_libdir}/libsvn_fs_x-1.a
%{_libdir}/libsvn_ra-1.a
%{_libdir}/libsvn_ra_local-1.a
%{_libdir}/libsvn_ra_serf-1.a
%{_libdir}/libsvn_ra_svn-1.a
%{_libdir}/libsvn_repos-1.a
%{_libdir}/libsvn_subr-1.a
%{_libdir}/libsvn_wc-1.a

%if %{with gnome}
%files -n gnome-keyring-subversion
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsvn_auth_gnome_keyring-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsvn_auth_gnome_keyring-1.so.0
# does anything use it? requires libsvn_auth_gnome_keyring.so
#%{_pkgconfigdir}/libsvn_auth_gnome_keyring.pc
%endif

%if %{with kwallet}
%files -n kde4-kwallet-subversion
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsvn_auth_kwallet-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsvn_auth_kwallet-1.so.0
# does anything use it? requires libsvn_auth_kwallet.so
#%{_pkgconfigdir}/libsvn_auth_kwallet.pc
%endif

%if %{without net_client_only}
%files svnserve
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/svnserve
%{_mandir}/man5/svnserve.conf.5*
%{_mandir}/man8/svnserve.8*
%dir %attr(750,svn,svn) /home/services/subversion
%dir %attr(750,svn,svn) /home/services/subversion/repos
%if %{with apache}
%attr(754,root,root) /etc/rc.d/init.d/svnserve
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/svnserve
%endif

%files tools
%defattr(644,root,root,755)
# tools/backup/hot-backup.py
%attr(755,root,root) %{_bindir}/svn-hot-backup

# tools/diff
%attr(755,root,root) %{_bindir}/svndiff
%attr(755,root,root) %{_bindir}/svndiff3
%attr(755,root,root) %{_bindir}/svndiff4

# tools/server-side
%attr(755,root,root) %{_bindir}/svnfsfs
%attr(755,root,root) %{_bindir}/svn-populate-node-origins-index
%attr(755,root,root) %{_bindir}/svnauthz
%attr(755,root,root) %{_bindir}/svnauthz-validate

# tools/client-side
%attr(755,root,root) %{_bindir}/svnbench

# tools/dev/svnraisetreeconflict
%attr(755,root,root) %{_bindir}/svnraisetreeconflict

# tools/dev/
%attr(755,root,root) %{_bindir}/fsfs-access-map
%attr(755,root,root) %{_bindir}/x509-parser

%files -n bash-completion-subversion
%defattr(644,root,root,755)
/etc/bash_completion.d/%{name}

%endif # net_client_only

%if %{with java}
%files -n java-subversion
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsvnjavahl-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsvnjavahl-1.so.0
%attr(755,root,root) %{_libdir}/libsvnjavahl-1.so
%{_javadir}/svn-javahl.jar
%endif

%if %{with python}
%files -n python-subversion
%defattr(644,root,root,755)
%doc tools/backup/*.py
%attr(755,root,root) %{_libdir}/libsvn_swig_py-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsvn_swig_py-1.so.0
%attr(755,root,root) %{_libdir}/libsvn_swig_py-1.so
%dir %{py_sitedir}/libsvn
%attr(755,root,root) %{py_sitedir}/libsvn/_*.so
%{py_sitedir}/libsvn/*.py[co]
%dir %{py_sitedir}/svn
%{py_sitedir}/svn/*.py[co]
%{_examplesdir}/python-%{name}-%{version}
%endif

%if %{with csvn}
%files -n python-csvn
%defattr(644,root,root,755)
%doc subversion/bindings/ctypes-python/{README,TODO}
%doc subversion/bindings/ctypes-python/examples/*.py
%dir %{py_sitescriptdir}/csvn
%{py_sitescriptdir}/csvn/*.py[co]
%dir %{py_sitescriptdir}/csvn/core
%{py_sitescriptdir}/csvn/core/*.py[co]
%dir %{py_sitescriptdir}/csvn/ext
%{py_sitescriptdir}/csvn/ext/*.py[co]
%{py_sitescriptdir}/svn_ctypes_python_bindings-0.1-py*.egg-info
%endif

%if %{with perl}
%files -n perl-subversion
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsvn_swig_perl-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsvn_swig_perl-1.so.0
%attr(755,root,root) %{_libdir}/libsvn_swig_perl-1.so
%{perl_vendorarch}/SVN
%dir %{perl_vendorarch}/auto/SVN
%dir %{perl_vendorarch}/auto/SVN/*
%attr(755,root,root) %{perl_vendorarch}/auto/SVN/*/*.so
%{_mandir}/man3/*.3pm*
%endif

%if %{with ruby}
%files -n ruby-subversion
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsvn_swig_ruby-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsvn_swig_ruby-1.so.0
%attr(755,root,root) %{_libdir}/libsvn_swig_ruby-1.so
%dir %{ruby_vendorarchdir}/svn
%{ruby_vendorarchdir}/svn/*.rb
%dir %{ruby_vendorarchdir}/svn/ext
%attr(755,root,root) %{ruby_vendorarchdir}/svn/ext/*.so
%{ruby_ridir}/Svn
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

%files -n apache-mod_dontdothat_svn
%defattr(644,root,root,755)
%doc tools/server-side/mod_dontdothat/README
%attr(755,root,root) %{apachelibdir}/mod_dontdothat.so
%endif
