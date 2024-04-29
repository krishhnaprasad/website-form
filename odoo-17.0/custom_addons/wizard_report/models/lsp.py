from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    lsp = fields.Float(string="Last Sold Price", compute="_compute_last_sold_price")

    @api.onchange("product_id")
    def _compute_last_sold_price(self):
        if self.product_id:
            last_sale_line = self.env['sale.order.line'].search([
                ('product_id', '=', self.product_id.id),
                ('order_id.state', '=', 'sale'),
            ], order='create_date desc', limit=1)
            if last_sale_line:
                self.lsp = last_sale_line.price_unit
            else:
                self.lsp = 0.0
