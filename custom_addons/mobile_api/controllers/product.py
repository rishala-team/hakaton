from odoo import http
from odoo.http import request
import json
import base64


class ProductController(http.Controller):
    @http.route(
        "/web/products", type="http", auth="public", methods=["GET"], csrf=False
    )
    def get_products(self, page, per_page):
        page = int(page)
        per_page = int(per_page)
        offset = (page - 1) * per_page
        products = (
            request.env["product.product"]
            .sudo()
            .search([], limit=per_page, offset=offset)
        )
        product_data = []
        for product in products:
            image_url = None
            if product.image_1920:
                image_url = "/web/image/product.product/%s/image_1920" % product.id
            product_data.append(
                {
                    "id": product.id,
                    "name": product.name,
                    "description": product.description_sale
                    if product.description_sale
                    else "",
                    "price": product.list_price,
                    "category_id": product.categ_id.id if product.categ_id else None,
                    "category_name": product.categ_id.name
                    if product.categ_id
                    else None,
                    "image": image_url,
                }
            )
        return http.Response(json.dumps(product_data), content_type="application/json")
