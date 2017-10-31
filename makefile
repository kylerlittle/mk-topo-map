# Run the driver program
run:
	python2.7 driver.py

# Remove any files beginning in ~ or ending with pyc/pyo
clean:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*~' -exec rm --force  {} +

# Help commands
help:
	@echo "clean"
	@echo "		Removes *.pyc, *.pyo, and ~* files"
	@echo "run"
	@echo "		Run driver.py in python2.7 on your machine"
