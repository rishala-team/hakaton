from datetime import datetime, timedelta
from collections import Counter
from odoo.models import expression, fields, Model
from odoo import api


class WebsiteSnippetFilter(Model):
    _inherit = "website.snippet.filter"

    @api.model
    def _get_products(self, mode, context):
        dynamic_filter = context.get("dynamic_filter")
        handler = getattr(
            self, "_get_products_%s" % mode, self._get_products_customize_filter
        )
        website = self.env["website"].get_current_website()
        search_domain = context.get("search_domain")
        limit = context.get("limit")
        domain = expression.AND(
            [
                [("website_published", "=", True)],
                website.website_domain(),
                [("company_id", "in", [False, website.company_id.id])],
                search_domain or [],
            ]
        )
        products = handler(website, limit, domain, context)
        return dynamic_filter._filter_records_to_values(products, False)

    # def _get_products_customize_filter(self, website, limit, domain, context):
    #     products = []
    #     visitor = self.env["website.visitor"]._get_visitor_from_request()
    #     if visitor:
    #         excluded_products = website.sale_get_order().order_line.product_id.ids
    #         tracked_products = (
    #             self.env["website.track"]
    #             .sudo()
    #             .read_group(
    #                 [
    #                     ("visitor_id", "=", visitor.id),
    #                     ("product_id", "!=", False),
    #                     ("product_id.website_published", "=", True),
    #                     ("product_id", "not in", excluded_products),
    #                 ],
    #                 ["product_id", "visit_datetime:max"],
    #                 ["product_id"],
    #                 limit=limit,
    #                 orderby="visit_datetime DESC",
    #             )
    #         )
    #         products_ids = [product["product_id"][0] for product in tracked_products]
    #         if products_ids:
    #             domain = expression.AND(
    #                 [
    #                     domain,
    #                     [("id", "in", products_ids)],
    #                 ]
    #             )
    #             products = (
    #                 self.env["product.product"]
    #                 .with_context(display_default_code=False, add2cart_rerender=True)
    #                 .search(domain, limit=limit)
    #             )
    #     return products
    def _get_products_customize_filter(self, website, limit, domain, context):
        products = []

        # Determine the start and end dates of the current week
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        # Filter sale orders and their products for the current week
        sale_orders = (
            self.env["sale.order"]
            .sudo()
            .search(
                [
                    ("website_id", "=", website.id),
                    ("state", "=", "sale"),
                    ("date_order", ">=", start_of_week),
                    ("date_order", "<=", end_of_week),
                ],
                limit=8,  # Limit the number of orders to fetch
                order="date_order DESC",
            )
        )

        if sale_orders:
            # Get the IDs of the most sold products
            sold_products = [p.product_id.id for p in sale_orders.order_line]
            products_ids = [id for id, _ in Counter(sold_products).most_common()]

            if products_ids:
                # Update the domain to include product IDs and any additional criteria
                domain = expression.AND(
                    [
                        domain,
                        [("id", "in", products_ids)],
                    ]
                )
                # Retrieve the most sold products in the current week
                products = (
                    self.env["product.product"]
                    .with_context(display_default_code=False)
                    .search(domain)
                )
                # Sort products based on their order of sale
                products = products.sorted(key=lambda p: products_ids.index(p.id))[
                    :limit
                ]

        return products
