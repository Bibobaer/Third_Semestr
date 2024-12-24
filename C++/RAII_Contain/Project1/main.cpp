#include <iostream>

class Container {
	int* data;
	size_t size;
public:
	Container() {
		data = nullptr;
		size = 0;
	}

	void Add(int value) {
		if (data == nullptr) {
			data = new int[1];
			data[0] = value;
			size++;
		}
		else {
			int* NewBuf = new int[size + 1];
			std::copy_n(data, size+1, NewBuf);
			NewBuf[size++] = value;
			delete[] data;
			data = NewBuf;
		}
	}

	void Sort() {
		for (auto i = 0; i < size; i++) {
			for (auto j = 0; j + 1 < size - i; j++) {
				if (data[j] > data[j + 1]) {
					data[j] ^= data[j + 1] ^= data[j] ^= data[j + 1];
				}
			}
		}
	}

	void Print() {
		for (auto i = 0; i < size; i++) {
			std::cout << data[i] << " ";
		}
	}

	~Container() {
		this->Sort();
		this->Print();
		delete[] data;
	}
};

int main(void) {
	Container a;

	while (true)
	{
		int c = 0;
		std::cin >> c;
		if (c == 0) {
			break;
		}
		a.Add(c);
	}
	return 0;
}