from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer_type = fields.Selection([
        ('retail', 'Retail'),
        ('wholesale', 'Wholesale'),
        ('vip', 'VIP')
    ], string='Customer Type', help='Define the discount policies applicable to this customer.', default='retail')
