from google.appengine.ext import ndb
from hashlib import sha256
from base64 import b64encode
from os import urandom
import uuid
import os


class UserAccount(ndb.Model):
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    company = ndb.StringProperty()
    confirmation_code = ndb.StringProperty(required=True)
    confirmation_email = ndb.BooleanProperty(default=False)
    user_admin = ndb.BooleanProperty(default=False)
    api_key = ndb.StringProperty()
    api_credits = ndb.IntegerProperty(default=50)


    @classmethod
    def check_if_exists(cls, email):
        return cls.query(cls.email == email).get()

    # User Credit
    @classmethod
    def check_credit_usage(cls, email):
        user = cls.check_if_exists(email)

        if user:
            use_credit = 1
            current = user.api_credits

            if int(current) <= 0:
                return None

            else:
                # -1 for every hit Generate button
                current_num = user.api_credits - use_credit
                user.api_credits = current_num
                user.put()

                return True
        else:
            return None

    @classmethod
    def add_new_user(cls, name, email, company, password):
        user = cls.check_if_exists(email)

        # API and Wep App Usage Credit
        defaultCredits = 100

        if not user:
            # do the stuff
            random_bytes = urandom(64)
            salt = b64encode(random_bytes).decode('utf-8')
            hashed_password = salt + sha256(salt + password).hexdigest()

            # Email Confirmation
            confirmation_code = str(uuid.uuid4().get_hex())

            # API
            api_key = os.urandom(24).encode('hex')
            api_credits = defaultCredits

            new_user_key = cls(
                name=name,
                email=email,
                company=company,
                password=hashed_password,
                confirmation_code=confirmation_code,
                api_key=api_key,
                api_credits=api_credits

            ).put()

            # print new_user_key

            return {
                'created': True,
                'user_id': new_user_key.id(),
                'confirmation_code': confirmation_code
            }

        else:
            return {
                'created': False,
                'title': 'This email is already in use',
                'message': 'Please login if this your email account'
            }

    # LOGIN Credentials

    @classmethod
    def check_password(cls, email, password):
        user = cls.check_if_exists(email)

        if user:
            hashed_password = user.password

            # fix length character as assuming is 88
            salt = hashed_password[:88]

            check_password = salt + sha256(salt + password).hexdigest()

            if check_password == hashed_password and user.confirmation_email:
                return user.key.id()
            else:
                return None
        else:
            return None

    # API LOGIN Access
    @classmethod
    def check_API_auth(cls, email, key):
        user = cls.check_if_exists(email)

        if user:
            stored_key = user.api_key
            check_password = key
            if check_password == stored_key:
                return True
            else:
                return None
        else:
            return None

    @classmethod
    def create_api_key(cls, email):
        user = cls.check_if_exists(email)

        if user:
            new_api_key = user.api_key

            return new_api_key

    @classmethod
    def createHashed_password(cls, password):

        random_bytes = urandom(64)
        salt = b64encode(random_bytes).decode('utf-8')
        newHashed_password = salt + sha256(salt + password).hexdigest()

        return newHashed_password

    # Updating Password:
    @classmethod
    def check_password_record(cls, email, password):
        user = cls.check_if_exists(email)

        if user:
            hashed_password = user.password

            # Fix length character as assuming is 88
            salt = hashed_password[:88]

            check_password = salt + sha256(salt + password).hexdigest()
            return check_password
        else:
            return None

     #### validation loging

    @classmethod
    def getUserByIdAndCode(cls, code):
        return cls.query(cls.confirmation_code == code).get()

    @classmethod
    def activateUser(cls, user):
        user.confirmation_email = True
        user.put()

    @classmethod
    def get_user_id(cls, email):
        user_id = cls.query(cls.email == email).get(keys_only=True)

        if user_id:
            user_id = user_id.id()
            return user_id
        else:
            return None

    @classmethod
    def check_emails(cls, email):
        user = cls.check_if_exists(email)
        if user:

            user_confirmation_code = user.confirmation_code
            user_id = user.key.id()

            return {
                'created': True,
                'user_id': user_id,
                'confirmation_code': user_confirmation_code
            }
        else:
            return {
                'created': False,
                'title': 'Email is not found',
                'message': 'Please make sure you use your registered email address'
            }

    @classmethod
    def is_admin(cls, email):
        user_id = cls.check_if_exists(email)

        if user_id:

            # Check if user is admin:
            if user_id.user_admin == True:

                return True
            else:
                # if not, return none:
                return False
        else:
            return None