%define major 0
%define libname %mklibname i2c %{major}
%define devname %mklibname -d i2c
%define staticname %mklibname -d -s i2c
%define _disable_ld_no_undefined 1

Summary:	Heterogeneous set of I2C tools for Linux
Name:		i2c-tools
Version:	4.2
Release:	1
Group:		System/Kernel and hardware
License:	GPL
URL:		http://www.lm-sensors.org/wiki/I2CTools
Source0:	https://mirrors.edge.kernel.org/pub/software/utils/i2c-tools/i2c-tools-%{version}.tar.xz
BuildRequires:	pkgconfig(python)
Conflicts:	lm_sensors < 3.0.0
Requires:	udev

%description
This package contains a heterogeneous set of I2C tools for Linux: a bus
probing tool, a chip dumper, register-level access helpers, EEPROM
decoding scripts, and more.

%package -n %{libname}
Summary:	Library for working with I2C bus devices
Group:		System/Libraries

%description -n %{libname}
Library for working with I2C bus devices

%package -n %{devname}
Summary:	Development files for the I2C library
Group:		System/Kernel and hardware
Requires:	%{libname} = %{EVRD}

%description -n %{devname}
Development files for the I2C library

%package -n %{staticname}
Summary:	Static library files for the I2C library
Group:		System/Kernel and hardware
Requires:	%{devname} = %{EVRD}

%description -n %{staticname}
Static library files for the I2C library

%package eepromer
Summary:	Programs for reading/writing i2c/smbus eeproms
Group:		System/Kernel and hardware
Requires:	%{name} = %{version}-%{release}

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
%autosetup -p1

%build
%set_build_flags

%make_build PREFIX=%{_prefix} EXTRA=eeprog libdir=%{_libdir} CC=%{__cc}

cd eepromer
%make_build PREFIX=%{_prefix} libdir=%{_libdir} CFLAGS="%{optflags} -I../include" CC=%{__cc}
cd ..

cd py-smbus
CFLAGS="%{optflags} -I../include" python setup.py build
cd ..

%install
%make_install PREFIX=%{_prefix} libdir=%{_libdir} EXTRA=eeprog
cp -a eeprog/eeprog eepromer/eeprom eepromer/eepromer %{buildroot}%{_sbindir}

cd py-smbus
python setup.py install --root=%{buildroot} --compile --optimize=2
cd ..

%files
%defattr(0644,root,root,0755)
%doc CHANGES COPYING README
%attr(660,root,root) %dev(c,89,0) /lib/udev/devices/i2c-0
%attr(660,root,root) %dev(c,89,0) /lib/udev/devices/i2c-1
%attr(660,root,root) %dev(c,89,0) /lib/udev/devices/i2c-2
%attr(660,root,root) %dev(c,89,0) /lib/udev/devices/i2c-3
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
%attr(0755,root,root) %{_sbindir}/i2ctransfer
%attr(0755,root,root) %{_sbindir}/i2c-stub-from-dump
%{_mandir}/man1/decode-dimms.1.*
%{_mandir}/man1/decode-vaio.1.*
%{_mandir}/man3/libi2c.3.*
%{_mandir}/man8/i2cdetect.8*
%{_mandir}/man8/i2cdump.8*
%{_mandir}/man8/i2cget.8*
%{_mandir}/man8/i2cset.8*
%{_mandir}/man8/i2ctransfer.8*
%{_mandir}/man8/i2c-stub-from-dump.8*

%files eepromer
%defattr(0644,root,root,0755)
%doc eepromer/README eepromer/README.eeprom eepromer/README.eepromer
%attr(0755,root,root) %{_sbindir}/eeprog
%attr(0755,root,root) %{_sbindir}/eeprom
%attr(0755,root,root) %{_sbindir}/eepromer
%{_mandir}/man8/eeprog.8*

%files -n python-smbus
%defattr(0644,root,root,0755)
%doc py-smbus/README
%{py_platsitedir}/smbus*

%files -n %{libname}
%{_libdir}/libi2c.so.%{major}*

%files -n %{devname}
%{_includedir}/i2c
%{_libdir}/*.so

%files -n %{staticname}
%{_libdir}/*.a
