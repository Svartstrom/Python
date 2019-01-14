import openpyxl
#from openpyxl import load_workbook
import numpy as np
import matplotlib.pyplot as plt
import math
import glob
import datetime
import time
import os
import sys

import Swingtrader_constants as C
"""
from TA_functions     import *
from Import_functions import *
from Report_functions import *
from test_Swingtrader_2 import *"""
from Importer   import *
from Calculator import *

import threading
import random

global mess,ii,jj,kk, QUE
mess = 'None'
QUE = []

def GUI():

	print(" Length of Que: ",len(QUE))
	try:print(QUE[0])
	except:print(" ")
	try:print(QUE[1])
	except:print(" ")
	try:print(QUE[2])
	except:print(" ")
	try:print(QUE[3])
	except:print(" ")
	try:print(QUE[4])
	except:print(" ")
	print(" ")
	options('NA',['NA'],'Yes')
	#print("D. Delete MA and DMA")
	#print("R. Make all reports")
	#print("I. Import")
	#print("M. MA to all")
	#print("T. Test all funktions")
	#print("X. Clear que")
	#print("Q. Quit")

def options(Internal,order,printThis):
	#########################################################
	if order[0] == 'START_PROGRAM':
		startProgram()
	#########################################################
	if order[0] == 'FOR_ALL':
		for _all in glob.glob(C.DataDir+"/*xlsx"):
			QUE.append([order[1],_all])
	#########################################################
	if printThis == 'No':
		print("D. Delete MA and DMA")
	if Internal == 'D' or Internal == 'd':
		for _all in glob.glob(C.DataDir+"/*xlsx"):
			QUE.append(['DELETE_MA_AND_DMA',_all])
	##
	if order[0] == 'DELETE_MA_AND_DMA':
		deleteFullMAandDMA(order[1])
	#########################################################
	if printThis == 'Yes':
		print("I. Import")
	if Internal == 'I' or Internal == 'i':
		for _all in glob.glob(C.DataDir+"/*xlsx"):
			QUE.append(['IMPORT',_all])
	##
	if order[0] == 'IMPORT':
		for AllNames in glob.glob(C.DailyDir+"/Bors*xlsx"):
			importOneFromDaily(order[1],AllNames)
	#########################################################
	#elif Internal == 'I' or Internal == 'i':
	#	QUE.append(['COPY_DOWNLOADS'])
	##
	#if order[0] == 'COPY_DOWNLOADS':
	#	for N in glob.glob("/home/sid/Downloads/*-Price.xls"):
	#		N = N.split('/')[-1]
	#		N = C.DataDir+'/'+N+'x'
	#		QUE.append(['PRINT_REPORT',N])
	#	copyFromDownloads()
	#########################################################
	if printThis == 'Yes':
		print("M. Make all reports")
	if Internal == 'M' or Internal == 'm':
		for _all in glob.glob(C.DataDir+"/*xlsx"):
			QUE.append(['PRINT_REPORT',_all])
	##
	if order[0] == 'PRINT_REPORT':
		R = makeReport(order[1])
		if R == 'MA15' or R == 'MA50':
			QUE.append(['FULL_MA',order[1]])
			QUE.append(['PRINT_REPORT',order[1]])
	#########################################################
	if printThis == 'Yes':
		print("S. make all Statistics")
	if Internal == 'S' or Internal == 's':
		for _all in glob.glob(C.DataDir+"/*xlsx"):
			QUE.append(['FULL_MA',_all])
	if order[0] == 'FULL_MA':
		printFullMAtoCurrentWB(order[1],'irellepant')
		DeriveAndPrintFullDMAtoCurrentWB(order[1],'irellepant')
	#########################################################
	if printThis == 'No':
		print("T. Test all funktions")
	if Internal == 'T' or Internal == 't':
		QUE.append(['RUN_TEST'])
	##
	if order[0] == 'RUN_TEST':
		tester()
	#########################################################
	if printThis == 'Yes':
		print("X. Delete que")
	#########################################################
	if printThis == 'Yes':
		print("R. Restart program")
	#########################################################
	if printThis == 'Yes':
		print("Q. Quit program")
	#########################################################

def EXThread():
	global mess, QUE

	"""
	m: FULL_MA
	p: PRINT_NAME
	r: PRINT_REPORT
	d: DELETE_MA_AND_DMA
	t: RUN_TEST
	i: COPY_DOWNLOADS
	x: DELETE_QUE
	"""
	while True:
		if len(QUE) > 0:
			order, QUE = QUE[0], QUE[1:]
			options('NA',order,'NA')

		if mess == 'RESTART_PROGRAM':
			restartProgram()
		if mess == 'DELETE_QUE':
			QUE = []
			mess = ''
		if mess == "Z":
			break

	time.sleep(0.001)

def restartProgram():
	while len(QUE) > 0:
		order, QUE = QUE[0], QUE[1:]
		
	os.execl(sys.executable, sys.executable, *sys.argv)
def startProgram():
	pass
def PrintThread():
	global mess, QUE
	QUE.append(['START_PROGRAM'])
	os.system('cls||clear')
	while True:
		Internal = ''
		os.system('cls||clear')
		GUI()

		Internal = input("What? ")
		Internal = str(Internal)
		options(Internal,['NA'],'NA')

		if Internal == 'R' or Internal == 'r':
			mess = 'RESTART_PROGRAM'
		if Internal == 'X' or Internal == 'x':
			mess = 'DELETE_QUE'
		if Internal == 'Q' or Internal == 'q': 
			mess = 'Z'
			break
		else:
			os.system('cls||clear')
		time.sleep(0.01)

print(":::::::::::::::::::::::::::::::::::::::::::::")
thread1 = threading.Thread(target=EXThread,   args=())
thread2 = threading.Thread(target=PrintThread,args=())

thread1.start()
thread2.start()
