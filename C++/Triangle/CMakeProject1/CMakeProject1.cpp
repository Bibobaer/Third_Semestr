#include <iostream>
#include "Triangle.hpp"
#include <fstream>

int main() {
	std::ofstream file;
	try {
		Geometry::Point pt[3] = { Geometry::Point(9, 0), Geometry::Point(0, 8), Geometry::Point(15, 8) };
		Geometry::Triangle t1(pt);
		/*file.open("output.txt");
		if (file.is_open()) {
			file << t1;
		}
		std::cout << t1;*/ 

		t1.Draw();
	}
	catch (std::string e) {
		std::cout << e << std::endl;
	}
	//file.close();

	return 0;
}
