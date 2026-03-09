from odoo import models, fields

class StockStorageTagWizard(models.TransientModel):
    _name = 'stock.storage.tag.wizard'
    _description = 'Wizard para Asignar Etiquetas Masivamente'

    tag_ids = fields.Many2many(
        'stock.storage.tag',
        string='Etiquetas a Asignar',
        help='Selecciona las etiquetas que deseas aplicar a los productos seleccionados.'
    )

    def action_apply_tags(self):
        active_ids = self.env.context.get('active_ids', [])
        if active_ids:
            products = self.env['product.template'].browse(active_ids)
            for product in products:
                for tag in self.tag_ids:
                    product.storage_tag_ids = [(4, tag.id)]
        return {'type': 'ir.actions.act_window_close'}
