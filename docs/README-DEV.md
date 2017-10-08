# Style check
python setup.py pep8

# Dev Mode
pip install -e

# Source Distribution
python setup.py sdist

# Universal Wheels
python setup.py bdist_wheel

# PEP8 - W291
vim:%s/\s\+$//e
