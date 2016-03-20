#include <stdio.h>
#include <signal.h>  
#include <stdlib.h>
#include <sys/epoll.h>
#include <errno.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <pthread.h>
#include <fcntl.h>
#include <string.h>
#include "session.h"
#include "kmp.h"
#include "log_info.h"
#define MAX_EPOLL_SIZE 1024
#define MAX_EVENTS 64
#define EPOLL_TIMEOUT 2000

extern st_kmp *kmp_table[KMP_MAX];
static int exit_flag = 0;
int epoll_fd = -1;

int set_non_block(int fd)
{
	int flags, ret;
	flags = fcntl(fd, F_GETFL, 0);

	if (flags == -1)
	{
		printf("cntl failed!\n");
		return -1;
	}
	flags |= O_NONBLOCK;
	ret = fcntl(fd, F_SETFL, flags);
	if (ret == -1)
	{
		printf("cntl failed!\n");
		return -1;
	}
	return 0;
}

void *connect_sess(void *arg)
{
	session *next_sess;
	session *sess = (session *)arg;
	int ret;
	char IPc[20];
	struct epoll_event event;
	struct sockaddr_in address;
    struct hostent *host;
	if (sess == NULL || sess->host == NULL)
	{
		LOGE("null sess\n");
		return NULL;
	}
	next_sess = sess_new();
	if (next_sess == NULL)
	{
		LOGE("null next\n");
		return NULL;
	}
	host = gethostbyname(sess->host->p);
	if (host == NULL)
	{
		herror("");
		goto failed;
	}
	inet_ntop(AF_INET, (void *)host->h_addr_list[0], IPc, 16);
	LOGD("host ip is :%s\n", IPc);
	next_sess->fd = socket(AF_INET, SOCK_STREAM, 0);
	address.sin_family = AF_INET;
	address.sin_addr.s_addr = inet_addr(IPc);
	address.sin_port = htons(atoi(sess->host_port->p));

	ret = connect(next_sess->fd, (struct sockaddr *)&address, sizeof(address));
	if (ret == -1)
	{
		perror("");
		goto failed;
	}
	ret = set_non_block(next_sess->fd);
	if (ret == -1)
	{
		LOGE("set non block failed\n");
		goto failed;
	}
	sess->next_sess = next_sess;
	next_sess->p_send = sess->p_read;
	sess->p_read = NULL;
	next_sess->next_sess = sess;
	ret = sess_add(next_sess);
	if (ret == -1)
	{
		LOGE("add sess failed\n");
		goto failed;
	}
	LOGD("add fd:%d\n", next_sess->fd);

	event.data.fd = next_sess->fd;
	event.events = EPOLLIN | EPOLLET | EPOLLOUT;
	ret = epoll_ctl(epoll_fd, EPOLL_CTL_ADD, next_sess->fd, &event);
	return NULL;
failed:
	sess_free(next_sess);
	sess->next_sess = NULL;
	clear_session(sess);
	return NULL;
}
void my_handler(int s){
	printf("Caught signal %d\n",s);  
	if (s == 2)
		exit_flag = 1;
}  
int clear_session(session *sess)
{ 
	struct epoll_event event;
	session *next_sess = NULL;
	if (sess == NULL)
	{
		LOGE("null sess\n");
		return -1;
	}
	next_sess = sess->next_sess;
	event.data.fd = sess->fd;
	epoll_ctl(epoll_fd, EPOLL_CTL_DEL, sess->fd, &event);
	sess_delete(sess);

	if (next_sess != NULL)
	{
		event.data.fd = next_sess->fd;
		epoll_ctl(epoll_fd, EPOLL_CTL_DEL, next_sess->fd, &event);
		sess_delete(next_sess);
	}
	return 0;
}

int process_data(session *sess)
{
	struct epoll_event event;
	pthread_t thread;
	pthread_attr_t attr;
	int ret;
	if (sess == NULL || sess->p_read == NULL)
	{
		LOGE("null sess\n");
		return -1;
	}
	LOGD("process fd:%d, size:%d\n", sess->fd, sess->p_read->cur_use_size);
	if (strncasecmp(sess->p_read->p, "CONNECT", strlen("CONNECT")) == 0)
	{
		LOGD("CONNECT sess\n");
	}else if (strncasecmp(sess->p_read->p, "GET", strlen("GET")) == 0)
	{

		LOGD("GET sess\n");

	}else if (strncasecmp(sess->p_read->p, "PUT", strlen("PUT")) == 0)
	{
		LOGD("PUT sess\n");

	}else if (strncasecmp(sess->p_read->p, "POST", strlen("POST")) == 0)
	{
		LOGD("POST sess\n");
	}

	
	if (sess->next_sess != NULL)
	{
		session *next_sess = sess->next_sess;
		str_nadd(&(next_sess->p_send), sess->p_read->p, sess->p_read->cur_use_size);
		str_free(sess->p_read);
		sess->p_read = NULL;
		event.data.fd = next_sess->fd;
		event.events = EPOLLET | EPOLLIN | EPOLLOUT;
		ret = epoll_ctl(epoll_fd, EPOLL_CTL_MOD, next_sess->fd, &event);
		return 0;
	}
	
	ret = find_host_port(sess);
	if(ret == -1)
	{
		return 0;;
	}
	event.data.fd = sess->fd;
	event.events = EPOLLET;
	ret = epoll_ctl(epoll_fd, EPOLL_CTL_MOD, sess->fd, &event);
	pthread_attr_init (&attr);
	pthread_attr_setdetachstate (&attr, PTHREAD_CREATE_DETACHED);
	pthread_create(&thread, &attr, connect_sess, (session *)sess);
	pthread_attr_destroy (&attr);
	return 0;

}

int main()
{
	int ret = -1;
	struct epoll_event event, *events = NULL;
	int server_len;
	int server_fd = -1;
	session *sess = NULL;
	struct sockaddr_in server_address;
	struct sigaction sigIntHandler;  
	epoll_fd = epoll_create(MAX_EPOLL_SIZE);
	if (epoll_fd == -1)
	{
		printf("create epoll failed");
		return 0;
	}
	LOGD("hup:%d err:%d in:%d out:%d\n", EPOLLHUP, EPOLLERR, EPOLLIN, EPOLLOUT);
	sigIntHandler.sa_handler = my_handler;  
	sigemptyset(&sigIntHandler.sa_mask);  
	sigIntHandler.sa_flags = 0;  

	sigaction(SIGINT, &sigIntHandler, NULL);
	
	init_kmp_table(kmp_table);
	server_fd = socket(AF_INET, SOCK_STREAM, 0);
	server_address.sin_family = AF_INET;
	server_address.sin_addr.s_addr = htonl(INADDR_ANY);
	server_address.sin_port = htons(9527);
	server_len = sizeof(server_address);
	ret = bind(server_fd, (struct sockaddr *)&server_address, server_len);
	if (ret == -1)
	{
		perror("");
		LOGE("bind failed\n");
		goto exit;
	}
	set_non_block(server_fd);

	ret = listen(server_fd, 5);
	if (ret == -1)
	{
		LOGE("listen failed\n");
		goto exit;
	}

	event.data.fd = server_fd;
	event.events = EPOLLIN | EPOLLET;

	ret = epoll_ctl(epoll_fd, EPOLL_CTL_ADD, server_fd, &event);
	if (ret == -1)
	{
		printf("ctrl failed");
		goto exit;
	}
	printf("server start!\n");
	events = calloc(MAX_EVENTS, sizeof(event));
	while(1)
	{
		int n, i;
		n = epoll_wait(epoll_fd, events, MAX_EVENTS, EPOLL_TIMEOUT);
		if (exit_flag == 1)
		{
			LOGI("will exit\n");
			break;
		}
		for (i = 0; i < n; i++)
		{
			LOGD("has fd:%d, evnets:%d\n", events[i].data.fd, events[i].events);
			
			if(server_fd == events[i].data.fd)
			{
				while(1)
				{
					struct sockaddr in_addr;
					socklen_t in_len;
					int client_fd; 
					char host_info[NI_MAXHOST], serv_info[NI_MAXSERV];

					in_len = sizeof(in_addr);
					client_fd = accept(server_fd, &in_addr, &in_len);
					if (client_fd == -1)
					{
						if ((errno == EAGAIN)
							|| (errno == EWOULDBLOCK))
						{
							break;
						}
						else
						{
							printf("error accept");
							break;
						}
					}

					ret = getnameinfo(&in_addr, in_len, host_info,
						sizeof(host_info), serv_info, sizeof(serv_info),
						NI_NUMERICHOST | NI_NUMERICSERV);
					if (ret == 0)
					{
						printf("fd:%d host is:%s, serv is :%s\n", client_fd, host_info, serv_info);
					}
					ret = set_non_block(client_fd);
					if (ret == -1)
					{
						printf("set non block failed\n");
					}

					event.data.fd = client_fd;
					event.events = EPOLLIN | EPOLLET;
					ret = epoll_ctl(epoll_fd, EPOLL_CTL_ADD, client_fd, &event);
					if (ret == -1)
					{
						printf("add client failed!\n");
					}
					
					sess = sess_new();
					sess->fd = client_fd;
					ret = sess_add(sess);
					if (ret == -1)
					{
						LOGE("add sess failed\n");
					}
					LOGD("add sess:%d\n", sess->fd);
				}
			}
			else if (events[i].events == EPOLLIN)
			{//message in 
				int done = 0;
				sess = sess_get(events[i].data.fd);
				if (sess == NULL)
				{
					printf("null sess get\n");
					continue;
				}
				LOGD("start read :%d\n", events[i].data.fd);
				while(1)
				{
					ssize_t count;
					char buf[512];
					count = read(events[i].data.fd, buf, sizeof(buf));
					if (count == -1)
					{
						if (errno != EAGAIN)
						{
							LOGW("read finish not eagain\n");
						}else
						{
							LOGW("read finish eagain\n");
						}
						done = 1;
						break;
					}
					else if (count == 0)
					{
						done = 2;
						LOGW("count == 0\n");
						break;
					}
					str_nadd(&(sess->p_read), buf, count);
//					ret = write(1, buf, count);
					printf("finish read \n");
				}
				if (done == 1)
				{
					process_data(sess);
				}else if(done == 2)
				{
					clear_session(sess);
				}
			}
			else if((events[i].events & EPOLLERR)
				|| (events[i].events & EPOLLHUP)
				|| (!(events[i].events & EPOLLOUT)))
			{
				LOGE("events error\n");
				sess = sess_get(events[i].data.fd);
				if (sess != NULL)
				{
					clear_session(sess);
				}else
				{
					LOGE("not find sess\n");
					close(events[i].data.fd);
				}
				continue;
			}
			else if (events[i].events == EPOLLOUT)
			{
				int cur = 0, count;
				st_str *send;
				sess = sess_get(events[i].data.fd);
				if (sess == NULL)
				{
					LOGE("get null sess\n");
					continue;
				}
				if (sess->p_send == NULL || sess->p_send->cur_use_size == 0)
				{
					LOGE("nothing to send\n");
					continue;
				}
				LOGD("ready to write:%d, size:%d\n", events[i].data.fd, sess->p_send->cur_use_size);
				send = sess->p_send;
				while(cur < send->cur_use_size)
				{
					count = write(sess->fd, send->p + cur, send->cur_use_size - cur);
					if (count == -1)
					{
						LOGE("write error\n");
						break;
					}else if (count == send->cur_use_size - cur)
					{
						str_free(send);
						sess->p_send = NULL;
						LOGD("send finished\n");
						break;
					}
					cur += count;
				}
				event.data.fd = sess->fd;
				event.events = EPOLLET | EPOLLIN;
				ret = epoll_ctl(epoll_fd, EPOLL_CTL_MOD, sess->fd, &event);
			}
		}
	}

exit:	
	if (events != NULL)
	{
		free(events);
	}
	free_kmp_table(kmp_table);
	sess_tree_free();
	if (server_fd != -1)
	{
		LOGD("close server\n");
		close(server_fd);
	}
	if (epoll_fd != -1)
	{
		close(epoll_fd);
	}
	return 0;
}
