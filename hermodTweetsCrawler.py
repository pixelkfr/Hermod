#!/usr/bin/env python
# -*- coding: utf-8 -*-

import twitter
import getopt, sys, os, json

"""
This script allow you to use the search API to find tweets. You can choose a language and a seed word.
You will recive 100 tweets.
"""

def tweetsCrawler( language=None, word=None, fileout=None, filelog=None ):
	
	if fileout:
		try:
			fileoutObj = open( os.path.abspath( fileout ), 'a' )
		except Exception, err:
			msg = "[ERROR] tweetsCrawler.py: file %s cannot be open : %s\n" % ( fileout, err )
			sys.exit( msg.encode( 'UTF-8' ) )
	else:
		fileoutObj = sys.stdout

	if filelog:
		try:
			filelogObj = open( os.path.abspath( filelog ), 'a' )
		except Exception, err:
			msg = "[ERROR] tweetsCrawler.py: file %s cannot be open : %s\n" % ( filelog, err )
			sys.exit( msg.encode( 'UTF-8' ) )

	if language:
		chosenLanguage=str(language)
	else:
		chosenLanguage="en"
	
	if word:
		chosenWord=str(word)
	else:
		chosenWord="hello"
	
	#LAUNCH THE SEARCH API REQUEST
	search = api.GetSearch(term=chosenWord, lang=chosenLanguage, count=100)
	
	for tweet in search:
		texte = tweet.text.encode("utf-8")
		date = tweet.created_at.encode("utf-8")
		userName = tweet.user.screen_name.encode("utf-8")
		source = tweet.source.encode("utf-8")
		source = source.split(">")[1]
		source = source.split("<")[0]
		
		LIST_OF_CERTIFIED_SOURCES=['Twitter Web Client', 'Mobile Web (M2)', 'Twitter for Android', 'Twitter for Windows', 'Twitter for BlackBerry®', 'Twitter for BlackBerry', 'Twitter for Windows Phone', 'Twitter for Android Tablets', 'Twitter for Android', 'Twitter for iPhone', 'Twitterfeed', 'The Tribez for Android', 'TweetDeck', 'Facebook', 'Tweetbot for iOS', 'Google', 'Tweet Button', 'Twitter for iPad']

	  #SOURCE_CHECK
		if source not in LIST_OF_CERTIFIED_SOURCES:
			if filelog:
				filelog.write( source + "[ERROR] not a certified source \n" )
			else:
				print ("source error " + source)
		else:
			#CLEANING
			texte = texte.replace("\n"," ")
			texte = texte.replace('\"','"')
			texte = texte.replace("\\\"" , "\"")
			texte = texte.replace("&lt;" , "<")
			texte = texte.replace("&gt;" , ">")
			texte = texte.replace("&amp;" , "&")
			texte = texte.replace("&euro;" , "€")
			texte = texte.replace("&pound;" , "£")
			texte = texte.replace("\\r", " ")
			if fileout:
				#OUTPUT FILE CONTENT
				fileoutObj.write("<-- " + "Date: " + date + " Username: " + userName + " Source: " + source + " -->\n")
				fileoutObj.write(texte + "\n")
				fileoutObj.write("\n")
			else:
				print ("<-- " + date + " - " + userName + " --> " + "\n" + texte + "\n")
		
if __name__ == "__main__":

	def usage():
		msg = """Usage: hermodTweetsCrawler.py [-W WORD] [-L LANG] [-O OUTPUT FILE ] [-LG LOG FILE ] CONSUMER_KEY CONSUMER_SECRET ACCESS_TOKEN ACCESS_TOKEN_SECRET

	-l --language		use this language to find tweets
	-w, --word			use this word to find tweets
	-o, --output=FILE	write result in a FILE
	-lg --log=FILE		write log and errors in a FILE
	-h, --help			display help and exit
"""
		sys.stderr.write( msg.encode( 'UTF-8' ) )

	try:
		opts, args = getopt.getopt( sys.argv[1:], "l:w:ho:lg:", ["word=", "language=", "help", "output=", "log="] )
	except getopt.GetoptError, err:
		sys.stderr.write( str( err ) )
		usage()
		sys.exit(2)

	fileout = language = word = filelog = None

	for o, a in opts:
		if o in ( "-h", "--help" ):
			usage()
			sys.exit()
		elif o in ( "-o", "--output" ):
			fileout = a.strip()
		elif o in ( "-w", "--word=" ):
			word = a.strip()
		elif o in ( "-l", "--language=" ):
			language = a.strip()
		elif o in ( "-lg", "--log" ):
			filelog = a.strip()
		else:
			assert False, "unhandled option"

	if len( args ) != 4:
		print len( args )
		usage()
		sys.exit(2)
	else:
		CONSUMER_KEY = args[0]
		CONSUMER_SECRET = args[1]
		ACCESS_TOKEN = args[2]
		ACCESS_TOKEN_SECRET = args[3]
		
	api = twitter.Api(
		consumer_key=CONSUMER_KEY,
		consumer_secret=CONSUMER_SECRET,
		access_token_key=ACCESS_TOKEN,
		access_token_secret=ACCESS_TOKEN_SECRET
	 )

	tweetsCrawler( language, word, fileout, filelog )
