
# python setup.py register sdist upload

python setup.py sdist bdist_wheel
twine check dist/*
twine upload dist/*

rm -r __pycache__
rm -r *.egg-info
