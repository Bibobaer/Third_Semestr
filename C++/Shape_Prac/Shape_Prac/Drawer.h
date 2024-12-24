#pragma once

struct Point;

class IDrawer {
public:
	virtual void DrawLine(Point a, Point b) = 0;
	virtual void DrawPoint(Point a) = 0;
	virtual int GetInfo() = 0;
};

class Drawer: public IDrawer {
public:
	virtual void DrawLine(Point a, Point b) = 0;
	virtual void DrawPoint(Point a) = 0;
	virtual int GetInfo() override;
};

class ConsoleDrawer : public Drawer {
	virtual void DrawLine(Point a, Point b) override;
	virtual void DrawPoint(Point a) override;
};

class RayDrawer : public Drawer {
	virtual void DrawLine(Point a, Point b) override;
	virtual void DrawPoint(Point a) override;
};