%define major 0
%define libname %mklibname i2c %{major}
%define devname %mklibname -d i2c
%define staticname %mklibname -d -s i2c
%define _disable_ld_no_undefined 1

Summary:	Heterogeneous set of I2C tools for Linux
Name:		i2c-tools
Version:	4.3
Release:	1
Group:		System/Kernel and hardware
License:	GPL
URL:		http://www.lm-sensors.org/wiki/I2CTools
Source0:	https://mirrors.edge.kernel.org/pub/software/utils/i2c-tools/i2c-tools-%{version}.tar.xz
BuildRequires:	pkgconfig(python)
Conflicts:	lm_sensors < 3.0.0
Requires:	udev
Requires(post):	kmod
%rename i2c-tools-eepromer

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
Development files for the I2C library.

%package -n %{staticname}
Summary:	Static library files for the I2C library
Group:		System/Kernel and hardware
Requires:	%{devname} = %{EVRD}

%description -n %{staticname}
Static library files for the I2C library.

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

cd py-smbus
CFLAGS="%{optflags} -I../include" python setup.py build
cd ..

%install
%make_install PREFIX=%{_prefix} libdir=%{_libdir} EXTRA=eeprog

# for i2c-dev ondemand loading through kmod
mkdir -p %{buildroot}%{_modprobedir}
echo "alias char-major-89-* i2c-dev" > \
  %{buildroot}%{_modprobedir}/i2c-dev.conf
# for /dev/i2c-# creation (which are needed for kmod i2c-dev autoloading)
mkdir -p %{buildroot}%{_sysconfdir}/udev/makedev.d
for (( i = 0 ; i < 8 ; i++ )) do
  echo "i2c-$i" >> %{buildroot}%{_sysconfdir}/udev/makedev.d/99-i2c-dev.nodes
done

# auto-load i2c-dev after reboot
mkdir -p %{buildroot}%{_modulesloaddir}
echo 'i2c-dev' > %{buildroot}%{_modulesloaddir}/%{name}.conf

cd py-smbus
python setup.py install --root=%{buildroot} --compile --optimize=2
cd ..

%post
# load i2c-dev after the first install
if [ "$1" = 1 ] ; then
    /sbin/modprobe i2c-dev
fi
exit 0

%files
%doc CHANGES COPYING README
%config(noreplace) %{_modprobedir}/i2c-dev.conf
%config(noreplace) %{_sysconfdir}/udev/makedev.d/99-i2c-dev.nodes
%{_modulesloaddir}/%{name}.conf
%{_bindir}/ddcmon
%{_bindir}/decode-dimms
%{_bindir}/decode-edid
%{_bindir}/decode-vaio
%{_sbindir}/i2c*
%{_sbindir}/eeprog
%doc %{_mandir}/man1/decode-dimms.1.*
%doc %{_mandir}/man1/decode-vaio.1.*
%doc %{_mandir}/man3/libi2c.3.*
%doc %{_mandir}/man8/eeprog.8*
%doc %{_mandir}/man8/i2cdetect.8*
%doc %{_mandir}/man8/i2cdump.8*
%doc %{_mandir}/man8/i2cget.8*
%doc %{_mandir}/man8/i2cset.8*
%doc %{_mandir}/man8/i2ctransfer.8*
%doc %{_mandir}/man8/i2c-stub-from-dump.8*

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
