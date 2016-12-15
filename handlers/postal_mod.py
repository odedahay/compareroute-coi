from framework.request_handler import CompareRouteHandler
import webapp2
from handlers import base
from model.admin_account import postalRecordDB


# class Add_new_postal(CompareRouteHandler):
class Add_new_postal(base.BaseHandler):
    def get(self):

        email = self.session.get("email")

        self.render('admin/admin_postal_new_global.html',  email=email)

    def post(self):

        email = self.session.get("email")

        # Get the data from form:
        postal_code = self.request.get("postal_code")
        longtitude = self.request.get("longtitude_val")
        latitude = self.request.get("latitude_val")

        print postal_code, longtitude, latitude
        msg =""
        status = []

        if len(postal_code) != 6:
            success = False
            msg = "Invalid Postal Code"

            status.append(success)
            status.append(msg)
            return status
        else:

            # update Postal Code records:
            updateStatus = postalRecordDB.add_new_records(postal_code, longtitude, latitude)
            updateStatus = updateStatus.id()

            new_postal_code = postalRecordDB.get_by_id(updateStatus)

            if new_postal_code == None:
                success = False
                msg = "No Postal Code Added"

            else:
                success = True
                msg = "Successful added"

        if success == False:

            self.render('admin/admin_postal_new_global.html', postal_update_error=msg)
        else:
            self.render('admin/admin_postal_new_global.html', postal_update_success=msg, email=email)




