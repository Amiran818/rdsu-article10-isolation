// Модульные тесты art-geo (запускаются через ctest)
#include "geo.hpp"

#include <cmath>
#include <cstdio>

static int failed;

static void near(const char *what, double got, double want, double eps)
{
    if (std::fabs(got - want) > eps) {
        std::printf("FAIL %s: %.3f != %.3f\n", what, got, want);
        failed++;
    } else {
        std::printf("ok   %s\n", what);
    }
}

int main()
{
    geo::Point msk{55.7558, 37.6173}, spb{59.9343, 30.3351};
    near("moscow-spb distance", geo::distance_km(msk, spb), 633.0, 1.0);
    near("same point", geo::distance_km(msk, msk), 0.0, 1e-9);
    near("due north", geo::bearing_deg({0, 0}, {10, 0}), 0.0, 1e-9);
    near("due east", geo::bearing_deg({0, 0}, {0, 10}), 90.0, 1e-9);
    near("parse", geo::parse("1.5,-2").lon, -2.0, 1e-12);
    return failed != 0;
}
