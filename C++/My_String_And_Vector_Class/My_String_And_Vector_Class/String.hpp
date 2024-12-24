#pragma once

class String {
private:
	char* data;
	size_t size;
public:
	String();
	String(const char* str);
	String(const String& str);
	~String();
	void Concat(const String& str);
	void Print();
	String operator=(const String& str);
	bool operator<(const String& str);
	bool operator>(const String& str);
};