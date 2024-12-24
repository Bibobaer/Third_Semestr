#pragma once

#include <map>
#include <string>
#include <Windows.h>
#include <wininet.h>

struct Response {
	int Status;
	std::string Response_Data;

	Response() = default;
	Response(int& s, std::string& d) : Status(s), Response_Data(d) {};
};

class HttpClient {
private:
	HINTERNET hInternet;
public:
	HttpClient();
	~HttpClient();

	std::string GetMultiPart(const std::string& chatID, const std::string& path, std::string name);

	Response Get(std::string url, std::map<std::string, std::string> headers);

	Response Post(std::string url, std::string data, std::map<std::string, std::string> headers);
};
