import webapp2
from handlers import base
from google.appengine.api import mail


class EmailInfo(base.BaseHandler):
    def post(self):
        email = self.session.get('email')
        postal = self.request.get('starting_postal')
        original = self.request.get('original')
        generated = self.request.get('generated')

        message = mail.EmailMessage()
        #message.sender = 'edmundchan1976@gmail.com'
        message.sender = 'noreply@compare-route-3.appspotmail.com'
        message.to = 'comparerouterp@gmail.com'
        message.body = """
                    Company Name: {0}
                    Verison: 0.1.0
                    Staring Postal: {1}
                    Original Sequence : {2}
                    New Sequence: {3}
                            """.format(email, postal, original, generated)
        message.send()


app = webapp2.WSGIApplication([
    ('/email_info', EmailInfo)
], config=base.sessionConfig, debug=True)
