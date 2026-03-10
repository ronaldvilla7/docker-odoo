from odoo import models, fields

class HrContract(models.Model):
    _inherit = 'hr.contract'

    contract_type_benefit = fields.Selection([
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('temporary', 'Temporary'),
        ('internship', 'Internship/Practices'),
    ], string='Contract Type (Benefits)', help='Classification used for automatic payroll and benefit rules.')
