from odoo import api, fields, models


class Custom_Image(models.TransientModel):
    _inherit = ['res.config.settings']

    image_show = fields.Boolean(string="Image on sale order line",
                                config_parameter='sale.image_show')

    @api.model
    def set_values(self):
        self.env['ir.config_parameter'].sudo().set_param('wizard_report.image_show',
                                                         self.image_show)
        res = super(Custom_Image, self).set_values()
        return res

    def get_values(self):
        res = super(Custom_Image, self).get_values()
        custom = self.env['ir.config_parameter'].sudo().get_param('wizard_report.image_show',
                                                                  self.image_show)
        res.update(image_show=custom)
        return res

class ImageOnSaleOrder(models.Model):
    _inherit = 'sale.order.line'
    image_add = fields.Binary(string="Image", related="product_id.image_1920")


