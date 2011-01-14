all:

test:
	python testHists.py

testvers:
	python2.6 testHists.py
	python2.7 -munittest discover
