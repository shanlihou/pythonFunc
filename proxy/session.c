#include <stdlib.h>
#include <stdio.h>
#include "session.h"
#include "rb_tree.h"

rb_node *sess_head = NULL;

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
	free((session *)temp);
	return 0;
}

int sess_tree_free()
{
	tree_free(sess_head, sess_free);
	sess_head = NULL;
	return 0;
}
