clear
rm cyclus.sqlite
rm -rf build
python setup.py install
cyclus test.xml