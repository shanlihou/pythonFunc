#ifndef _STR_H_
#define _STR_H_
typedef struct
{
	char *p;
	int max_size;
	int cur_use_size;
}st_str;

int str_nassign(st_str** str, const char *buf, int buf_len);

int str_assign(st_str **str, const char *buf);
int str_delete_space(st_str *str);

int str_add(st_str** str, const char* buf);
int str_nadd(st_str** str, const char* buf, int len);
st_str *str_replace(st_str *str, const char *org, int org_len, const char *buf, int buf_len);

int str_free(st_str* str);
#endif
