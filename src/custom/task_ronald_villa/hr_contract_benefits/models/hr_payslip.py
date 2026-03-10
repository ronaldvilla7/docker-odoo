from odoo import models, fields, api, _
from odoo.exceptions import UserError

class HrPayslip(models.Model):
    _name = 'hr.payslip'
    _description = 'Payslip (Custom CE)'

    name = fields.Char(string='Payslip Reference', required=True, copy=False, default=lambda self: _('Nuevo'))
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    contract_id = fields.Many2one('hr.contract', string='Contract', required=True, domain="[('employee_id', '=', employee_id)]")
    
    date_from = fields.Date(string='Start Date', required=True)
    date_to = fields.Date(string='End Date', required=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('verify', 'Waiting'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], string='Status', default='draft', tracking=True)

    line_ids = fields.One2many('hr.payslip.line', 'payslip_id', string='Payroll Lines')

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        if self.employee_id:
            contract = self.env['hr.contract'].search([
                ('employee_id', '=', self.employee_id.id),
                ('state', '=', 'open')
            ], limit=1)
            if contract:
                self.contract_id = contract.id

    def compute_sheet(self):
        for payslip in self:
            payslip.line_ids.unlink()

            contract = payslip.contract_id
            if not contract:
                raise UserError(_("Debes seleccionar un contrato para generar el recibo de nómina."))

            lines = []
            base_wage = contract.wage or 0.0
            lines.append((0, 0, {
                'name': 'Salario Base',
                'amount': base_wage,
                'is_base': True
            }))

            if contract.contract_type_benefit:
                rules = self.env['hr.contract.benefit.rule'].search([
                    ('contract_type_benefit', '=', contract.contract_type_benefit),
                    ('active', '=', True)
                ])
                for rule in rules:
                    calc_amount = rule.amount
                    if rule.amount_type == 'percent':
                        calc_amount = base_wage * (rule.amount / 100.0)
                    
                    lines.append((0, 0, {
                        'name': rule.name,
                        'amount': calc_amount,
                        'is_base': False
                    }))

            payslip.line_ids = lines

    def action_payslip_done(self):
        self.write({'state': 'done'})

    def action_payslip_draft(self):
        self.write({'state': 'draft'})


class HrPayslipLine(models.Model):
    _name = 'hr.payslip.line'
    _description = 'Payslip Line'

    payslip_id = fields.Many2one('hr.payslip', string='Payslip', required=True, ondelete='cascade')
    name = fields.Char(string='Concept', required=True)
    amount = fields.Float(string='Amount', required=True)
    is_base = fields.Boolean(string='Is Base Salary', default=False)
