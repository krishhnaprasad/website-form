from odoo import http
from odoo.http import request


class InvoiceDue(http.Controller):

    @http.route('/customer-details', type="http", auth="public", website=True)
    def customer_details(self, **kw):
        return http.request.render("invoice_due.customer_details", {})

    @http.route('/create/customer', type="http", auth="public", website=True)
    def button_create(self, **kw):
        print("saved", kw)
        request.env['res.partner'].sudo().create(kw)
        return request.render("invoice_due.customer_thanks", {})
