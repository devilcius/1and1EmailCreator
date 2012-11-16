#1and1EmailCreator

A python module for automated 1and1 email accounts creation


Getting started:

<pre>
import oneandoneemailcreator

emaildata = {'domainname':'domainname.com',
            'emailusername':'john.smith', 
            'emaildisplayname' : 'john smith', 
            'emailfirstname':'john', 
            'emaillastname':'smith',
            'emailpassword':'emailuserpass',
            'oneandoneuser': 'server.com' #domain name or client id,
            'oneandonepassword' : 'ultrasecretpass'
            }
# create an instance of 1and1EmailCreator
emailcreator = oneandoneemailcreator.EmailAccountCreator(emaildata)
# create account
emailcreator.createAccount()	

</pre>