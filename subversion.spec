# TODO:
# - move modules to some directory (+ link with rpath)
# - python bindings subpackage
Summary:	A Concurrent Versioning system similar to but better than CVS.
Summary(pl):	System Concurrent Versioning System ale lepszy ni¿ CVS
Name:		subversion
Version:	1587
Release:	1
License:	Apache/BSD Style
Group:		Development/Version Control
Source0:	http://subversion.tigris.org/%{name}-r%{version}.tar.gz
Source1:	%{name}-dav_svn.conf
Patch0:		%{name}-lib.patch
Patch1:		%{name}-apache2.patch
URL:		http://subversion.tigris.org/
BuildRequires:	apache-devel >= 2.0.35
BuildRequires:	apr-devel >= 2.0.35
BuildRequires:	autoconf >= 2.53
BuildRequires:	bison
BuildRequires:	db4-devel >= 4.0.14
BuildRequires:	expat-devel
BuildRequires:	libtool >= 1.4
BuildRequires:	neon-devel >= 0.19.2
BuildRequires:	python >= 2.2
BuildRequires:	texinfo
Requires(post):	/usr/sbin/fix-info-dir
Requires(post):	/sbin/ldconfig
Requires(postun): /sbin/ldconfig 
Requires(postun): /usr/sbin/fix-info-dir 
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	/usr/lib/apache

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

%package devel
Summary:	Header files and develpment documentation for subversion
Summary(pl):	Pliki nag³ówkowe i dokumetacja do subversion
Group:		Development/Libraries
Requires:	%{name} = %{version}

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
%setup -q -n %{name}-r%{version}
%patch0 -p1
%patch1 -p1

%build
./autogen.sh
# EXPAT is external so get rid of all except (patched) xmlparse.h
rm -rf expat-lite/[a-w]*.[ch] expat-lite/xmldef.h expat-lite/xmlparse.c
rm -rf expat-lite/xmlrole* expat-lite/xmltok* neon apr
%configure \
	--enable-dso \
	--with-neon \
	--with-apr=%{_bindir}/apr-config \
	--with-apxs=%{_sbindir}/apxs \
	--with-berkeley-db=%{_includedir}/db4:%{_libdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/httpd/httpd.conf,%{_libexecdir}}

# relinking sux
for i in 1 2; do
[ "$i" = "2" ] && find . -name "*.la" -exec rm -f "{}" ";"
%{__make} install \
	INSTALL_MOD_SHARED=echo \
	DESTDIR=$RPM_BUILD_ROOT \
	libdir=$RPM_BUILD_ROOT%{_libdir} \
	fs_libdir=$RPM_BUILD_ROOT%{_libdir} \
	base_libdir=$RPM_BUILD_ROOT%{_libdir} \
	swig_py_libdir=$RPM_BUILD_ROOT%{_libdir} \
	bindir=$RPM_BUILD_ROOT%{_bindir} \
	fs_bindir=$RPM_BUILD_ROOT%{_bindir} \
	includedir=$RPM_BUILD_ROOT%{_includedir}/%{name}
done

install subversion/mod_dav_svn/.libs/*.so $RPM_BUILD_ROOT%{_libexecdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/httpd.conf/65_mod_dav_svn.conf

gzip -9nf BUGS CHANGES IDEAS INSTALL README

%post
/sbin/ldconfig
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
/sbin/ldconfig
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

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
%doc *.gz
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/libsvn_[cdsw]*.so.*
%attr(755,root,root) %{_libdir}/libsvn_ra.so.*
%attr(755,root,root) %{_libdir}/libsvn_fs*.so*
%attr(755,root,root) %{_libdir}/libsvn_ra_*.so*
%attr(755,root,root) %{_libdir}/libsvn_repos.so*
%{_mandir}/man1/*
%{_infodir}/svn*

%files devel
%defattr(644,root,root,755)
%{_includedir}/%{name}
%attr(755,root,root) %{_libdir}/libsvn_[cdsw]*.so
%attr(755,root,root) %{_libdir}/libsvn_ra.so
%attr(755,root,root) %{_libdir}/lib*.la

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files -n apache-mod_dav_svn
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/httpd/httpd.conf/*_mod_dav_svn.conf
%attr(755,root,root) %{_libexecdir}/*.so
