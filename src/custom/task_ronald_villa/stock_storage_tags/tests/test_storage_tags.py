from odoo.tests.common import TransactionCase

class TestStorageTags(TransactionCase):

    def setUp(self):
        super(TestStorageTags, self).setUp()
        self.ProductTemplate = self.env['product.template']
        self.StorageTag = self.env['stock.storage.tag']

        # Crear algunas etiquetas
        self.tag_fragile = self.StorageTag.create({
            'name': 'Frágil',
            'color': 2, # Naranja
            'description': 'Manejar con cuidado'
        })
        self.tag_heavy = self.StorageTag.create({
            'name': 'Pesado',
            'color': 1, # Rojo
        })

    def test_assign_tags_to_product(self):
        """Prueba que las etiquetas puedan asignarse y buscarse en el producto"""
        product = self.ProductTemplate.create({
            'name': 'Caja Fuerte de Cristal',
            'storage_tag_ids': [(6, 0, [self.tag_fragile.id, self.tag_heavy.id])]
        })

        # Verifica que el producto tiene 2 etiquetas
        self.assertEqual(len(product.storage_tag_ids), 2, "El producto debería tener 2 etiquetas asignadas.")

        # Busca el producto mediante las etiquetas
        products_fragile = self.ProductTemplate.search([('storage_tag_ids', 'in', self.tag_fragile.ids)])
        self.assertIn(product, products_fragile, "El producto debería encontrarse buscando por la etiqueta 'Frágil'.")
