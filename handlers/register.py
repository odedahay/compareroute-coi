from framework.request_handler import CompareRouteHandler
from model.user_account import UserAccount
from google.appengine.api import mail
from os import environ
import re

# http://compareroute-v1.appspot.com/

class RegisterHandler(CompareRouteHandler):

    @classmethod
    def send_email(cls, to, user_id, confirmation_code):
        email_object = mail.EmailMessage(
            sender='noreply@compareroute-v1.appspotmail.com',
            subject='Confirm your Compare Route account',
            to=to
        )
        email_parameters = {
            'domain': 'http://localhost:8080' if environ['SERVER_SOFTWARE'].startswith(
                'Development') else 'http://compareroute-v1.appspot.com/',
            'user_id': user_id,
            'confirmation_code': confirmation_code
        }

        html_from_template = cls.jinja_environment.get_template('email/confirmation_email.html').render(email_parameters)

        email_object.html = html_from_template
        email_object.send()

    def post(self):

        name = self.request.get('name')
        email = self.request.get('email')
        company = self.request.get('company')
        password = self.request.get('password')

        status = 200

        # JSON Validation for Forms:
        if name and email and company and password:
            email_validation_pattern = "(^[a-zA-Z0-9_.+]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

            if re.match(email_validation_pattern, email):
                user = UserAccount.add_new_user(name, email, company, password)
                # print user

                if user['created']:
                    html = self.jinja_environment.get_template('commons/register_success.html').render()
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
                    'title': 'The email is not valid',
                    'message': 'Please enter a valid email address'
                }

        else:
            status = 400
            json_response = {}

            if not name:
                json_response.update({
                    'title': 'The name field is required',
                    'message': 'Please fill in your name in order to continue'
                })
            if not email:
                json_response.update({
                    'title': 'You have not sent us an email',
                    'message': 'Please send us a valid email address, thanks!'
                })
            if not password:
                json_response.update({
                    'title': 'Please type in a password',
                    'message': 'Please fill in your password in order to continue'
                })

        self.json_response(status_code=status, **json_response)


class ConfirmUser(CompareRouteHandler):
    def get(self, user_id, confirmation_code):
        user = UserAccount.get_by_id(int(user_id))

        if user:
            if UserAccount.confirmation_code == confirmation_code:
                UserAccount.confirmed_email = True
                UserAccount.put()

        self.redirect('/login')

