#include "rb_tree.h"
#include <stdlib.h>
#include <stdio.h>
static rb_node TREE_NIL;

#define NONE		 "\033[m" 
#define RED 		 "\033[0;32;31m"
#define DARY_GRAY    "\033[1;30m" 

int init_rb_tree()
{
	TREE_NIL.color = TREE_BLACK;
	TREE_NIL.father = NULL;
	TREE_NIL.key = -1;
	TREE_NIL.data = NULL;
	TREE_NIL.left = NULL;
	TREE_NIL.right = NULL;
	return 0;
}
int left_rotate(rb_node **head, rb_node *node)
{
	rb_node *right;
	if (node == NULL)
	{
		printf("null tree node\n");
		return -1;
	}else if (node->right == &TREE_NIL)
	{
		printf("null right node \n");
		return -1;
	}

	right = node->right;
	tree_transplant(head, node, right);
	
	node->right = right->left;
	if (right->left != &TREE_NIL)
	{
		right->left->father = node;
	}
	
	right->left = node;
	node->father = right;
	return 0;
}

int right_rotate(rb_node **head, rb_node *node)
{
	rb_node *left;
	if (node == NULL)
	{
		printf("null tree node\n");
		return -1;
	}else if (node->left == &TREE_NIL)
	{
		printf("null left node \n");
		return -1;
	}

	left = node->left;
	tree_transplant(head, node, left);
	
	node->left = left->right;
	if (left->right != &TREE_NIL)
	{
		left->right->father = node;
	}
	left->right = node;
	node->father = left;
	return 0;
}

int tree_insert_fix(rb_node **head, rb_node *node)
{
	rb_node *father, *uncle;
	if (node == NULL)
	{
		printf("fix but node is NULL\n");
		return -1;
	}
	father = node->father;
	while(father != &TREE_NIL && father->color == TREE_RED)
	{
		rb_node *g_father = father->father;
		if (g_father == &TREE_NIL)
		{
			printf("g father is null?root is red?\n");
			break;
		}

		if (g_father->left == father)
		{
			uncle = g_father->right;
			if (uncle != &TREE_NIL && uncle->color == TREE_RED)
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
				left_rotate(head, node);
			}
			node->father->color = TREE_BLACK;
			g_father->color = TREE_RED;
			right_rotate(head, g_father);
			node = g_father->father;
			break;
		}else
		{
			uncle = g_father->left;
			if (uncle != &TREE_NIL && uncle->color == TREE_RED)
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
				right_rotate(head, node);
			}
			node->father->color = TREE_BLACK;
			g_father->color = TREE_RED;
			left_rotate(head, g_father);
			node = g_father->father;
			break;
		}
	}
	if (node->father == &TREE_NIL)
	{
		*head = node;
		(*head)->color = TREE_BLACK;
	}
	return 0;
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
	if (temp == NULL || temp == &TREE_NIL)
	{
		*head = node;
		node->color = TREE_BLACK;
		node->father = &TREE_NIL;
		node->left = &TREE_NIL;
		node->right = &TREE_NIL;
		printf("not has head\n");
		return 0;
	}

	while (1)
	{
		if (node->key > temp->key)
		{
			if (temp->right == &TREE_NIL)
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
			if (temp->left == &TREE_NIL)
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
	tree_insert_fix(head, node);
	return 0;
}

rb_node *tree_get_node(rb_node *head, int key)
{
	rb_node *temp = head;
	if (head == NULL)
	{
		printf("null tree\n");
		return NULL;
	}
	while (temp != &TREE_NIL)
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

int tree_delete_fix(rb_node **head, rb_node *node_x)
{
	rb_node *brother, *father;
	while(node_x->father != &TREE_NIL && node_x->color == TREE_BLACK)
	{
		father = node_x->father;
		if (node_x == father->left)
		{
			brother = father->right;
			if (brother->color == TREE_RED)
			{
				brother->color = TREE_BLACK;
				father->color = TREE_RED;
				left_rotate(head, father);
				brother = father->right;
			}

			if (brother->left->color == TREE_BLACK && brother->right->color == TREE_BLACK)
			{
				brother->color = TREE_RED;
				node_x = father;
				continue;
			}else if (brother->right->color == TREE_BLACK)
			{
				brother->left->color = TREE_BLACK;
				brother->color = TREE_RED;
				right_rotate(head, brother);
				brother = father->right;
			}
			brother->color = father->color;
			father->color = TREE_BLACK;
			brother->right->color = TREE_BLACK;
			left_rotate(head, father);
			node_x = *head;
		}else
		{
			brother = father->left;
			if (brother->color == TREE_RED)
			{
				brother->color = TREE_BLACK;
				father->color = TREE_RED;
				right_rotate(head, father);
				brother = father->left;
			}

			if (brother->left->color == TREE_BLACK && brother->right->color == TREE_BLACK)
			{
				brother->color = TREE_RED;
				node_x = father;
				continue;
			}else if (brother->left->color == TREE_BLACK)
			{
				brother->right->color = TREE_BLACK;
				brother->color = TREE_RED;
				left_rotate(head, brother);
				brother = father->left;
			}
			brother->color = father->color;
			father->color = TREE_BLACK;
			brother->left->color = TREE_BLACK;
			right_rotate(head, father);
			node_x = *head;
		}
	}
	node_x->color = TREE_BLACK;
	return 0;
}

rb_node *tree_delete(rb_node **head, int key)
{
	rb_node *node_del = tree_get_node(*head, key);
	rb_node *node_y, *node_x;
	TREE_COLOR color_y;
	if (node_del == NULL)
	{
		printf("the node not find:%d\n", key);
		return NULL;
	}
	color_y = node_del->color;
	if (node_del->left == &TREE_NIL)
	{
		node_x = node_del->right;
		tree_transplant(head, node_del, node_del->right);
	}else if (node_del->right == &TREE_NIL)
	{
		node_x = node_del->left;
		tree_transplant(head, node_del, node_del->left);
	}else
	{
		node_y = tree_minimum(node_del->right);
		color_y = node_y->color;
		node_x = node_y->right;
		if (node_y == node_del->right)
		{
			node_x->father = node_y;
		}else
		{
			tree_transplant(head, node_y, node_y->right);
			node_y->right = node_del->right;
			node_y->right->father = node_y;
		}
		tree_transplant(head, node_del, node_y);
		node_y->left = node_del->left;
		node_y->left->father = node_y;
		node_y->color = node_del->color;
	}
	
	if (color_y == TREE_BLACK)
	{
		tree_delete_fix(head, node_x);
	}
	return node_del;
}

int print_format(int key, int length, int color)
{
	int size = 0, i;
	int temp_key = key;
	if (key == -1)
	{
		for (i = 0; i < length - 1; i++)
		{
			printf(" ");
		}
		printf("|");
		return 0;
	}else if (key == 0)
	{
		length -= 2;
	}else
	{
		while(temp_key != 0)
		{
			size++;
			temp_key /= 10;
		}
		length -= size + 1;
	}
	for (i = 0; i < length; i++)
	{
		printf(" ");
	}
	if (color == TREE_BLACK)
	{
		printf(DARY_GRAY"%d"NONE, key);
	}else if (color == TREE_RED)
	{
		printf(RED"%d"NONE, key);
	}
	printf("|");
	
	return 0;
}

int display_tree(rb_node *node)
{
	rb_node *array[256];
	int deep[256], num[256], cur_dep = -1, cur_num = -1, sub = -1;
	int head = 0, tail = 1;
	if (node == NULL || node == &TREE_NIL)
	{
		return -1;
	}
	array[head] = node;
	deep[head] = 0;
	num[head] = 1;
	while(head != tail)
	{
		rb_node *temp = array[head];
		int i_dep = deep[head];
		int i_num = num[head];
		int i;
		head = (head + 1) % 256;
		if (cur_dep == -1)
		{
			cur_dep = i_dep;
			cur_num = i_num;
			sub = 1;
		}else if(cur_dep != i_dep)
		{
			cur_dep = i_dep;
			cur_num *= 2;
			sub = cur_num;
			printf("%d", 256 / cur_num);
			printf("\n");
		}
		
		for (i = 0; i < i_num - sub; i++)
		{
			print_format(-1, 256 / cur_num, -1);
		}
		sub = i_num + 1;
		print_format(temp->key, 256 / cur_num, temp->color);
		if (temp->left != &TREE_NIL)
		{
			array[tail] = temp->left;
			deep[tail] = i_dep + 1;
			num[tail] = i_num * 2;
			tail = (tail + 1) % 256;
		}
		if (temp->right != &TREE_NIL)
		{
			array[tail] = temp->right;
			deep[tail] = i_dep + 1;
			num[tail] = i_num * 2 + 1;
			tail = (tail + 1) % 256;
		}
	}
	
	return 0;
}
rb_node *tree_minimum(rb_node *node)
{
	rb_node *temp = node;
	while(temp->left != &TREE_NIL)
	{
		temp = temp->left;
	}
	return temp;
}
int tree_transplant(rb_node **head, rb_node *a, rb_node *b)
{
	rb_node *father = a->father;
	if (father == &TREE_NIL)
	{
		*head = b;
	}else if (father->left == a)
	{
		father->left = b;
	}else
	{
		father->right = b;
	}
	b->father = father;
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
	node->left = &TREE_NIL;
	node->right = &TREE_NIL;
	node->father = &TREE_NIL;
	node->data = NULL;
	node->color = TREE_RED;
	return node;
}
int print_wrong_father(rb_node *node, int deep)
{
	rb_node *father = node->father;
	if (father != NULL && father != &TREE_NIL)
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
	if (head == NULL || head == &TREE_NIL)
	{
		return 0;
	}
	size += print_tree(head->left, deep + 1);
	if (head->father != &TREE_NIL)
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
	if (head == NULL || head == &TREE_NIL)
	{
		return 0;
	}
	tree_free(head->left, fun);
	tree_free(head->right, fun);
	if (fun != NULL)
	{
		(*fun)(head->data);
	}
	free(head);
	return 0;
}
int tree_count(rb_node *head)
{
	int size = 1;
	if (head == NULL || head == &TREE_NIL)
	{
		return 0;
	}
	size += tree_count(head->left);
	size += tree_count(head->right);
	return size;
}
int tree_start(rb_node *head, int deep, TREE_COLOR color)
{
	int ret;
	TREE_NIL.key = -1;
	ret = tree_test(head, deep, color);
	if (ret == -2)
	{
		printf("\n");
		abort();
	}
	return 0;
}
int tree_test(rb_node *head, int deep, TREE_COLOR color)
{
	int left, right;;
	if (head == NULL)
	{
		return -1;
	}else if (head == &TREE_NIL)
	{
		if (head->key == -1)
		{
			head->key = deep;
		}else if(head->key != deep)
		{
			printf("wrong deep:%d key:%d\n", deep, head->key);
			return -2;
		}
		return -1;
	}
	
	if (head->color == TREE_BLACK)
	{
		deep++;
	}else if (color == TREE_RED)
	{
		printf("wrong color:%d\n", head->key);
		return -2;
	}
	
	left = tree_test(head->left, deep, head->color);
	if (left == -2)
	{
		printf(" %d ", head->key);
		return -2;
	}
	
	right = tree_test(head->right, deep, head->color);
	if (right == -2)
	{
		printf(" %d ", head->key);
		return -2;
	}
	
	if (left != -1 && left >= head->key)
	{
		printf("wrong cmp:%d", head->key);
		return -2;
	}else if(right != -1 && right <= head->key)
	{
		printf("wrong cmp:%d", head->key);
		return -2;
	}
	return head->key;
}

