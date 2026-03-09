from odoo.tests.common import TransactionCase

class TestFinancialKpi(TransactionCase):

    def setUp(self):
        super(TestFinancialKpi, self).setUp()
        self.Kpi = self.env['account.financial.kpi']

        # En lugar de crear movimientos contables completos para testear `bal`, 
        # testearemos la manipulación de la fórmula matemática como baseline.
        # En una situación real, crearíamos facturas y pagos para afectar las cuentas y validarlo.
        
        # Test baseline con valores directos
        self.kpi_margin = self.Kpi.create({
            'name': 'Margen Estático (Test)',
            'formula': '500 - 300', # Simula bal('ingresos') - bal('costos')
            'threshold_direction': 'greater_is_better',
            'threshold_warning': 150.0,
            'threshold_critical': 100.0,
        })
        
        self.kpi_debt = self.Kpi.create({
            'name': 'Deuda Estática (Test)',
            'formula': '500 / 100', # Simula ratio de deuda
            'threshold_direction': 'lower_is_better',
            'threshold_warning': 3.0,
            'threshold_critical': 6.0,
        })

    def test_kpi_evaluation_greater_is_better(self):
        """Prueba que un KPI donde mayor es mejor evalúe correctamente color y valor"""
        # Valor estático = 200
        # warning = 150, critical = 100
        # Mayor es mejor, así que 200 > 150 -> Debe ser Verde (10)

        # Trigger compute calling mapped since its computed fields
        self.kpi_margin.mapped('current_value')

        self.assertEqual(self.kpi_margin.current_value, 200.0, "La fórmula debe sumar/restar a 200.")
        self.assertEqual(self.kpi_margin.color, 10, "El color debe ser Verde (10) ya que el valor supera el warning en 'greater_is_better'")

    def test_kpi_evaluation_lower_is_better(self):
        """Prueba que un KPI donde menor es mejor evalúe correctamente color y valor"""
        # Valor estático = 5.0
        # warning = 3.0, critical = 6.0
        # Menor es mejor. 5.0 es mayor que 3.0 pero menor que 6.0. Debería ser Amarillo (3)

        self.kpi_debt.mapped('current_value')

        self.assertEqual(self.kpi_debt.current_value, 5.0, "La fórmula debe dividir a 5.0")
        self.assertEqual(self.kpi_debt.color, 3, "El color debe ser Amarillo (3) ya que el valor está entre warning y critical en 'lower_is_better'")
