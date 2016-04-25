# mobily-python

## Examples
All examples assume you have a mobily.ws account with an available balance

* Managing your mobily.ws account *

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

* Configuring Senders *

Check the activation status of all previously requested senders:

```python
from mobily.utilities import MobilyApiAuth
from mobily.sender import MobilySender
sender = MobilySender(MobilyApiAuth('966555555555', 'demo'))
senders_by_status = sender.get_activation_status_for_all_senders()
print 'Active Senders:', [sender for sender in d['active']]
print 'Pending Senders:', [sender for sender in d['pending']]
print 'Inactive Senders:', [sender for sender in d['notActive']]
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

* Sending SMS messages *



## Tests
Tests for the core logic behind the utilities can be run from the terminal with:
```bash
     python -m unittest discover -v
```