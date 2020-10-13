# -*- coding: utf-8 -*-
from odoo import http

# class VitLandedJournnal(http.Controller):
#     @http.route('/vit_landed_journnal/vit_landed_journnal/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vit_landed_journnal/vit_landed_journnal/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vit_landed_journnal.listing', {
#             'root': '/vit_landed_journnal/vit_landed_journnal',
#             'objects': http.request.env['vit_landed_journnal.vit_landed_journnal'].search([]),
#         })

#     @http.route('/vit_landed_journnal/vit_landed_journnal/objects/<model("vit_landed_journnal.vit_landed_journnal"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vit_landed_journnal.object', {
#             'object': obj
#         })