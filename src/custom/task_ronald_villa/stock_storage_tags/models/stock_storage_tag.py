from odoo import models, fields

class StockStorageTag(models.Model):
    _name = 'stock.storage.tag'
    _description = 'Storage Tag'

    name = fields.Char(string='Tag Name', required=True)
    color = fields.Integer(string='Index Color', default=0)
    description = fields.Text(string='Description')
