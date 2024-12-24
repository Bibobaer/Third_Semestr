#include <iostream>
#include "Polynomial.h"

int main(void) {
 	Polynomial a("1x^2+-2x+1");
	auto d = a.Get_Roots();
	if (d.has_value()) {
		std::cout << d.value().first << " " << d.value().second << std::endl;
	}
	return 0;
}