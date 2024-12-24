#include "Matrix.h"

int main(void) {
	Matrix mat(std::cin);
	Matrix A(std::cin);

	mat = mat * A;
	mat.Print();
	return 0;
}