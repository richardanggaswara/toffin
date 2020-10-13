# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MarketingFee(models.Model):
	_inherit = 'sale.order'

	od_id = fields.Many2one('res.partner', string='OD', domain=[('category_id.name', '=', 'OD')])