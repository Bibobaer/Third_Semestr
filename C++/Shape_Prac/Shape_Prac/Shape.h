#pragma once
#include <vector>

class IDrawer;

struct Point {
	int x;
	int y;
	Point() = default;
	Point(int a, int b) : x(a), y(b) {}
};

class IShape {
public:
	virtual void Draw(IDrawer& dr) = 0;
	virtual std::vector<Point> GetCoords() = 0;
};

class Shape : public IShape {
protected:
	std::vector<Point> points;
public:
	Shape() = default;
	Shape(const std::vector<Point>& pts);
	virtual void Draw(IDrawer& dr) = 0;
	virtual std::vector<Point> GetCoords() override;
};

class Triangle : public Shape {
public:
	Triangle() = default;
	Triangle(std::vector<Point> pts);

	void Draw(IDrawer& dr) override; 
};