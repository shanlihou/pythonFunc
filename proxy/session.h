#ifndef _SESSION_H_
#define _SESSION_H_
#include "str.h"
typedef struct _session
{
	int fd;
	st_str *p_send;
	int send_len;
	struct _session *next_sess;
}session;

int sess_add(session *sess);
session *sess_get(int key);
session *sess_new();

int sess_free(void *sess);

int sess_tree_free();

#endif
