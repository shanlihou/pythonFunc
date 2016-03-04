#include <stdio.h>
#include <stdlib.h>
#include "rb_tree.h"

int main()
{
	rb_node *head = NULL;
	rb_node *ins = NULL;
	int i, ret;
	int count = 0;
	int delete;
	init_rb_tree();
	
	for (i = 0; i < 1000; i++)
	{
		srand(i);
		ins = new_tree_node();
		ins->key = rand() % 1000;
		printf("%d ", ins->key);
		ret = tree_insert(&head, ins);
		if (ret == -1)
		{
			free(ins);
		}else
		{
			count++;
			/*
			ret = print_tree(head, 0);
			printf("count is :%d\n", count);
			printf("size:%d\n\n", ret);*/
			if (tree_count(head) != count)
			{
				printf("wrong number\n");
				abort();
			}
			tree_start(head, 0, TREE_RED);
		}
	}

	printf("\n\n\ndelete:\n");
	for (i = 0; i < 1000; i++)
	{
		srand(i);
		delete = rand() % 1000;
		printf("%d ", delete);
		ins = tree_delete(&head, delete);
		if (ins != NULL)
		{
			count--;
			if (tree_count(head) != count)
			{
				printf("wrong number\n");
				abort();
			}
			/*
			display_tree(head);
			printf("\nend\n\n\n");
			*/
			tree_start(head, 0, TREE_RED);
			free(ins);
		}else
		{
			printf("not has:%d\n", delete);
		}
	}
	
	while(1)
	{
		scanf("%d", &delete);
		getchar();
		printf("d:%d\n", delete);
		ins = tree_delete(&head, delete);
		if (ins == NULL)
		{
			printf("not find:%d\n", ins->key);
		}else
		{
			printf("find ins and delete it\n");
			count--;
			free(ins);
		}
		ret = print_tree(head, 0);
		printf("count is :%d\n", count);
		printf("size:%d\n\n", ret);
	}
	tree_free(head, NULL);
	return 0;
}
