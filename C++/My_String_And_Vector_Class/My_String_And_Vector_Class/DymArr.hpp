#pragma once

class String;

class Dynamic_Array {
	String* Data;
	int Count_Element;
	size_t Size;
public:
	Dynamic_Array();
	~Dynamic_Array();
	bool Push(const String& elem);
	void Sort();
	void Print();
};