from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    area = fields.Char(string="Area")


class ResCompany(models.Model):
    _inherit = 'res.company'

    trn = fields.Integer(string="Tax Registration Number")


class AccountMove(models.Model):
    _inherit = 'account.move'

    delivery_charge = fields.Monetary(string='Delivery Charge', compute='_compute_delivery_charge', store=True)

    @api.depends('partner_id')
    def _compute_delivery_charge(self):
        for move in self:
            if move.partner_id.area == 'Local':
                move.delivery_charge = 5.00
            else:
                move.delivery_charge = 10.00
