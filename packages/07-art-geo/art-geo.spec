Name: art-geo
Version: 1.0
Release: alt1

Summary: Great-circle distance and bearing between two points
License: MIT
Group: Sciences/Geosciences

Source: %name-%version.tar

BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: ctest

%description
C++ utility computing the great-circle distance and the initial
bearing between two geographic points; built with CMake and tested
with CTest. Training package for the build isolation experiment.

%prep
%setup

%build
%cmake
%cmake_build

%check
%ctest

%install
%cmake_install

%files
%_bindir/art-geo

%changelog
* Wed Nov 25 2026 Amir Dzhakishev <dzhakishev@altlinux.org> 1.0-alt1
- Initial build.
