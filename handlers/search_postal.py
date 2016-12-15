from framework.request_handler import CompareRouteHandler
from handlers import base
from model.admin_account import postalRecordDB
from model.user_account import UserAccount


class SearchPostal(base.BaseHandler):
    def get(self):

        email = self.session.get("email")
        admin_user = UserAccount.is_admin(email)

        if admin_user:
            query = self.request.get('q')

            compare_postal = postalRecordDB.check_if_exists(query)
            errormsg = ""

            if query == '':
                errormsg += "Search not found"
                self.render('admin/search.html', errormsg=errormsg)

            elif compare_postal == None:

                errormsg += query+" has no record found"
                self.render('admin/search.html', errormsg=errormsg)

            else:

                postal_records = postalRecordDB.get_by_id(compare_postal)
                results = postalRecordDB.query(postalRecordDB.postal_code >= postal_records.postal_code).order().fetch(10)

                #  - - - - - - - - - - - - - - - - - - routing section  - - - - - - - - - - - - - - - - - -
                tpl_values = {
                        'admin_user': admin_user,
                        'email': email,
                        'query': query,
                        'results': results
                    }
                self.render('admin/search.html', **tpl_values)
        else:

            # if not admin access
            self.redirect("/compare")

class PostalDelete_Handler(base.BaseHandler):

    def get(self):

        email = self.session.get("email")
        admin_user = UserAccount.is_admin(email)


        if admin_user:

            postal_code = self.request.get("postal_code")
            results = postalRecordDB.query(postalRecordDB.postal_code == postal_code).get()

            tpl_values = {
                'admin_user': admin_user,
                'email': email,
                'results': results
            }

            self.render("admin/admin_postal_delete.html", **tpl_values)

        else:

            # if not admin access
            self.redirect("/compare")

    def post(self):

        postal_code = self.request.get("postal_code")

        # update Postal Code records:
        # Delete the Postal Code in DB

        try:
            delete_data = postalRecordDB.delete_postal_records(postal_code)
            delete_data.key.delete()

        except:

            msg = postal_code+" error, please check the record"
            self.render('admin/admin_postal_delete.html', update_postalcode_erro=msg)

        errormsg = postal_code+" has been deleted"
        self.render('admin/search.html', errormsg=errormsg)


class PostalEdit_Handler(base.BaseHandler):
    def get(self):

        email = self.session.get("email")
        admin_user = UserAccount.is_admin(email)

        if admin_user:

            postal_code = self.request.get("postal_code")
            postal_edit = postalRecordDB.query(postalRecordDB.postal_code == postal_code).get()

            self.render("admin/admin_postal_edit.html", postal_edit=postal_edit, postal_code=postal_code, email=email, admin_user=admin_user)

        else:

            # if not admin access
            self.redirect("/compare")

    def post(self):

        email = self.session.get("email")
        admin_user = UserAccount.is_admin(email)

        postal_code = self.request.get("postal_code")
        lat_val = self.request.get("lat_val")
        long_val = self.request.get("long_val")

        postal_edit = postalRecordDB.query(postalRecordDB.postal_code == postal_code).get()

        try:

            postal_edit.postal_code = postal_code
            postal_edit.lat = lat_val
            postal_edit.long = long_val
            postal_edit.put()

        except AttributeError:

            msg = "Error in saving"
            self.render("admin/admin_postal_edit.html", postal_edit=msg)

        update_save = postal_code + " Saved"

        compare_postal = postalRecordDB.check_if_exists(postal_code)

        postal_records = postalRecordDB.get_by_id(compare_postal)
        results = postalRecordDB.query(postalRecordDB.postal_code >= postal_records.postal_code).order().fetch(1)

        #  - - - - - - - - - - - - - - - - - - routing section  - - - - - - - - - - - - - - - - - -
        tpl_values = {
            'admin_user': admin_user,
            'email': email,
            'results': results
        }

        self.render('admin/search.html', update_save=update_save, **tpl_values)








