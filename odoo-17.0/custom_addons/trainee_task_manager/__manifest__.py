# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Trainee Task Manager',
    'version': '17.0.0.0',
    'licence': 'LGPL-3',
    'author': "krishna prasad",
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/trainee_task.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': True,
}
