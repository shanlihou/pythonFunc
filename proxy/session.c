#include "session.h"
#include "rb_tree.h"
#include "str.h"
#include <stdlib.h>

rb_node *sess_head = NULL;

int sess_add(session *sess)
{
	rb_ndoe *node;
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
	return sess;
}

int (*sess_free)(void *sess)
{
	free((session *)sess);
	return 0;
}

int sess_tree_free()
{
	tree_free(sess_head, sess_free);
	sess_head = NULL;
	return 0;
}
