from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    storage_tag_ids = fields.Many2many(
        'stock.storage.tag',
        string='Etiquetas de Almacenamiento',
        help='Etiquetas dinámicas para organizar el producto en almacén.'
    )
