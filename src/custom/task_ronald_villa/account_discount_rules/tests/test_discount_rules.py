from odoo.tests.common import TransactionCase

class TestDiscountRules(TransactionCase):

    def setUp(self):
        super(TestDiscountRules, self).setUp()
        self.Partner = self.env['res.partner']
        self.DiscountRule = self.env['account.discount.rule']
        self.AccountMove = self.env['account.move']
        self.Product = self.env['product.product']

        # Limpiar cualquier regla existente que ensucie el test (ya que corre sobre la BD local)
        self.DiscountRule.search([]).write({'active': False})

        # Crear Tipos de Cliente
        self.partner_retail = self.Partner.create({
            'name': 'Cliente Retail',
            'customer_type': 'retail'
        })
        self.partner_vip = self.Partner.create({
            'name': 'Cliente VIP',
            'customer_type': 'vip'
        })

        # Crear Producto
        self.product_a = self.Product.create({
            'name': 'Producto Prueba',
            'list_price': 100.0,
        })

        # Crear reglas de descuento
        self.rule_retail = self.DiscountRule.create({
            'name': 'Regla Retail',
            'customer_type': 'retail',
            'discount_percentage': 0.0
        })
        self.rule_vip = self.DiscountRule.create({
            'name': 'Regla VIP',
            'customer_type': 'vip',
            'discount_percentage': 15.0
        })

    def test_discount_applied_on_vip(self):
        """Prueba que el descuento se aplique al crear una factura para un cliente VIP"""
        move = self.AccountMove.create({
            'move_type': 'out_invoice',
            'partner_id': self.partner_vip.id,
            'invoice_line_ids': [
                (0, 0, {
                    'product_id': self.product_a.id,
                    'quantity': 1,
                    'price_unit': 100.0,
                })
            ]
        })

        # El descuento en la linea deberia ser 15% al crearla
        self.assertEqual(move.invoice_line_ids[0].discount, 15.0, "El descuento para VIP debe ser del 15%.")

    def test_no_discount_applied_on_retail(self):
        """Prueba que no se aplique descuento o se aplique 0% a cliente Retail"""
        move = self.AccountMove.create({
            'move_type': 'out_invoice',
            'partner_id': self.partner_retail.id,
            'invoice_line_ids': [
                (0, 0, {
                    'product_id': self.product_a.id,
                    'quantity': 1,
                    'price_unit': 100.0,
                })
            ]
        })

        # El descuento en la linea deberia ser 0%
        self.assertEqual(move.invoice_line_ids[0].discount, 0.0, "El cliente minorista no debe tener descuento.")
