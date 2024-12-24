#include "Shape.h"
#include "Drawer.h"
#include <string>

Shape::Shape(const std::vector<Point>& pts) {
	this->points = std::vector<Point>(pts.size());
	for (auto i = 0; i < pts.size(); i++) {
		this->points[i] = pts[i];
	}
}

std::vector<Point> Shape::GetCoords() {
	return this->points;
}

Triangle::Triangle(std::vector<Point> pts) {
	if (pts.size() != 3) {
		throw std::string("Error");
	}

	this->points = std::vector<Point>(pts.size());
	for (auto i = 0; i < pts.size(); i++) {
		this->points[i] = pts[i];
	}
}

void Triangle::Draw(IDrawer& dr) {
	dr.DrawLine(this->points[0], this->points[1]);
	dr.DrawLine(this->points[0], this->points[2]);
	dr.DrawLine(this->points[1], this->points[2]);
}