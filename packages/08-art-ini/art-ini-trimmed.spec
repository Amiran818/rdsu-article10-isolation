Name: art-ini
Version: 1.0
Release: alt1

Summary: Read values from INI files
License: MIT
Group: Text tools

Source: %name-%version.tar

BuildRequires: meson
BuildRequires: ninja-build

%description
Reads values from INI-style key files using GLib GKeyFile; built
with Meson and Ninja. Training package for the build isolation
experiment.

%prep
%setup

%build
%meson
%meson_build

%check
%meson_test

%install
%meson_install

%files
%_bindir/art-ini

%changelog
* Wed Nov 25 2026 Amir Dzhakishev <dzhakishev@altlinux.org> 1.0-alt1
- Initial build.
