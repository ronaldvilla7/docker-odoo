from odoo.tests.common import TransactionCase
from datetime import date

class TestHrContractBenefits(TransactionCase):

    def setUp(self):
        super(TestHrContractBenefits, self).setUp()
        self.Employee = self.env['hr.employee']
        self.Contract = self.env['hr.contract']
        self.BenefitRule = self.env['hr.contract.benefit.rule']
        self.Payslip = self.env['hr.payslip']

        # Limpiar basuras de pruebas previas en la bd local
        self.BenefitRule.search([]).write({'active': False})

        # Empleado 1
        self.employee_full = self.Employee.create({
            'name': 'Juan Pérez (Full Time)',
        })
        # Contrato Full Time (con tipo de beneficio marcado)
        self.contract_full = self.Contract.create({
            'name': 'Contrato Juan - Full Time',
            'employee_id': self.employee_full.id,
            'state': 'open',
            'wage': 1000.0,
            'contract_type_benefit': 'full_time',
        })

        # Empleado 2 sin tipo de beneficio
        self.employee_none = self.Employee.create({
            'name': 'Pedro Gomez (Sin Tipo)',
        })
        self.contract_none = self.Contract.create({
            'name': 'Contrato Pedro - Base',
            'employee_id': self.employee_none.id,
            'state': 'open',
            'wage': 500.0,
            'contract_type_benefit': False,
        })

        # Crear reglas
        self.rule_bonus = self.BenefitRule.create({
            'name': 'Bono Fijo Full Time',
            'contract_type_benefit': 'full_time',
            'amount_type': 'fixed',
            'amount': 200.0,
        })
        self.rule_vacation = self.BenefitRule.create({
            'name': 'Vacaciones % Full Time',
            'contract_type_benefit': 'full_time',
            'amount_type': 'percent',
            'amount': 10.0, # 10% del salario
        })

    def test_payslip_generation_with_benefits(self):
        """Prueba que un recibo para un contrato full_time inyecte sueldo base + bono fijo + porcentaje"""
        payslip = self.Payslip.create({
            'name': 'Nomina Enero (Con Beneficios)',
            'employee_id': self.employee_full.id,
            'contract_id': self.contract_full.id,
            'date_from': date(2023, 1, 1),
            'date_to': date(2023, 1, 31),
        })
        
        # Generar
        payslip.compute_sheet()

        # Deberia tener 3 lienas: Sueldo(1000) + Bono Fijo(200) + Bono \%(100)
        self.assertEqual(len(payslip.line_ids), 3, "El recibo debe tener 3 líneas (Salario Base + 2 reglas activas)")
        
        base_line = payslip.line_ids.filtered(lambda l: l.is_base)
        self.assertEqual(base_line.amount, 1000.0)

        bonus_line = payslip.line_ids.filtered(lambda l: l.name == 'Bono Fijo Full Time')
        self.assertEqual(bonus_line.amount, 200.0)

        vacation_line = payslip.line_ids.filtered(lambda l: l.name == 'Vacaciones % Full Time')
        self.assertEqual(vacation_line.amount, 100.0) # 10% of 1000

    def test_payslip_generation_without_benefits(self):
        """Prueba que un recibo para un contrato sin tipo solo inyecte sueldo base"""
        payslip = self.Payslip.create({
            'name': 'Nomina Enero (Sin Beneficios)',
            'employee_id': self.employee_none.id,
            'contract_id': self.contract_none.id,
            'date_from': date(2023, 1, 1),
            'date_to': date(2023, 1, 31),
        })
        payslip.compute_sheet()

        # Solo debe existir la linea del sueldo base (500)
        self.assertEqual(len(payslip.line_ids), 1, "Debe existir únicamente la línea de salario base")
        self.assertEqual(payslip.line_ids[0].amount, 500.0)
