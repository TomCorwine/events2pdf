# **events2pdf Installation**

 

## **Installing the events2pdf app**:

Unzip the **events2pdf** archive to the desired directory. 

 ##**Dependencies**:
 
 This version requires the following python modules:

​	**pip install filetype**
​	**pip install pyphen**
​	**pip install reportlab**
​	**pip install requests**


## **Zip contents:**

	AA-Logo.png			-  Logo included by html cover page.

​	events2pdf.py			- The script that creates the pdf file.

	coverpage.png			-  cover page image

​	coverpage.html		-  html version

​	events2pdf_conf.json   -  config file, may be changed by hand or with the gui.

	events2pdf_default_conf.json	- backup config file
	
	events2pdfMW.py		-  Main window for the gui, imported by gui.pyw.
	
	gui.pyw					-  Gui to change config.
	
**gui/**

	events2pdfMW.ui	-  created with Qt Designer, main window for gui.

	makeMW.bat			- primitive make file, creates events2pdfMW.py
	
	gui.pyw					- backup gui copy.

**docs/**

​    Configuration
​    Installation
​    LICENSE
​    README
​    README-Reportlab
​    

 

## **Simple primer for creating  virtual environment:**

May not be applicable for your server.

**Installing virtualenv:**

​	***python3 -m pip install --user virtualenv***

**Creating a virtual environment**:

To create a virtual environment, go to your project’s directory and run **venv**.

​	***python3 -m venv env*** 

The second argument is the location to create the virtual environment. Generally, you can just create this in your project and call it env. venv will create a virtual Python installation in the env folder.

**Activating a virtual environment**:

Before you can start installing or using packages in your virtual environment you’ll need to activate it. Activating a virtual environment will put the virtual environment specific python and pip executables into your shell’s PATH.

​	UNIX:  ***source env/bin/activate***

​	WIN:  ***.\env\Scripts\activate***

**Confirm you’re in the virtual environment** :

​	UNIX:  ***which python*** should give: 	./env/bin/python

​	WIN:  ***where python*** should give	.\env\Scripts\python.exe

**Leave virtual environment**:

​	***deactivate***

**Reactivate virtual environment**:

​	UNIX:  ***source env/bin/activate***

​	WIN:  ***.\env\Scripts\activate***

 

 

 

 