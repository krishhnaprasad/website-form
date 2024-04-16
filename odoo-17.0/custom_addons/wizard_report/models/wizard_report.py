# my_module/models/wizard_report.py

from odoo import api, models


class MyWizard(models.TransientModel):
    _name = 'wizard_report'
    _description = 'Wizard for Report Generation'

    name = fields.Char(string='Name')
    age = fields.Integer(string='Age')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender')
    adhar_number = fields.Char(string='Adhar Number')

    @api.multi
    def action_print_excel(self):
        import openpyxl
        from odoo.http import request

        # Create a new workbook
        workbook = openpyxl.Workbook()
        sheet = workbook.active

        # Write headers
        sheet.append(['Name', 'Age', 'Gender', 'Adhar Number'])

        # Add data rows
        sheet.append([self.name, self.age, self.gender, self.adhar_number])

        # Save the workbook
        file_path = '/path/to/generated/excel.xlsx'  # Set the desired file path
        workbook.save(file_path)

        # Return an action to download the file
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content?model=wizard_report&id=%s&field=excel_file&filename=wizard_report.xlsx' % self.id,
            'target': 'self',
        }

    @api.multi
    def action_print_pdf(self):
        # Implement logic to generate PDF file based on wizard data
        # Example: Create a PDF report using `reportlab` or other PDF generation libraries
        return {'type': 'ir.actions.act_url', 'url': '/path/to/generated/pdf', 'target': 'self'}
