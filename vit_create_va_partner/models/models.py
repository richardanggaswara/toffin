# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import requests
import simplejson
import time
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)


class ResPartnerVA(models.Model):
	_inherit = 'res.partner'

	partner_va_ids = fields.One2many('partner.va', 'partner_id', string='Partner VA')
	is_create_va = fields.Boolean(string='Is Create VA', default=False, readonly=True)

	@api.multi
	def create_va(self):
		self.is_create_va = True

		test_xendit_toffin = "xnd_development_kdzbsTmz9p1JZUcs58mcjNCDMEI7RT8mH55NIjHFhuZ2XgJGcpBk44AeBRdu5zx"
		xendit_url = "https://api.xendit.co/callback_virtual_accounts"

		obj_bank = self.env['master.bank.xendit'].search([])

		for rec in obj_bank:
			data = {
				'external_id'	: 'fixed-va-' + time.strftime('%Y%m%d%H%M%S'),
				'bank_code'		: rec.bank_code,
				'name'			: self.name,
			}

			r = requests.post(xendit_url, data=data, auth=(test_xendit_toffin, ''))
			res = simplejson.loads(r.text)

			_logger.warning(res)

			self.env['partner.va'].create({
				'partner_id'	: self.id,
				'va_external_id': res['id'],
				'va_number'		: res['account_number'],
				'va_bank'		: res['bank_code'],
			})



class MasterBankXendit(models.Model):
	_name = 'master.bank.xendit'

	name = fields.Char(string='Name')
	bank_code = fields.Char(string='Bank Code')



class PartnerVA(models.Model):
	_name = 'partner.va'

	va_bank = fields.Char(string='VA Bank', readonly=True)
	va_number = fields.Char(string='VA Number', readonly=True)
	va_external_id = fields.Char(string='VA External ID', readonly=True)
	partner_id = fields.Many2one('res.partner', string='Partner')
