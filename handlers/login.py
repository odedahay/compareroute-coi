from framework.request_handler import CompareRouteHandler
from model.user_account import UserAccount
import logging

from encryption import EncryptionHandler


class LoginHandler(CompareRouteHandler):
    def get(self):

        # check if activation code is provided
        # if yes, validate

        user_id = self.request.get('id')
        code = self.request.get('code')
        msg = ""

        if user_id != '' and code != '':
            user = UserAccount.getUserByIdAndCode(code)
            logging.info(user)
            # msg = "You're account is Validated"

            if user != None:
                UserAccount.activateUser(user)
                msg = "Your account is now confirmed. Please Sign in."

        self.render('/login/login.html', login_status=msg)

    def validateUser(self, email, password):
        # Status for login
        status = []
        success = False
        msg = ""

        user_id = UserAccount.check_password(email, password)

        print "user_id", user_id

        # If user does not exist, send an error message
        # Else, log the user in
        if user_id == None:
            success += False
            msg += "Wrong email/password!"
            status.append(success)
            status.append(msg)
            # self.render('/login.html')
            return status
        else:
            success += True
            msg += ""  # no message needed for a successful login
            status.append(success)
            status.append(msg)
            # status.append(user_id.ws_key)
            return status
