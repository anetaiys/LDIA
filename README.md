# LDIA
## Lie derivative image analysis
	LDIA is an image processing tool to obtain deviation vector field 
 	between two image flows according to Lie derivative

## - - - - - - - - - - - - - - - - - - - - - - - -

### Overview
### """""""""

	Lie derivative image analysis (LDIA)

	This calculation code provides:

	(1) LDIA calculation for input two .csv image files (2D array)
		and output .csv images including the following value as a list

	(2) 2D Lie derivative components (Lx and Ly)

	(3) L-value, S-value, U-value maps according to the 2D Lie derivatve

	If a researcher use this code, please refer to

		Extracting the gradient component of the gamma index
		using the Lie derivative method
		(doi: 10.1088/1361-6560/acf990)
	
	and include the reference.

	This calculation code is licensed under Apache License 2.0 

### """""""""

### Requirement
### """"""""""""
	numpy
 	csv
  	math
	tkinter
 	numpy

### Install
### """"""""""""
	No install method.

### Usage
### """""""""
	Import LDIA and create instance of LDIA class in your code.
	Then, start LieDerivativeModule(img1, img2, dx, dy).
	Input two same shape (rows and columns) .csv image files (img1, img2).
 	Typically, calculation grid size dx and dy are usually 1.0.

### License
### """""""""
	Apache License 2.0 

### Author
### """""""""
	Yusuke Anetai 
 	anetaiys (atmark) hirakata.kmu.ac.jp
