#include "raylib.h"
#include <iostream>

#define WINDOWS_WIDTH	700
#define WINDOWS_HEIGHT	700

struct Point
{
	int x;
	int y;
	Point() : x(0), y(0) {}
	Point(int a, int b) : x(a), y(b) {}
};

void Brezeham_line(Point a, Point b) {
	int dx = b.x - a.x;
	int dy = b.y - a.y;
	int sx = (dx > 0) ? 1 : -1;
	int sy = (dy > 0) ? 1 : -1;

	dx = abs(dx);
	dy = abs(dy);

	if (dx > dy) {
		int err = dx / 2;
		while (a.x != b.x) {
			if (a.x >= 0 && a.x < WINDOWS_WIDTH && a.y >= 0 && a.y < WINDOWS_HEIGHT) {
				DrawPixel(a.x, a.y, GREEN);
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
			if (a.x >= 0 && a.x < WINDOWS_WIDTH && a.y >= 0 && a.y < WINDOWS_HEIGHT) {
				DrawPixel(a.x, a.y, GREEN);
			}
			err -= dx;
			if (err < 0) {
				a.x += sx;
				err += dy;
			}
			a.y += sy;
		}
	}
	if (b.x >= 0 && b.x < WINDOWS_WIDTH && b.y >= 0 && b.y < WINDOWS_HEIGHT) {
		DrawPixel(b.x, b.y, GREEN);
	}
}

int main() {
	InitWindow(WINDOWS_WIDTH, WINDOWS_HEIGHT, "Test");

	Point Center(WINDOWS_WIDTH / 2, WINDOWS_HEIGHT / 2);
	Point b(150, 150);
	Point c(500, 500);

	while (!WindowShouldClose()) {

		BeginDrawing();

		DrawCircle(WINDOWS_WIDTH / 2, WINDOWS_HEIGHT / 2, 300, RAYWHITE);

		Brezeham_line(Center, b);

		EndDrawing();
	}

	CloseWindow();

	return 0;
}