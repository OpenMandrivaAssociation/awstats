Name:		awstats
Version:	7.0
Release:	3
Summary:	Advanced Web Statistics
License:	GPLv2
Group:		Networking/WWW
URL:		http://awstats.sourceforge.net
Source0:	http://prdownloads.sourceforge.net/awstats/%{name}-%{version}.tar.gz
Patch0:		awstats-6.9-better-configuration.patch
Requires:	webserver
BuildArch:	noarch

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
# apache configuration
install -d -m 755 %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf <<EOF
# Awstats configuration

Alias /awstats %{_datadir}/%{name}/www
<Directory %{_datadir}/%{name}/www>
	Require all granted
    
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

%post
if [ $1 -eq 1 ]; then
	perl -pi -e 's/SiteDomain=""/SiteDomain="'`hostname`'"/' %{_sysconfdir}/%{name}/%{name}.conf
fi

%files
%doc README.TXT docs/*
%config(noreplace) %{_webappconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/cron.daily/%{name}
%{_datadir}/%{name}
%{_localstatedir}/lib/%{name}




%changelog
* Sun Feb 20 2011 dmorgan <dmorgan> 7.0-1.mga1
+ Revision: 54626
- Remove mdv macros
- Remove mdv macros
- imported package awstats


* Thu Dec 09 2010 Oden Eriksson <oeriksson@mandriva.com> 7.0-1mdv2011.0
+ Revision: 617791
- 7.0

* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 6.95-5mdv2011.0
+ Revision: 610013
- rebuild

* Mon Mar 01 2010 Guillaume Rousse <guillomovitch@mandriva.org> 6.95-4mdv2010.1
+ Revision: 513156
- fix install dependencies

* Thu Feb 04 2010 Guillaume Rousse <guillomovitch@mandriva.org> 6.95-3mdv2010.1
+ Revision: 500979
- rely on filetrigger for reloading apache configuration begining with 2010.1, rpm-helper macros otherwise

* Fri Dec 04 2009 Guillaume Rousse <guillomovitch@mandriva.org> 6.95-2mdv2010.1
+ Revision: 473508
- install all files under %%{_datadir}/name
- enforce new default access policy

* Wed Nov 11 2009 Frederik Himpe <fhimpe@mandriva.org> 6.95-1mdv2010.1
+ Revision: 464851
- update to new version 6.95

* Thu Sep 10 2009 Thierry Vignaud <tv@mandriva.org> 6.9-2mdv2010.0
+ Revision: 436734
- rebuild

* Mon Dec 29 2008 Frederik Himpe <fhimpe@mandriva.org> 6.9-1mdv2009.1
+ Revision: 321199
- Update to new version 6.9 (fixes XSS vulnerability CVE-2008-3714)
- Rediff configuration patch and fix a typo

* Sat Aug 16 2008 Guillaume Rousse <guillomovitch@mandriva.org> 6.8-1mdv2009.0
+ Revision: 272819
- new version

* Wed Jul 23 2008 Thierry Vignaud <tv@mandriva.org> 6.7-3mdv2009.0
+ Revision: 243097
- rebuild

  + Pixel <pixel@mandriva.com>
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

* Thu Dec 20 2007 Olivier Blin <oblin@mandriva.com> 6.7-1mdv2008.1
+ Revision: 135826
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sat Aug 18 2007 Guillaume Rousse <guillomovitch@mandriva.org> 6.7-1mdv2008.0
+ Revision: 65428
- drop eol fixing, now handled by spec-helper
- new version


* Wed Feb 14 2007 Guillaume Rousse <guillomovitch@mandriva.org> 6.6-1mdv2007.0
+ Revision: 120982
- ooops, forgotten new sources
- new version

* Mon Jan 08 2007 Oden Eriksson <oeriksson@mandriva.com> 6.5-10mdv2007.1
+ Revision: 106018
- make it backportable (dacapo)

* Sun Jan 07 2007 Oden Eriksson <oeriksson@mandriva.com> 6.5-9mdv2007.1
+ Revision: 105363
- make it backportable

* Sun Jan 07 2007 Oden Eriksson <oeriksson@mandriva.com> 6.5-8mdv2007.1
+ Revision: 105347
- Import awstats

* Tue Sep 05 2006 Oden Eriksson <oeriksson@mandrakesoft.com> 6.5-8mdv2007.0
- revert last change, the correct fix is needed for the 2006 package

* Tue Sep 05 2006 Oden Eriksson <oeriksson@mandrakesoft.com> 6.5-7mdv2007.0
- don't trash the pdf files (#22889)

* Tue Sep 05 2006 Guillaume Rousse <guillomovitch@mandriva.org> 6.5-6mdv2007.0
- make cron task as configuration (#15701)

* Thu Jul 27 2006 Guillaume Rousse <guillomovitch@mandriva.org> 6.5-5mdv2007.0
- fix cron task (fix #23657)

* Sat Jul 01 2006 Guillaume Rousse <guillomovitch@mandriva.org> 6.5-4mdv2007.0
- relax buildrequires versionning

* Tue Jun 27 2006 Guillaume Rousse <guillomovitch@mandriva.org> 6.5-3mdv2007.0
- new webapps macros
- fix doc (fix #22927)
- change access URL to /awstats, instead of /cgi-bin/awstats.pl
- update conf patch
- decompress patches

* Tue May 23 2006 Guillaume Rousse <guillomovitch@mandriva.org> 6.5-2mdk
- sanitize parameters (security fix from 6.6)
- backport compatible apache configuration file

* Wed Jan 11 2006 Guillaume Rousse <guillomovitch@mandriva.org> 6.5-1mdk
- new version
- %%mkrel

* Tue Jul 05 2005 Guillaume Rousse <guillomovitch@mandriva.org> 6.4-4mdk 
- better fix encoding
- use new apache rpm macros
- fix cron task perms

* Thu Jun 23 2005 Guillaume Rousse <guillomovitch@mandriva.org> 6.4-3mdk 
- new apache setup

* Sat Mar 19 2005 Guillaume Rousse <guillomovitch@mandrake.org> 6.4-2mdk 
- incluse missing web files (fix bug #14788)
- rediff configuration patch
- fix files encoding
- fix cron task shellbang

* Sun Mar 06 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 6.4-1mdk 
- Release 6.4 - SECURITY FIX - UPGRADE IS HIGHLY RECOMMANDED

* Fri Feb 18 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 6.3-2mdk
- spec file cleanups, remove the ADVX-build stuff

* Thu Jan 27 2005 Guillaume Rousse <guillomovitch@mandrake.org> 6.3-1mdk 
- new version (fix remote vulnerability)
- herein document whenever possible
- no more order for apache configuration
- reload apache instead of restart it
- don't tag executables in /etc as executables

* Tue Dec 21 2004 Erwan Velu <velu@seanodes.com> 6.2-1mdk 
- 6.2

* Wed Jul 14 2004 Guillaume Rousse <guillomovitch@mandrake.org> 6.1-1mdk 
- new version
- apache config file in /etc/httpd/webapps.d

* Sat Jul 03 2004 Guillaume Rousse <guillomovitch@mandrake.org> 6.0-3mdk 
- fix perms

* Sat Jul 03 2004 Guillaume Rousse <guillomovitch@mandrake.org> 6.0-2mdk 
- remove useless provide

* Thu Feb 26 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 6.0-1mdk
- Release 6.0
- Regenerate patch0
- Ensure cron file is executable

