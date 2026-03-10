from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    storage_tag_ids = fields.Many2many(
        'stock.storage.tag',
        string='Storage Tags',
        help='Dynamic tags to organize the product in the warehouse.'
    )
