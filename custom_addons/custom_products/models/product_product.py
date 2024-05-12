from odoo.exceptions import ValidationError
from odoo.models import Model, api
from odoo import fields


class Product(Model):
    _inherit = "product.template"

    required_quantity = fields.Integer(string="Required Quantity", default=1)

    @api.constrains("required_quantity")
    def _check_required_quantity(self):
        if self.required_quantity <= 0:
            raise ValidationError("Required Quantity must be positive")
