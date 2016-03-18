#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "str.h"
#include "log_info.h"
#include "kmp.h"

int str_assign(st_str** str, const char *buf)
{
	int buf_len = 0;
	char *p_temp;
	if (str == NULL || buf == NULL)
	{
		printf("null pointer!\n");
		return -1;
	}
	buf_len = strlen(buf);
	if (buf_len == 0)
	{
		LOGE("zero size of buf\n");
		return -1;
	}
	if (*str == NULL)
	{
		*str = (st_str *)malloc(sizeof(st_str));
		if(*str == NULL)
		{
			printf("str malloc failed\n");
			return -1;
		}
		(*str)->max_size = (buf_len / 1024 + 1) * 1024;
		(*str)->cur_use_size = buf_len;
		(*str)->p = (char *)malloc(sizeof(char) * (*str)->max_size);
		if((*str)->p == NULL)
		{
			printf("*str p malloc failed\n");
			free(*str);
			*str = NULL;
			return -1;
		}
		strncpy((*str)->p, buf, buf_len);
		(*str)->p[buf_len] = 0;
	}else
	{
		if ((*str)->p == NULL)
		{
			(*str)->max_size = (buf_len / 1024 + 1) * 1024;
			(*str)->cur_use_size = buf_len;
			(*str)->p = (char *)malloc(sizeof(char) * (*str)->max_size);
			if((*str)->p == NULL)
			{
				printf("*str p malloc failed\n");
				free(*str);
				*str = NULL;
				return -1;
			}
		}else
		{
			if ((*str)->max_size <= buf_len)
			{
				(*str)->max_size = (buf_len / 1024 + 1) * 1024;
				p_temp = (*str)->p;
				(*str)->p = (char *)realloc(p_temp, sizeof(char) * (*str)->max_size);
				if ((*str)->p == NULL)
				{
					printf("*str p malloc failed\n");
					free(*str);
					*str = NULL;
					return -1;
				}
			}
			(*str)->cur_use_size = buf_len;
		}
		strncpy((*str)->p, buf, buf_len);
		(*str)->p[buf_len] = 0;
	}
	return 0;
}

int str_nassign(st_str** str, const char *buf, int buf_len)
{
	char *p_temp;
	if (str == NULL || buf == NULL || buf_len <= 0)
	{
		printf("null pointer!\n");
		return -1;
	}
	if (*str == NULL)
	{
		*str = (st_str *)malloc(sizeof(st_str));
		if(*str == NULL)
		{
			printf("str malloc failed\n");
			return -1;
		}
		(*str)->max_size = (buf_len / 1024 + 1) * 1024;
		(*str)->cur_use_size = buf_len;
		(*str)->p = (char *)malloc(sizeof(char) * (*str)->max_size);
		if((*str)->p == NULL)
		{
			printf("*str p malloc failed\n");
			free(*str);
			*str = NULL;
			return -1;
		}
		strncpy((*str)->p, buf, buf_len);
		(*str)->p[buf_len] = 0;
	}else
	{
		if ((*str)->p == NULL)
		{
			(*str)->max_size = (buf_len / 1024 + 1) * 1024;
			(*str)->cur_use_size = buf_len;
			(*str)->p = (char *)malloc(sizeof(char) * (*str)->max_size);
			if((*str)->p == NULL)
			{
				printf("*str p malloc failed\n");
				free(*str);
				*str = NULL;
				return -1;
			}
		}else
		{
			if ((*str)->max_size <= buf_len)
			{
				(*str)->max_size = (buf_len / 1024 + 1) * 1024;
				p_temp = (*str)->p;
				(*str)->p = (char *)realloc(p_temp, sizeof(char) * (*str)->max_size);
				if ((*str)->p == NULL)
				{
					printf("*str p malloc failed\n");
					free(*str);
					*str = NULL;
					return -1;
				}
			}
			(*str)->cur_use_size = buf_len;
		}
		strncpy((*str)->p, buf, buf_len);
		(*str)->p[buf_len] = 0;
	}
	return 0;
}

int str_add(st_str** str, const char* buf)
{
	int buf_len, new_use;
	char *p_temp;
	if (buf == NULL)
	{
		printf("buf is null\n");
		return -1;
	}
	buf_len = strlen(buf);

	if (*str == NULL || (*str)->p == NULL)
	{
		return str_assign(str, buf);
	}else
	{
		new_use = (*str)->cur_use_size + buf_len;
		if ((*str)->max_size <= new_use)
		{
			(*str)->max_size = (new_use / 1024 + 1) * 1024;
			p_temp = (*str)->p;
			(*str)->p = (char*)realloc(p_temp, sizeof(char) * (*str)->max_size);
			if ((*str)->p == NULL)
			{
				printf("*str p realloc failed\n");
				return -1;
			}
		}
		strncat((*str)->p + (*str)->cur_use_size, buf, buf_len);
		(*str)->p[new_use] = 0;
		(*str)->cur_use_size = new_use;
	}
	return 0;
}
int str_nadd(st_str** str, const char* buf, int len)
{
	int new_use;
	char *p_temp;
	if (str == NULL || buf == NULL || len <= 0)
	{
		printf("buf is null\n");
		return -1;
	}

	if (*str == NULL || (*str)->p == NULL)
	{
		return str_nassign(str, buf, len);
	}else
	{
		new_use = (*str)->cur_use_size + len;
		if ((*str)->max_size <= new_use)
		{
			(*str)->max_size = (new_use / 1024 + 1) * 1024;
			p_temp = (*str)->p;
			(*str)->p = (char*)realloc(p_temp, sizeof(char) * (*str)->max_size);
			if ((*str)->p == NULL)
			{
				printf("*str p realloc failed\n");
				return -1;
			}
		}
		strncat((*str)->p + (*str)->cur_use_size, buf, len);
		(*str)->p[new_use] = 0;
		(*str)->cur_use_size = new_use;
	}
	return 0;
}
int str_delete_space(st_str *str)
{
	char *p;
	int i, start, end;
	int flag = 0;
	if (str == NULL || str->p == NULL)
	{
		LOGE("str is NULL\n");
		return -1;
	}
	p = str->p;
	i = 0;
	start = 0;
	end = 0;
	while(i < str->cur_use_size)
	{
		if (!flag && (*p != ' ' && *p != '\n' && *p != '\t'))// not find disspace
		{
			flag = 1;
			start = i;
			end = i;
		}else if (flag == 1 && 
			(*p != ' ' && *p != '\n' && *p != '\t'))
		{
			end = i;
		}
		i++;
		p++;
	}
	LOGD("start sp is :%d\n", start);
	LOGD("end sp is :%d\n", end);
	str->cur_use_size = end + 1 - start;
	p = str->p;
	for (i = 0; i < str->cur_use_size; i++)
	{
		*p = *(p + start);
		p++;
	}
	*p = '\0';
	return 0;
}

st_str *str_replace(st_str *str, const char *org, int org_len, const char *buf, int buf_len)
{
	st_kmp *org_pat;
	st_str *ret = NULL;
	char *temp;
	int start, temp_len;
	if (str == NULL || str->p == NULL || org == NULL || buf == NULL)
	{
		return NULL;
	}
	org_pat = init_kmp(org);
	if (org_pat == NULL)
	{
		return NULL;
	}
	temp = str->p;
	temp_len = str->cur_use_size;
	do
	{
		start = kmp(temp, temp_len, org_pat);
		if (start == -1)
		{
			str_nadd(&ret, temp, temp_len);
			break;
		}else
		{
			str_nadd(&ret, temp, start);
			str_nadd(&ret, buf, buf_len);
			temp_len -= start + org_len;
			temp += start + org_len;
		}
	}while(temp_len > 0);
	return ret;
}

int str_free(st_str* str)
{
	if (str == NULL)
	{
		printf("str is null\n");
		return -1;
	}
	if (str->p == NULL)
	{
		printf("str.p is null\n");
		free(str);
		return -1;
	}
	free(str->p);
	str->p = NULL;
	free(str);
	return 0;
}
