#include <iostream>
#include <compare>
#include <vector>


class Type {
private:
	int val;
public:
	Type() = default;

	Type(int&& a) : val(a) {};

	auto operator<=>(const Type& a) const = default;
	void Print() {
		std::cout << this->val << " ";
	}
};


void Sort(std::vector<Type>& Arr) {
	for (auto i = 0; i < Arr.size(); i++)
		for (auto j = 0; j + 1 < Arr.size() - i; j++)
			if ((Arr[j] <=> Arr[j + 1]) == std::partial_ordering::greater) {
				auto tmp = Arr[j];
				Arr[j] = Arr[j+1];
				Arr[j + 1] = tmp;
			}
}

int main(void) {
	std::vector<Type> a = { Type(1), Type(12) , Type(2), Type(9), Type(0)};
	Sort(a);
	for (auto el : a) {
		el.Print();
	}
	return 0;
}