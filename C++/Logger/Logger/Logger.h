#pragma once

// Добавьте сюда заголовочные файлы для предварительной компиляции
#include "framework.h"
#include <iostream>

class Logger {
	std::ostream& out;
public:
	Logger() = default;
	Logger(std::ostream& out_str);
	void INFO(std::string message);
	void ERROR(std::string message);
	void WARNINGS(std::string message);
	void DEBUG(std::string message);
};