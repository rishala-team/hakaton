from odoo import http
from odoo.http import request


class Authentication(http.Controller):
    @http.route(
        "/web/register", type="json", auth="public", methods=["POST"], csrf=False
    )
    def authenticate(self, **rec):
        if request:
            if "name" in rec and "email" in rec and "password" in rec:
                vals_for_partner = {"name": rec["name"], "email": rec["email"]}
                new_user = request.env["res.partner"].sudo().create(vals_for_partner)
                vals_for_users = {
                    "partner_id": new_user.id,
                    "login": rec["email"],
                    "password": rec["password"],
                }
                request.env["res.users"].sudo().create(vals_for_users)
                args = {"status": 200, "message": "success", "id": new_user.id}
            else:
                return {"status": 400, "message": "musor blya tori yoz jalla"}
        return args
