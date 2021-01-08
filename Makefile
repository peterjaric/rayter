test:
	python -m unittest discover

dist: test dist/*
	rm -f dist/*
	python setup.py sdist

upload: dist
	twine upload dist/*
