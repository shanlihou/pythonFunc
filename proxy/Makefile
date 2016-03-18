all:test_rb proxy
test_rb:test_rb.o rb_tree.o
	cc -g -Wall -o test_rb test_rb.o rb_tree.o
proxy:proxy.o rb_tree.o session.o str.o kmp.o log_info.o
	cc -g -Wall -o proxy proxy.o rb_tree.o session.o str.o kmp.o log_info.o  -lpthread
proxy.o:proxy.c session.h kmp.h log_info.h
	cc -g -Wall -c proxy.c -lpthread
test_rb.o:test_rb.c rb_tree.h
	cc -g -Wall -c test_rb.c
rb_tree.o:rb_tree.c rb_tree.h
	cc -g -Wall -c rb_tree.c
session.o:session.c str.h session.h rb_tree.h log_info.h kmp.h
	cc -g -Wall -c session.c
str.o:str.c str.h log_info.h kmp.h
	cc -g -Wall -c str.c
kmp.o:kmp.c kmp.h
	cc -g -Wall -c kmp.c
log_info.o:log_info.c log_info.h
	cc -g -Wall -c log_info.c

clean:
	rm *.o proxy
