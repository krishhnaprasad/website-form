from odoo import models


class ExpenseXlsx(models.AbstractModel):
    _name = 'report.wizard_report.appointment_wizard_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objs):
        sheet = workbook.add_worksheet('demo')
        bold = workbook.add_format({"bold": True})
        sheet.set_column('D:D', 20)
        sheet.set_column('E:E', 15)

        row = 3
        col = 3

        sheet.write(row, col, 'Patient name', bold)
        sheet.write(row, col + 1, 'Symptoms')
        sheet.write(row, col + 2, 'Fees')
        for wizard in data['demo']:
            row += 1
            sheet.write(row, col, wizard['patient_id'])
            sheet.write(row, col + 1, wizard['date_from'])
            sheet.write(row, col + 2, wizard['date_to'])
