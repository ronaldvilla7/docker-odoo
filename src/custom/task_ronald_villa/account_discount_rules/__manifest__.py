{
    'name': 'Políticas de Descuento en Facturas',
    'version': '1.0',
    'category': 'Accounting/Accounting',
    'summary': 'Aplicación automática de descuentos en facturas según el tipo de cliente',
    'description': """
        Módulo para configurar reglas de descuento basadas en el tipo de cliente (Retail, Wholesale, VIP).
        Aplica los descuentos automáticamente al validar facturas o de forma manual.
    """,
    'author': 'Ronald Villa',
    'depends': ['base', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_views.xml',
        'views/account_discount_rule_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
