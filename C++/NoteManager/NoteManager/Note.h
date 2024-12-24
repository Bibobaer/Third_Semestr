#pragma once
#include <string>

void ShowFiles(const wchar_t* path);

class Note
{
private:
	std::string filename;
public:
	Note() = default;
	Note(const std::string& name);

	virtual void ReadFile();
	virtual void WriteFile();
};

class Chip_Note : public Note {
private:
	std::string key;
public:

};



