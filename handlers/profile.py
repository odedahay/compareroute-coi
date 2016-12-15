from handlers import base
from model.user_account import UserAccount

class ProfilePage(base.BaseHandler):
    def get(self):

        email = self.session.get("email")
        admin_user = UserAccount.is_admin(email)
        user_account = UserAccount.check_if_exists(email)

        if email:
            ws_key = self.session.get("ws_key")
            self.render("/compare/compare_user_profile.html", email=email, ws_key=ws_key, user_account=user_account, admin_user=admin_user)
        else:
            self.render("/login/login.html", register_error="Please login!")

    def post(self):

        email = self.session.get("email")
        admin_user = UserAccount.is_admin(email)
        ws_key = self.session.get("ws_key")

        user_account = UserAccount.check_if_exists(email)

        # From user input:
        old_password = self.request.get("old_password")
        new_password = self.request.get("new_password")
        cfm_new_password = self.request.get("cfm_new_password")

        # Validate user credentials:
        change_password_status = self.changePassword(email, old_password, new_password, cfm_new_password)

        success = change_password_status[0]
        msg = change_password_status[1]

        #  - - - - - - - - - - - - - - - - - - routing section  - - - - - - - - - - - - - - -
        template_values = {
            'ws_key': ws_key,
            'admin_user': admin_user,
            'email': email,
            'user_account': user_account,
        }

        if success == False:
            self.render("/compare/compare_user_profile.html", change_password_error=msg, **template_values)
        else:
            self.render("/compare/compare_user_profile.html", change_password_success=msg, **template_values)

    def changePassword(self, email, old_password, new_password, cfm_new_password):
        # Status for change password
        status = []
        success = False
        msg = ""

        userPassword = UserAccount.check_password(email, old_password)

        # If user does not exist, send an error message
        if userPassword == None:
            success += False
            msg += "Wrong old password!"
            status.append(success)
            status.append(msg)

            return status

        else:

            # Find userRecord:
            userRecord = UserAccount.query(UserAccount.email == email).get()

            # Generate password hash from password input
            newHashed_password = UserAccount.createHashed_password(cfm_new_password)

            # Update the DataStore
            userRecord.password = newHashed_password
            userRecord.put()

            success += True
            msg += "Password changed!"
            status.append(success)
            status.append(msg)

            return status