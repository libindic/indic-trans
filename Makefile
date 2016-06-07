travis:
	python setup.py test --coverage \
		--coverage-package-name=indictrans
	flake8 --max-complexity 22 indictrans
clean:
	find . -iname "*.pyc" -exec rm -vf {} \;
	find . -iname "__pycache__" -delete
