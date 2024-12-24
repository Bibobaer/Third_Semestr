#include "String.hpp"
#include "DymArr.hpp"
#include <iostream>

Dynamic_Array::Dynamic_Array() : Count_Element(0), Size(1) {
	this->Data = new String[1];
}

Dynamic_Array::~Dynamic_Array() {
	delete[] this->Data;
}

bool Dynamic_Array::Push(const String& elem) {
	if (this->Count_Element == this->Size) {
		String* NewBuf = new String[this->Size + 1];
		std::copy_n(this->Data, this->Size, NewBuf);
		delete[] this->Data;
		this->Data = NewBuf;
		this->Data[this->Count_Element] = elem;
		this->Count_Element++;
		this->Size++;
		return 1;
	}
	else {
		this->Data[Count_Element] = elem;
		this->Count_Element++;
		return 1;
	}
	return 0;
}

void Dynamic_Array::Sort() {
	for (int i = 0; i < this->Count_Element; i++) {
		for (int j = 0; j + 1 < this->Count_Element - i; j++) {
			if (this->Data[j] < this->Data[j + 1]) {
				String tmp = this->Data[j];
				this->Data[j] = this->Data[j + 1];
				this->Data[j + 1] = tmp;
			}
		}
	}
}

void Dynamic_Array::Print() {
	for (auto i = 0; i < this->Count_Element; i++) {
		std::cout << i + 1 << ". ";
		this->Data[i].Print();
	}
}