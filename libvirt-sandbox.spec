# -*- rpm-spec -*-

%define with_tcg 1
%define with_kvm 1

# RHEL does not provide the 9p.ko kernel module
# nor the virtio-9p KVM backend driver.
%if 0%{?rhel}
%define with_tcg 0
%define with_kvm 0
%endif

%define libvirt_version 1.0.2


Name: libvirt-sandbox
Version: 0.5.0
Release: 5%{?dist}%{?extra_release}
Summary: libvirt application sandbox framework
Group: Development/Tools
License: LGPLv2+
URL: http://libvirt.org/
Source0: ftp://libvirt.org/libvirt/sandbox/%{name}-%{version}.tar.gz
Patch1: 0001-Fix-path-to-systemd-binary.patch
Patch2: 0002-Update-man-page-about-virt-sandbox-service.patch
Patch3: 0003-Fix-delete-of-running-container.patch
Patch4: 0004-Fix-upgrade-command-wrt-to-generic-containers.patch
Patch5: 0005-Fix-logrotate-script-to-use-virsh-list.patch
Patch6: 0006-Check-return-value-from-mkdir-in-libvirt-sandbox-ini.patch
Patch7: 0007-Remove-unused-int-fd-variable.patch
Patch8: 0008-Fix-crash-if-mount-option-is-not-fully-specified.patch
Patch9: 0009-Add-pod-docs-for-ram-filesystem-mount-syntax.patch
Patch10: 0010-Avoid-close-of-un-opened-file-descriptor.patch
Patch11: 0011-Fix-leak-of-file-handle-in-libvirt-sandbox-init-comm.patch
Patch12: 0012-Fix-leak-of-file-handle-in-libvirt-sandbox-init-qemu.patch
Patch13: 0013-Remove-bogus-check-for-NULL-in-cleanup-path.patch
Patch14: 0014-Fix-broken-default-case-in-switch-statement.patch
Patch15: 0015-Stop-using-broken-shutil.copytree-method.patch
Patch16: 0016-Avoid-crash-when-gateway-is-missing.patch
Patch17: 0017-Fix-symlink-path-in-multi-user.target.wants.patch
Patch18: 0018-Add-p-PATH-arg-to-virt-sandbox-service-clone-delete-.patch
Patch19: 0019-Only-allow-lxc-URI-usage-with-virt-sandbox-service.patch
Patch20: 0020-Rollback-state-if-cloning-container-fails-part-way.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libvirt-gobject-devel >= 0.1.7
BuildRequires: gobject-introspection-devel
BuildRequires: glibc-static
BuildRequires: /usr/bin/pod2man
BuildRequires: intltool
BuildRequires: glib2-devel >= 2.32.0
Requires: rpm-python
# For virsh lxc-enter-namespace command
Requires: libvirt-client >= %{libvirt_version}
Requires: systemd >= 198
Requires: pygobject3-base
Requires: libselinux-python
Requires: %{name}-libs = %{version}-%{release}

%package libs
Group: Development/Libraries
Summary: libvirt application sandbox framework libraries
# So we get the full libvirtd daemon, not just client libs
%ifarch %{ix86} x86_64
%if %{with_kvm}
Requires: libvirt-daemon-kvm >= %{libvirt_version}
%endif
%endif
%if %{with_tcg}
Requires: libvirt-daemon-qemu >= %{libvirt_version}
%endif
Requires: libvirt-daemon-lxc >= %{libvirt_version}

%package devel
Group: Development/Libraries
Summary: libvirt application sandbox framework development files
Requires: %{name}-libs = %{version}-%{release}

%description
This package provides a command for running applications within
a sandbox using libvirt.

%description libs
This package provides a framework for building application sandboxes
using libvirt.

%description devel
This package provides development header files and libraries for
the libvirt sandbox

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1

%build

%configure --enable-introspection
%__make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
chmod a-x examples/*.py examples/*.pl examples/*.js
%__make install  DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/libvirt-sandbox-1.0.a
rm -f $RPM_BUILD_ROOT%{_libdir}/libvirt-sandbox-1.0.la

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_datadir}/bash-completion/completions/virt-sandbox-service
%config(noreplace) %{_sysconfdir}/cron.daily/virt-sandbox-service.logrotate
%dir %{_sysconfdir}/libvirt-sandbox/services
%{_bindir}/virt-sandbox
%{_bindir}/virt-sandbox-service
%{_libexecdir}/virt-sandbox-service-util
%{_mandir}/man1/virt-sandbox.1*
%{_mandir}/man1/virt-sandbox-service.1*
%{_mandir}/man1/virt-sandbox-service-*.1*

%files libs -f %{name}.lang
%defattr(-,root,root,-)
%doc README COPYING AUTHORS ChangeLog NEWS
%dir %{_sysconfdir}/libvirt-sandbox
%dir %{_sysconfdir}/libvirt-sandbox/scratch
%config %{_sysconfdir}/libvirt-sandbox/scratch/README
%{_libexecdir}/libvirt-sandbox-init-common
%{_libexecdir}/libvirt-sandbox-init-lxc
%{_libexecdir}/libvirt-sandbox-init-qemu
%{_libdir}/libvirt-sandbox-1.0.so.*
%{_libdir}/girepository-1.0/LibvirtSandbox-1.0.typelib

%files devel
%defattr(-,root,root,-)
%doc examples/virt-sandbox.pl
%doc examples/virt-sandbox.py
%doc examples/virt-sandbox.js
%doc examples/virt-sandbox-mkinitrd.py
%{_libdir}/libvirt-sandbox-1.0.so
%{_libdir}/pkgconfig/libvirt-sandbox-1.0.pc
%dir %{_includedir}/libvirt-sandbox-1.0
%dir %{_includedir}/libvirt-sandbox-1.0/libvirt-sandbox
%{_includedir}/libvirt-sandbox-1.0/libvirt-sandbox/libvirt-sandbox.h
%{_includedir}/libvirt-sandbox-1.0/libvirt-sandbox/libvirt-sandbox-*.h
%{_datadir}/gir-1.0/LibvirtSandbox-1.0.gir
%{_datadir}/gtk-doc/html/Libvirt-sandbox

%changelog
* Thu Oct  3 2013 Daniel P. Berrange <berrange@redhat.com> - 0.5.0-5
- Add fully versioned dep between libvirt-sandbox & libvirt-sandbox-libs

* Wed Oct  2 2013 Daniel P. Berrange <berrange@redhat.com> - 0.5.0-4
- Rollback state if cloning fails (rhbz #966854)
- Only allow lxc:/// URI (rhbz #967772)
- Support -p arg with clone/delet commands (rhbz #970952)
- Fix symlink in multi-user.target.wants (rhbz #973974)
- Avoid crash when gateway is missing (rhbz #993557)
- Fix copying of trees with non-regular file (rhbz #1003720)

* Mon Aug 19 2013 Daniel P. Berrange <berrange@redhat.com> - 0.5.0-3
- Fix misc coverity flaws (rhbz #922639)
- Fix logrotate script (rhbz #994311)
- Fix upgrade command wrt generic containers (rhbz #994371)

* Tue Aug 13 2013 Daniel P. Berrange <berrange@redhat.com> - 0.5.0-2
- Fix systemd init path (rhbz #990347)
- Fix command list in man page (rhbz #996617)
- Fix delete of running container (rhbz #994495)

* Thu Aug  1 2013 Daniel P. Berrange <berrange@redhat.com> - 0.5.0-1
- Update to 0.5.0 release

* Tue Jul  9 2013 Daniel P. Berrange <berrange@redhat.com> - 0.2.1-1
- Update to 0.2.1 release

* Tue May  7 2013 Daniel P. Berrange <berrange@redhat.com> - 0.2.0-1
- Update to 0.2.0 release

* Tue Mar  5 2013 Daniel P. Berrange <berrange@redhat.com> - 0.1.2-1
- Update to 0.1.2 release

* Fri Feb 22 2013 Daniel P. Berrange <berrange@redhat.com> - 0.1.1-4
- Add dep on pod2man

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 17 2013 Daniel P. Berrange <berrange@redhat.com> - 0.1.1-2
- Conditionalize dep on libvirt-daemon-qemu

* Mon Dec 10 2012 Daniel P. Berrange <berrange@redhat.com> - 0.1.1-1
- Update to 0.1.1 release

* Mon Aug 13 2012 Daniel P. Berrange <berrange@redhat.com> - 0.1.0-1
- Update to 0.1.0 release

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Apr 27 2012 Daniel P. Berrange <berrange@redhat.com> - 0.0.3-2
- Rebuild for libvirt-gobject update

* Fri Apr 13 2012 Daniel P. Berrange <berrange@redhat.com> - 0.0.3-1
- Update to 0.0.3 release

* Thu Jan 12 2012 Daniel P. Berrange <berrange@redhat.com> - 0.0.2-1
- Update to 0.0.2 release

* Wed Jan 11 2012 Daniel P. Berrange <berrange@redhat.com> - 0.0.1-1
- Initial package

