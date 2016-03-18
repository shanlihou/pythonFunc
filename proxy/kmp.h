#ifndef _KMP_H_
#define _KMP_H_
#define KMP_MAX 2
#include <stdio.h>
#define STR_HOST "Host:"
#define STR_ENTER "\r\n"

typedef enum _KMP_NUM_
{
	KMP_HOST = 0,
	KMP_ENTER
}KMP_NUM;
typedef struct 
{
	char *pattern;
	size_t length;
	unsigned int *next;
}st_kmp;
int init_kmp_table(st_kmp **table);
int kmp_free(st_kmp *kmp);
st_kmp *init_kmp(const char *str);
int free_kmp_table(st_kmp **table);
inline void build_next(const char* pattern, size_t length, unsigned int* next);
unsigned int kmp(const char* text, size_t text_length, st_kmp *kmp);
#endif