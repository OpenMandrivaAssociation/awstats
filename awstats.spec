Name:		awstats
Version:	6.95
Release:	%mkrel 4
Summary:	Advanced Web Statistics
License:	GPLv2
Group:		Networking/WWW
URL:		http://awstats.sourceforge.net
Source0:	http://prdownloads.sourceforge.net/awstats/%{name}-%{version}.tar.gz
Patch0:		awstats-6.9-better-configuration.patch
Requires:	webserver
%if %mdkversion < 201010
Requires(post):   rpm-helper
Requires(postun):   rpm-helper
%endif
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
Advanced Web Statistics is a powerful and featureful tool that generates
advanced web server graphic statistics. This server log analyzer works
from command line or as a CGI and shows you all information your log contains,
in graphical web pages. It can analyze a lot of web/wap/proxy servers like
Apache, IIS, Weblogic, Webstar, Squid, ... but also mail or ftp servers.

This program can measure visits, unique vistors, authenticated users, pages,
domains/countries, OS busiest times, robot visits, type of files, search
engines/keywords used, visits duration, HTTP errors and more...
Statistics can be updated from a browser or your scheduler.
The program also supports virtual servers, plugins and a lot of features.

%prep
%setup -q
%patch0 -p 1 -b .defaultconf
# fix perms
find . -type f -exec chmod 644 {} \;
find . -name *.pl -exec chmod 755 {} \;
rm -f  wwwroot/cgi-bin/plugins/.#geoip_city_maxmind.pm.1.8

%build

%install
rm -rf %{buildroot}

# apache configuration
install -d -m 755 %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf <<EOF
# Awstats configuration

Alias /awstats %{_datadir}/%{name}/www
<Directory %{_datadir}/%{name}/www>
    Order allow,deny
    Allow from all

    Options ExecCGI
    AddHandler cgi-script .pl
    DirectoryIndex awstats.pl
</Directory>

SetEnv PERL5LIB %{_datadir}/%{name}/lib:%{_datadir}/%{name}/plugins
EOF

# cron task
install -d -m 755 %{buildroot}%{_sysconfdir}/cron.daily
cat > %{buildroot}%{_sysconfdir}/cron.daily/%{name} <<EOF
#!/bin/sh
%{_datadir}/%{name}/www/awstats.pl -config=awstats.conf -update > /dev/null
EOF
chmod 755 %{buildroot}%{_sysconfdir}/cron.daily/%{name}

install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}
install -m 644 wwwroot/cgi-bin/awstats.model.conf %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf


install -d -m 755 %{buildroot}%{_datadir}/%{name}
install -d -m 755 %{buildroot}%{_datadir}/%{name}/www
install -m 755 wwwroot/cgi-bin/awstats.pl %{buildroot}%{_datadir}/%{name}/www
cp -r wwwroot/icon %{buildroot}%{_datadir}/%{name}/www
cp -r wwwroot/css %{buildroot}%{_datadir}/%{name}/www
cp -r wwwroot/js %{buildroot}%{_datadir}/%{name}/www

cp -r tools %{buildroot}%{_datadir}/%{name}
cp -r wwwroot/cgi-bin/lang %{buildroot}%{_datadir}/%{name}
cp -r wwwroot/cgi-bin/lib %{buildroot}%{_datadir}/%{name}
cp -r wwwroot/cgi-bin/plugins %{buildroot}%{_datadir}/%{name}

install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}

%clean
rm -rf %{buildroot}

%post
if [ $1 -eq 1 ]; then
	perl -pi -e 's/SiteDomain=""/SiteDomain="'`hostname`'"/' %{_sysconfdir}/%{name}/%{name}.conf
fi
%if %mdkversion < 201000
%_post_webapp
%endif

%postun
%if %mdkversion < 201000
%_postun_webapp
%endif

%files
%defattr(-,root,root)
%doc README.TXT docs/*
%config(noreplace) %{_webappconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/cron.daily/%{name}
%{_datadir}/%{name}
%{_localstatedir}/lib/%{name}
