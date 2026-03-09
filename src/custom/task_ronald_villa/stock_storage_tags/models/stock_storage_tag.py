from odoo import models, fields

class StockStorageTag(models.Model):
    _name = 'stock.storage.tag'
    _description = 'Etiqueta de Almacenamiento'

    name = fields.Char(string='Nombre de la Etiqueta', required=True)
    color = fields.Integer(string='Color de Índice', default=0)
    description = fields.Text(string='Descripción')
