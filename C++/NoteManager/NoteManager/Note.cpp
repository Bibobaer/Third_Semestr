#include "Note.h"
#include <Windows.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <conio.h>

void XOR_cipher(std::string& message, std::string& key, std::string& encrypted) {
	for (auto i = 0; i < message.size(); i++) {
		encrypted[i] = message[i] ^ key[i % key.size()];
	}
	encrypted[message.size()] = '\0';
}

Note::Note(const std::string& name) : filename(name){}

void Note::ReadFile() {
	std::ifstream file(filename);

	if (!file) {
		std::cout << "Dont have that file";
		return;
	}

	std::string line;

	while (std::getline(file, line)) {
		std::cout << line << std::endl;
	}
	file.close();
	return;
}

void Note::WriteFile() {
	std::ifstream file(filename);

	std::vector<char> buffer;
	if (file.is_open()) {
		char c;
		while (file.get(c)) {
			buffer.push_back(c);
		}
	}
	file.close();

	for (const auto& el : buffer) {
		std::cout << el;
	}

	std::ofstream f(filename);

	char c;
	while ((c = _getch()) != 13)
	{
		if (c == 8) {
			std::cout << "\b \b";
			buffer.pop_back();
			continue;
		}
		else {
			std::cout << c;
			buffer.push_back(c);
		}
	}

	for (const auto& el : buffer) {
		f << el;
	}
	f.close();
	return;
}

void ShowFiles(const wchar_t* path) {
	WIN32_FIND_DATAW findFileData;
	HANDLE hFind = INVALID_HANDLE_VALUE;

	// Создаем шаблон пути, чтобы найти все файлы в директории
	wchar_t fullPath[MAX_PATH];
	swprintf(fullPath, MAX_PATH, L"%s\\*", path);

	// Находим первый файл в директории
	hFind = FindFirstFileW(fullPath, &findFileData);
	if (hFind == INVALID_HANDLE_VALUE) {
		wprintf(L"Ошибка при открытии директории: %s\n", path);
		return;
	}
	// Перебираем все найденные файлы и директории
	do {
		if (wcscmp(findFileData.cFileName, L".") != 0 && wcscmp(findFileData.cFileName, L"..") != 0) {
			wprintf(L"\t%s\n", findFileData.cFileName);
		}
	} while (FindNextFileW(hFind, &findFileData) != 0);
	FindClose(hFind);
}