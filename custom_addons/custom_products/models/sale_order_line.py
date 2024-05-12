from odoo.exceptions import ValidationError
from odoo.models import Model, api
from odoo import fields


class SaleOrderLine(Model):
    _inherit = "sale.order.line"

    @api.constrains("product_id")
    def _check_product_quantity(self):
        for line in self:
            if line.product_id and line.product_id.required_quantity > line.product_uom_qty:
                raise ValidationError("Required quantity is not met")
