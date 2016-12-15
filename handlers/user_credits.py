from handlers import base

# DB Account
from model.user_account import UserAccount


class summaryCredits(base.BaseHandler):
    def get(self):

        email = self.session.get("email")

        userAccounts = UserAccount.query().order().fetch()
        success = self.request.get("success")
        msg = ""

        if success:
            msg += "Save"


        template_values = {
            'email': email,
            'userAccounts': userAccounts,
            'update_success': msg,
        }
        self.render("admin/admin-credits.html", **template_values)


class summaryCredits_edit(base.BaseHandler):

    def get(self):

        email = self.session.get("email")

        user_id = self.request.get("id")
        user_account = UserAccount.get_by_id(int(user_id))
        user_id = user_account.email

        # user_id = self.request.get("user_email")
        user_accounts = UserAccount.query(UserAccount.email == user_id).get()

        template_values_get = {
            'email': email,
            'user_accounts': user_accounts,
        }
        self.render("admin/admin-credits-edit.html", **template_values_get)

    def post(self):

        # Credit Edit:
        credit = self.request.get("api_credits")

        success = True
        msg = ""

        user_id = self.request.get("user_id")
        user_account = UserAccount.get_by_id(int(user_id))
        user_id = user_account.email

        # user_id = self.request.get("user_email")
        user_accounts = UserAccount.query(UserAccount.email == user_id).get()

        if user_accounts:

            user_accounts.api_credits = int(credit)
            user_accounts.put()

            msg += "Successful Save"

        else:

            success = False
            msg += "Error in Credits Saving"

        # API Key function
        # api_key = os.urandom(24).encode('hex')

        template_values_post = {
            'user_accounts': user_accounts,
            'update_error': msg,
            'update_succes': msg,
        }

        if success == False:

            self.render("admin/admin-credits-edit.html", **template_values_post)
        else:
            self.redirect("/admin-credits?success=True")