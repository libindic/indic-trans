travis:
	python setup.py test --coverage \
		--coverage-package-name=indictrans
clean:
	find . -iname "*.pyc" -exec rm -vf {} \;
	find . -iname "__pycache__" -delete
