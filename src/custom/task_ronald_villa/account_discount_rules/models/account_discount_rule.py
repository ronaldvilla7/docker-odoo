from odoo import models, fields

class AccountDiscountRule(models.Model):
    _name = 'account.discount.rule'
    _description = 'Discount Rule by Customer Type'

    name = fields.Char(string='Description', required=True)
    customer_type = fields.Selection([
        ('retail', 'Retail'),
        ('wholesale', 'Wholesale'),
        ('vip', 'VIP')
    ], string='Customer Type', required=True)
    discount_percentage = fields.Float(string='Discount Percentage (%)', required=True, default=0.0)
    active = fields.Boolean(string='Active', default=True)
