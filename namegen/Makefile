
test: surname_hash.py male_hash.py female_hash.py
	PYTHONPATH=. python markov

surname_hash.py: sur.names
	python genmarkov $+ surname > $@
female_hash.py: female.names
	python genmarkov $+ female > $@
male_hash.py: male.names
	python genmarkov $+ male > $@
clean:
	rm *.pyc *_hash.py
