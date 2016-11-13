import imageTest



#XT,YT,XB,YB = 2.0,2.0,-2.0,-2.0	#Standard Mandelbrot
#XT,YT,XB,YB = -0.6,0.5,-0.9,0.0	#Seahorse valley
#XT,YT,XB,YB = -0.5,1.2,0.6,0.5		#Top sphere
#XT,YT,XB,YB = -1.8,-0.1,-1.6,0.1	#Front spheres

imageTest.mainMandel(2.0,2.0,-2.0,-2.0,16*1024)
imageTest.mainMandel(-1.8,-0.1,-1.6,0.1,16*1024)
imageTest.mainMandel(-0.6,0.5,-0.9,0.0,12*1024)
imageTest.mainMandel(-0.5,1.2,0.6,0.5,12*1024)
