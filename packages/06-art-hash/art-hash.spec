Name: art-hash
Version: 1.0
Release: alt1

Summary: SHA-256 and SHA-512 digests of files
License: MIT
Group: File tools

Source: %name-%version.tar

BuildRequires: libssl-devel
BuildRequires: discount

%description
Prints SHA-256 or SHA-512 digests of files using OpenSSL, with
messages translated through gettext. Training package for the build
isolation experiment.

%prep
%setup

%build
%make_build CFLAGS="%optflags" LOCALEDIR=%_datadir/locale

%check
make check

%install
%makeinstall_std PREFIX=%_prefix LOCALEDIR=%_datadir/locale
%find_lang %name

%files -f %name.lang
%_bindir/art-hash
%_datadir/doc/art-hash/README.html

%changelog
* Wed Nov 25 2026 Amir Dzhakishev <dzhakishev@altlinux.org> 1.0-alt1
- Initial build.
