from odoo import models, fields

class HrContractBenefitRule(models.Model):
    _name = 'hr.contract.benefit.rule'
    _description = 'Regla Automática de Beneficio Laboral'

    name = fields.Char(string='Nombre del Beneficio', required=True)
    contract_type_benefit = fields.Selection([
        ('full_time', 'Tiempo Completo'),
        ('part_time', 'Medio Tiempo'),
        ('temporary', 'Temporal'),
        ('internship', 'Pasantía/Prácticas'),
    ], string='Aplicable a (Tipo de Contrato)', required=True)
    
    amount_type = fields.Selection([
        ('fixed', 'Monto Fijo'),
        ('percent', 'Porcentaje del Salario Base'),
    ], string='Tipo de Cálculo', required=True, default='fixed')
    
    amount = fields.Float(string='Valor (Monto o %)', required=True, default=0.0)
    
    active = fields.Boolean(string='Activo', default=True)
