%define svnver 1671
%define realver 0.2.4
%define orgname mt-daapd

Summary: A multi-threaded implementation of Apple's DAAP server
Name: firefly-media-server
Version: %realver
Release: %mkrel 1.r%svnver.1
License: GPL
Group: System/Servers
URL: http://www.mt-daapd.org
Source0: http://download.sourceforge.net/sourceforge/mt-daapd/%{orgname}-svn-%{svnver}.tar.gz
Source1: %{orgname}-init.d
Source2: %{orgname}-logrotate.d
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: libid3tag-devel, ffmpeg-devel
BuildRequires: sqlite-devel, sqlite3-devel, gdbm-devel
BuildRequires: libogg-devel, libflac-devel
BuildRequires: avahi-client-devel, avahi-core-devel, avahi-common-devel
Provides: mt-daapd

%description
A multi-threaded implementation of Apple's DAAP server, mt-daapd
allows a Linux machine to advertise MP3 files to to used by
Windows or Mac iTunes clients.  This version uses Apple's ASPL Rendezvous
daemon.

%package devel
Summary: Development libraries for mt-daapd
Group: Development/Libraries

%description devel
Development libraries for mt-daapd.

%prep
%setup -q -n %{orgname}-svn-%{svnver}

%build
#export CPPFLAGS=-DPIDFILE=\'\"/var/run/mt-daapd/mt-daapd.pid\"\'
%configure \
	--enable-oggvorbis \
	--enable-flac \
	--enable-avahi \
	--enable-upnp \
	--enable-sqlite \
	--enable-sqlite3 \
	--enable-gdbm
%make

%install
rm -rf %{buildroot}
%makeinstall

%{__install} -d %{buildroot}/%{_sysconfdir}
%{__install} -m 644 contrib/mt-daapd.conf %{buildroot}/%{_sysconfdir}/%{orgname}.conf
#%{__install} -m 644 contrib/mt-daapd.playlist %{buildroot}/%{_sysconfdir}/%{name}.playlist

%{__install} -d %{buildroot}/%{_sysconfdir}/rc.d/init.d
%{__install} -m 755 %{SOURCE1} %{buildroot}/%{_sysconfdir}/rc.d/init.d/%{orgname}

%{__install} -d %{buildroot}/%{_sysconfdir}/logrotate.d
%{__install} -m 644 %{SOURCE2} %{buildroot}/%{_sysconfdir}/logrotate.d/%{orgname}

%{__strip} %{buildroot}/%{_sbindir}/%{orgname}
%{__strip} %{buildroot}/%{_bindir}/wavstreamer
%{__strip} %{buildroot}/%{_libdir}/%{orgname}/plugins/*.so

%{__install} -d %{buildroot}/%{_var}/log/%{orgname}
%{__install} -d %{buildroot}/%{_var}/run/%{orgname}
%{__install} -d %{buildroot}/%{_var}/cache/%{orgname}

%pre
%_pre_useradd %{orgname} %{_var}/cache/%{orgname} /sbin/nologin

%post
%_post_service %{orgname}

%preun
%_preun_service %{orgname}

%postun
%_postun_userdel %{orgname}
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/mt-daapd ]; then
        %{_initrddir}/%{orgname} restart 1>&2
    fi
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%doc AUTHORS ChangeLog COPYING CREDITS INSTALL NEWS README TODO
%config %{_sysconfdir}/rc.d/init.d/%{orgname}
%config(noreplace) %{_sysconfdir}/%{orgname}.conf
#%config(noreplace) %{_sysconfdir}/%{name}.playlist
%config(noreplace) %{_sysconfdir}/logrotate.d/%{orgname}
%{_bindir}/*
%{_sbindir}/%{orgname}
%{_datadir}/%{orgname}/admin-root
%{_libdir}/%{orgname}/plugins/*.so
%attr(-, %{orgname}, %{orgname}) %dir %{_var}/cache/%{orgname}
%attr(-, %{orgname}, %{orgname}) %dir %{_var}/log/%{orgname}
%attr(-, %{orgname}, %{orgname}) %dir %{_var}/run/%{orgname}

%files devel
%{_libdir}/%{orgname}/plugins/*.a
%{_libdir}/%{orgname}/plugins/*.la
