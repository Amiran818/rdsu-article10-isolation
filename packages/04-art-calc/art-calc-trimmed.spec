Name: art-calc
Version: 1.0
Release: alt1

Summary: Integer expression calculator
License: MIT
Group: Sciences/Mathematics

Source: %name-%version.tar

BuildRequires: txt2man

%description
Integer expression calculator built from a flex scanner and
a bison grammar. Training package for the build isolation experiment.

%prep
%setup

%build
%make_build CFLAGS="%optflags"

%check
make check

%install
%makeinstall_std PREFIX=%_prefix

%files
%_bindir/art-calc
%_man1dir/art-calc.1*

%changelog
* Wed Nov 25 2026 Amir Dzhakishev <dzhakishev@altlinux.org> 1.0-alt1
- Initial build.
