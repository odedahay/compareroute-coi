from handlers import base
from model.admin_account import RouteDistance


class SummaryBMapHandler(base.BaseHandler):
    def get(self):

        routes = RouteDistance.query().order(-RouteDistance.created_date).fetch(1)
        self.render("/compare/compare_sum_table.html", routes=routes)
