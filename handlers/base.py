import webapp2
from config import JINJA_ENV
from webapp2 import cached_property
from webapp2_extras import sessions

# Configure the session
sessionConfig = {}

sessionConfig["webapp2_extras.sessions"] = {
    "secret_key": "Arbitrary-Randomness-and-Unforeseen-Circumstances"
}


class BaseHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = JINJA_ENV.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

    def clearSession(self):
        # Clears the session
        self.session.clear()
