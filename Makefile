.PHONY: test

install:
	python setup.py 

test:
	python -m unittest tests/*.py
