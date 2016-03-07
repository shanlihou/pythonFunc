#include <stdio.h>
#include <stdlib.h>
#include <sys/epoll.h>
#include <errno.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netdb.h>
#include <fcntl.h>
#include <string.h>
#include "session.h"
#define MAX_EPOLL_SIZE 1024
#define MAX_EVENTS 64

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
int findHostPort()
{
	return 0;
}
int main()
{
	int epoll_fd = epoll_create(MAX_EPOLL_SIZE);
	int ret = -1;
	struct epoll_event event, *events = NULL;
	int server_len;
	int server_fd = -1;
	struct sockaddr_in server_address;
	if (epoll_fd == -1)
	{
		printf("create epoll failed");
		return 0;
	}
	server_fd = socket(AF_INET, SOCK_STREAM, 0);
	server_address.sin_family = AF_INET;
	server_address.sin_addr.s_addr = htonl(INADDR_ANY);
	server_address.sin_port = htons(9527);
	server_len = sizeof(server_address);
	bind(server_fd, (struct sockaddr *)&server_address, server_len);
	set_non_block(server_fd);

	listen(server_fd, 5);

	event.data.fd = server_fd;
	event.events = EPOLLIN | EPOLLET;

	ret = epoll_ctl(epoll_fd, EPOLL_CTL_ADD, server_fd, &event);
	if (ret == -1)
	{
		printf("ctrl failed");
		goto exit;
	}

	events = calloc(MAX_EVENTS, sizeof(event));
	while(1)
	{
		int n, i;
		n = epoll_wait(epoll_fd, events, MAX_EVENTS, -1);
		for (i = 0; i < n; i++)
		{
			printf("has fd\n");
			if((events[i].events & EPOLLERR)
				|| (events[i].events & EPOLLHUP)
				|| (!(events[i].events & EPOLLIN)))
			{
				printf("events error");
				close(events[i].data.fd);
				continue;
			}
			else if(server_fd == events[i].data.fd)
			{
				while(1)
				{
					struct sockaddr in_addr;
					socklen_t in_len;
					int client_fd;
					session *sess;
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
					
					sess = sess_new();
					sess->fd = client_fd;
					ret = sess_add(sess);
					if (ret == -1)
					{
						printf("add sess failed\n");
					}

					if (ret == -1)
					{
						printf("add client failed!\n");
					}
				}
			}
			else if (events[i].events == EPOLLIN)
			{//message in 
				int done = 0;
				session *sess = sess_get(events[i].data.fd);
				if (sess == NULL)
				{
					printf("null sess get\n");
				}
				while(1)
				{
					ssize_t count;
					char buf[512];
					printf("start read \n");
					count = read(events[i].data.fd, buf, sizeof(buf));
					if (count == -1)
					{
						if (errno == EAGAIN)
						{
							printf("read finish");
							done = 1;
						}
						break;
					}
					else if (count == 0)
					{
						done = 1;
						break;
					}
					str_nadd(sess->p_send, buf, count);
					ret = write(1, buf, count);
					if (ret == -1)
					{
						printf("write 1 failed");
					}
					printf("finish read \n");
				}
				if (done)
				{
					printf("close fd:%d", events[i].data.fd);
					close(events[i].data.fd);
				}
			}
		}
	}

exit:	
	if (events != NULL)
	{
		free(events);
	}
	sess_tree_free();
	close(epoll_fd);
	return 0;
}
