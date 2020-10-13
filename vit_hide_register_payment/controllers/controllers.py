# -*- coding: utf-8 -*-
from odoo import http

# class VitHideRegisterPayment(http.Controller):
#     @http.route('/vit_hide_register_payment/vit_hide_register_payment/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vit_hide_register_payment/vit_hide_register_payment/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vit_hide_register_payment.listing', {
#             'root': '/vit_hide_register_payment/vit_hide_register_payment',
#             'objects': http.request.env['vit_hide_register_payment.vit_hide_register_payment'].search([]),
#         })

#     @http.route('/vit_hide_register_payment/vit_hide_register_payment/objects/<model("vit_hide_register_payment.vit_hide_register_payment"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vit_hide_register_payment.object', {
#             'object': obj
#         })