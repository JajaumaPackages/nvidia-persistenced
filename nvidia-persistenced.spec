Name:           nvidia-persistenced
Version:        367.57
Release:        1%{?dist}
Summary:        NVIDIA GPU persistence daemon

License:        GPLv2
URL:            http://docs.nvidia.com/deploy/driver-persistence/index.html
Source0:        ftp://download.nvidia.com/XFree86/nvidia-persistenced/nvidia-persistenced-%{version}.tar.bz2
Source1:        %{name}.service
Source2:        %{name}.conf

BuildRequires:  m4
BuildRequires:  systemd

Requires:           nvidia-driver-cfg%{?_isa}
Requires(pre):      shadow-utils
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd


%description
The %{name} utility is used to enable persistent software state in the NVIDIA
driver. When persistence mode is enabled, the daemon prevents the driver from
releasing device state when the device is not in use. This can improve the
startup time of new clients in this scenario.


%prep
%setup -q


%build
export CFLAGS="%{optflags}"
make %{?_smp_mflags} NV_VERBOSE=1 STRIP_CMD="/bin/true"


%install
rm -rf %{buildroot}
%make_install INSTALL="install -p" PREFIX=%{_prefix}

mv %{buildroot}%{_bindir} %{buildroot}%{_sbindir}

mkdir -p %{buildroot}%{_unitdir}/
install -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/

mkdir -p  %{buildroot}%{_tmpfilesdir}/
install -p -m 0644 %{SOURCE2} %{buildroot}%{_tmpfilesdir}/


%files
%doc COPYING README
%{_sbindir}/%{name}
%{_unitdir}/%{name}.service
%{_tmpfilesdir}/%{name}.conf
%{_mandir}/man1/%{name}.1.*


%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
    useradd -r -g %{name} -d /var/run/%{name} -s /sbin/nologin \
    -c "NVIDIA persistent software state" %{name}


%post
%systemd_post %{name}.service


%preun
%systemd_preun %{name}.service


%postun
%systemd_postun_with_restart %{name}.service


%changelog
* Thu Oct 20 2016 Jajauma's Packages <jajauma@yandex.ru> - 367.57-1
- Update to latest upstream version

* Sun Oct 02 2016 Jajauma's Packages <jajauma@yandex.ru> - 367.44-1
- Public release
