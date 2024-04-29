from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    area = fields.Char(string="Area")


class ResCompany(models.Model):
    _inherit = 'res.company'

    trn = fields.Integer(string="Tax Registration Number")


class AccountMove(models.Model):
    _inherit = 'account.move'

    delivery_charge = fields.Monetary(string="Delivery Charge")
