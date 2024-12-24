#include "String.hpp"
#include "DymArr.hpp"
#include "Menu.hpp"
#include <iostream>

int main() {
	try {
		Dynamic_Array arr;
		Menu(arr);
	}
	catch(std::string e){
		std::cout << e << std::endl;
	}
	return 0;
}
