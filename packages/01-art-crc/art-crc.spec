Name: art-crc
Version: 1.0
Release: alt1

Summary: CRC-32 and Adler-32 checksums of files
License: MIT
Group: File tools

Source: %name-%version.tar

BuildRequires: zlib-devel
BuildRequires: help2man

%description
Small utility that prints CRC-32 and Adler-32 checksums of files
using zlib. Training package for the build isolation experiment.

%prep
%setup

%build
%make_build CFLAGS="%optflags"

%check
make check

%install
%makeinstall_std PREFIX=%_prefix

%files
%_bindir/art-crc
%_man1dir/art-crc.1*

%changelog
* Wed Nov 25 2026 Amir Dzhakishev <dzhakishev@altlinux.org> 1.0-alt1
- Initial build.
