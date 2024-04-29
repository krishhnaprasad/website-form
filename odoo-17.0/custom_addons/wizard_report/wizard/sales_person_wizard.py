from odoo import api, fields, models


class SalesPersonWizard(models.TransientModel):
    _name = "sales.person.wizard"
    _description = "Print sales person wizard"

    sales_person = fields.Many2one('res.users', string="Sales Person")
    date_from = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")
    total_count = fields.Integer(string="Total Count", compute='_compute_sales_count')

    @api.depends('date_from', 'to_date', 'sales_person')
    def _compute_sales_count(self):
        if not self.sales_person:
            total_count = 0
            for person in self.env['res.users'].search([('is_salesperson', '=', True)]):
                sales_data = self.env['sale.order'].search([
                    ('user_id', '=', person.id),
                    ('date_order', '>=', self.date_from),
                    ('date_order', '<=', self.to_date),
                ])
                total_count += len(sales_data)
            self.total_count = total_count
        else:
            # Existing logic to calculate total count for a specific salesperson
            sales_data = self.env['sale.order'].search([
                ('user_id', '=', self.sales_person.id),
                ('date_order', '>=', self.date_from),
                ('date_order', '<=', self.to_date),
            ])
            self.total_count = len(sales_data)

    def print_sales_pdf(self):
        demo = self.env['sales.report'].search_read([])
        data = {
            'demo': demo,
            'model': 'sales.person.wizard',
            'form_data': self.read()[0]
        }
        return self.env.ref('wizard_report.sales_pdf_report_action').report_action(self, data=data)

    # if not self.sales_person:
    #     sales_persons = self.env['res.users'].search([('is_salesperson', '=', True)])
    #     for person in sales_persons:
    #         sales_data = self.env['sale.order'].search([
    #             ('user_id', '=', person.id),
    #             ('date_order', '>=', self.date_from),
    #             ('date_order', '<=', self.to_date),
    #         ])
    #         person.total_count = len(sales_data)
    # else:
    #     # If a specific sales person is provided, calculate their total count
    #     sales_data = self.env['sale.order'].search([
    #         ('user_id', '=', self.sales_person.id),
    #         ('date_order', '>=', self.date_from),
    #         ('date_order', '<=', self.to_date),
    #     ])
    #     self.total_count = len(sales_data)
