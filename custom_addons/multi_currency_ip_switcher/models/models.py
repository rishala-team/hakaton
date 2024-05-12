from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"
    _name = "currency_model"
    currency_map_ids = fields.Many2many("res.currency", string="Currency Mapping")
