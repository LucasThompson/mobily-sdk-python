# mobily-python

## Examples
*All examples assume you have a mobily.ws account with an available balance *

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

## Tests
Tests for the core logic behind the utilities can be run from the terminal with:
```bash
     python -m unittest discover -v
```