#include "Triangle.hpp"
#include <string>
#include <math.h>

namespace Geometry {

	Point::Point(int a, int b) {
		this->x = a;
		this->y = b;
	}

	inline float LineLength(Point a, Point b) {
		return static_cast<float>(sqrt((a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y)));
	}

	Triangle::Triangle(Point pts[3]) {
		float len_1 = LineLength(pts[0], pts[1]);
		float len_2 = LineLength(pts[0], pts[2]);
		float len_3 = LineLength(pts[1], pts[2]);

		if (len_1 + len_2 <= len_3 || len_1 + len_3 <= len_2 || len_2 + len_3 <= len_1) {
			throw std::string("Error. Not a triangle");
		}
		for (int i = 0; i < 3; i++) {
			this->points[i] = pts[i];
		}
	}

	void Triangle::print() {
		for (int i = 0; i < 3; i++) {
			std::cout << this->points[i].x << this->points[i].y << std::endl;
		}
	}

	void Triangle::Draw() {
		int absMaxX = std::max(std::abs(this->points[0].x), std::abs(this->points[1].x));
		absMaxX = std::max(absMaxX, std::abs(this->points[2].x));
		int absMaxY = std::max(std::abs(this->points[0].y), std::abs(this->points[1].y));
		absMaxY = std::max(absMaxY, std::abs(this->points[2].y));

		std::vector<std::vector<char>> field(absMaxY + 1, std::vector<char>(absMaxX + 1, ' '));

		Brezeham_line(this->points[1], this->points[2], field);
		Brezeham_line(this->points[1], this->points[0], field);
		Brezeham_line(this->points[0], this->points[2], field);

		for (const auto& row : field) {
			for (auto elem : row) {
				std::cout << elem;
			}
			std::cout << std::endl;
		}
	}

	Point Triangle::Get_Point_By_Index(int index) {
		return this->points[index];
	}

	void Triangle::Set_Point_By_Index(int newX, int newY, int index) {
		this->points[index].x = newX;
		this->points[index].y = newY;
		return;
	}

	std::ostream& operator<<(std::ostream& str, Triangle& tr) {
		for (int i = 0; i < 3; i++) {
			str << "(" << tr.points[i].x << " " << tr.points[i].y << ")" << std::endl;
		}
		return str;
	}

	void Brezeham_line(Point a, Point b, std::vector<std::vector<char>>& field) {
		int dx = b.x - a.x;
		int dy = b.y - a.y;
		int sx = (dx > 0) ? 1 : -1;
		int sy = (dy > 0) ? 1 : -1;

		dx = abs(dx);
		dy = abs(dy);

		if (dx > dy) {
			int err = dx / 2;
			while (a.x != b.x) {
				if (a.x >= 0 && a.x < field[0].size() && a.y >= 0 && a.y < field.size()) {
					field[a.y][a.x] = '*';
				}
				err -= dy;
				if (err < 0) {
					a.y += sy;
					err += dx;
				}
				a.x += sx;
			}
		}
		else {
			int err = dy / 2;
			while (a.y != b.y) {
				if (a.x >= 0 && a.x < field[0].size() && a.y >= 0 && a.y < field.size()) {
					field[a.y][a.x] = '*';
				}
				err -= dx;
				if (err < 0) {
					a.x += sx;
					err += dy;
				}
				a.y += sy;
			}
		}
		if (b.x >= 0 && b.x < field[0].size() && b.y >= 0 && b.y < field.size()) {
			field[b.y][b.x] = '*';
		}
	}
}
