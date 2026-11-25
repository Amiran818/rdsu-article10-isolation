Name: art-pyext
Version: 1.0
Release: alt1

Summary: Small integer helpers for Python written in C
License: MIT
Group: Development/Python3

Source: %name-%version.tar

BuildRequires: rpm-build-python3
BuildRequires: python3-dev
BuildRequires: python3-module-setuptools

%description
Python extension module artfast implemented in C (gcd, popcount).
Training package for the build isolation experiment.

%prep
%setup

%build
%python3_build

%check
PYTHONPATH=$(echo build/lib*) %__python3 test_artfast.py

%install
%python3_install

%files
%python3_sitelibdir/artfast*.so
%python3_sitelibdir/artfast-%version-*.egg-info

%changelog
* Wed Nov 25 2026 Amir Dzhakishev <dzhakishev@altlinux.org> 1.0-alt1
- Initial build.
