from odoo import models, fields

class HrContract(models.Model):
    _inherit = 'hr.contract'

    contract_type_benefit = fields.Selection([
        ('full_time', 'Tiempo Completo'),
        ('part_time', 'Medio Tiempo'),
        ('temporary', 'Temporal'),
        ('internship', 'Pasantía/Prácticas'),
    ], string='Tipo de Contrato (Beneficios)', help='Clasificación utilizada para las reglas automáticas de nómina y beneficios.')
