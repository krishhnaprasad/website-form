from odoo import models, fields, api
from odoo.exceptions import UserError


class ButtonForm(models.Model):
    _inherit = 'res.partner'

    state = fields.Selection([('draft', 'Draft'), ('approved', 'Approved')])
    approve = fields.Boolean(string='Approve')

    def approved_function(self):
        self.approve = True

    @api.model
    def create(self, vals):
        if vals.get('approve'):
            # If the 'approve' field is set, create the record
            return super(ButtonForm, self).create(vals)
        else:
            raise UserError('Please approve before saving.')

    def write(self, vals):
        if vals.get('approve'):
            # If the 'approve' field is set, allow saving
            return super(ButtonForm, self).write(vals)
        else:
            raise UserError('Please approve before saving....')
