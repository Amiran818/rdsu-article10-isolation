// art-geo: расстояние по дуге большого круга и азимут (C++)
#pragma once
#include <string>

namespace geo {

struct Point {
    double lat, lon; // градусы
};

double distance_km(const Point &a, const Point &b);
double bearing_deg(const Point &a, const Point &b);
Point parse(const std::string &s); // "lat,lon"

} // namespace geo
