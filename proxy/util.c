#include "util.h"
#include "log_info.h"
int atoi(const char *str)
{
	int num = 0;
	int neg_flag = 0;
	int sp_flag = 0;
	if(str == NULL)
	{
		LOGE("null str\n");
		return 0;
	}
	
	while(*str != '\0')
	{
		if(!sp_flag)
		{
			if (*str == ' ' || *str == '\t' || *str == '\n')
			{
				continue;
			}else if(*str == '-')
			{
				neg_flag = 1;
				sp_flag = 1;
			}else if(*str > '9' || *str < '0')
			{
				LOGE("not number\n");
				return 0;
			}else
			{
				sp_flag = 1;
				num = *str - '0';
			}
		}else if(*str > '9' || *str < '0')
		{
			LOGE("not number\n");
			return 0;
		}else
		{
			num = num * 10 + (*str - '0');
		}
		str++;
	}
	if (neg_flag)
	{
		num = -num;
	}
	return num;
}
