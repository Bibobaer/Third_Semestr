#include "Shape.h"
#include "Drawer.h"
#include <iostream>
#include <string>

void DrawShapes(std::vector<IShape> arrSh, IDrawer& dr) {
	for (auto i = 0; i, arrSh.size(); i++) {
		arrSh[i].Draw(dr);
	}
}

int main(void) {
	try {
		std::vector<Point> pts = { Point(1, 2), Point(0, 6), Point(4, 5) };

		Triangle t1(pts);
		ConsoleDrawer cdr;
		IDrawer& tmp = cdr;

		t1.Draw(tmp);
	}
	catch (std::string e) {
		std::cout << e;
	}
	return 0;
}