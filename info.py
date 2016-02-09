#!/usr/bin/env python

import mechanize

def get_info(sid, pin):

	br = mechanize.Browser()

	br.set_handle_robots(False)

	br.open("https://uos.sharjah.ac.ae:9050/prod_enUS/twbkwbis.P_WWWLogin")

	br.select_form(nr=0)

	br["sid"] = sid
	br["PIN"] = pin

	br.submit()

	br.open("https://uos.sharjah.ac.ae:9050/prod_enUS/twbkwbis.P_GenMenu?name=bmenu.P_AdminMnu")

	for link in br.links():
		if link.url == "/prod_enUS/bwskotrn.P_ViewTermTran":
		    br.follow_link(link)

	br.select_form(nr=1)

	result = br.submit()

	return result.read()
