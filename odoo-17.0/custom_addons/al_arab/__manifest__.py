# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'bake_al_arab',
    'version': '17.0.0.0',
    'licence': 'LGPL-3',
    'author': "krishna prasad",
    'depends': ['base', 'sale_management', 'contacts', 'account'],
    'data': [
        'views/tax_invoice_view.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': True,
}
