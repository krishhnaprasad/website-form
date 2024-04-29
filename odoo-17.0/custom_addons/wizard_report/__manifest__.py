# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'report wizard',
    'version': '17.0.0.0',
    'licence': 'LGPL-3',
    'author': "krishna prasad",
    'depends': ['base', 'report_xlsx', 'sale_management', 'purchase', 'contacts', ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/appointment_report.xml',
        'wizard/sales_report.xml',
        'report/appointmen_xls.xml',
        'report/appointment_pdf.xml',
        'report/sales_pdf.xml',
        'report/pdf_report_action.xml',
        'report/sales_pdf_report_action.xml',
        'report/image_line.xml',
        'views/menu.xml',
        'views/lsp.xml',
        'views/lpp.xml',
        'views/contact_button.xml',
        'views/image_order_line.xml',
        'views/user_tab.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': True,
}
