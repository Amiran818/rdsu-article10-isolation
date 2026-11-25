Name: art-tui
Version: 1.0
Release: alt1

Summary: Draw a framed message in the terminal
License: MIT
Group: Terminals

Source: %name-%version.tar

BuildRequires: libncursesw-devel
BuildRequires: scdoc

%description
Tiny ncursesw program that draws a frame with a centered message.
Training package for the build isolation experiment.

%prep
%setup

%build
%make_build CFLAGS="%optflags"

%check
make check

%install
%makeinstall_std PREFIX=%_prefix

%files
%_bindir/art-tui
%_man1dir/art-tui.1*

%changelog
* Wed Nov 25 2026 Amir Dzhakishev <dzhakishev@altlinux.org> 1.0-alt1
- Initial build.
