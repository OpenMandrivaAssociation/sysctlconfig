%define	name	sysctlconfig
%define	version	0.15
%define	release	%mkrel 9

Summary:	A configuration tool for operating system tunable parameters
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
URL:		http://www.redhat.de/
Source0:	%{name}-%{version}.tar.bz2
Source1:	sysctlconfig-gtk.png.bz2
Patch0:		sysctlconfig-0.15-gcc34.diff
ExcludeArch:	ia64
BuildRequires:	desktop-file-utils recode
BuildRequires:	gtk+-devel
BuildRequires:	gtk+
BuildRequires:	libxml-devel
BuildRequires:	chrpath
Requires:	procps
Requires:	usermode
BuildRoot:	%{_tmppath}/%{name}-buildroot

%description
sysctl-config is a tool for configuring operating system tunable
parameters. It eases modifying /etc/sysctl.conf.

%prep

%setup -q 
%patch0 -p0

%build

%configure2_5x

%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall

%find_lang %{name}

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_iconsdir}
install -d %{buildroot}%{_sysconfdir}/security/console.apps
install -d %{buildroot}%{_sysconfdir}/X11/applnk/System
install -d %{buildroot}%{_sysconfdir}/pam.d
install -d %{buildroot}%{_libdir}/menu

mv %{buildroot}%{_bindir}/sysctlconfig-gtk %{buildroot}%{_sbindir}/sysctlconfig-gtk

bzcat %{SOURCE1} > %{buildroot}%{_iconsdir}/sysctlconfig-gtk.png
rm -f %{buildroot}%{_iconsdir}/*.xpm

cat > %{buildroot}/%{_sysconfdir}/pam.d/sysctlconfig-gtk <<EOF
#%PAM-1.0
auth       sufficient   pam_rootok.so
auth       include      system-auth
session    optional     pam_xauth.so
account    required     pam_permit.so
EOF

cat > %{buildroot}/%{_sysconfdir}/security/console.apps/sysctlconfig-gtk <<EOF
USER=root
FALLBACK=true
PROGRAM=%{_sbindir}/sysctlconfig-gtk
SESSION=true
EOF
ln -s %{_bindir}/consolehelper %{buildroot}%{_bindir}/sysctlconfig-gtk


mkdir -p %{buildroot}%{_datadir}/applications 
mv %{buildroot}%{_sysconfdir}/X11/applnk/System/%{name}.desktop %{buildroot}%{_datadir}/applications/

recode ISO-8859-15..UTF-8 %{buildroot}%{_datadir}/applications/%{name}.desktop
perl -pi -e 's,%{name}-gtk.xpm,%{name}-gtk,g' %{buildroot}%{_datadir}/applications/*

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --remove-key="Name" \
  --add-category="System" \
  --add-category="Settings" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

# nuke rpath
chrpath -d %{buildroot}%{_sbindir}/*

%if %mdkversion < 200900
%post
%{update_menus}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-, root,root)
%doc AUTHORS ChangeLog INSTALL README TODO
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/pam.d/sysctlconfig-gtk
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/security/console.apps/sysctlconfig-gtk
#%config(noreplace) %{_sysconfdir}/X11/applnk/System/sysctlconfig.desktop
%{_sbindir}/sysctlconfig-gtk
%{_bindir}/sysctlconfig-gtk
%{_iconsdir}/*.png
%{_datadir}/sysctlconfig/*
%{_datadir}/applications/*.desktop

