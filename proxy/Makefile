test_rb:test_rb.o rb_tree.o
	cc -g -Wall -o test_rb test_rb.o rb_tree.o
test_rb.o:test_rb.c rb_tree.h
	cc -g -Wall -g -c test_rb.c
rb_tree.o:rb_tree.c rb_tree.h
	cc -g -Wall -c rb_tree.c
