#pragma once

#include <iostream>
#include <vector>

namespace Geometry {
	struct Point {
		int x;
		int y;
		Point(int a, int b);
		Point() = default;
	};

	class Triangle {
		Point points[3];
	public:
		Triangle(Point pts[3]);
		void print();
		void Draw();
		Point Get_Point_By_Index(int index);
		void Set_Point_By_Index(int newX, int newY, int index);
		friend std::ostream& operator<<(std::ostream& str, Triangle& tr);
		friend void Brezeham_line(Point a, Point b, std::vector<std::vector<char>>& field);
	};

	std::ostream& operator<<(std::ostream& str, Triangle& tr);

	void Brezeham_line(Point a, Point b, std::vector<std::vector<char>>& field);
}