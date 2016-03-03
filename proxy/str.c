#include <str.h>

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

	if (*str == NULL)
	{
		return str_assign(str, buf);
	}else if ((*str)->p == NULL)
	{
		return str_assgin(str, buf);
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
	str->p = -1;
	free(str);
	return 0;
}
