# # # # # # # # # # # # # # # # # # # # # # # # #
"""

	Lie derivative image analysis (LDIA)

	This calculation code provides:

	(1) LDIA calculation for input two .csv image files (2D array)
		and output .csv images including the following value as a list

	(2) 2D Lie derivative components (Lx and Ly)

	(3) L-value, S-value, U-value maps according to the 2D Lie derivatve

	If a researcher use this code, please refer to

		Ectracting the gradient component of the gamma index
		using the Lie derivative method
		(doi: 10.1088/1361-6560/acf990)
	
	and include the reference.

	This calculation code is licensed under Apache License 2.0 

	(c) Yusuke Anetai

"""
# # # # # # # # # # # # # # # # # # # # # # # # #

import sys;
import os;
import csv;
import math;
import numpy as np;
import tkinter as tk;
import tkinter.ttk as ttk;
import tkinter.filedialog as tkF;

##########################
class LDIAcalc():
	def __init__(self):
		__val = 0;
		
	#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
	#1. CSV image reader and writer
	#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

	def csvpathread(self):
		roottk = tk.Tk();
		fType = [("","*.csv")];
		iDir = os.path.abspath(os.path.dirname(__file__));
		filepath = tkF.askopenfilename(parent = roottk,filetypes = fType,initialdir = iDir);
		roottk.withdraw();
		roottk.destroy();
		print(filepath);
		return(filepath);

	def csvreadTXT(self,filepath):
		data0 = list();
		ftxt = np.genfromtxt(filepath,delimiter=',');
		#data0.append(np.array(ftxt,dtype='float64').transpose());
		data0.append(np.array(ftxt,dtype='float64'));
		return np.array(data0);

	def csvWriter2L(self,Data,filename):
		cdpath = os.getcwd();
		print(cdpath);
		## Directory:: _csvtmp
		newdir = '_csvtmp';
		if(os.path.exists(newdir)):
			print('path exists');
		else:
			os.mkdir(newdir);
		newpath = '%s/%s' % (cdpath,newdir);
		os.chdir(newpath);
		## Directory:: _LDIA
		newdirL = '_LDIA';
		if(os.path.exists(newdirL)):
			print('path exists');
		else:
			os.mkdir(newdirL);
		newpathL = '%s/%s/%s' % (cdpath,newdir,newdirL);
		os.chdir(newpathL);
		if(len(filename)==0):
			filename = 'mccArray.csv';
		filenameR = ('%s/%s')%(newpathL,filename);
		fid = open(filenameR,'w');
		#writer = csv.writer(fid,lineterminator = '\r\n');
		writer = csv.writer(fid,lineterminator = '\r');
		#writer.writerow(Data[:]);
		writer.writerows(np.array(Data[:],dtype='float64'));
		os.chdir(cdpath);
		fid.close();

	#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
	#2. Image derivative with second order accuracy
	#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

	def image_derivative_module(self,img,dx,dy):
		mm = img.shape[0]; nn = img.shape[1];
		#print(mm,nn);
		dA = np.zeros((6,mm,nn));
		#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#
		# The anser array comprises of
		# [1,d/dx,d/dy,d^2/dx^2,d^2/dy^2,d^2/dxdy] I
		#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#
		dA[0,:,:] = img;
		for jj in range(mm):
			#Y-directional(jj)
			if(jj == 0):
				dA[2,0,:] = (-3.0*img[0,:]+4.0*img[1,:]-img[2,:])/(2.0*dy);
				dA[4,0,:] = (2.0*img[0,:]-5.0*img[1,:]+4.0*img[2,:]-img[3,:])/(dy*dy);
			elif(jj == mm-1):
				dA[2,mm-1,:] = (3.0*img[mm-1,:]-4.0*img[mm-2,:]+img[mm-3,:])/(2.0*dy);
				dA[4,mm-1,:] = (2.0*img[mm-1,:]-5.0*img[mm-2,:]+4.0*img[mm-3,:]-img[mm-4,:])/(dy*dy);
			else:
				#X-directional(ii)
				for ii in range(nn):
					if(ii == 0):
						dA[1,:,0] = (-3.0*img[:,0]+4.0*img[:,1]-img[:,2])/(2.0*dx);
						dA[3,:,0] = (2.0*img[:,0]-5.0*img[:,1]+4.0*img[:,2]-img[:,3])/(dx*dx);
					elif(ii == nn-1):
						dA[1,:,nn-1] = (3.0*img[:,nn-1]-4.0*img[:,nn-2]+img[:,nn-3])/(2.0*dx);
						dA[3,:,nn-1] = (2.0*img[:,nn-1]-5.0*img[:,nn-2]+4.0*img[:,nn-3]-img[:,nn-4])/(dx*dx);
					else:
						tmp11 = (img[jj,ii+1]-img[jj,ii-1])/(2.0*dx);
						tmp12 = (img[jj+1,ii]-img[jj-1,ii])/(2.0*dy);
						tmp21 = (img[jj,ii+1]-2.0*img[jj,ii]+img[jj,ii-1])/(dx*dx);
						tmp22 = (img[jj+1,ii]-2.0*img[jj,ii]+img[jj-1,ii])/(dy*dy);
						dA[1,jj,ii] =tmp11;
						dA[2,jj,ii] = tmp12;
						dA[3,jj,ii] = tmp21;
						dA[4,jj,ii] = tmp22;
		#d^2/dxdy calculation
		BB = dA[1,:,:];
		for jj in range(mm):
			if(jj == 0):
				dA[5,0,:] = (-3.0*BB[0,:]+4.0*BB[1,:]-BB[2,:])/(2.0*dy);
			elif(jj == mm-1):
				dA[5,mm-1,:] = (3.0*BB[mm-1,:]-4.0*BB[mm-2,:]+BB[mm-3,:])/(2.0*dy);
			else:
				dA[5,jj,:] = (BB[jj+1,:]-BB[jj-1,:])/(2.0*dy);
		return dA;

	#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
	#3. Lie derivative calculation
	#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

	def LieDerivativeModule(self,IMG1,IMG2,dx,dy):
		anslist = list();
		dA1 = self.image_derivative_module(IMG1,dx,dy);
		dA2 = self.image_derivative_module(IMG2,dx,dy);
		##
		## velocity potencial base ##
		A1 = (dA1[1]*dA2[3]+dA1[2]*dA2[5])-(dA2[1]*dA1[3]+dA2[2]*dA1[5]);
		A2 = (dA1[1]*dA2[5]+dA1[2]*dA2[4])-(dA2[1]*dA1[5]+dA2[2]*dA1[4]);
		AA0 = A1*A1+A2*A2; AL = np.sqrt(AA0);
		dAL = self.image_derivative_module(AL,dx,dy);
		dALx = self.image_derivative_module(A1,dx,dy);
		dALy = self.image_derivative_module(A2,dx,dy);
		Wz = dALy[1]-dALx[2];
		AA2 = Wz*Wz; AS = np.sqrt(AA2);
		AUo = dALx[1]+dALy[2]; AU = np.abs(AUo);
		## calculation finished ##
		anslist.append(A1); anslist.append(A2);
		anslist.append(AL); anslist.append(AS); anslist.append(AU);
		return(anslist);
