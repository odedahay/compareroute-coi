from framework.request_handler import CompareRouteHandler
from model.user_account import UserAccount
from google.appengine.api import mail
from os import environ
import re

class PasswordRecover(CompareRouteHandler):

    @classmethod
    def send_email(cls, to, user_id, confirmation_code):

        email_object = mail.EmailMessage(
            sender='noreply@compare-route-3.appspotmail.com',
            subject='Reset your password',
            to=to
        )
        email_parameters = {

            'domain': 'http://localhost:8080' if environ['SERVER_SOFTWARE'].startswith(
                'Development') else 'http://compare-route-3.appspot.com',
            'user_id': user_id,
            'confirmation_code': confirmation_code
        }

        html_from_template = cls.jinja_environment.get_template('email/pass_recover_email.html').render(email_parameters)

        email_object.html = html_from_template
        email_object.send()

    def post(self):
        email = self.request.get('email')

        status = 200

        # JSON Validation for Forms:
        if email:
            email_validation_pattern = "(^[a-zA-Z0-9_.+]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

            if re.match(email_validation_pattern, email):
                user = UserAccount.check_emails(email)
                # print user

                if user['created']:
                    html = self.jinja_environment.get_template('commons/resetpassword_success.html').render()
                    json_response = {
                        'html': html
                    }
                    self.send_email(to=email, user_id=user['user_id'], confirmation_code=user['confirmation_code'])

                else:
                    status = 400
                    json_response = user
            else:
                status = 400
                json_response = {
                    'created': False,
                    'title': 'Email is not valid',
                    'message': 'Please enter a valid email address'
                }
        else:
            status = 400
            json_response = {}

            if not email:
                json_response.update({
                    'title': 'Email address is empty',
                    'message': 'Please provide email address, thanks!'
                })

        self.json_response(status_code=status, **json_response)

class ConfirmUser(CompareRouteHandler):
    def get(self, user_id, confirmation_code):
        user = UserAccount.get_by_id(int(user_id))

        if user:
            if user.confirmation_code == confirmation_code:
                user.confirmed_email = True
                user.put()

        self.redirect('/login')


