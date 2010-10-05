#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# prevod kurzu CZK <-> jina mena (podle CNB)
# GNU GPL v3
# author: Jakub Jedelsky <jakub.jedelsky@gmail.com>
#

from optparse import OptionParser
import re
import urllib2
import string

class gv:
	"""
	Globalni promenne.
	"""
	verze = "10^-1"
	url = "http://www.cnb.cz/cs/financni_trhy/devizovy_trh/kurzy_devizoveho_trhu/denni_kurz.txt"

def get_data(date=False):
	# TODO:
	# - vyber podle data
	# - cache; ukladani txt do pc, aby se to nemuselo furt stahovat
	"""
	Vrati pole se aktualnim kurzem. [0] je datum a den v roce, [1] je hlavicka.
	"""
	
	url = gv.url

	if date:
		pass

	try:
		page = urllib2.urlopen(url)
		data = page.read()
		page.close
	except:
		print "Nemohu nacist kurzy men, pravdepodobne chyba pri pripojeni."
		return False

	data = data.splitlines()
	return data

def get_curr(data, mena):
	"""
	Vrati pole s kurzem pro danou menu. [0] je mnozstvi, [1] kurz.
	"""
	kurz = []
	for radek in data:
		r = radek.split("|")
		if r[3] == mena:
			kurz.append(r[2])
			kurz.append(r[4])
			break
	if kurz:
		return kurz
	else:
		return False

def list_data(data):
	"""
	Prehledne vypise tabulku s kurzy.
	"""
	datum = data[0]
	del data[0]
	
	print "Datum: " + datum
	for radek in data:
		r = radek.split("|")
		print string.ljust(r[0], 20), 
		print string.ljust(r[1], 10),
		print string.ljust(r[2], 10),
		print string.ljust(r[3], 10),
		print string.ljust(r[4], 10)
		#print "%20s %20s %20s %20s %20s" % (r[0], r[1], r[2], r[3], r[4])

def list_curr(data):
	"""
	Vrati pole s menami.
	"""
	del data[0:2]
	mena = []
	for radek in data:
		r = radek.split("|")
		mena.append(r[3])
	return mena

def main():
	pass

if __name__ == "__main__":
	main()
