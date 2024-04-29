from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    @property
    def SELF_READABLE_FIELDS(self):
        return super().SELF_READABLE_FIELDS + [
            'dialog_size',
            'chatter_position',

        ]

    @property
    def SELF_WRITEABLE_FIELDS(self):
        return super().SELF_WRITEABLE_FIELDS + [
            'dialog_size',
            'chatter_position',

        ]

    dialog_size = fields.Selection(
        selection=[
            ('minimize', 'Minimize'),
            ('maximize', 'Maximize'),
        ],
        string="Dialog Size",
        default='minimize',
        required=True,
    )

    chatter_position = fields.Selection(
        selection=[
            ('side', 'Side'),
            ('bottom', 'Bottom'),
        ],
        string="Chatter Position",
        default='side',
        required=True,
    )
