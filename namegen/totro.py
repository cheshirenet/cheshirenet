#!/usr/bin/env python
""" Totro.pl: generate random (fantasy) names.
 Copyright (C) 2002-2006 David A. Wheeler and Chris X. Edwards.
 This is Totro.pl, Version 1.20, 2006-04-19.
 
 The original program was written by David A. Wheeler in Javascript,
 and is available via http://www.dwheeler.com/totro.html
 Totro.pl is a port of Totro to Perl by Chris X Edwards xed.ch.

 As a direct port, Totro.pl is also released under the GPL:

 Totro.pl is Copyright (C) 2002-2005 David A. Wheeler and Chris X. Edwards,
 and comes with ABSOLUTELY NO WARRANTY.
 Totro.pl is licensed under the
 GNU General Public License (GPL), version 2 or later.


 Default values...
"""
NUMBER= 50 
MINSYL= 2
MAXSYL= 6

# List of possible vowels, followed by list of possible consonants.
# In both lists, duplicates increase the likelihood of that selection.
# The second parameter indicates if the syllable can occur
# at the beginning, middle, or ending of a name, and is the sum of
# the following:
#  1=can be at ending,
#  2=can be at beginning
#  4=can be in middle
# Thus, the value 7 means "can be anywhere", 6 means "beginning or middle".
# This is a binary encoding, as (middle) (beginning) (end).
# Occasionally, 'Y' will be duplicated as a vowel and a consonant.
# That's so rare that we won't worry about it, in fact it's interesting.
# There MUST be a possible vowel and possible consonant for any
# possible position; if you want to have "no vowel at the end", use
# ['',1] and make sure no other vowel includes "can be at end".

# Occasionally, 'Y' will be duplicated as a vowel and a consonant.
# That's so rare that we won't worry about it, in fact it's interesting.

# Note - an older version used the binary encoding xy,
# where x is the beginning, y is the ending, and 0=no, 1=yes (middle always ok)

vowels = [
 ("a", 7),	("e", 7),  ("i", 7),  ("o", 7),  ("u", 7),
 ("a", 7),	("e", 7),  ("i", 7),  ("o", 7),  ("u", 7),
 ("a", 7),	("e", 7),  ("i", 7),  ("o", 7),  ("u", 7),
 ("a", 7),	("e", 7),  ("i", 7),  ("o", 7),  ("u", 7),
 ("a", 7),	("e", 7),  ("i", 7),  ("o", 7),  ("u", 7),
 ("a", 7),	("e", 7),  ("i", 7),  ("o", 7),  ("u", 7),
 ("a", 7),	("e", 7),  ("i", 7),  ("o", 7),  ("u", 7),
 ("a", 7),	("e", 7),  ("i", 7),  ("o", 7),  ("u", 7),
 ("a", 7),	("e", 7),  ("i", 7),  ("o", 7),  ("u", 7),
 ("a", 7),	("e", 7),  ("i", 7),  ("o", 7),  ("u", 7),
 ("a", 7),	("e", 7),  ("i", 7),  ("o", 7),  ("u", 7),
 ("a", 7),	("e", 7),  ("i", 7),  ("o", 7),  ("u", 7),
 ("ae", 7), ("ai", 7), ("ao", 7), ("au", 7), ("aa", 7), 
 ("ea", 7), ("eo", 7), ("eu", 7), ("ee", 7), ("eau", 7),
 ("ia", 7), ("io", 7), ("iu", 7), ("ii", 7),
 ("oa", 7), ("oe", 7), ("oi", 7), ("ou", 7), ("oo", 7),
 ("'", 4),
 ("y", 7),
 ("ay", 7), ("ay", 7), ("ei", 7), ("ei", 7), ("ei", 7),
 ("ua", 7), ("ua", 7),
];

# List of possible consonants.

consonants= [
("b", 7),  ("c", 7),  ("d", 7),  ("f", 7),	("g", 7),  ("h", 7), 
("j", 7),  ("k", 7),  ("l", 7),  ("m", 7),	("n", 7),  ("p", 7), 
("qu", 6),	("r", 7), ("s", 7),  ("t", 7),	("v", 7),  ("w", 7),
("x", 7),  ("y", 7),  ("z", 7), 
# Blends, sorted by second character:
("sc", 7),
("ch", 7),	("gh", 7),	("ph", 7), ("sh", 7),  ("th", 7), ("wh", 6),
("ck", 5),	("nk", 5),	("rk", 5), ("sk", 7),  ("wk", 0),
("cl", 6),	("fl", 6),	("gl", 6), ("kl", 6),  ("ll", 6), ("pl", 6), ("sl", 6),
("br", 6),	("cr", 6),	("dr", 6),	("fr", 6),	("gr", 6),	("kr", 6), 
("pr", 6),	("sr", 6),	("tr", 6),
("ss", 5),
("st", 7),	("str", 6),
# Repeat some entries to make them more common.
("b", 7),  ("c", 7),  ("d", 7),  ("f", 7),	("g", 7),  ("h", 7), 
("j", 7),  ("k", 7),  ("l", 7),  ("m", 7),	("n", 7),  ("p", 7), 
("r", 7), ("s", 7),  ("t", 7),	("v", 7),  ("w", 7),
("b", 7),  ("c", 7),  ("d", 7),  ("f", 7),	("g", 7),  ("h", 7), 
("j", 7),  ("k", 7),  ("l", 7),  ("m", 7),	("n", 7),  ("p", 7), 
("r", 7), ("s", 7),  ("t", 7),	("v", 7),  ("w", 7),
("br", 6),	("dr", 6),	("fr", 6),	("gr", 6),	("kr", 6),
# ("x", 7), ("x", 7), ("x", 7), ("x", 7), ("x", 7), ("xx", 7), ("xx",5),
]

def diceinit(n):
	global die
	die=n

die=0

class RandError(Exception):
	pass

def rolldie (minvalue,maxvalue):
	""" Return a random value between minvalue and maxvalue, inclusive,
		 with equal probability.
	"""
	global die
	if die==0:
		raise RandError("No randomness left in the pool")
	diff=maxvalue-minvalue+1
	
	if diff <=0 :
		raise ValueError("Minvalue greater than Maxvalue")
	r=die % diff
	die=die/diff
	return r+minvalue


# Create a random name.  It must have at least between minsyl and maxsyl
# number of syllables (inclusive).
def RandomName(minsyl,maxsyl): 
	genname = ""		 # this accumulates the generated name.
	leng = rolldie(minsyl, maxsyl) # Compute number of syllables in the name
	isvowel = rolldie(0, 1); # randomly start with vowel or consonant
	for i in xrange(1, leng+1):  # syllable #. Start is 1 (not 0)
		# Pick a potential syllable until we find a good one.
		# The "extra" FINDSYLLABLE block is necessary to counter a Perl
		# bug - the "last" command doesn't work correctly in "do" blocks.
		ok=False
		while not ok:
			if isvowel:
				data= vowels[rolldie(0, len(vowels)-1)];
			else :
				data= consonants[rolldie(0, len(consonants)-1)];
			# Check if this syllable can occur in this part of the name.
			if	i == 1 : # first syllable.
				if (data[1] & 2):
					break
			elif i == leng:  # last syllable.
				if (data[1] & 1):
					break
			else : # Middle syllable
				if data[1] & 4 :
					break
			
			# If got here, it wasn't an okay pick. Try again.
		genname += data[0]	# Found good one, add to name.
		isvowel= 1 - isvowel # Alternate between vowels and consonants.
	return genname.title()

if __name__ == "__main__":
# MAINV
#======================================================
# Allows these values to be args...
	import sys
	if len(sys.argv)<2:
		print >>sys.stderr,"Please specify 256-bit hash value in hex as first argument"
		sys.exit(1)
	if len(sys.argv[1])!=64:
		print >>sys.stderr,"Invalid hash length. Shoudl be 64 hex digits"
		sys.exit(1)
	try:
		diceinit(int(sys.argv[1],16))
	except ValueError as e:
		print >>sys.stderr,e.message
		sys.exit(1)
	finish=False
	n=""
	while not finish:
		try:
			n+=RandomName(MINSYL,MAXSYL)+" "
		except RandError:
			finish=True
	print n
