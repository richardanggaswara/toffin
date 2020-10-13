# -*- coding: utf-8 -*-
from odoo import http
import simplejson
import time
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)


class VitXenditCallback(http.Controller):
	@http.route('/xendit/invoice/paid', methods=['GET','POST'], auth='public', type='json')
	def invoice_paid(self, **kw):
		data = request.jsonrequest
		_logger.info(data)

		sale_order = request.env['sale.order'].sudo().search([('name','like',data['external_id']), ('partner_id.email','=',data['payer_email'])])

		if not sale_order:
			res = {'status':'FAILED', 'message':'SO not found'}
			return simplejson.dumps(res)

		journal_id = request.env['account.journal'].sudo().search([('name','=','Bank')])
		payment_method = request.env['account.payment.method'].sudo().search([('code','=','electronic')])
		payment = request.env['account.payment']

		payment.sudo().create({
			'payment_type'		: 'inbound',
			'partner_type'		: 'customer',
			'partner_id'		: sale_order.partner_id.id,
			'amount'			: sale_order.amount_total,
			'journal_id'		: journal_id.id,
			'payment_date'		: time.strftime('%Y-%m-%d'),
			'communication'		: 'XENDIT ' + sale_order.name,
			'payment_method_id' : payment_method.id,
			'name'				: 'XENDIT-' + sale_order.name,
		}).sudo().post()

		return data



	@http.route('/xendit/fva/paid', methods=['GET','POST'], auth='public', type='json')
	def fva_paid(self, **kw):
		_logger.info(request.jsonrequest)
		data = request.jsonrequest
		res_partner = request.env['res.partner'].sudo().search([('va_bank','=',data['bank_code']), ('va_number','=',data['account_number'])])

		if not res_partner:
			rest = {'status':'FAILED', 'message':'SO not found'}
			return simplejson.dumps(rest)

		journal_id = request.env['account.journal'].sudo().search([('name','=','Bank')])
		payment_method= request.env['account.payment.method'].sudo().search([('code','=','electronic')])
		payment = request.env['account.payment']

		payment.sudo().create({
			'payment_type'		: 'inbound',
			'partner_type'		: 'customer',
			'partner_id'		: res_partner.id,
			'amount'		: data['amount'],
			'journal_id'		: journal_id.id,
			'payment_date'		: time.strftime('%Y-%m-%d'),
			'communication'		: 'XENDIT ' + res_partner.name,
			'payment_method_id'	: payment_method.id,
			'name'			: 'XENDIT-' + res_partner.name,
		}).sudo().post()

		return data
