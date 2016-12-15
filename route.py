from webapp2 import WSGIApplication
from webapp2 import Route

app = WSGIApplication(
    routes=[
        Route('/', handler='app.home.Home'),
        Route('/register', handler='app.register.RegisterHandler'),
        Route('/account/<user_id:[0-9]+>/login/confirmation_code:[a-z0-9]{32}>', handler='app.register.ConfirmUser'),
        Route('/login', handler='app.login.LoginHandler'),
        Route('/account', handler='app.account.UserAccount'),
        Route('/logout', handler='main.Logout'),
    ]
)
