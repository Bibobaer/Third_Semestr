#define _CRT_SECURE_NO_WARNINGS
#include <iostream>
#include "String.hpp"

String::String() : size(1) {
	this->data = new char[1];
	this->data[0] = '\0';
}

String::String(const char* str) {
	if (str == NULL) {
		throw std::string("Error. str cant be null");
	}
	this->size = strlen(str);
	this->data = new char[this->size + 1];
	strcpy(this->data, str);
}

String::String(const String& str) {
	this->size = str.size;
	this->data = new char[this->size + 1];
	strcpy(this->data, str.data);
}

String::~String() {
	delete[] this->data;
}

void String::Concat(const String& str) {
	if (str.data == nullptr || this->data == nullptr)
		return;

	char* NewData = new char[this->size + str.size + 1];
	if (NewData == nullptr)
		return;
	std::copy_n(this->data, this->size + 1, NewData);
	delete[] this->data;
	this->data = NewData;
	strcat(this->data, str.data);
	this->size += str.size;

}

void String::Print() {
	std::cout << this->data << std::endl;
}

String String::operator=(const String& str) {
	this->size = str.size;
	this->data = new char[this->size + 1];
	strcpy(this->data, str.data);
	return *this;
}

bool String::operator<(const String& str) {
	return strcmp(this->data, str.data) == 1 ? 1 : 0;
}

bool String::operator>(const String& str) {
	return strcmp(this->data, str.data) == -1 ? 1 : 0;
}