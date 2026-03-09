{
    'name': 'Etiquetas Inteligentes de Almacenamiento',
    'version': '1.0',
    'category': 'Inventory/Inventory',
    'summary': 'Etiquetas dinámicas para organizar y filtrar productos en almacén',
    'description': """
        Módulo para asignar etiquetas (tags) a los productos.
        Permite clasificar, filtrar y agrupar visualmente la vista Kanban de productos
        en el módulo de Inventario basados en estas etiquetas dinámicas.
    """,
    'author': 'Ronald Villa',
    'depends': ['stock', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/stock_storage_tag_wizard_views.xml',
        'views/stock_storage_tag_views.xml',
        'views/product_template_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
