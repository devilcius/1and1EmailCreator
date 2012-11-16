#!/usr/bin/env python
# coding=utf-8
import urllib
import urllib2
import mechanize

class AuthError(Exception):
	pass

class EmailAccountCreator (object):
	
	loginURL = 'https://clientes.1and1.es/xml/config/Login'
	createEmailURL = 'https://clientes.1and1.es/xml/config/Email_EditTargets'
	commitedEmailURL = 'https://clientes.1and1.es/xml/config/Email_Committed'
	newEmailAccountURL = 'https://clientes.1and1.es/xml/config/Email_Overview'
	userAgent = 'Mozilla/6.0 (Windows NT 6.2; WOW64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1'

	
	def __init__(self, data):
	
		self.headers = {'User-Agent' : EmailAccountCreator.userAgent}		
		self.jsessionid = None
		self.referer = None
		self.fixedurl = None
		self.oneandoneuser = data['oneandoneuser']
		self.onenandonepassword = data['oneandonepassword']
		self.emaildomainname = data['domainname'] 
		self.emailusername = data['emailusername']
		self.emaildisplayname = data['emaildisplayname']	
		self.emailfirstname = data['emailfirstname']
		self.emaillastname = data['emaillastname']
		self.emailpassword = data['emailpassword']
		self.emailaccount = "%s@%s" % (self.emailusername,self.emaildomainname)
					
				
	def submitForm(self):
		br = mechanize.Browser()		
		
		# Don't handle cookies!!!
		br.set_cookiejar(None)
		
		# Browser options
		br.set_handle_equiv(True)
		# br.set_handle_gzip(True)
		br.set_handle_redirect(True)
		br.set_handle_referer(True)
		br.set_handle_robots(False)		
		
		br.addheaders = [('User-Agent', EmailAccountCreator.userAgent)]
		
		# Follows refresh 0 but not hangs on refresh > 0
		br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
		
		# Want debugging messages?
		# br.set_debug_http(True)
		# br.set_debug_redirects(True)
		# br.set_debug_responses(True)				
		
		# First we need the right url to create a new email account
		request = urllib2.Request(EmailAccountCreator.newEmailAccountURL + ";" + self.jsessionid + '?__frame=_top&__lf=email_delete_flow&__sendingdata=1&selectEmail.CreateType=mbox&selectEmail.Action=CREATE&__pageflow=email_create_flow', None, self.headers)
		response = urllib2.urlopen(request)
		self.fixedurl = response.geturl()				
		
		br.open(self.fixedurl)			

		print "creating account %s..." % self.emailaccount
		
		br.set_handle_redirect(True)

		br.form = list(br.forms())[0]
		
		control = br.form.find_control("address.Domainname")
		control.value = [self.emaildomainname]
		control = br.form.find_control("address.Localpart")
		control.value = self.emailusername
		control = br.form.find_control("mbox.Password.0")
		control.value = self.emailpassword
		control = br.form.find_control("mbox.PasswordRepeated.0")
		control.value = self.emailpassword
		control = br.form.find_control("ox.DisplayName.0")
		control.value = self.emaildisplayname
		control = br.form.find_control("ox.FirstName.0")
		control.value = self.emailfirstname
		control = br.form.find_control("ox.LastName.0")
		control.value = self.emaillastname
		control = br.form.find_control("target.Type.0")
		control.value = ["mbox"]	
		control = br.form.find_control("ox.NotUpgradable.0")
		control.value = ["true"]	
				
		# self.createEmailAccount(postdata)
		# for control in br.form.controls:
			# print ' ', control.type, control.name, repr(control.value)			
		
		req = br.click(type="submit", nr=0)
		response = br.open(req)
		
		content = response.get_data()
		if self.emailaccount in content:
			print "email account %s created succesfully!" % self.emailaccount
		else:
			print "somenthing went wrong creating the email account"
		
		# with open("buh.html", "a") as f:
			# f.write(content)
			# f.close()

			
	def authenticate(self):
		loginformdata = {"__SBMT:d0e672d1": "",
							"__lf": "HomeFlow",
							"__sendingauthdata": 1,
							"__sendingdata": 1,
							"login.Pass": self.onenandonepassword,
							"login.SelectContract": "",	
							"login.User": self.oneandoneuser}
		
		data = urllib.urlencode(loginformdata)
		request = urllib2.Request(EmailAccountCreator.loginURL + ";" + self.jsessionid, data, self.headers)
		response = urllib2.urlopen(request)
		url = response.geturl()
		responsebody = response.read() 
		if "Panel de Control" in responsebody:
			print "authenticated to 1and1"
			# print "with jsessionid " + url[url.find(";")+1:]
			self.referer = url[url.find(";")+1:]
			#self.jsessionid = url[url.find(";")+1:]			
			self.submitForm()
		else:
			print "cannot login to 1and1"
			
			
	def createAccount(self):
		# first step: login
		request = urllib2.Request(EmailAccountCreator.loginURL, None, self.headers)
		response = urllib2.urlopen(request)
		url = response.geturl()
		if "Panel de Control" in response.read():
			self.jsessionid = url[url.find(";")+1:]
			print "attempting to authenticate to server..."
			# print "with sessionid " + self.jsessionid
			self.authenticate()
		else:
			print "cannot connect to login page"
			
		
if __name__ == "__main__":
	print "Module to create 1and1 email account"