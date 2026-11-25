// art-geo LAT,LON LAT,LON - расстояние (км) и начальный азимут (градусы)
#include "geo.hpp"

#include <cstdio>
#include <exception>

int main(int argc, char **argv)
{
    if (argc != 3) {
        std::fprintf(stderr, "usage: art-geo LAT,LON LAT,LON\n");
        return 2;
    }
    try {
        geo::Point a = geo::parse(argv[1]), b = geo::parse(argv[2]);
        std::printf("%.1f km, bearing %.1f\n", geo::distance_km(a, b),
                    geo::bearing_deg(a, b));
    } catch (const std::exception &e) {
        std::fprintf(stderr, "art-geo: %s\n", e.what());
        return 1;
    }
    return 0;
}
