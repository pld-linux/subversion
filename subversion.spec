%define	repov	2817
%include        /usr/lib/rpm/macros.python
Summary:	A Concurrent Versioning system similar to but better than CVS
Summary(pl):	System kontroli wersji ale lepszy ni¿ CVS
Name:		subversion
Version:	0.14.0
Release:	r%{repov}.1
License:	Apache/BSD Style
Group:		Development/Version Control
Source0:	svn://svn.collab.net/repos/svn/trunk/%{name}-r%{repov}.tar.gz
Source1:	%{name}-dav_svn.conf
Patch0:		%{name}-lib.patch
Patch1:		%{name}-python.patch
Patch2:		%{name}-DESTDIR.patch
URL:		http://subversion.tigris.org/
BuildRequires:	apache-devel >= 2.0.39
BuildRequires:	apr-devel >= 2.0.39
BuildRequires:	autoconf >= 2.53
BuildRequires:	bison
BuildRequires:	db4-devel >= 4.0.14
BuildRequires:	expat-devel
BuildRequires:	libtool >= 1.4-9
BuildRequires:	neon-devel >= 0.21.3
BuildRequires:	python >= 2.2
BuildRequires:	rpm-pythonprov >= 4.0.2-50
BuildRequires:	swig >= 1.3.12
BuildRequires:	texinfo
Requires(post):	/usr/sbin/fix-info-dir
Requires(postun):	/usr/sbin/fix-info-dir
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

%package libs
Summary:	Subversion libraries and modules
Summary(pl):	Biblioteka subversion oraz ³adowalne modu³y
Group:		Libraries

%description libs
Subversion libraries and modules.

%description libs -l pl
Biblioteka subversion oraz ³adowalne modu³y.

%package devel
Summary:	Header files and develpment documentation for subversion
Summary(pl):	Pliki nag³ówkowe i dokumetacja do subversion
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}

%description devel
Header files and develpment documentation for subversion.

%description devel -l pl
Pliki nag³ówkowe i dokumetacja do subversion.

%package static
Summary:	Static subversion library
Summary(pl):	Biblioteka statyczna subversion
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static subversion library.

%description static -l pl
Biblioteka statyczna subversion.

%package python
Summary:	Subversion python bindings
Summary(pl):	Dowi±zania do subversion dla pythona
Group:		Development/Languages/Python
Requires:	python >= 2.2
%pyrequires_eq	python

%description python
Subversion python bindings.

%description python -l pl
Dowi±zania do subversion dla pythona.

%package -n apache-mod_dav_svn
Summary:	Apache module: Subversion Server
Summary(pl):	Modu³ apache: Serwer Subversion
Group:		Networking/Daemons
Requires:	apache >= 2.0.35
Requires:	apache-mod_dav >= 2.0.35

%description -n apache-mod_dav_svn
Apache module: Subversion Server.

%description -n apache-mod_dav_svn
Modu³ apache: Serwer Subversion.

%prep
%setup -q -n %{name}-r%{repov}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
chmod +x ./autogen.sh && ./autogen.sh
%configure \
	--disable-dso \
	--with-neon=%{_prefix} \
	--with-apr=%{_bindir}/apr-config \
	--with-apr-util=%{_bindir}/apu-config \
	--with-apxs=%{_sbindir}/apxs \
	--with-berkeley-db=%{_includedir}/db4:%{_libdir}
%{__make}

cd subversion/bindings/swig/python
CFLAGS="%{rpmcflags}" python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/httpd/httpd.conf,%{_apachelibdir}}

%{__make} install \
	INSTALL_MOD_SHARED=echo \
	DESTDIR=$RPM_BUILD_ROOT

install subversion/mod_dav_svn/.libs/*.so $RPM_BUILD_ROOT%{_apachelibdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/httpd.conf/65_mod_dav_svn.conf

cd subversion/bindings/swig/python
python setup.py install --root=$RPM_BUILD_ROOT

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc  BUGS CHANGES IDEAS INSTALL README
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*
%{_infodir}/svn*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/%{name}*
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %{_libdir}/lib*.la

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files python
%defattr(644,root,root,755)
%doc tools/backup tools/cvs2svn/*.py tools/examples/*.py
%dir %{py_sitedir}/svn
%{py_sitedir}/svn/*.py[co]
%attr(755,root,root) %{py_sitedir}/svn/*.so

%files -n apache-mod_dav_svn
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/httpd/httpd.conf/*_mod_dav_svn.conf
%attr(755,root,root) %{_apachelibdir}/*.so
