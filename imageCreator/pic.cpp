#include <fstream>
#include <iostream>
#include <cmath>
#include <complex>

using namespace std;

int width = 10*512, height = 10*512;

#define norm(a,b) a/b 

void Mandelbrot(float X, float Y, int* r, int* g, int* b)
// -2 < X,Y < 2
{
	if (abs(X) > 2 || abs(Y) > 2)
	{
		*r = 0;
		*b = 0;	
		*g = 0;
		return;
	}
	complex<float> C, Z = (0,0);
	C.real(X);
	C.imag(Y);
	//cout << C<<pow(C,2)<<endl;
	int temp;
	for (int T = 1; T < 21; T++)
	{
		Z = pow(Z,2) + C;
		if (abs(Z) > 2)
		{
			//*r= T + 1 - log(log2(abs(Z)));
			*r = (255*T)/20;
			*b = 0;//(255*T)/20;
			*g = (255*T)/80;
			return;
		}
		temp = T;
	}

	*r = 0;
	*b = 0;	
	*g = 0;

	//Z0 = 0
	//Ẑ+1 = Z² + c
}
void pallet(int X, int Y, int* r, int* g, int* b)
{
	if (X > width / 2)
	{
		int T = width - ( X - width /2 );
		*r = T % 255;
	} else
	{
		*r = X % 255;
	}
	if (Y < height / 2)
	{
		int T = height - ( Y - height /2 );
		*g = T % 255;
	} else
	{
		*g = Y % 255;
	}
	*b = *r * *g % 255;
}

void circle(int X, int Y, int* r, int* g, int* b)
{
	X -= width / 2;
	Y -= height / 2;
	if (pow(X,2) + pow(Y,2) > pow(height/2,2) )
	{
		*r = 255;
		*g = 255;
		*b = 255;
	} /*else 
	{
		*r = 0;
		*g = 0;
		*b = 0;
	}*/
}
int main(void)
{
	/*cout<<"width: ";
	cin >> width;
	cout<<"height: ";
	cin >> height;*/
	ofstream img ("picture.ppm");
	img << "P3" << endl;
	img << width << " " << height << endl;
	img << "255" << endl;
	int M = 2;
	float X=0,Y=0;
	int r, g, b;
	float L = -2, R=-1, T=0.9,B=-0.1;
	for (float y = 0; y < height; y++)
	{
		for (float x = 0; x < width; x++)
		{
			X = L + ((R-L)*x)/width;
			Y = B + ((T-B)*(height-y))/height;
			Mandelbrot(X,Y,&r,&g,&b);
			img << r << " " << g << " " << b << endl;
		}
	}

	//system("open picture.ppm");
	return 0;
}