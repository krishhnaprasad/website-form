# report_wizard.py (if needed)
from odoo import models, fields, api


class ReportWizard(models.TransientModel):
    _name = "report.wizard"

    patient_id = fields.Char(string="Patient Name")
    date_from = fields.Char(string="Symptom")
    date_to = fields.Char(string="Fees")
    total_count = fields.Integer(string="Total Count", compute='_compute_sales_count', store=True)
