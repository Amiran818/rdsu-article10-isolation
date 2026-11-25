Name: art-xq
Version: 1.0
Release: alt1

Summary: Evaluate XPath expressions over XML files
License: MIT
Group: Text tools

Source: %name-%version.tar

BuildRequires: xsltproc

%description
Command line XPath evaluator based on libxml2; its manual page is
generated from an XML description with xsltproc. Training package
for the build isolation experiment.

%prep
%setup

%build
%make_build CFLAGS="%optflags"

%check
make check

%install
%makeinstall_std PREFIX=%_prefix

%files
%_bindir/art-xq
%_man1dir/art-xq.1*

%changelog
* Wed Nov 25 2026 Amir Dzhakishev <dzhakishev@altlinux.org> 1.0-alt1
- Initial build.
