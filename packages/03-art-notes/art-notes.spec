Name: art-notes
Version: 1.0
Release: alt1

Summary: Keep short notes in an SQLite database
License: MIT
Group: Databases

Source: %name-%version.tar

BuildRequires: libsqlite3-devel
BuildRequires: libreadline-devel

%description
Command line notebook storing notes in an SQLite database, with
an interactive readline mode. Training package for the build
isolation experiment.

%prep
%setup

%build
%make_build CFLAGS="%optflags"

%check
make check

%install
%makeinstall_std PREFIX=%_prefix

%files
%_bindir/art-notes

%changelog
* Wed Nov 25 2026 Amir Dzhakishev <dzhakishev@altlinux.org> 1.0-alt1
- Initial build.
