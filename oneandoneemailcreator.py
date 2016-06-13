#!/usr/bin/env python
# coding=utf-8
import urllib
import urllib2
import ssl
import cookielib

class AuthError(Exception):
	pass	
	
class EmailAccountCreator (object):
	
	loginURL = 'https://account.1and1.es'
	createEmailURL = 'https://clientes.1and1.es/create-basic-email'
	userAgent = 'Mozilla/6.0 (Windows NT 6.2; WOW64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1'

	
	def __init__(self, username, password):
		self.oneandoneuser = username
		self.onenandonepassword = password
		self.headers = {'User-Agent' : EmailAccountCreator.userAgent}
		self.cookies = cookielib.LWPCookieJar()
		handlers = [
			urllib2.HTTPHandler(),
			urllib2.HTTPSHandler(),
			urllib2.HTTPCookieProcessor(self.cookies)
			]
		ctx = ssl.create_default_context()
		ctx.check_hostname = False
		ctx.verify_mode = ssl.CERT_NONE			
		self.opener = urllib2.build_opener(urllib2.HTTPSHandler(context=ctx), *handlers)		
		self.authenticate()
								
			
	def authenticate(self):
		# get cookie from login page
		request = urllib2.Request(EmailAccountCreator.loginURL)
		response = self.opener.open(request)
		
		loginformdata = {"__lf": "Login",
							"__sendingdata": 1,
							"oaologin.password": self.onenandonepassword,
							"oaologin.username": self.oneandoneuser}
		
		data = urllib.urlencode(loginformdata)
		request = urllib2.Request(EmailAccountCreator.loginURL, data, self.headers)
		response = self.opener.open(request)
		responsebody = response.read() 
		if "Panel de Control" in responsebody:
			print "authenticated to 1and1"
		else:
			print "cannot login to 1and1"
			
		
	def createAccount(self, data):
		emaildomainname = data['domainname'] 
		emailusername = data['emailusername']
		emaildisplayname = data['emaildisplayname']	
		emailfirstname = data['emailfirstname']
		emaillastname = data['emaillastname']
		emailpassword = data['emailpassword']
		emailaccount = "%s@%s" % (emailusername, emaildomainname)	
	
		newAccountData = {"__lf": "create-basic-email-flow",
							"create-basic.type": "MAILACCOUNT_STANDARD",
							"create-basic.isOrderRequired": "false",
							"create-basic.email": emailusername,
							"create-basic.domain": emaildomainname,
							"create-basic.firstName": emailfirstname,
							"create-basic.lastName": emaillastname,
							"create-basic.password": emailpassword,
							"create-basic.repeatPassword": emailpassword,
							"__sendingdata": 1,
							"__SBMT:d0e8796d2:":""}
		
		data = urllib.urlencode(newAccountData)
		request = urllib2.Request(EmailAccountCreator.createEmailURL, data, self.headers)
		response = self.opener.open(request)
		url = response.geturl()
		responsebody = response.read() 
		if emailaccount in responsebody:
			print "Account %s created successfully" % emailaccount
		else:
			print "Cannot create account"		
			
		
if __name__ == "__main__":
	print "Module to create 1and1 email account"