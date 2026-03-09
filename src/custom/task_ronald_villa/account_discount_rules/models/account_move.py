from odoo import models, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    def _apply_customer_discount(self):
        """
        Aplica reglas de descuento en las líneas de factura
        basado en el tipo de cliente.
        """
        for move in self:
            if move.move_type == 'out_invoice' and move.state == 'draft':
                customer_type = move.partner_id.customer_type
                if customer_type:
                    rule = self.env['account.discount.rule'].search([
                        ('customer_type', '=', customer_type),
                        ('active', '=', True)
                    ], limit=1)
                    
                    if rule and rule.discount_percentage > 0:
                        for line in move.invoice_line_ids:
                            if line.display_type == 'product':
                                if line.discount < rule.discount_percentage:
                                    line.discount = rule.discount_percentage

    @api.model_create_multi
    def create(self, vals_list):
        moves = super().create(vals_list)
        moves._apply_customer_discount()
        return moves

    def write(self, vals):
        res = super().write(vals)
        if 'partner_id' in vals or 'invoice_line_ids' in vals:
            self._apply_customer_discount()
        return res
