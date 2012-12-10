Name:           i2c-tools
Version:        3.1.0
Release:        1
Summary:        Heterogeneous set of I2C tools for Linux
Group:          System/Kernel and hardware
License:        GPL
URL:            http://www.lm-sensors.org/wiki/I2CTools
Source0:        http://dl.lm-sensors.org/i2c-tools/releases/i2c-tools-%{version}.tar.bz2
Conflicts:      lm_sensors < 3.0.0
Requires:       udev

%description
This package contains a heterogeneous set of I2C tools for Linux: a bus
probing tool, a chip dumper, register-level access helpers, EEPROM
decoding scripts, and more.

%package eepromer
Summary:        Programs for reading/writing i2c/smbus eeproms
Group:          System/Kernel and hardware
Requires:       %{name} = %{version}-%{release}

%description eepromer
Programs for reading/writing i2c/smbus eeproms. Notice that writing the
eeproms in your system is very dangerous and is likely to render your system
unusable. Do not install, let alone use this, unless you really, _really_ know
what you are doing.

%package -n python-smbus
Summary:	Python module for SMBus access via I2C
Group:		System/Kernel and hardware
BuildRequires:	python
BuildRequires:	python-setuptools
Requires:	python

%description -n python-smbus
This Python module allows SMBus access through the I2C /dev interface
on Linux hosts. The host kernel must have I2C support, I2C device
interface support, and a bus adapter driver.

%prep
%setup -q

%build
%{make} CFLAGS="%{optflags}"

pushd eepromer
%{make} CFLAGS="%{optflags} -I../include"
popd

pushd py-smbus
CFLAGS="%{optflags} -I../include" python setup.py build
popd

%install
%{__rm} -rf %{buildroot}
%{makeinstall}
%{__cp} -a eepromer/eeprog eepromer/eeprom eepromer/eepromer %{buildroot}%{_sbindir}

pushd py-smbus
python setup.py install --root=%{buildroot} --compile --optimize=2
popd

%{__rm} -r %{buildroot}%{_includedir}/linux

%files
%defattr(0644,root,root,0755)
%doc CHANGES COPYING README
%attr(660,root,root) %dev(c,89,0) /lib/udev/devices/i2c-0
%attr(660,root,root) %dev(c,89,0) /lib/udev/devices/i2c-1
%attr(660,root,root) %dev(c,89,0) /lib/udev/devices/i2c-2
%attr(660,root,root) %dev(c,89,0) /lib/udev/devices/i2c-3
#%attr(0755,root,root) %{_bindir}/*
#%attr(0755,root,root) %{_sbindir}/*
%exclude %{_sbindir}/eeprog
%exclude %{_sbindir}/eeprom
%exclude %{_sbindir}/eepromer
%attr(0755,root,root) %{_bindir}/ddcmon
%attr(0755,root,root) %{_bindir}/decode-dimms
%attr(0755,root,root) %{_bindir}/decode-edid
%attr(0755,root,root) %{_bindir}/decode-vaio
%attr(0755,root,root) %{_sbindir}/i2cdetect
%attr(0755,root,root) %{_sbindir}/i2cdump
%attr(0755,root,root) %{_sbindir}/i2cget
%attr(0755,root,root) %{_sbindir}/i2cset
%attr(0755,root,root) %{_sbindir}/i2c-stub-from-dump
%{_mandir}/man8/i2cdetect.8*
%{_mandir}/man8/i2cdump.8*
%{_mandir}/man8/i2cget.8*
%{_mandir}/man8/i2cset.8*
%{_mandir}/man8/i2c-stub-from-dump.8*

%files eepromer
%defattr(0644,root,root,0755)
%doc eepromer/README eepromer/README.eeprom eepromer/README.eepromer eepromer/README.eeprog
%attr(0755,root,root) %{_sbindir}/eeprog
%attr(0755,root,root) %{_sbindir}/eeprom
%attr(0755,root,root) %{_sbindir}/eepromer

%files -n python-smbus
%defattr(0644,root,root,0755)
%doc py-smbus/README
%{py_platsitedir}/smbus*


%changelog
* Fri Apr 20 2012 Alexander Khrukin <akhrukin@mandriva.org> 3.1.0-1
+ Revision: 792461
- version update 3.1.0

* Wed Mar 16 2011 Stéphane Téletchéa <steletch@mandriva.org> 3.0.3-1
+ Revision: 645236
- update to new version 3.0.3

* Tue Nov 02 2010 Jani Välimaa <wally@mandriva.org> 3.0.2-3mdv2011.0
+ Revision: 592187
- rebuild for python 2.7

* Fri Sep 11 2009 Thierry Vignaud <tv@mandriva.org> 3.0.2-2mdv2010.1
+ Revision: 437911
- rebuild

* Wed Feb 18 2009 Jérôme Soyer <saispo@mandriva.org> 3.0.2-1mdv2009.1
+ Revision: 342304
- New upstream release

* Fri Jan 02 2009 Funda Wang <fwang@mandriva.org> 3.0.1-6mdv2009.1
+ Revision: 323371
- rebuild

* Thu Nov 20 2008 Adam Williamson <awilliamson@mandriva.org> 3.0.1-5mdv2009.1
+ Revision: 305334
- fix the CFLAGS for the pysmbus build to include -I../include (right fix)
- drop pysmbus_include.patch (completely the wrong 'fix')

* Sun Nov 09 2008 Adam Williamson <awilliamson@mandriva.org> 3.0.1-4mdv2009.1
+ Revision: 301638
- requires python
- move kernel-headers BR into the python-smbus section for clarity
- python buildrequires
- add pysmbus_include.patch: add a necessary include for py-smbus to build
- build and package python-smbus too

* Fri Aug 29 2008 Olivier Blin <blino@mandriva.org> 3.0.1-3mdv2009.0
+ Revision: 277375
- install udev helpers in /lib/udev (this is the default on x86_64 too now, as per upstream)

* Thu Aug 07 2008 Thierry Vignaud <tv@mandriva.org> 3.0.1-2mdv2009.0
+ Revision: 267108
- rebuild early 2009.0 package (before pixel changes)

* Sun Apr 20 2008 David Walluck <walluck@mandriva.org> 3.0.1-1mdv2009.0
+ Revision: 195989
- fix file list
- 3.0.1

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Dec 11 2007 David Walluck <walluck@mandriva.org> 3.0.0-1mdv2008.1
+ Revision: 117438
- import i2c-tools

