Name:           i2c-tools
Version:        3.0.1
Release:        %mkrel 3
Summary:        Heterogeneous set of I2C tools for Linux
Group:          System/Kernel and hardware
License:        GPL
URL:            http://www.lm-sensors.org/wiki/I2CTools
Source0:        http://dl.lm-sensors.org/i2c-tools/releases/i2c-tools-%{version}.tar.bz2
Source1:        http://dl.lm-sensors.org/i2c-tools/releases/i2c-tools-%{version}.tar.bz2.sig
Conflicts:      lm_sensors < 3.0.0
Requires:       udev
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

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

%prep
%setup -q 

%build
%{make} CFLAGS="%{optflags}"

cd eepromer
%{make} CFLAGS="%{optflags} -I../include"

%install
%{__rm} -rf %{buildroot}
%{makeinstall}
%{__cp} -a eepromer/eeprog eepromer/eeprom eepromer/eepromer %{buildroot}%{_sbindir}
%{__rm} -r %{buildroot}%{_includedir}/linux

%clean
%{__rm} -rf %{buildroot}

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

