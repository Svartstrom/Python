import Image
import math
from random import randrange
#MAXX,MAXY = 1024.0,1024.0#4096.0,4096.0
XT,YT,XB,YB = 2.0,2.0,-2.0,-2.0		#Standard Mandelbrot
#XT,YT,XB,YB = -0.6,0.5,-0.9,0.0	#Seahorse valley
#XT,YT,XB,YB = -0.5,1.2,0.6,0.5		#Top sphere
#XT,YT,XB,YB = -1.8,-0.1,-1.6,0.1	#Front spheres

#MAXPIX is the amount of pixles on the shortest side, 
#this calculates and prints the other side.
MAXPIX = 0.5*1024
if math.fabs(XT-XB)>math.fabs(YT-YB):
	MAXY = MAXPIX
	MAXX = round((math.fabs(XT-XB)/math.fabs(YT-YB))*MAXPIX)
else:
	MAXX = MAXPIX
	MAXY = round((math.fabs(YT-YB)/math.fabs(XT-XB))*MAXPIX)
print MAXX,MAXY

MAXC = 512		#maximum amoute on one collor channel
MAXK = 100		#How many iterations to run in the Mandelbrot calculations


#Function for transforming the coordinates on the pixels too coordinates on the complex plane
def trans(i,j):
	j=MAXY-j
	i=((XT-XB)/MAXX)*i+XB#(XT+XB)/2+(XT-XB)/2
	j=((YT-YB)/MAXY)*j+YB#(YT+YB)/2+(YT-YB)/2
	return (i,j)

#Calculating the actual Mandelbrot number for a given complex point	
def mandel(i,j):
	i,j=trans(i,j)
	#Skip the calculations of known values.
	if ((i**2+j**2)**(1/2.0))>2:
		return (0,0,0)#(MAXC,MAXC,MAXC)#(0,0,0)
	if (((i+1)**2+j**2)**(1/2.0))<0.2:
		return (0,0,0)
	if i<0 and i>-0.5 and j>-0.4 and j<0.4:
		return (0,0,0)
	
	z = complex(0,0)
	for k in range(MAXK):
		z = z*z + complex(i,j)
		
		if abs(z) > 2:
			aa = k*MAXC/MAXK if k<MAXK/2 else 0
			bb = k*MAXC/MAXK if k>MAXK/4 and k<3*MAXK/4 else 0
			cc = k*MAXC/MAXK if k>MAXK/2 else 0
			return (aa,bb,cc)
	return (0,0,0)
def mainMandel(XTi,YTi,XBi,YBi,MAXPIXi):
	global XT,YT,XB,YB,MAXPIX,MAXX,MAXY
	XT,YT,XB,YB,MAXPIX = XTi,YTi,XBi,YBi,MAXPIXi
	OLD=0
	if math.fabs(XT-XB)>math.fabs(YT-YB):
		MAXY = MAXPIX
		MAXX = round((math.fabs(XT-XB)/math.fabs(YT-YB))*MAXPIX)
	else:
		MAXX = MAXPIX
		MAXY = round((math.fabs(YT-YB)/math.fabs(XT-XB))*MAXPIX)
	print MAXX,MAXY
	img = Image.new( 'RGB', (int(MAXX),int(MAXY)), "black") # create a new black image
	pixels = img.load() # create the pixel map

	for i in range(img.size[0]):    # for every pixel:
		for j in range(img.size[1]):
			NEW=int(((i*MAXY+j)/float((MAXX*MAXY))*100))
			if (NEW is not OLD):
				print NEW
				OLD = NEW
			pixels[i,j] = mandel(i,j)
			#pixels[i,j]=(i,j,0)
	Rname = randrange(100000)
	img.save(str(Rname)+'_'+str(MAXX)+'_'+str(MAXY)+'_'+str(MAXK)+'test.jfif')
