# CMakeList.txt: проект CMake для Firefox_Telegram_Sender; включите исходный код и определения,
# укажите здесь логику для конкретного проекта.
#

# Добавьте источник в исполняемый файл этого проекта.
find_package(OpenSSL)

add_executable (Firefox_Telegram_Sender "Firefox_Telegram_Sender.cpp" "Firefox_Telegram_Sender.h" )
target_link_libraries(Firefox_Telegram_Sender PRIVATE OpenSSL::SSL)
	target_link_libraries(Firefox_Telegram_Sender PRIVATE OpenSSL::Crypto)

if (CMAKE_VERSION VERSION_GREATER 3.12)
  set_property(TARGET Firefox_Telegram_Sender PROPERTY CXX_STANDARD 20)
endif()

# TODO: Добавьте тесты и целевые объекты, если это необходимо.
