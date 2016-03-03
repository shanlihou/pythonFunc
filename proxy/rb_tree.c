#include "rb_tree.h"
#include <stdlib.h>
#include <stdio.h>
int left_rotate(rb_node *node)
{
	rb_node *temp, *right;
	if (node == NULL)
	{
		printf("null tree node\n");
		return -1;
	}else if (node->right == NULL)
	{
		printf("null right node \n");
		return -1;
	}

	temp = node->father;
	right = node->right;
	if (temp != NULL)
	{
		if (temp->left == node)
		{
			temp->left = right;
		}else
		{
			temp->right = right;
		}
	}
	right->father = temp;
	node->right = right->left;
	if (right->left != NULL)
	{
		right->left->father = node;
	}
	right->left = node;
	node->father = right;
	return 0;
}

int right_rotate(rb_node *node)
{
	rb_node *temp, *left;
	if (node == NULL)
	{
		printf("null tree node\n");
		return -1;
	}else if (node->left == NULL)
	{
		printf("null left node \n");
		return -1;
	}

	temp = node->father;
	left = node->left;
	if (temp != NULL)
	{
		if (temp->left == node)
		{
			temp->left = left;
		}else
		{
			temp->right = left;
		}
	}
	left->father = temp;
	node->left = left->right;
	if (left->right != NULL)
	{
		left->right->father = node;
	}
	left->right = node;
	node->father = left;
	return 0;
}

int tree_fix(rb_node **head, rb_node *node)
{
	rb_node *father, *uncle;
	if (node == NULL)
	{
		printf("fix but node is NULL\n");
		return -1;
	}
	father = node->father;
	while(father != NULL && father->color == TREE_RED)
	{
		rb_node *g_father = father->father;
		if (g_father == NULL)
		{
			printf("g father is null?root is red?\n");
			break;
		}

		if (g_father->left == father)
		{
			uncle = g_father->right;
			if (uncle != NULL && uncle->color == TREE_RED)
			{
				uncle->color = TREE_BLACK;
				father->color = TREE_BLACK;
				g_father->color = TREE_RED;
				node = g_father;
				father = node->father;
				continue;
			}else if(node == father->right)
			{
				node = father;
				left_rotate(node);
			}
			node->father->color = TREE_BLACK;
			g_father->color = TREE_RED;
			right_rotate(g_father);
			node = g_father->father;
			break;
		}else
		{
			uncle = g_father->left;
			if (uncle != NULL && uncle->color == TREE_RED)
			{
				uncle->color = TREE_BLACK;
				father->color = TREE_BLACK;
				g_father->color = TREE_RED;
				node = g_father;
				father = node->father;
				continue;
			}else if(node == father->left)
			{
				node = father;
				right_rotate(node);
			}
			node->father->color = TREE_BLACK;
			g_father->color = TREE_RED;
			left_rotate(g_father);
			node = g_father->father;
			break;
		}
	}
	if (node->father == NULL)
	{
		*head = node;
		(*head)->color = TREE_BLACK;
	}
	return 0;
}
rb_node *tree_get_node(rb_node *head, int key)
{
	rb_ndoe *temp = head;
	if (head == NULL)
	{
		printf("null tree\n");
		return NULL;
	}
	while (temp != NULL)
	{
		if (key > temp->key)
		{
			temp = temp->right;
		}else if(key < temp->key)
		{
			temp = temp->left;
		}else
		{
			return temp;
		}
	}
	return NULL;
}
int tree_insert(rb_node **head, rb_node *node)
{	
	rb_node *temp;
	if (head == NULL || node == NULL)
	{
		printf("null node insert\n");
		return -1;
	}
	node->color = TREE_RED;

	temp = *head;
	if (temp == NULL)
	{
		*head = node;
		node->color = TREE_BLACK;
		node->father = NULL;
		node->left = NULL;
		node->right = NULL;
		printf("not has head\n");
		return 0;
	}

	while (1)
	{
		if (node->key > temp->key)
		{
			if (temp->right == NULL)
			{
				temp->right = node;
				node->father = temp;
				break;
			}else
			{
				temp = temp->right;
			}

		}else if(node->key < temp->key)
		{
			if (temp->left == NULL)
			{
				temp->left = node;
				node->father = temp;
				break;
			}else
			{
				temp = temp->left;
			}
		}else
		{
			printf("has this key;\n");
			return -1;
		}
	}
	tree_fix(head, node);
	return 0;
}

rb_node *new_tree_node()
{
	rb_node *node = (rb_node *)malloc(sizeof(rb_node));
	if (node == NULL)
	{
		printf("malloc node failed\n");
		return NULL;
	}
	node->left = NULL;
	node->right = NULL;
	node->father = NULL;
	node->data = NULL;
	node->color = TREE_RED;
	return node;
}
int print_wrong_father(rb_node *node, int deep)
{
	rb_node *father = node->father;
	if (father != NULL)
	{
		if (father->left != node && father->right != node)
		{
			printf("it is not my father!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n");
		}
	}else if(deep != 0)
	{
		printf("i'm not root!!!!!\n");
	}
	return 0;
}

int print_tree(rb_node *head, int deep)
{
	int size = 1;
	if (head == NULL)
	{
		return 0;
	}
	size += print_tree(head->left, deep + 1);
	if (head->father != NULL)
	{
		printf("tree key:%d, father:%d, color:%d, deep:%d\n", head->key, head->father->key, head->color, deep);
	}else
	{
		printf("tree key:%d, color:%d, deep:%d\n", head->key, head->color, deep);
	}
	print_wrong_father(head, deep);
	size += print_tree(head->right, deep + 1);
	return size;
}


int tree_free(rb_node *head, int (*fun)(void *arg))
{
	if (head == NULL)
	{
		return 0;
	}
	tree_free(head->left);
	tree_free(head->right);
	if (fun != NULL)
	{
		(*fun)(head->data);
	}
	free(head);
	return 0;
}
