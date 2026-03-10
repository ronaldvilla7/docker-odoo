{
    'name': 'Gestión de Payroll y Beneficios (Custom)',
    'version': '1.0',
    'category': 'Human Resources/Payroll',
    'summary': 'Generación de recibos de nómina y reglas de beneficios automáticos por tipo de contrato',
    'description': """
        Este módulo provee un ecosistema autónomo para generar recibos de nómina (Payslips)
        en Odoo Community, inyectando el salario base del empleado e integrando reglas de beneficios
        automáticamente en función del tipo de contrato (Full Time, Part Time, etc).
        
        No requiere dependencias externas como hr_payroll de Enterprise.
    """,
    'author': 'Ronald Villa',
    'depends': ['hr', 'hr_contract'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_contract_benefit_rule_views.xml',
        'views/hr_contract_views.xml',
        'views/hr_payslip_views.xml',
        'views/hr_payslip_menus.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
