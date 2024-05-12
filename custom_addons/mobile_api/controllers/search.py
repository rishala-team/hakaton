from odoo import http
from odoo.http import request
import json
import base64


class ProductController(http.Controller):
    @http.route(
        "/web/products/search", type="http", auth="public", methods=["GET"], csrf=False
    )
    def search_products(self, **kwargs):
        name = kwargs.get("name")
        domain = []
        if name:
            domain += [("name", "ilike", name)]
        products = request.env["product.template"].sudo().search(domain)
        product_data = []
        for product in products:
            image_url = None
            if product.image_1920:
                image_data = base64.b64encode(product.image_1920).decode("utf-8")
                image_url = f"data:image/png;base64,{image_data}"
            product_data.append(
                {
                    "id": product.id,
                    "name": product.name,
                    "description": product.description,
                    "price": product.list_price,
                    "category_id": product.categ_id.id if product.categ_id else None,
                    "category_name": product.categ_id.name
                    if product.categ_id
                    else None,
                    "image": image_url,
                }
            )

        return http.Response(json.dumps(product_data), content_type="application/json")
