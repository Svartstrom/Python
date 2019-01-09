

#include <iostream>
#include <cstdlib>
#include "btree.cpp"

using namespace std;


int main(void)
{
	std::cout << "hello"<<std::endl;
	btree R;// = new btree;
	btree *tree = new btree();
	//btree R = new btree;
	R.insert(5);
	R.insert(3);
	R.insert(7);
	R.insert(2);
	R.insert(6);
	R.insert(4);
	R.insert(8);
	tree->insert(2);
	//tree->printTree();
/*
 		5
 	3		7
2	  4   6		8
*/
 //R.printTree();
 

 R.destroy_tree();
srand (time(NULL));
int rrr;
for (int i = 0; i<1000;i++)
{
	rrr=rand()%1000;
	//cout<<rrr<<"\n";
	R.insert(rrr);
}
cout<<"\n\n\n";
cout<<"Max balance: "<<R.checkBalance()<<"\n";
cout<<"Root B: "<<R.root->B<<" Root V: "<<R.root->V<<"\n";
cout<<"L B: "<<R.root->L->B<<" L V: "<<R.root->L->V<<"\n";
cout<<"R B: "<<R.root->R->B<<" R V: "<<R.root->R->V<<"\n";
cout<<"\n\n\n";
//R.printTree(); 
//delete R;
}