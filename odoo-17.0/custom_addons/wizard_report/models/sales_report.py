# report_wizard.py (if needed)
from odoo import models, fields, api


class PdfReportWizard(models.TransientModel):
    _name = "sales.report"

    sales_person = fields.Many2one('res.users', string="Sales Person")
    date_from = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")
    total_count = fields.Integer(string="Total Count", compute='_compute_sales_count')


class ResUsers(models.Model):
    _inherit = 'res.users'

    is_salesperson = fields.Boolean(string="Is Salesperson")
