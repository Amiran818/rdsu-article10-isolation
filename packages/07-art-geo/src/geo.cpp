#include "geo.hpp"

#include <cmath>
#include <sstream>
#include <stdexcept>

namespace geo {

static constexpr double R = 6371.0088; // средний радиус Земли, км
static double rad(double d) { return d * M_PI / 180.0; }

double distance_km(const Point &a, const Point &b)
{
    double dlat = rad(b.lat - a.lat), dlon = rad(b.lon - a.lon);
    double h = std::sin(dlat / 2) * std::sin(dlat / 2) +
               std::cos(rad(a.lat)) * std::cos(rad(b.lat)) *
               std::sin(dlon / 2) * std::sin(dlon / 2);
    return 2 * R * std::asin(std::sqrt(h));
}

double bearing_deg(const Point &a, const Point &b)
{
    double dlon = rad(b.lon - a.lon);
    double y = std::sin(dlon) * std::cos(rad(b.lat));
    double x = std::cos(rad(a.lat)) * std::sin(rad(b.lat)) -
               std::sin(rad(a.lat)) * std::cos(rad(b.lat)) * std::cos(dlon);
    return std::fmod(std::atan2(y, x) * 180.0 / M_PI + 360.0, 360.0);
}

Point parse(const std::string &s)
{
    std::istringstream in(s);
    Point p{};
    char comma = 0;
    if (!(in >> p.lat >> comma >> p.lon) || comma != ',')
        throw std::invalid_argument("expected LAT,LON: " + s);
    return p;
}

} // namespace geo
