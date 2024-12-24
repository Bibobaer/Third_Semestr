// MyRequest.cpp : Определяет функции для статической библиотеки.
//

#include "pch.h"
#include "framework.h"
#include "MyRequest.h"

#include <iostream>
#include <fstream>

#pragma comment(lib, "wininet.lib")

HttpClient::HttpClient() {
	hInternet = InternetOpenA("HttpClient", INTERNET_OPEN_TYPE_PRECONFIG, NULL, NULL, 0);
	if (!hInternet) {
		throw std::invalid_argument("Wrong!");
	}
}

HttpClient::~HttpClient() {
	if (hInternet) {
		InternetCloseHandle(hInternet);
	}
}

std::string boundary = "------------------------boundary_string";

static std::string ReadFile(const std::string& path) {
	std::string res;

	std::ifstream file(path, std::ios::binary);

	if (file.is_open()) { while (std::getline(file, res)) {} }

	return res;
}

std::string HttpClient::GetMultiPart(const std::string& chatID, const std::string& path, std::string name) {
	std::string res;
	res += "--" + boundary + "\r\n";
	res += "Content-Disposition: form-data; name=\"chat_id\"\r\n\r\n";
	res += chatID + "\r\n";
	res += "--" + boundary + "\r\n";
	res += "Content-Disposition: form-data; name=\"document\"; filename=\"" + name + "\"\r\n";
	res += "Content-Type: application/octet-stream\r\n\r\n";
	res += ReadFile(path);
	res += "\r\n--" + boundary + "--\r\n";

	return res;
}

Response HttpClient::Get(std::string url, std::map<std::string, std::string> headers) {
	Response response;

	HINTERNET hConnect = InternetOpenUrlA(hInternet, url.c_str(), NULL, 0, INTERNET_FLAG_RELOAD, 0);
	if (!hConnect) {
		response.Status = static_cast<int>(GetLastError());
		response.Response_Data = "Failed to connect";
		return response;
	}

	HINTERNET hRequest = HttpOpenRequestA(hConnect, "GET", NULL, NULL, NULL, NULL, INTERNET_FLAG_RELOAD | INTERNET_FLAG_SECURE, 0);
	if (!hRequest) {
		response.Response_Data = "Failed connection request";
		response.Status = GetLastError();

		InternetCloseHandle(hConnect);
		return response;
	}

	std::string headerString; 

	for (const auto& header : headers) {
		headerString += header.first + ": " + header.second + "\r\n";
	}

	if (!HttpSendRequestA(hRequest, headerString.c_str(), headerString.size(), (LPVOID)"", 0)) {

		response.Response_Data = "Failed to send request.\n";
		response.Status = GetLastError();

		InternetCloseHandle(hRequest);
		InternetCloseHandle(hConnect);
		
		return response;
	}

	DWORD status_code = 0;
	DWORD status_code_size = sizeof(status_code);

	HttpQueryInfoA(hRequest, HTTP_QUERY_STATUS_CODE | HTTP_QUERY_FLAG_NUMBER, &status_code, &status_code_size, NULL);

	response.Status = status_code;


	char buffer[4096];
	DWORD bytes_read;

	while (InternetReadFile(hRequest, buffer, sizeof(buffer), &bytes_read) && bytes_read != 0) {
		response.Response_Data.append(buffer, bytes_read);
	}

	InternetCloseHandle(hRequest);
	InternetCloseHandle(hConnect);
	
	return response;
}

Response HttpClient::Post(std::string url, std::string data, std::map<std::string, std::string> headers) {
    Response response;

    URL_COMPONENTSA urlComp = { 0 };
    urlComp.dwStructSize = sizeof(urlComp);

    char hostName[256];
    char urlPath[1024];

    urlComp.lpszHostName = hostName;
    urlComp.dwHostNameLength = sizeof(hostName);
    urlComp.lpszUrlPath = urlPath;
    urlComp.dwUrlPathLength = sizeof(urlPath);

    if (!InternetCrackUrlA(url.c_str(), 0, 0, &urlComp)) {
        response.Response_Data = "Failed to parse URL.";
        response.Status = GetLastError();

        return response;
    }

    HINTERNET hConnect = InternetConnectA(hInternet, urlComp.lpszHostName, urlComp.nPort, NULL, NULL, INTERNET_SERVICE_HTTP, 0, 0);

    if (!hConnect) {
        response.Response_Data = "URL connect failed.";
        response.Status = GetLastError();

        return response;
    }

    HINTERNET hRequest = HttpOpenRequestA(hConnect, "POST", urlComp.lpszUrlPath, NULL, NULL, NULL, INTERNET_FLAG_RELOAD | INTERNET_FLAG_SECURE, 0);

    if (!hRequest) {
        response.Response_Data = "Failed connection request.";
        response.Status = GetLastError();

        InternetCloseHandle(hConnect);
        return response;

    }
    std::string headers_str;

    for (const auto& header : headers) {
        headers_str += header.first + ": " + header.second + "\r\n";
    }

    if (!HttpSendRequestA(hRequest, headers_str.c_str(), headers_str.size(), (void*)data.c_str(), data.size())) {
        response.Response_Data = "Failed to send request.";
        response.Status = GetLastError();

        InternetCloseHandle(hRequest);
        InternetCloseHandle(hConnect);
        return response;

    }

    DWORD status_code = 0;
    DWORD status_code_size = sizeof(status_code);

    HttpQueryInfoA(hRequest, HTTP_QUERY_STATUS_CODE | HTTP_QUERY_FLAG_NUMBER, &status_code, &status_code_size, NULL);

    response.Status = status_code;

    char buffer[4096];
    DWORD bytes_read;

    while (InternetReadFile(hRequest, buffer, sizeof(buffer), &bytes_read) && bytes_read != 0) {
        response.Response_Data.append(buffer, bytes_read);
    }

    InternetCloseHandle(hRequest);
    InternetCloseHandle(hConnect);

    return response;

}
