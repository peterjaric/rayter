test:
	python tests/runtests.py

dist: dist/*
	rm -f dist/*
	python setup.py sdist

upload:
	twine upload dist/*
