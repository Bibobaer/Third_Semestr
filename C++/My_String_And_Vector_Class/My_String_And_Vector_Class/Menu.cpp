#include "Menu.hpp"
#include "DymArr.hpp"
#include "String.hpp"
#include <iostream>
#include <string>
#include <conio.h>

void Menu(Dynamic_Array& arr) {
	int c = 0;

	while (true)
	{
		system("cls");
		std::cout << "\t\033[34mMenu\033[0m" << std::endl;
		std::cout << "\033[32m1 - Print Array\033[0m" << std::endl;
		std::cout << "\033[36m2 - Add new strings\033[0m" << std::endl;
		std::cout << "\033[35m3 - Sort Array\033[0m" << std::endl;
		std::cout << "\033[31m4 - Quit\033[0m" << std::endl;
		c = _getch();
		system("cls");
		if (c == '1') {
			arr.Print();
			system("pause");
		}
		else if (c == '2') {
			int N = 0;
			std::cout << "Enter how many strings add: ";
			std::cin >> N;
			if (N < 1) {
				std::cout << "Count cant be less then zero" << std::endl;
				system("pause");
				continue;
			}

			while (N)
			{
				std::string read;
				std::cin >> read;
				String tmp = read.c_str();
				arr.Push(tmp);
				N--;
			}
		}
		else if (c == '3') {
			arr.Sort();
			system("pause");
		}
		else if (c == '4') {
			break;
		}
		else {
			std::cout << "\033[31mWrong Action\033[0m" << std::endl;
			system("pause");
		}
	}
	return;
}