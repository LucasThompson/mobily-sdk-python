# mobily-python

## Examples
*All examples assume you have a mobily.ws account with an available balance*

**_Managing your mobily.ws account_**

Request to change account password:

```python
from mobily.utilities import MobilyApiAuth
from mobily.account import MobilyAccount
account = MobilyAccount(MobilyApiAuth('966555555555', 'demo'))
account.change_password('TrustNo1')
```

Get current password sent to email or phone:

```python
account.forgot_password()  # send to email registered on account
account.forgot_password(send_to_email=False)  # send to phone registered on account
```

Check the available balance on the account:

```python
balance = account.check_balance()
print '{0} credits available, total {1}'.format(balance['current'], balance['total'])
```


**_Configuring Senders_**

Check the activation status of all previously requested senders:

```python
from mobily.utilities import MobilyApiAuth
from mobily.sender import MobilySender
sender = MobilySender(MobilyApiAuth('966555555555', 'demo'))
senders_by_status = sender.get_activation_status_for_all_senders()
print 'Active Senders:', [sender for sender in senders_by_status['active']]
print 'Pending Senders:', [sender for sender in senders_by_status['pending']]
print 'Inactive Senders:', [sender for sender in senders_by_status['notActive']]
```

Request to add a new sender word name:

```python
sender.request_alphabetical_license('NEW SMS')
```

Two step process for activating a mobile number as a sender name:

```python
sender_id = sender.request_mobile_number_license('966444444444')
#  the above call returns an id if successful, and a code is sent via SMS to the number
sender.activate_mobile_number_license(sender_id, 'CODE_FROM_SMS')

#  check it worked
if sender.is_mobile_number_license_active(sender_id):
    print 'Activated!'
```


**_Sending SMS messages_**

Check the Mobily.ws SMS sending service is available:

```python
from mobily.sms import MobilySMS
if MobilySMS.can_send():
    print 'Service is available!'
```

Send SMS, immediately, saying 'Hello, World' to 966444444444, from 'YOUR MOM':

```python
from mobily.utilities import MobilyApiAuth
from mobily.sms import MobilySMS
sms = MobilySMS(MobilyApiAuth('966555555555', 'demo'))
sms.add_number('966444444444')
sms.sender = 'YOUR MOM'
sms.msg = 'Hello, World!'
sms.send()
```

As above, but using constructor, and sending to multiple numbers:

```python
auth = MobilyApiAuth('966555555555', 'demo')
sms = MobilySMS(auth, ['96202258669', '967965811686'], 'YOUR MOM', 'Hello, World!')
sms.send()
```

As above, but schedule to send on 25th December 2020 at midday:

```python
auth = MobilyApiAuth('966555555555', 'demo')
sms = MobilySMS(auth, ['96202258669', '967965811686'], 'YOUR MOM', 'Hello, World!')
sms.schedule_to_send_on(25, 12, 2017, 12, 0, 0)
sms.delete_key('666')
sms.send()
```

Delete the above scheduled SMS before it sends:

```python
sms.delete()
```

Send a bulk SMS to multiple people, letting them know about their subscription, with personalised messages just for them:

```python
from mobily.utilities import MobilyApiAuth
from mobily.sms import MobilyFormattedSMS

auth = MobilyApiAuth('966555555555', 'demo')
msg = 'Hi (1), your subscription will end on (2).'
sms = MobilyFormattedSMS(auth, ['966505555555', '966504444444'], 'NEW SMS', msg)
sms.add_variable_for_number('966505555555', '(1)', 'Ahmad')
sms.add_variable_for_number('966505555555', '(2)', '31/12/2013')
sms.add_variable_for_number('966504444444', '(1)', 'Mohamed')
sms.add_variable_for_number('966504444444', '(2)', '01/11/2013')
sms.send()
```


**_Handling errors_**

When a request has been unsuccessful, whether due to a known error (insufficient balance), or otherwise, an MobilyApiError is raised.

This error contains a message in English and Arabic.

```python
from mobily.utilities import MobilyApiAuth, MobilyApiError
from mobily.account import MobilyAccount

account = MobilyAccount(MobilyApiAuth('DOESNT_EXIST', 'demo'))
try:
    response = request_handler.handle()
except MobilyApiError => error:
    print error.msg_english, error.msg_arabic
```


## Tests
Tests for the core logic behind the utilities can be run from the terminal with:
```bash
     python -m unittest discover -v
```