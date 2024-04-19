# appointment_report.py
from odoo import api, fields, models


class AppointmentReportWizard(models.TransientModel):
    _name = "appointment.report.wizard"
    _description = "Print appointment wizard"

    patient_id = fields.Char(string="Patient Name")
    date_from = fields.Char(string="Symptom")
    date_to = fields.Char(string="fee")

    def print_excel_report(self):
        demo = self.env['report.wizard'].search_read([])
        data = {
            'demo': demo,
            'form_data': self.read()[0]
        }
        return self.env.ref('wizard_report.appointment_xls').report_action(self, data=data)

    def save_data(self):
        data = self.env['report.wizard'].create({
            'patient_id': self.patient_id,
            'date_from': self.date_from,
            'date_to': self.date_to,
        })

    def print_pdf_report(self):
        demo = self.env['report.wizard'].search_read([])
        data = {
            'demo': demo,
            'model': 'appointment.report.wizard',
            'form_data': self.read()[0]
        }
        return self.env.ref('wizard_report.pdf_report_action').report_action(self, data=data)

