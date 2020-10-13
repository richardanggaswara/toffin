# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class AccountInvoice(models.Model):
	_inherit = "account.invoice"

	account_line_ids = fields.One2many('vendorbill.expense', 'invoice_id', string='Account Lines')

	@api.multi
	def finalize_invoice_move_lines(self, move_lines):
		total_product_line = len(self.invoice_line_ids) 
		for line in self.invoice_line_ids:
			for expense in self.account_line_ids:
				if expense.apply_items :
					account_id = line.product_id.categ_id.property_stock_valuation_account_id.id
				else:
					account_id = expense.account_id.id
				if expense.other_vendor:
					partner_id = expense.vendor_landed.id
				else:
					partner_id = self.partner_id.id
				amount = expense.amount*line.price_subtotal/self.amount_untaxed
				move_lines.append((0, 0, {
					'date_maturity': self.date_due, 
					'partner_id': partner_id, 
					'name': line.product_id.name, 
					'debit': amount, 
					'credit': 0, 
					'account_id': account_id, 
					# 'analytic_line_ids': [], 
					'amount_currency': 0, 
					# 'currency_id': False, 
					'quantity': 1.0, 
					'product_id': False, 
					'product_uom_id': False, 
					# 'analytic_account_id': False, 
					'invoice_id': self.id, 
					'tax_ids': [], 
					'tax_line_id': False, 
					'analytic_tag_ids': []
					}))
				move_lines.append((0, 0, {
					'date_maturity': self.date_due, 
					'partner_id': partner_id, 
					'name': expense.account_id.name, 
					'debit': 0, 
					'credit': amount, 
					# 'account_id': self.account_id.id, 
					'account_id': line.product_id.categ_id.property_stock_account_input_categ_id.id, 
					# 'analytic_line_ids': [], 
					'amount_currency': 0, 
					# 'currency_id': False, 
					'quantity': 1.0, 
					'product_id': False, 
					'product_uom_id': False, 
					# 'analytic_account_id': False, 
					'invoice_id': self.id, 
					'tax_ids': [], 
					'tax_line_id': False, 
					'analytic_tag_ids': []
					})) 
				
		_logger.info(move_lines)
		# import pdb
		# pdb.set_trace()
		return move_lines
	
	def action_invoice_open(self):
		res = super(AccountInvoice, self).action_invoice_open()
		total_product_line = len(self.invoice_line_ids)
		# line = self.env['account.invoice.line'].search([('invoice_id.id','in',self.account_line_ids.id)])
		# expense = self.env['vendorbill.expense'].search([()])
		inv_line_vals = []
		for expense in self.account_line_ids:
			if expense.other_vendor:
				partner_id = expense.vendor_landed.id	
				for line in self.invoice_line_ids:
					amount = expense.amount*line.price_subtotal/self.amount_untaxed 
					inv_line_vals.append((0,0,{
						'product_id': line.product_id.id,
						'name': expense.account_id.name + ' ' + (expense.note or ''),
						'account_id': line.product_id.categ_id.property_stock_account_input_categ_id.id, #interim 
						# 'account_id': expense.account_id.id,
						'quantity': 1,
						'price_unit': amount 
					}))

				invoice_id = self.env['account.invoice'].create({
						'partner_id': partner_id,
						'journal_id': self.journal_id.id,
						# 'reference' : self.number,
						'account_id': self.account_id.id, #payable 
						'type': 'in_invoice',
						'origin': 'Expenses of ' + self.number,
						'invoice_line_ids': inv_line_vals,
						'comment': "Expenses %s" % self.name ,
					})
		return res

	# @api.depends('product_variant_ids', 'product_variant_ids.standard_price')
 #    def _compute_standard_price(self):
 #    	res = super(ProductTemplate, self)._compute_standard_price()
 #        unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
 #        for template in unique_variants:
 #            template.standard_price = template.product_variant_ids.standard_price/
 #        for template in (self - unique_variants):
 #            template.standard_price = 0.0

class VendorbillExpense(models.Model):
	_name = "vendorbill.expense"

	invoice_id = fields.Many2one('account.invoice', string='Invoice')
	account_id = fields.Many2one('account.account', string='Account', domain=[('user_type_id','in','Expenses')])
	note = fields.Char(string="Notes")	
	apply_items = fields.Boolean(string="Apply to Item", track_visibility="onchange")
	other_vendor = fields.Boolean(string="Other Vndr", track_visibility="onchange")
	amount = fields.Float("Amount")
	vendor_landed = fields.Many2one('res.partner', string="Expense are charge to vendor")
