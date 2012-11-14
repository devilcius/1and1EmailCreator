#!/usr/bin/env python
import cookielib
import urllib
import urllib2
import os
import sys
import re
import mechanize
from collections import defaultdict

class AuthError(Exception):
	pass

class EmailAccountCreator:
	
	loginURL = 'https://clientes.1and1.es/xml/config/Login'
	createEmailURL = 'https://clientes.1and1.es/xml/config/Email_EditTargets'
	#Location: https://clientes.1and1.es:443/xml/config/Email_Committed;jsessionid=A4FA8A68D788FE0736C16807F79E126D.TCpfix311b?__reuse=1352917068690&__frame=&__lf=email_create_flow

	userAgent = 'Mozilla/6.0 (Windows NT 6.2; WOW64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1'
	clientContract = "41265403"
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

	
	def __init__(self):
		self.headers = {'User-Agent' : EmailAccountCreator.userAgent}		
		self.jsessionid = None
		self.referer = None
				
				
	def createEmailAccount(self):
		data = urllib.urlencode(EmailAccountCreator.createemailformdata)		
		headers = {"Host": "clientes.1and1.es",
				   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
				   "Connection" : "keep-alive",
				   "Referer" : self.referer,
				   "Content-Type": "application/x-www-form-urlencoded",
				   "Content-Length" : len(data)
				   }
		redirectionHandler = urllib2.HTTPRedirectHandler()
		opener = urllib2.build_opener(redirectionHandler)
		urllib2.install_opener(opener)
		request = urllib2.Request(EmailAccountCreator.createEmailURL + ";" + self.jsessionid + "?__frame=", data, headers)
		response = urllib2.urlopen(request)
		responsebody = re.sub('<script type="text/javascript">[^<]+</script>', '', response.read())

		if "finalizada" in responsebody:
			print "email account created ok!"
			with open("okresponse.html", "a") as f:
				f.write(responsebody)				
		else:
			print "error while creating the account"
			with open("errorresponse.html", "a") as f:
				f.write(responsebody)
				
	def getFormData(self):
		br = mechanize.Browser()
		
		# Cookie Jar
		#cj = cookielib.LWPCookieJar()
		#br.set_cookiejar(cj)
		
		# Browser options
		br.set_handle_equiv(True)
		br.set_handle_gzip(True)
		br.set_handle_redirect(True)
		br.set_handle_referer(True)
		br.set_handle_robots(False)		
		
		# Follows refresh 0 but not hangs on refresh > 0
		#br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
		
		# Want debugging messages?
		br.set_debug_http(True)
		br.set_debug_redirects(True)
		br.set_debug_responses(True)				
		
		br.open(EmailAccountCreator.createEmailURL + ";" + self.jsessionid)
		br.form = list(br.forms())[0]
		
		control = br.form.find_control("address.Domainname")
		control.value = ["augc.info"]
		control = br.form.find_control("address.Localpart")
		control.value = "prueba26"
		control = br.form.find_control("mbox.Password.0")
		control.value = "1234567"
		control = br.form.find_control("mbox.PasswordRepeated.0")
		control.value = "1234567"
		control = br.form.find_control("ox.DisplayName.0")
		control.value = "pr26"
		control = br.form.find_control("ox.DisplayName.0")
		control.value = "buhbaho"
		control = br.form.find_control("ox.FirstName.0")
		control.value = "afadfa"
		control = br.form.find_control("ox.LastName.0")
		control.value = "dddddd"
		control = br.form.find_control("target.Type.0")
		control.value = ["mbox"]	
	
		
		#for control in br.form.controls:
		#	print ' ', control.type, control.name, repr(control.value)
		
		response = br.submit()
		content = response.get_data()		
		with open("buh.html", "a") as f:
			f.write(content)	
		quit()
			
	def authenticate(self):
		data = urllib.urlencode(EmailAccountCreator.loginformdata)
		request = urllib2.Request(EmailAccountCreator.loginURL + ";" + self.jsessionid, data)
		response = urllib2.urlopen(request)
		url = response.geturl()
		responsebody = response.read() 
		if EmailAccountCreator.clientContract in responsebody:
			print "authenticated to 1and1"
			self.referer = url[url.find(";")+1:]
			#self.jsessionid = url[url.find(";")+1:]			
			self.getFormData()
		else:
			print "cannot login to 1and1"
			
			
	def getLoginPage(self):
		request = urllib2.Request(EmailAccountCreator.loginURL)
		response = urllib2.urlopen(request)
		url = response.geturl()
		if "Panel de Control" in response.read():
			self.jsessionid = url[url.find(";")+1:]
			print "attempting to authenticate to server..."
			self.authenticate()
		else:
			print "cannot connect to login page"
		
		
if __name__ == "__main__":
	
	emailcreator = EmailAccountCreator()
	emailcreator.getLoginPage()
	#print emailcreator.jsessionid

