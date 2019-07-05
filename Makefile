test:
	python -m unittest tests.runtests

dist: test dist/*
	rm -f dist/*
	python setup.py sdist

upload: dist
	twine upload dist/*
