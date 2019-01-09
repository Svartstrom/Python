#include <iostream>

using namespace std;

struct node{
	int value;
	node *left;
	node *right;
};

class btree
{
public:
	node *root;
	btree();
	void insert(int n);
};

btree::btree()
{
	root=NULL;
	root = new node;
}
void btree::insert(int n)
{
	//if (root == NULL)
	//{
	root->value = n;
	//}
}

int main()
{
	int e = 3;
	btree R;
	R.root->value = 22;
	cout<<"Hello World\n";
	node *root;
	root = NULL;
	root = new node;
	root->value = e;
	root->left = NULL;
	root->right= NULL;
	root->left = new node;
	root->left->value = 2;
	cout<<root->value;
	cout<<"\n";
	cout<<root->left->value;
	cout<<"\n";
	R.insert(33);
	cout<<R.root->value;
	cout<<"\n";
}