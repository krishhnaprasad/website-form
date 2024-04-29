from odoo import models, fields, api


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    lpp = fields.Float(string="Last purchased Price", compute="_compute_last_purchase_price")

    @api.onchange("product_id")
    def _compute_last_purchase_price(self):
        if self.product_id:
            last_purchase_line = self.env['purchase.order.line'].search([
                ('product_id', '=', self.product_id.id),
                ('order_id.state', '=', 'purchase'),
            ], order='create_date desc', limit=1)
            if last_purchase_line:
                self.lpp = last_purchase_line.price_unit
            else:
                self.lpp = 0.0
