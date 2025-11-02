
# python setup.py register sdist upload

python setup.py sdist bdist_wheel
twine check dist/*
twine upload dist/*

find . -type d -name "__pycache__" -exec rm -r -v {} +
rm -r *.egg-info
rm -r dist
