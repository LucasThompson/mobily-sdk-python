class MobilyAccount:
    def __init__(self):
        pass

    def change_password(self):
        # changePassword api method wrapper
        pass

    def forgot_password(self):
        # forgotPassword api method wrapper
        pass

    def check_balance(self):
        # balance api method wrapper
        pass


class MobilyAuth:
    def __init__(self, mobile_number, password):
        self.mobile_number = mobile_number
        self.password = password
