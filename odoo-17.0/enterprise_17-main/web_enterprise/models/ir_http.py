import json

from odoo import models
from odoo.http import request


class Http(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _post_logout(cls):
        request.future_response.set_cookie('color_scheme', max_age=0)

    def webclient_rendering_context(self):
       return {
            'session_info': self.session_info(),
        }

    def session_info(self):
        # ICP = self.env['ir.config_parameter'].sudo()
        # User = self.env['res.users']
        #
        # if User.has_group('base.group_system'):
        #     warn_enterprise = 'admin'
        # elif User.has_group('base.group_user'):
        #     warn_enterprise = 'user'
        # else:
        #     warn_enterprise = False

        result = super(Http, self).session_info()
        result['support_url'] = "https://www.odoo.com/help"
        # if warn_enterprise:
        #     result['warning'] = warn_enterprise
        #     result['expiration_date'] = False
        #     result['expiration_reason'] = False


        if request.env.user._is_internal():
            for company in request.env.user.company_ids.with_context(bin_size=True):
                result['user_companies']['allowed_companies'][company.id].update({
                    'has_background_image_light': bool(company.background_image_light),
                    'has_background_image_dark': bool(company.background_image_dark),
                })
        result['dialog_size'] = self.env.user.dialog_size
        result['chatter_position'] = self.env.user.chatter_position
        return result

