#include "Binary_Parser.h"

int main(void) {
	try {
		std::string file;
		std::getline(std::cin, file);
		PE_Parser pars(file);
		pars.PrintData();
	}
	catch (std::string e) {	std::cout << e; }
	return 0;
}