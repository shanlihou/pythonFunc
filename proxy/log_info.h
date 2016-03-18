#ifndef LOG_INFO_H
#define LOG_INFO_H
#include <stdio.h>
#include <stdarg.h>
#include <string.h>

#define COLOR_NONE         "\033[m" 
#define COLOR_RED          "\033[0;32;31m" 
#define COLOR_LIGHT_RED    "\033[1;31m" 
#define COLOR_GREEN        "\033[0;32;32m" 
#define COLOR_LIGHT_GREEN  "\033[1;32m" 
#define COLOR_BLUE         "\033[0;32;34m" 
#define COLOR_LIGHT_BLUE   "\033[1;34m" 
#define COLOR_DARY_GRAY    "\033[1;30m" 
#define COLOR_CYAN         "\033[0;36m" 
#define COLOR_LIGHT_CYAN   "\033[1;36m" 
#define COLOR_PURPLE       "\033[0;35m" 
#define COLOR_LIGHT_PURPLE "\033[1;35m" 
#define COLOR_BROWN        "\033[0;33m" 
#define COLOR_YELLOW       "\033[1;33m" 
#define COLOR_LIGHT_GRAY   "\033[0;37m" 
#define COLOR_WHITE        "\033[1;37m"
void logInfo(const char *color, const char*file, int line, const char* fmt, ...);

#define LOGW(fmt, ...) printf("%s", COLOR_PURPLE);\
	printf("[%s:%d]:", __FILE__, __LINE__);\
	printf(fmt, ##__VA_ARGS__);\
	printf("%s", COLOR_NONE);

    

#define LOGD(fmt, ...) printf("%s", COLOR_YELLOW);\
	printf("[%s:%d]:", __FILE__, __LINE__);\
	printf(fmt, ##__VA_ARGS__);\
	printf("%s", COLOR_NONE);

    
#define LOGI(fmt, ...) printf("%s", COLOR_GREEN);\
	printf("[%s:%d]:", __FILE__, __LINE__);\
	printf(fmt, ##__VA_ARGS__);\
	printf("%s", COLOR_NONE);
    
	
#define LOGE(fmt, ...) printf("%s", COLOR_RED);\
		printf("[%s:%d]:", __FILE__, __LINE__);\
		printf(fmt, ##__VA_ARGS__);\
		printf("%s", COLOR_NONE);



#endif
