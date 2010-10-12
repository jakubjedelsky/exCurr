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
import sys

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
	del data[0] # datum nechceme
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
	
	# Options
	USAGE = "%prog [options] CASTKA"
	DESCR = "Prevede CASTKA z nebo na CZK (ceske koruny) podle aktualniho \
kurzu Ceske narodni banky (CNB). Hodnota je zaokrouhlena na dve desetinna \
mista. Pro oddeleni desetinnych mist pouzijte tecku."
	EPILOG = "Zdojovy kod ke stazeni naleznete na \
<http://github.com/jakubjedelsky/exCurr>. Pripadne chyby muzete zaslat \
na <jakub.jedelsky@gmail.com>."

	parser = OptionParser(usage=USAGE, description=DESCR, epilog=EPILOG, add_help_option=None)
	parser.add_option("-h", "--help", action="help",
					help="zobrazi tuto napovedu a skonci")
	parser.add_option("-f", "--from", dest="from_curr",
					help="Urcuje z jake meny bude prevadet na CZK", metavar="KOD_MENY")
	parser.add_option("-t", "--to", dest="to_curr",
					help="Urcuje na jakou menu bude z CZK prevadet.", metavar="KOD_MENY")
	parser.add_option("-l", "--list", action="store_true",
					help="vypis kurzu dle CNB (Ceska nardni banka)")
	parser.add_option("-a", action="store_true",
					help="Vypise dostupne kody men a skonci.")
	
	(options, args) = parser.parse_args()
	# End Options
	
	if options.from_curr and options.to_curr:
		parse.error("Je mozne pouzit jen jednu z voleb -f/--from nebo -t/--to.")
	
	if len(args) > 1:
		parser.error("Muzete zadat maximalne jeden argument typu CASTKA (cislo).")
	
	data = get_data()
	
	if options.to_curr:
		try:
			castka = float(args[0])
		except (IndexError, ValueError):
			sys.exit("Nezadali jste CASTKA nebo zadana hodnota neni cislo.\nNapovedu lze zobrazit pomoci prepinace '-h'.")
		mena = options.to_curr
		kurz = get_curr(data, mena)
		if not kurz:
			sys.exit("Kurz nenalezen, je mena zadana spravne?\nDostupne kody men vypisete pomoci prepinace '-a'")
		kurz_en = re.sub(',', '.', kurz[1])		# desetinna cisla chceme s teckou
		
		vysledek = castka * (int(kurz[0])/float(kurz_en))
		print "%.2f %s" % (vysledek, mena)
	
	if options.from_curr:
		try:
			castka = float(args[0])
		except (IndexError, ValueError):
			sys.exit("Nezadali jste CASTKA nebo zadana hodnota neni cislo.\nNapovedu lze zobrazit pomoci prepinace '-h'.")
		mena = options.from_curr
		kurz = get_curr(data, mena)
		if not kurz:
			sys.exit("Kurz nenalezen, je mena zadana spravne?\nDostupne kody men vypisete pomoci prepinace '-a'")
		kurz_en = re.sub(',', '.', kurz[1])		# desetinna cisla chceme s teckou
		
		vysledek = castka * (float(kurz_en)/int(kurz[0]))
		print "%.2f CZK" % vysledek
	
	if options.a:
		mena = list_curr(data)
		for i in mena:
			print i
	
	if options.list:
		print "Omlouvte snizenou kvalitu tabulky..\n-----------------------------------"
		list_data(data)

if __name__ == "__main__":
	main()
