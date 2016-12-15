import csv
import webapp2
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import taskqueue
from model.admin_account import postalRecordDB
from framework.request_handler import CompareRouteHandler

import logging

# import json



class CSVUploaderHandler(CompareRouteHandler):
    def get(self):

        results = postalRecordDB.query().order(postalRecordDB.postal_code).fetch(1000)
        self.render('admin/uploader.html', results=results)


class MainHandler3(webapp2.RequestHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/admin-csv-load')

        html_string = """
         <form action="%s" method="POST" enctype="multipart/form-data">
        Upload File:
        <input type="file" name="file"> <br>
        <input type="submit" name="submit" value="Submit">
        </form>""" % upload_url

        self.response.write(html_string)


class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload_files = self.get_uploads('file')  # 'file' is file upload field in the form

        blob_info = upload_files[0]
        process_csv(blob_info)

        blobstore.delete(blob_info.key())  # optional: delete file after import
        self.redirect("/admin-csv")



def process_csv(blob_info):

    blob_reader = blobstore.BlobReader(blob_info.key())
    reader = csv.reader(blob_reader, delimiter=',')

    for row in reader:
        print row
        postal_code, long, lat = row

        taskqueue.add(url='/admin-csv-taskq',
                      params=({'postal_code': postal_code,
                               'long': long,
                               'lat': lat
                               })
                      )

        print ('Task added to the queue.')

class TaskqHandler(webapp2.RequestHandler):
    def post(self):

        if not 'X-AppEngine-TaskName' in self.request.headers:
               self.error(403)

        postal_code = self.request.get('postal_code')
        long = self.request.get('long')
        lat = self.request.get('lat')

        logging.info(postal_code)

        postalRecordDB.add_new_records(postal_code, long, lat)

