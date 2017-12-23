#######
#Currently running unoptimized (i.e. not python2.7 -O), so that assertions are checked.
#######

# Run all. (i.e. all options as a single function)
all:
	python2.7 test-driver.py all

vary whd:
	python2.7 vary-parameters.py vary whd

vary mps:
	python2.7 vary-parameters.py vary mps

vary both:
	python2.7 vary-parameters.py vary both

# Remove any files beginning in ~ or ending with pyc/pyo
clean:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*~' -exec rm --force  {} +

# Crop all photos
crop:
	python2.7 test-driver.py crop

# Resize all photos to minimum image file size in 'cropped-images/'
resize:
	python2.7 test-driver.py resize

# For each image in 'resized-images/', calculate variance of laplacian on
# subdivisions of the image; gives the regions in focus a high variance
# and blurry regions a very low variance
lpc:
	python2.7 test-driver.py lpc

# Create 3D model from laplacian image stack.
3D:
	python2.7 test-driver.py 3D

# Create 3D model from laplacian image stack in a slightly
# faster way and possibly make a few mistakes.
o_3D:
	python2.7 test-driver.py o_3D

# Graph the 3D model if it has already been created
graph:
	python2.7 test-driver.py graph

# Allows the user to start the program from the top. Delete all
# processed images (i.e. images in cropped-images/ & resized-images/)
reset:
	rm -I cropped-images/*
	rm -I resized-images/*

# Help commands
help:
	@echo "clean"
	@echo "		Removes *.pyc, *.pyo, and ~* files"
	@echo "all"
	@echo "		Run test-driver.py in python2.7 on your machine"
	@echo "		Warning: it's best to run each command separately."
	@echo "crop"
	@echo "		Crop all photos in 'raw_images/' with given threshold lvl"
	@echo "resize"
	@echo "		Resize all images in 'cropped-images/' to smallest image in dir"
	@echo "lpc"
	@echo "		Forms variance of laplacian matrix of each image in 'resized-images/'"
	@echo "		For more explanation: type 'make help_lpc'"
	@echo "3D"
	@echo "		Produce the 3D model of the object."
	@echo "o_3D"
	@echo "		Slightly more optimized version of 3D. Could fail with too much image noise."
	@echo "graph"
	@echo "		Graph the topographical map of the object."
	@echo "reset"
	@echo "		Remove all files from 'cropped-images/' & 'resized-images/'"

help_lpc:
	@echo "LPC help:"
	@echo "The Laplacian operator measures the 2nd derivate of an image."
	@echo "Since the image's entries are (of course) not functions, the"
	@echo "Laplacian operator is performed by convolving the image with"
	@echo "a Laplacian 'kernel.' When I calculate the variance of the"
	@echo "result, I can find meaning in that value. A high variance"
	@echo "indicates a wide spread of responses, both edge-like and"
	@echo "non-edge like. These are qualities of an in-focus image."
	@echo "A low variance indicates there are few edges, indicating"
	@echo "blurriness."
