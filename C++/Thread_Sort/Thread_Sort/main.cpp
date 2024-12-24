#include <iostream>
#include "sort.h"
#include <algorithm>
#include <chrono>

int main(void) {
	std::chrono::time_point<std::chrono::system_clock> start_1, end_1, start_2, end_2;
	std::srand((unsigned int)std::time(NULL));
	std::vector<int> arr_1;
	std::vector<int> arr_2;

	GenetareVector(arr_1);
	GenetareVector(arr_2);
	
	start_1 = std::chrono::system_clock::now();
	SortOneThread(arr_1);
	end_1 = std::chrono::system_clock::now();
	PrintVector(arr_1);
	
	start_2 = std::chrono::system_clock::now();
	SortTwoThread(arr_2);
	end_2 = std::chrono::system_clock::now();
	PrintVector(arr_2);

	std::chrono::duration<double> elapsed_seconds_1 = end_1 - start_1;
	std::chrono::duration<double> elapsed_seconds_2 = end_2 - start_2;
	std::cout << "One Thread: " << elapsed_seconds_1.count() << std::endl;
	std::cout << "Two Thread: " << elapsed_seconds_2.count() << std::endl;

	return 0;
}