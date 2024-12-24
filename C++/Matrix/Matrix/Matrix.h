#pragma once
#include <vector>
#include <iostream>
#include <fstream>

class Matrix
{
private:
	unsigned int rows;
	unsigned int cols;
	std::vector<std::vector<int>> data;
public:
	Matrix() = default;
	Matrix(std::istream& istr);
	Matrix(std::vector<std::vector<int>>& data);
	Matrix operator+ (const Matrix& A);
	Matrix operator* (const Matrix& A);
	void Print(void);
};

