from odoo import models, fields, api, _
from odoo.exceptions import UserError

class HrPayslip(models.Model):
    _name = 'hr.payslip'
    _description = 'Recibo de Nómina (Custom CE)'

    name = fields.Char(string='Referencia del Recibo', required=True, copy=False, default=lambda self: _('Nuevo'))
    employee_id = fields.Many2one('hr.employee', string='Empleado', required=True)
    contract_id = fields.Many2one('hr.contract', string='Contrato', required=True, domain="[('employee_id', '=', employee_id)]")
    
    date_from = fields.Date(string='Fecha Inicio', required=True)
    date_to = fields.Date(string='Fecha Fin', required=True)
    
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('verify', 'En Espera'),
        ('done', 'Realizado'),
        ('cancel', 'Cancelado')
    ], string='Estado', default='draft', tracking=True)

    line_ids = fields.One2many('hr.payslip.line', 'payslip_id', string='Líneas de Nómina')

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
    _description = 'Línea de Recibo de Nómina'

    payslip_id = fields.Many2one('hr.payslip', string='Recibo de Nómina', required=True, ondelete='cascade')
    name = fields.Char(string='Concepto', required=True)
    amount = fields.Float(string='Monto', required=True)
    is_base = fields.Boolean(string='Es Salario Base', default=False)
