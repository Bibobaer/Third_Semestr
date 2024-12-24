#include "sort.h"
#include <algorithm>
#include <windows.h>
#include <iostream>
#include <thread>
#include <chrono>

#define COUNT_ELEMENTS	1000

void GenetareVector(std::vector<int>& Arr) {
	int N = COUNT_ELEMENTS;
	
	while (N) {
		Arr.push_back(std::rand());
		N--;
	}
	return;
}

DWORD WINAPI Sort(LPVOID lpParam) {
	std::vector<int>* arr = static_cast<std::vector<int>*>(lpParam);
	std::sort((*arr).begin(), (*arr).end());
	return 0;
}

void SortS(std::vector<int>& arr) {
	std::sort(arr.begin(), arr.end());
}

void SortOneThread(std::vector<int>& arr) {
	auto thread = CreateThread(NULL, 0, Sort, &arr, 0, NULL);

	WaitForSingleObject(thread, INFINITE);

	CloseHandle(thread);
	return;

	/*std::thread t1(SortS, std::reference_wrapper(arr));

	t1.join();
	return;*/
}



void SortTwoThread(std::vector<int>& arr) {
	std::vector<int> tmp1(arr.begin(), arr.begin() + arr.size()/2);
	std::vector<int> tmp2(arr.begin() + arr.size()/2, arr.end());

	auto thread1 = CreateThread(NULL, 0, Sort, &tmp1, 0, NULL);
	auto thread2 = CreateThread(NULL, 0, Sort, &tmp2, 0, NULL);

	WaitForSingleObject(thread1, INFINITE);
	WaitForSingleObject(thread2, INFINITE);

	CloseHandle(thread1);
	CloseHandle(thread2);

	arr.clear();
	std::merge(tmp1.begin(), tmp1.end(), tmp2.begin(), tmp2.end(), std::back_inserter(arr));
	return;

	/*std::vector<int> tmp1(arr.begin(), arr.begin() + arr.size() / 2);
	std::vector<int> tmp2(arr.begin() + arr.size() / 2, arr.end());

	std::thread t1(SortS, std::reference_wrapper(tmp1));
	std::thread t2(SortS, std::reference_wrapper(tmp2));
	t1.join(), t2.join();

	arr.clear();
	std::merge(tmp1.begin(), tmp1.end(), tmp2.begin(), tmp2.end(), std::back_inserter(arr));
	return;*/
}

void PrintVector(std::vector<int> arr) {
	for (auto element : arr) {
		std::cout << element << " ";
	}
	std::cout << std::endl;
}