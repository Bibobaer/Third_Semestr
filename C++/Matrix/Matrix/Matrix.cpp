#include "Matrix.h"
#include <string>

Matrix::Matrix(std::istream& istr) {
	istr >> rows >> cols;
	if (rows == 0 || cols == 0)
		throw std::string("Error");

	this->data = std::vector<std::vector<int>>(rows, std::vector<int>(cols));
	for (unsigned int i = 0; i < rows; i++) {
		for (unsigned int j = 0; j < cols; j++) {
			if (istr.eof())
				throw std::string("Error");
			istr >> this->data[i][j];
		}
	}
}

Matrix::Matrix(std::vector<std::vector<int>>& data) : rows(data.size()), cols(data[0].size()), data(data) {
}

Matrix Matrix::operator+ (const Matrix& A) {
	if (this->rows != A.rows || this->cols != A.cols)
		throw (std::string)"Error. Matrix not equal by rows or cols";

	for (unsigned int i = 0; i < A.rows; i++) {
		for (unsigned int j = 0; j < A.cols; j++) {
			this->data[i][j] = this->data[i][j] + A.data[i][j];
		}
	}
	return *this;
}

Matrix Matrix::operator* (const Matrix& A) {
	if (this->cols != A.rows)
		throw (std::string)"Error. Matrix not equal by rows and cols";

	std::vector<std::vector<int>> res(this->rows, std::vector<int>(A.cols));

	for (unsigned int i = 0; i < this->rows; i++) {
		for (unsigned int j = 0; j < A.cols; j++) {
			for (unsigned int k = 0; k < this->cols; k++) {
				res[i][j] += this->data[i][k] * A.data[k][j];
			}
		}
	}

	return Matrix(res);
}

void Matrix::Print(void) {
	for (const auto& rw : this->data) {
		for (auto elem : rw) {
			std::cout << elem << ' ';
		}
		std::cout << std::endl;
	}
}