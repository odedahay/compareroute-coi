import webapp2
from model.user_account import UserAccount

class ResetHandler(webapp2.RequestHandler):
    
    def changePassword(self, email, new_password, cfm_new_password):
        # Status for change password
        status = []
        success = False
        msg = ""
        
        # Generate password hash from password input
        userEmail = UserAccount.check_password_record(email)
        userRecord = UserAccount.query(UserAccount.email == email, UserAccount.password == userEmail).get()

        # If user does not exist, send an error message
        # Else, log the user in

        if not userRecord:

            pass

            # success = False
            # msg = "Wrong old password!"
            # status.append(success)
            # status.append(msg)
            #
            # return status

        else:

            if new_password != cfm_new_password:
                success = False
                msg = "Password mismatch!"
                status.append(success)
                status.append(msg)
                return status

            else:

                newHashed_password = UserAccount.createHashed_password(cfm_new_password)
                userRecord.password = newHashed_password
                userRecord.put()

                success = True
                msg = "Password changed!"
                status.append(success)
                status.append(msg)
                return status

class New_password_Handler(webapp2.RequestHandler):

    def reset_password(self, email, new_password):
        # Status for change password
        status = []
        success = False
        msg = ""

        # Check the User Record in DataStore
        user_record = UserAccount.query(UserAccount.email == email).get()

        if not user_record:
            success = False
            msg = "Password Failed!"
            status.append(success)
            status.append(msg)

            return status
        else:
            # Generate password hash from password input
            generated_hashed_password = UserAccount.createHashed_password(new_password)
            user_record.password = generated_hashed_password
            user_record.put()

            success = True
            msg = "Password changed!"
            status.append(success)
            status.append(msg)

            return status
