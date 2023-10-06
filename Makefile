.PHONY: all test docs package upload clean

all: test docs

test:
	@pytest tests/

docs:
	sphinx-apidoc -o docs/source .
	make -C docs html

package:
	python setup.py sdist bdist_wheel

upload:
	twine upload dist/*

clean:
	rm -rf build dist klingon_serial.egg-info

