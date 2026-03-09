from odoo import models, fields

class AccountDiscountRule(models.Model):
    _name = 'account.discount.rule'
    _description = 'Regla de Descuento por Tipo de Cliente'

    name = fields.Char(string='Descripción', required=True)
    customer_type = fields.Selection([
        ('retail', 'Minorista'),
        ('wholesale', 'Mayorista'),
        ('vip', 'VIP')
    ], string='Tipo de Cliente', required=True)
    discount_percentage = fields.Float(string='Porcentaje de Descuento (%)', required=True, default=0.0)
    active = fields.Boolean(string='Activo', default=True)
