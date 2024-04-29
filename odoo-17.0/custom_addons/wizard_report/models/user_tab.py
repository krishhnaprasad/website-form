from odoo import models, fields


class AllowedProducts(models.Model):
    _inherit = 'res.users'

    r_type = fields.Selection([('product', 'Product'), ('category', 'Category')], string="Restriction type")
