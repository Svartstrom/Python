using namespace std;
struct Leaf
{
	int V;
	int B;
	Leaf *L;
	Leaf *R;
};

class btree
{
public:
	btree();
	~btree();

	void insert(int key);
	Leaf *search(int key);
	void destroy_tree();
	void printTree();
	int checkBalance(); 

	Leaf *root;
private:
	void Destroy_Tree(Leaf *leaf);
	void Insert(int key, Leaf *leaf);
	Leaf *Search(int key, Leaf *leaf);
	void PrintTree(Leaf *leaf);
	int CheckBalance(Leaf *leaf);

};
btree::btree()
{
	root = NULL;
}
btree::~btree()
{
	destroy_tree();
}
void btree::insert(int key)
{
	if (root != NULL)
	{
		Insert(key, root);
	} else {
		root    = new Leaf;
		root->V = key;
		root->B = 0;
		root->L = NULL;
		root->R = NULL;
	}
}
Leaf *btree::search(int key)
{
	return Search(key, root);
}
void btree::destroy_tree()
{
	Destroy_Tree(root);
}
void btree::Destroy_Tree(Leaf *leaf)
{
	if (leaf != NULL)
	{
		Destroy_Tree(leaf->L);
		Destroy_Tree(leaf->R);
		delete leaf;
	}
}
void btree::Insert(int key, Leaf *leaf)
{
	if (key < leaf->V)
	{
		if (leaf->L != NULL)
		{
			Insert(key, leaf->L);
			root->B -= 1;
		} else {
			leaf->L    = new Leaf;
			leaf->L->V = key;
			root->B = 0;
			leaf->L->L = NULL;
			leaf->L->R = NULL;
		}

	}

	if (key > leaf->V)
	{
		if (leaf->R != NULL)
		{
			Insert(key, leaf->R);
			root->B += 1;
		} else {
			leaf->R    = new Leaf;
			leaf->R->V = key;
			root->B = 0;
			leaf->R->L = NULL;
			leaf->R->R = NULL;
		}

	}
}
Leaf *btree::Search(int key, Leaf *leaf)
{
	if (leaf != NULL)
	{
		cout<<leaf->V<<" ";
		if (leaf->V == key)
		{
			return leaf;
		} else if (leaf->V >= key)
		{
			return Search(key, leaf->L);
		} else {
			return Search(key, leaf->R);
		}
	}
	return NULL;
}
void btree::printTree()
{
	PrintTree(root);
}
void btree::PrintTree(Leaf *leaf)
{
	if (leaf != NULL)
	{
		PrintTree(leaf->L);
		std::cout << leaf->V<<" ";
		PrintTree(leaf->R);
	}
}
int btree::checkBalance()
{
	return CheckBalance(root);
}
int btree::CheckBalance(Leaf *leaf)
{
	if (leaf != NULL)
	{
		//((a < b) ? a : b)
		int LC, RC,T;
		LC = CheckBalance(leaf->L);
		RC = CheckBalance(leaf->R);
		( (abs(LC) < abs(RC) )      ? T = RC   : T = LC );
		( (abs(T ) > abs(root->B) ) ? T = T : T = root->B);
		return T;  
	}
	return 0;
}

