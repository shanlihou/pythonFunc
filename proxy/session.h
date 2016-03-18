#ifndef _SESSION_H_
#define _SESSION_H_
#include "str.h"
typedef struct _session
{
	int fd;
	st_str *p_read;
	st_str *p_send;
	st_str *host;
	st_str *host_port;
	int send_len;
	struct _session *next_sess;
}session;

int sess_add(session *sess);
session *sess_get(int key);
int sess_delete(session *sess);

session *sess_new();

int sess_free(void *sess);

int sess_tree_free();

int sess_get_port(session *sess);
int find_host_port(session *sess);


#endif
