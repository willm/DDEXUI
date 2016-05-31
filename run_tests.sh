#python3 -m unittest discover 
PYTHONPATH=$(readlink -f ..):$PYTHONPATH nosetests -v
