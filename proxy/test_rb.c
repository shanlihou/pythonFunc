#include <stdio.h>
#include <stdlib.h>
#include "rb_tree.h"

int main()
{
	rb_node *head = NULL;
	rb_node *ins = NULL;
	int i, ret;
	
	for (i = 0; i < 100; i++)
	{
		srand(i);
		ins = new_tree_node();
		ins->key = rand() % 100;
		printf("%d ", ins->key);
		ret = tree_insert(&head, ins);
		if (ret == -1)
		{
			free(ins);
		}else
		{
			ret = print_tree(head, 0);
			printf("size:%d\n\n", ret);
		}
	}
	tree_free(head);
	head = NULL;
	while(1)
	{
		int add, ret;
		scanf("%d", &add);
		getchar();
		printf("d:%d\n", add);
		ins = new_tree_node();
		ins->key = add;
		ret = tree_insert(&head, ins);
		if (ret == -1)
		{
			printf("free:%d\n", ins->key);
			free(ins);
		}
		print_tree(head, 0);
	}
	tree_free(head);
	return 0;
}
