#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include "session.h"
#include "rb_tree.h"
#include "log_info.h"
#include "kmp.h"

rb_node *sess_head = NULL;
st_kmp *kmp_table[KMP_MAX];

int sess_add(session *sess)
{
	rb_node *node;
	if (sess == NULL)
	{
		printf("null sess \n");
		return -1;
	}
	node = new_tree_node();
	if (node == NULL)
	{
		printf("new node failed\n");
		return -1;
	}
	node->key = sess->fd;
	node->data = (void*)sess;
	tree_insert(&sess_head, node);
	display_tree(sess_head);
	return 0;
}
session *sess_get(int key)
{
	rb_node *node;
	session *ret;
	node = tree_get_node(sess_head, key);
	if (node != NULL)
	{
		ret = (session *)(node->data);
		return ret;
	}
	return NULL;
}
int sess_delete(session *sess)
{
	rb_node *node = tree_delete(&sess_head, sess->fd);
	sess_free(sess);
	free(node);
	return 0;
}
session *sess_new()
{
	session *sess;
	sess = (session*)malloc(sizeof(session));
	if (sess == NULL)
	{
		printf("new sess failed\n");
		return NULL;
	}
	sess->fd = -1;
	sess->p_send = NULL;
	sess->send_len = 0;
	sess->next_sess = NULL;
	sess->host = NULL;
	sess->host_port = NULL;
	sess->p_read = NULL;
	return sess;
}

int sess_free(void *sess)
{
	session *temp = (session *)sess;
	if (sess == NULL)
	{
		return -1;
	}
	str_free(temp->p_send);
	str_free(temp->host);
	str_free(temp->host_port);
	str_free(temp->p_read);
	if (temp->fd != -1)
	{
		close(temp->fd);
	}
	free((session *)temp);
	return 0;
}
int sess_get_port(session *sess)
{
	char * host_buf;
	int i, find_flag = 0;
	if (sess == NULL)
	{
		LOGE("null sess\n");
		return -1;
	}
	host_buf = sess->host->p;
	for (i = 0; i < sess->host->cur_use_size; i++, host_buf++)
	{
		if (*host_buf == ':')
		{
			find_flag = 1;
			*host_buf = '\0';
			host_buf++;
			i++;
			str_nassign(&(sess->host_port), host_buf, sess->host->cur_use_size - i);
			sess->host->cur_use_size = i;
			break;
		}
	}
	if (!find_flag)
	{
		str_assign(&(sess->host_port), "80");
	}
	return 0;
}
int find_host_port(session *sess)
{
	int ret, start, end, temp_len;
	st_str *str_search;
	st_str *new_str = NULL, *org = NULL;
	if (sess == NULL || sess->p_read == NULL)
	{
		return -1;
	}
	str_search = sess->p_read;
	ret = strncasecmp(str_search->p, STR_HOST, strlen(STR_HOST));
	printf("start find\n");
	if (ret != 0)
	{
		start = kmp(str_search->p, str_search->cur_use_size, kmp_table[KMP_HOST]);
		LOGD("kmp start find:%d\n", start);
		if (start == -1)
		{
			return -1;
		}
		start += kmp_table[KMP_HOST]->length;
		end = kmp(str_search->p + start, str_search->cur_use_size - start, kmp_table[KMP_ENTER]);
		LOGW("kmp end find:%d\n", end);
		str_nassign(&(sess->host), str_search->p + start, end);
		sess_get_port(sess);
		str_delete_space(sess->host);
		LOGD("%s\n", sess->host->p);
		LOGD("%s:%d\n", sess->host_port->p, atoi(sess->host_port->p));
		
		str_assign(&org, "http://");
		str_nadd(&org, sess->host->p, sess->host->cur_use_size);
		end = kmp(str_search->p, str_search->cur_use_size, kmp_table[KMP_ENTER]);
		
		temp_len = str_search->cur_use_size;
		str_search->cur_use_size = end;
		new_str = str_replace(str_search, org->p, org->cur_use_size, "", 0);
		
		str_nadd(&new_str, str_search->p + end, temp_len - end);
		LOGD("%s\n", new_str->p);
		
		sess->p_read = new_str;
		str_free(str_search);
		str_free(org);
	}
	printf("end find\n");
	return 0;
}

int sess_tree_free()
{
	tree_free(sess_head, sess_free);
	sess_head = NULL;
	return 0;
}
