# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class AccountInvoice(models.Model):
	_inherit = 'account.invoice'