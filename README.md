# Requirements
- numpy
- opencv2
- python 3.7+

# Instructions

The file 'Main.py' is the entrypoint for the application. Run it using Python to activate the application. This application only does black and white images at this time.
	python Main.py

Basic application settings are controlled in the 'Main.py' file:
	- Input image path
	- Output image path
	- Number of simulation steps

Physics settings are controlled in the 'CONSTANTS.py' file:
	- Brush mass
	- Gravity
	- Maximum possible velocity
	- Drag
	- Image Size

Brush placement settings are controlled in the 'Artist.py' file, in the paint() method. You can extend the list variable called 'brushes' in order to add additional brushes, or change the current brush placement. 
See the code that is currently in the paint() method for an example.

Modify these settings/files to get different results.