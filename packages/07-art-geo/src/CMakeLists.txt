cmake_minimum_required(VERSION 3.16)
project(art-geo VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
include(GNUInstallDirs)

add_library(geo STATIC geo.cpp)
add_executable(art-geo main.cpp)
target_link_libraries(art-geo PRIVATE geo)

enable_testing()
add_executable(test-geo test_geo.cpp)
target_link_libraries(test-geo PRIVATE geo)
add_test(NAME geo COMMAND test-geo)
add_test(NAME cli COMMAND art-geo 0,0 0,1)
set_tests_properties(cli PROPERTIES PASS_REGULAR_EXPRESSION "111\\.2 km, bearing 90\\.0")

install(TARGETS art-geo RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})
