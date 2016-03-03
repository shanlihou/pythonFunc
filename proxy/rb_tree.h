#ifndef _RB_TREE_H
#define _RB_TREE_H
typedef enum _TREE_COLOR 
{
	TREE_BLACK = 0,
	TREE_RED
}TREE_COLOR;
typedef struct _rb_node
{
	int key;
	TREE_COLOR color;
	struct _rb_node *left;
	struct _rb_node *right;
	struct _rb_node *father;
	void *data;
}rb_node;
int left_rotate(rb_node *node);
int right_rotate(rb_node *node);
int tree_fix(rb_node **head, rb_node *node);
int tree_insert(rb_node **head, rb_node *node);
rb_node *new_tree_node();
int print_tree(rb_node *head, int deep);
int tree_free(rb_node *head, int (*fun)(void *arg));
rb_node *tree_get_node(rb_node *head, int key)
#endif
