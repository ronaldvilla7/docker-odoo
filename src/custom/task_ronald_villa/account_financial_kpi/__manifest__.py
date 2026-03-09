{
    'name': 'Indicadores de Salud Financiera',
    'version': '1.0',
    'category': 'Accounting/Accounting',
    'summary': 'Tablero de indicadores financieros simples (KPIs)',
    'description': """
        Módulo para definir y visualizar indicadores clave de rendimiento financiero (KPIs).
        Permite establecer fórmulas basadas en códigos de cuenta contable y configurar umbrales
        para advertencias visuales (semáforos).
    """,
    'author': 'Ronald Villa',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_financial_kpi_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
