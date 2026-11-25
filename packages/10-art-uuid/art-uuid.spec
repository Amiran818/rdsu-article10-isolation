Name: art-uuid
Version: 1.0
Release: alt1

Summary: Generate and inspect UUIDs
License: MIT
Group: System/Base

Source: %name-%version.tar

BuildRequires: autoconf-archive
BuildRequires: libuuid-devel

%description
Generates random or time-based UUIDs and shows the version of a given
UUID using libuuid; built with Autoconf and Automake. Training package
for the build isolation experiment.

%prep
%setup

%build
%autoreconf
%configure
%make_build

%check
%make_build check

%install
%makeinstall_std

%files
%_bindir/art-uuid

%changelog
* Wed Nov 25 2026 Amir Dzhakishev <dzhakishev@altlinux.org> 1.0-alt1
- Initial build.
