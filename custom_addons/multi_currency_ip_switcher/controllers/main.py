from odoo import http
from odoo.http import request
import requests


class MultiCurrencySwitcher(http.Controller):
    @http.route("/currency/", type="http", auth="public")
    def switch_currency(self, **kw):
        client_ip = request.httprequest.environ["REMOTE_ADDR"]
        currency = requests.get(f"https://ipapi.co/{client_ip}/currency/").text
        return currency
