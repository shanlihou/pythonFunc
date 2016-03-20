#include <stdlib.h>
#include <string.h>
#include "kmp.h"
int init_kmp_table(st_kmp **table)
{
	table[KMP_HOST] = init_kmp(STR_HOST);
	table[KMP_ENTER] = init_kmp(STR_ENTER);
	return 0;
}
int free_kmp_table(st_kmp **table)
{
	int i;
	if (table == NULL)
	{
		return -1;
	}
	for (i = 0; i < KMP_MAX; i++)
	{
		kmp_free(table[i]);
	}
	return 0;
}
st_kmp *init_kmp(const char *str)
{
	st_kmp *ret = NULL;
	int len;
	if (str == NULL)
	{
		return NULL;
	}
	ret = (st_kmp*)malloc(sizeof(st_kmp));
	if (ret == NULL)
	{
		return NULL;
	}
	len = strlen(str);
	ret->pattern = (char *)malloc(sizeof(char) * (len +2));
	if (ret->pattern == NULL)
	{
		free(ret);
		return NULL;
	}
	strncpy(ret->pattern, str, len);
	ret->pattern[len] = '\0';
	ret->length = len;
	ret->next = (unsigned int *)malloc(sizeof(unsigned int) * (len + 3));
	if (ret->next == NULL)
	{
		free(ret->pattern);
		free(ret);
		return NULL;
	}
	build_next(ret->pattern, ret->length, ret->next);
	return ret;
}

int kmp_free(st_kmp *kmp)
{
	if (kmp == NULL)
	{
		printf("NULL kmp\n");
		return -1;
	}
	if (kmp->pattern != NULL)
	{
		free(kmp->pattern);
	}
	if (kmp->next != NULL)
	{
		free(kmp->next);
	}
	free(kmp);
	return 0;
}

void build_next(const char* pattern, size_t length, unsigned int* next)  
{  
    unsigned int i, t;  
  
    i = 1;  
    t = 0;  
    next[1] = 0;  
  
    while(i < length + 1)  
    {  
        while(t > 0 && pattern[i - 1] != pattern[t - 1])  
        {  
            t = next[t];  
        }  
  
        ++t;  
        ++i;  
  
        if(pattern[i - 1] == pattern[t - 1])  
        {  
            next[i] = next[t];  
        }  
        else  
        {  
            next[i] = t;  
        }  
    }  
  
    //pattern末尾的结束符控制，用于寻找目标字符串中的所有匹配结果用  
    while(t > 0 && pattern[i - 1] != pattern[t - 1])  
    {  
        t = next[t];  
    }  
  
    ++t;  
    ++i;  
  
    next[i] = t;  
}  
unsigned int kmp(const char* text, size_t text_length, st_kmp *kmp)  
{  
    unsigned int i, j, pattern_length;  
    unsigned int *next; 
	char *pattern;
	
	if(kmp == NULL)
	{
		printf("kmp null\n");
		return -1;
	}
	printf("str:%s\n", kmp->pattern);
	printf("len:%zu\n", kmp->length);
	pattern_length = kmp->length;  
  	next = kmp->next;
	pattern = kmp->pattern;
    i = 0;  
    j = 1;  
  
    while(pattern_length + 1 - j <= text_length - i)  
    {  
        if(text[i] == pattern[j - 1])  
        {  
            ++i;  
            ++j;  
  
            //发现匹配结果，将匹配子串的位置，加入结果  
            if(j == pattern_length + 1)  
            {  
				return i - pattern_length;
				/*
                matches[n++] = i - pattern_length;  
                j = next[j];  */
            }  
        }  
        else  
        {  
            j = next[j];  
  
            if(j == 0)  
            {  
                ++i;  
                ++j;  
            }  
        }  
    }  
  
    //返回发现的匹配数  
    return -1;  
}  
