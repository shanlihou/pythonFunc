#ifndef _SESSION_H_
#define _SESSION_H_

typedef struct _session
{
	int fd;
	struct _session *next_sess;
}session;
#endif
