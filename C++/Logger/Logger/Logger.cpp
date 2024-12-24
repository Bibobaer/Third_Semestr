// Logger.cpp : Определяет функции для статической библиотеки.
//

#include "pch.h"
#include "framework.h"

Logger::Logger(std::ostream& out_str): out(out_str) {}

void Logger::INFO(std::string message) {
	this->out << message;
}

void Logger::ERROR(std::string message) {
	std::cerr << message;
}

void Logger::WARNINGS(std::string message) {
	this->out << message;
}

void Logger::DEBUG(std::string message) {
	this->out << message;
}
