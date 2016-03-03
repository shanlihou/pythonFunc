#ifndef _STR_H_
#define _STR_H_
typedef struct
{
	char *p;
	int max_size;
	int cur_use_size;
}st_str;

int str_assign(st_str **str, const char *buf);
int str_add(st_str** str, const char* buf);
int str_free(st_str* str);
#endif
