#!/usr/bin/env python
from ghost import Ghost
import cookielib
import urllib
import urllib2
from lxml import html
import pickle
import os
import sys
import re

class AuthError(Exception):
	pass

class EmailCreator:
	
	loginURL = 'https://clientes.1and1.es/xml/config/Login'
	createEmailURL = '	https://clientes.1and1.es:443/xml/config/Email_Committed'
	userAgent = 'Mozilla/6.0 (Windows NT 6.2; WOW64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1'
	loginformdata = {"__SBMT:d0e672d1": "",
						"__lf": "HomeFlow",
						"__sendingauthdata": 1,
						"__sendingdata": 1,
						"login.Pass": "Au11111111",
						"login.SelectContract": "",	
						"login.User":"augc.info"}
	createemailformdata = {"__SBMT:d0e31897d0:":"",
						"__SYNT:d0e31897d0:__CMD[Email_EditTargets]:SELWRP":"selectEmail",
						"__SYNT:d0e31897d0:__CMD[Email_EditTargets]:SELWRP":"address",
						"__SYNT:d0e31897d0:__CMD[Email_EditTargets]:SELWRP":"target",
						"__SYNT:d0e31897d0:__CMD[Email_EditTargets]:SELWRP":"ox",
						"__SYNT:d0e31897d0:__CMD[Email_EditTargets]:SELWRP":"mbox",
						"__SYNT:d0e31897d0:__CMD[Email_EditTargets]:SELWRP":"mail",
						"__SYNT:d0e31897d0:__CMD[Email_EditTargets]:SELWRP":"sms",
						"__SYNT:d0e31897d0:__CMD[Email_EditTargets]:SELWRP":"fax",
						"__SYNT:d0e31897d0:__CMD[Email_EditTargets]:SELWRP":"virusprotection",
						"__SYNT:d0e31897d0:__CMD[Email_EditTargets]:SELWRP":"spamfilter",
						"__SYNT:d0e31897d0:__CMD[Email_EditTargets]:SELWRP":"addon",
						"__SYNT:d0e31897d0:__CMD[Email_EditTargets]:SELWRP":"check",
						"__SYNT:d0e31897d0:tuneup.Artikelgruppe":"32",
						"__SYNT:d0e31897d0:tuneup.Artikelnummer":"1",
						"__SYNT:d0e31897d0:tuneup.Featurenummer":"0",
						"__SYNT:d0e31897d0:tuneup.Quantitaet":"1",
						"__lf":"email_create_flow",
						"__sendingdata":"1",
						"address.Domainname":"augc.info",
						"address.Localpart":"prueba3",
						"mbox.Password.0":"1234567",
						"mbox.PasswordRepeated.0":"1234567",
						"ox.DisplayName.0":"pr3",
						"ox.FirstName.0":"pruebo",
						"ox.LastName.0":"tres",
						"target.Type.0":"mbox"
						}

	def __init__(self, cookie):
		self.headers = {}		
		self.jsessionid = None
		self.cookieFile = cookie
		self.getGhostPage()
		self.authenticate()
		
	def setUpCookiesAndUserAgent(self):
	
		self.ghost = None
		cookieJar = cookielib.LWPCookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
		opener.addheaders = [('User-Agent', EmailCreator.userAgent)]
		urllib2.install_opener(opener)
	
		self.loadCookiesFromFile(cookieJar)
	
		try:
			self.authenticate()
			print "using cookie"
		except AuthError:
			self.getFreshCookies()

	def loadCookiesFromFile(self, cookieJar):
		try:
			cookieJar.load(self.cookieFile)
		except IOError:
			self.authenticate()
			cookieJar.save(self.cookieFile)

	def getFreshCookies(self):
		cookieJar = cookielib.LWPCookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
		opener.addheaders = [('User-Agent', EmailCreator.userAgent)]
		urllib2.install_opener(opener)
		self.authenticate()
		cookieJar.save(self.cookieFile)
		print "new cookie created"
		
	def setCookie(self, response):
		print "creating cookie"
		f = open('cookie', 'w')
		try:
			cookie = dict(response.headers)['set-cookie']
			session = re.search("__.+=[^;]+", cookie).group(0)
			session = session[0:session.find(";")]
			self.headers["Cookie"] = session
			pickle.dump(self.headers, f)
			
		except (KeyError, AttributeError):
			f.close()
			os.remove('cookie')
			self.headers = None
			raise Exception("Login failed, most likely bad creds or the site is down, nothing to do")
		f.close()	
		
	def authenticate(self):
		data = urllib.urlencode(EmailCreator.loginformdata)
		request = urllib2.Request(EmailCreator.loginURL + ";" + self.jsessionid, data)
		response = urllib2.urlopen(request)
		self.checkIfAuthenticated(response)
				
				
	def createEmailAccount(self):
		if self.ghost is None:
			self.ghost = Ghost()
		page, extra_resources = self.ghost.open("https://clientes.1and1.es/xml/config/Email_EditTargets" + ";" + self.jsessionid)
		result, resources = self.ghost.fill("form", EmailCreator.createemailformdata)
		page, resources = self.ghost.fire_on("form", "submit", expect_loading=True)
		print page.url
		
		
	def createEmail(self):
		data = urllib.urlencode(EmailCreator.createemailformdata)
		request = urllib2.Request(EmailCreator.createEmailURL + ";" + self.jsessionid, data)
		response = urllib2.urlopen(request)
		self.checkIfEmailCreated(response)	

	def checkIfAuthenticated(self, response):
		page = html.parse(response).getroot()
		#print html.tostring(page)
		if ('Panel de Control' not in page.xpath('head/title/text()')[0]):
		  raise AuthError('Login page returned, not logged in')
		else:
			self.createEmail()

	def checkIfEmailCreated(self, response):
		page = html.parse(response).getroot()
		print html.tostring(page)
		quit()
		if (page.xpath('head/title/text()')[0] != '1&1 Panel de Control'):
		  raise AuthError('Login page returned, not logged in')
		else:
			self.createEmail()
			
	def getGhostPage(self):
		self.ghost = Ghost()
		page, extra_resources = self.ghost.open("https://clientes.1and1.es/xml/config/Login")
		if page.http_status==200 and 'Acceso a su' in self.ghost.content:
			urlstring = str(page.url)
			self.jsessionid = urlstring[urlstring.find(";")+1:]			
		
if __name__ == "__main__":
	
	emailcreator = EmailCreator("cookie")
	print emailcreator.jsessionid

