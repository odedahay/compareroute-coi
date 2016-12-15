from framework.request_handler import CompareRouteHandler


class LoginHandler(CompareRouteHandler):

    def post(self):
        email = self.request.get('email')
        password = self.request.get('password')

        # print email, password
        # JSON Validation for Forms:
        if email and password:
            #success
            pass

        else:
            status = 400
            json_response = {}

            if not email:
                json_response.update({
                    'title': 'You have not sent us an email',
                    'message': 'Please send us a valid email address, thanks!'
                })
            if not password:
                json_response.update({
                    'title': 'Please type your password',
                    'message': 'Please fill in your password in order to continue'
                })

            self.json_response(status_code=status, **json_response)

class password_recover(CompareRouteHandler):
    def post(self):
        email = self.request.get('email')


