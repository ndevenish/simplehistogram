all:

test:
	python setup.py test

testvers:
	python2.6 testHists.py
	python2.7 -munittest discover

distclean:
	rm -rf ./build ./dist ./*.egg-info
	rm simplehist/*.pyc
	rm simplehist/test/*.pyc

dist:
	python setup.py sdist