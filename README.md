#1and1EmailCreator
---

## A python module for automated 1and1 email accounts creation


Getting started:

```python

	#!/usr/bin/env python
	# coding=utf-8
    import oneandoneemailcreator
    
    emaildata = {
                'emailusername':'john.smith', 
                'emaildisplayname' : 'john smith', 
                'emailfirstname':'john', 
                'emaillastname':'smith',
                'emailpassword':'emailuserpass'
                }
    # create an instance of 1and1EmailCreator
	emailcreator = oneandoneemailcreator.EmailAccountCreator('clientdomain.com', '1and1clientSecretePass')
	emailcreator.createAccount(emaildata) 	
```	