#include "Binary_Parser.h"

PE_Parser::PE_Parser(std::string filename) {
	this->stream.open(filename, std::ios::binary);

	if (!this->stream.is_open()) {
		throw std::string("Error. File dont open\n");
	}
	DOS_HEADER dosHeader;
	stream.read(reinterpret_cast<char*>(&dosHeader), sizeof(dosHeader));

	if (dosHeader.e_magic != 0x5A4D) {
		throw std::string("This is not MZ");
	}

	stream.seekg(dosHeader.e_lfanew, std::ios::beg);

	uint32_t Sign;

	stream.read(reinterpret_cast<char*>(&Sign), sizeof(Sign));

	if (Sign != 0x00004550) {
		throw std::string("This is not PE file");
	}
	
	DOS_FILE DF;

	stream.read(reinterpret_cast<char*>(&DF), sizeof(DF));
	buffer = DF;

	_IMAGE_OPTIONAL_HEADER tmp;
	stream.read(reinterpret_cast<char*>(&tmp), sizeof(tmp));
	std::cout <<std::hex<< tmp.DataDirectory[0].VirtualAddress<<std::dec<<std::endl;
	
	stream.seekg(tmp.DataDirectory[0].VirtualAddress, std::ios::beg);
	_IMAGE_IMPORT_DESCRIPTOR importDescriptor;
	uint32_t r;
	stream.read(reinterpret_cast<char*>(&r), sizeof(r));
	std::cout << r << std::endl;
	//while (true) {
	//	stream.read(reinterpret_cast<char*>(&importDescriptor), sizeof(importDescriptor));
	//	if (importDescriptor.Name == 0)
	//		break; // Заканчиваем, если достигнут конец импортного дескриптора

	//	// Читаем имя импортируемого модуля
	//	char moduleName[256];
	//	stream.seekg(importDescriptor.Name, std::ios::beg);
	//	stream.getline(moduleName, sizeof(moduleName), '\0');

	//	std::cout << "Импортируемый модуль: " << moduleName << std::endl;

	//	// Читаем адрес первой функции
	//	uint32_t thunk = importDescriptor.FirstThunk;
	//	stream.seekg(thunk, std::ios::beg);
	//	while (true) {
	//		uint32_t functionAddress;
	//		stream.read(reinterpret_cast<char*>(&functionAddress), 8);
	//		if (functionAddress == 0)
	//			break; // Заканчиваем, если достигнут конец

	//		// Читаем имя функции
	//		uint32_t functionNameAddress = functionAddress + 2; // Пропускаем атрибут и получаем адрес имени
	//		stream.seekg(functionNameAddress, std::ios::beg);
	//		char functionName[256];
	//		stream.getline(functionName, sizeof(functionName), '\0');
	//		std::cout << "  " << functionName << std::endl;
	//	}
	//}
}

void PE_Parser::PrintData() { 
	std::cout << "Machine: " << buffer.Machine << std::endl;
	std::cout << "NumberOfSections: " << buffer.NumberOfSections << std::endl;
	std::cout << "TimeDateStamp: " << buffer.TimeDateStamp << std::endl;
	std::cout << "PointerToSymbolTable: " << buffer.PointerToSymbolTable << std::endl;
	std::cout << "NumberOfSymbols: " << buffer.NumberOfSymbols << std::endl;
	std::cout << "SizeOfOptionalHeader: " << buffer.SizeOfOptionalHeader << std::endl;
	std::cout << "Characteristics: " << buffer.Characteristics << std::endl;
}