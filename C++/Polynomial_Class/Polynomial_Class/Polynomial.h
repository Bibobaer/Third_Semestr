#pragma once
#include <vector>
#include <optional>
#include <string>
#include <sstream>
#include <cmath>

class Polynomial
{
private:
	std::string tmp;
	double a, b, c;

	void ParseString() {
		size_t pos_a = tmp.find('x');
		size_t pos_b = tmp.find('x', pos_a + 1);

		a = tmp[pos_a - 1] - 48;
		b = tmp[pos_b - 1] - 48;
		c = tmp.back() - 48;
	}
public:
	template <typename T>
	Polynomial(T&& Str) : tmp(Str){
		ParseString();
	}

	std::optional<std::pair<double, double>> Get_Roots() {
		if (a == 0) {
			return std::nullopt;
		}

		double Desc = b * b - 4 * a * c;
		if (Desc < 0) {
			return std::nullopt;
		}
		else if (Desc == 0) {
			return std::make_pair<double, double>(-b/(2*a), -b/(2*a));
		}
		else {
			return std::make_pair<double, double>((-b + sqrt(Desc))/(2 * a), (-b - sqrt(Desc)) / (2 * a));
		}
	}
};

