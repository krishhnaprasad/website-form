# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'report wizard',
    'version': '17.0.0.0',
    'licence': 'LGPL-3',
    'author': "krishna prasad",
    'depends': ['base', 'report_xlsx'],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'wizard/appointment_report.xml',
        'report/appointmen_xls.xml',
        'report/appointment_pdf.xml',
        'report/pdf_report_action.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': True,
}
