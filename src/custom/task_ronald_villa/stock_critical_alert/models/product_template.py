from odoo import models, fields, api, _

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    config_min_stock = fields.Float(
        string='Minimum Stock',
        default=0.0,
        help='Threshold to generate critical stock alerts'
    )
    
    is_critical_stock = fields.Boolean(
        string='In Critical Stock',
        default=False,
        help='Indicates if the product is currently below minimum stock'
    )

