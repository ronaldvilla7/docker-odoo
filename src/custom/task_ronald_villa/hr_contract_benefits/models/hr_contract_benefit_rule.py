from odoo import models, fields

class HrContractBenefitRule(models.Model):
    _name = 'hr.contract.benefit.rule'
    _description = 'Automatic Labor Benefit Rule'

    name = fields.Char(string='Benefit Name', required=True)
    contract_type_benefit = fields.Selection([
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('temporary', 'Temporary'),
        ('internship', 'Internship/Practices'),
    ], string='Applicable To (Contract Type)', required=True)
    
    amount_type = fields.Selection([
        ('fixed', 'Fixed Amount'),
        ('percent', 'Percentage of Base Salary'),
    ], string='Calculation Type', required=True, default='fixed')
    
    amount = fields.Float(string='Value (Amount or %)', required=True, default=0.0)
    
    active = fields.Boolean(string='Active', default=True)
