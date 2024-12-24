#include "Shape.h"
#include "Drawer.h"
#include <iostream>
#include "raylib.h"

void ConsoleDrawer::DrawLine(Point a, Point b) {
	std::cout << '(' << a.x << ", " << a.y << ')' << std::endl;
	std::cout << "Some Line" << std::endl;
	std::cout << '(' << b.x << ", " << b.y << ')' << std::endl << std::endl;
}

void ConsoleDrawer::DrawPoint(Point a) {
	std::cout << '(' << a.x << ', ' << a.y << ')' << std::endl;
}

void RayDrawer::DrawLine(Point a, Point b) {
	return;
}

void RayDrawer::DrawPoint(Point a) {
	DrawPixel(a.x, a.y, GREEN);
}

int Drawer::GetInfo() {
	return 1;
}

