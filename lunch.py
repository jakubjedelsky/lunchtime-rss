#!/usr/bin/env python

import feedparser as fp
import codecs
import json

###################
#  Simple config

FEEDS = [
	'http://www.lunchtime.cz/rss/restaurant215.rss', # Nekonecno
	'http://www.lunchtime.cz/rss/restaurant7792.rss', # U seminaru
	'http://www.lunchtime.cz/rss/restaurant5024.rss', # Zakki
	'http://www.lunchtime.cz/rss/restaurant7778.rss' # Hospoda Stodola
]

OUTPUT_FILE = 'index.html'
CACHE = '.lunchfeed'
COLUMNS	= 2

#  Das ist ende
###################

HEAD = """
<html>
<head>
	<title>Let's go for a lunch!</title>
</head>
<html>
<table>
<tr>
"""
FOOTER = """
</tr>
</html>
</body>
"""

def read_cache(f):
	"""Just open cache file or init empty dict."""
	try:
		cache_file = open(f, 'r')
		cache = json.load(cache_file)
		cache_file.close()
	except IOError:
		cache = json.loads('{}')
	return cache

def write_cache(cache,f):
	"""Save dict as json file."""
	cf = open(f, 'w')
	json.dump(cache, cf)
	cf.close()
	return True

def init_cache(cache,key):
	"""Init cache key if it does not exists."""
	try:
		out = cache[key]
	except KeyError:
		cache[key] = {'modified': '', 'content': ''}
	return cache

def write_document(content):
	html = codecs.open(OUTPUT_FILE, 'w', 'utf-8')
	html.write(HEAD)
	html.write(content)
	html.write(FOOTER)
	html.close()
	return True


def main():

	c = read_cache(CACHE)
	col = 0
	content = ''
	for rest in FEEDS:
		cache = init_cache(c, rest)
			
		try:
			modified = cache[rest]['modified']
		except KeyError:
			modified = ''
		rss = fp.parse(rest, modified=modified)
		if rss.status == 304:
			print "%s: 304 : read from cache" % rest
			#print
			out = cache[rest]['content']
		else:
			print "read from web"
			#print
			out = rss['entries'][0]['description']
			cache[rest]['content'] = out
		
		if col < COLUMNS:
			col += 1
		else:
			content += "<tr>\n"
			col = 0

		content += "<td>%s</td>\n" % out
		
		cache[rest]['modified'] = rss.modified

	
	write_document(content)
	write_cache(cache, CACHE)


if __name__ == "__main__":
	main()
