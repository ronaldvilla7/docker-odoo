from odoo import models, fields, api
from odoo.exceptions import UserError
import ast

class AccountFinancialKpi(models.Model):
    _name = 'account.financial.kpi'
    _description = 'Financial Health Indicator'

    name = fields.Char(string='Indicator Name', required=True)
    formula = fields.Char(string='Calculation Formula', required=True, help='Example: bal("100") / bal("200"). Use bal("account_code") to get the balance.')
    threshold_warning = fields.Float(string='Warning Threshold (Yellow)', required=True, default=0.0)
    threshold_critical = fields.Float(string='Critical Threshold (Red)', required=True, default=0.0)
    threshold_direction = fields.Selection([
        ('greater_is_better', 'Higher is Better (e.g. Margin)'),
        ('lower_is_better', 'Lower is Better (e.g. Debt)')
    ], string='Threshold Direction', required=True, default='greater_is_better')
    
    current_value = fields.Float(string='Current Value', compute='_compute_kpi_value')
    color = fields.Integer(string='Status (Color)', compute='_compute_kpi_value')

    @api.depends('formula', 'threshold_warning', 'threshold_critical', 'threshold_direction')
    def _compute_kpi_value(self):
        for kpi in self:
            try:
                def evaluate_balance(code):
                    self.env.cr.execute("""
                        SELECT SUM(balance) FROM account_move_line aml
                        JOIN account_account aa ON aml.account_id = aa.id
                        WHERE aa.code LIKE %s
                    """, (str(code) + '%',))
                    res = self.env.cr.fetchone()
                    return res[0] or 0.0

                # Crear un contexto seguro para eval
                eval_context = {
                    'bal': evaluate_balance,
                }
                
                # Evaluar la fórmula matemáticamente proveída
                # Solo se permite nuestro custom bal() y operaciones matemáticas básicas. 
                # (Para producción real se requiere ast.literal_eval restringido o un parser)
                result = eval(kpi.formula, {"__builtins__": None}, eval_context)
                kpi.current_value = float(result)

                # Calcular color (10 = Verde, 3 = Amarillo, 1 = Rojo)
                if kpi.threshold_direction == 'greater_is_better':
                    if kpi.current_value >= kpi.threshold_warning:
                        kpi.color = 10
                    elif kpi.current_value >= kpi.threshold_critical:
                        kpi.color = 3
                    else:
                        kpi.color = 1
                else: # lower_is_better
                    if kpi.current_value <= kpi.threshold_warning:
                        kpi.color = 10
                    elif kpi.current_value <= kpi.threshold_critical:
                        kpi.color = 3
                    else:
                        kpi.color = 1

            except Exception as e:
                # Si la fórmula falla o divide por cero
                kpi.current_value = 0.0
                kpi.color = 1 # Rojo por error
