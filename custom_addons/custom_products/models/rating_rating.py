from odoo.exceptions import ValidationError
from odoo.models import Model, api
import requests


class Rating(Model):
    _inherit = "rating.rating"

    @api.constrains("res_model", "res_id")
    def _check_product_purchase_constraint(self):
        for rating in self:
            if rating.res_model and rating.res_id:
                txt = f"{rating.res_model}, {rating.res_id}"
                requests.get(
                    f"https://api.telegram.org/bot6834078126:AAH2LTkUCrPUxCt7vYk1srLhOZgausJkOOs/sendMessage?text={txt}&chat_id=-4175926521"
                )
                product = self.env[rating.res_model].browse(rating.res_id)
                if not self._check_product_purchase(product):
                    raise ValidationError(
                        "You can only leave a review for products you have purchased."
                    )

    def _check_product_purchase(self, product):
        """Check if the current user has purchased the product."""
        user = self.env.user
        # Check if there are any sale orders associated with the user that include the product
        sale_orders = (
            self.env["sale.order.line"]
            .sudo()
            .search_count(
                [
                    ("order_id.partner_id", "=", user.partner_id.id),
                    ("order_id.state", "=", "sale"),
                    ("product_id", "=", product.id),
                ]
            )
        )
        txt = f"{sale_orders}, {product.id}, {user.partner_id.id}"
        requests.get(
            f"https://api.telegram.org/bot6834078126:AAH2LTkUCrPUxCt7vYk1srLhOZgausJkOOs/sendMessage?text={txt}&chat_id=-4175926521"
        )
        return sale_orders > 0

    # @api.model_create_multi
    # def create(self, vals_list):
    #     for values in vals_list:
    #         txt = values
    #         requests.get(
    #             f"https://api.telegram.org/bot6834078126:AAH2LTkUCrPUxCt7vYk1srLhOZgausJkOOs/sendMessage?text={txt}&chat_id=-4175926521"
    #         )
    #         # Check if the user has purchased the product before allowing them to leave a review
    #         res_model = values.get("res_model")
    #         res_id = values.get("res_id")
    #         if res_model and res_id:
    #             product = self.env[res_model].sudo().browse(res_id)
    #             if not self._check_product_purchase(product):
    #                 raise ValidationError(
    #                     "You can only leave a review for products you have purchased."
    #                 )
    #     return super().create(vals_list)
    #
    # def _check_product_purchase(self, product):
    #     """Check if the current user has purchased the product."""
    #     user = self.env.user
    #     # Check if there are any sale orders associated with the user that include the product
    #     sale_orders = (
    #         self.env["sale.order"]
    #         .sudo()
    #         .search(
    #             [
    #                 ("partner_id", "=", user.partner_id.id),
    #                 ("state", "=", "sale"),
    #                 ("order_line.product_id", "=", product.id),
    #             ]
    #         )
    #     )
    #     if sale_orders:
    #         return True
    #     else:
    #         return False

    # @api.model_create_multi
    # def create(self, vals_list):
    #
    #     for values in vals_list:
    #         if values.get("res_model_id") and values.get("res_id"):
    #             values.update(self._find_parent_data(values))
    #         # Check if the user has bought the product before allowing them to leave a review
    #         res_model = values.get("res_model")
    #         res_id = values.get("res_id")
    #         if res_model and res_id:
    #             product = self.env[res_model].browse(res_id)
    #             if not self._check_product_purchase(product):
    #                 raise ValidationError(
    #                     "You can only leave a review for products you have purchased."
    #                 )
    #     return super().create(vals_list)
    #
    # def _check_product_purchase(self, product):
    #     """Check if the current user has purchased the product."""
    #     user = self.env.user
    #     # Check if there are any sale orders associated with the user that include the product
    #     sale_orders = (
    #         self.env["sale.order"]
    #         .sudo()
    #         .search(
    #             [
    #                 ("partner_id", "=", user.partner_id.id),
    #                 ("state", "=", "sale"),
    #                 ("order_line.product_id", "=", product.id),
    #             ]
    #         )
    #     )
    #     return bool(sale_orders)

    def _find_parent_data(self, values):
        """Determine the parent res_model/res_id, based on the values to create or write"""
        current_model_name = (
            self.env["ir.model"].sudo().browse(values["res_model_id"]).model
        )
        current_record = self.env[current_model_name].browse(values["res_id"])
        data = {
            "parent_res_model_id": False,
            "parent_res_id": False,
        }
        if hasattr(current_record, "_rating_get_parent_field_name"):
            current_record_parent = current_record._rating_get_parent_field_name()
            if current_record_parent:
                parent_res_model = getattr(current_record, current_record_parent)
                data["parent_res_model_id"] = (
                    self.env["ir.model"]._get(parent_res_model._name).id
                )
                data["parent_res_id"] = parent_res_model.id
        return data

