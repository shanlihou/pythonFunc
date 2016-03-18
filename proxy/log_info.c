#include "log_info.h"



void logInfo(const char* color, const char*file, int line, const char* fmt, ...)
{
	va_list ap; /* points to each unnamed arg in turn */
	int test;
	char buf[1024];
	char fileAndLine[256];
	snprintf(fileAndLine, 256, "[%s:%d]:", file, line);
	
	va_start(ap, fmt);
	sprintf(buf, fmt, ap);
	va_end(ap);
	va_start(ap, fmt);
	test = va_arg(ap, int);
	printf("test is :%d\n", test);
	va_end(ap);
	printf("%s", color);
	printf("%s", fileAndLine);
	printf("%s", buf);
	printf("%s", COLOR_NONE);
}
