from odoo.tests.common import SavepointCase
from odoo.exceptions import UserError
from odoo.tests import tagged


@tagged('at_install')
class EstateTestCase(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(EstateTestCase, cls).setUpClass()
        cls.properties = cls.env['estate.property'].create([
            {'name': 'Test Estate Property'},
            {'name': 'Test Estate Property 2', 'garden_area': 10},
        ])

    def test_creation_area(self):
        """Test that total_area is computed like it should."""
        self.properties.living_area = 20
        self.assertRecordValues(self.properties, [
            {'name': 'Test Estate Property', 'total_area': 10},
            {'name': 'Test Estate Property 2', 'total_area': 30},
        ])

    def test_action_sell(self):
        """Test that everything behaves like it should when selling a property."""
        self.properties.change_status_to_sold()
        self.assertRecordValues(self.properties, [
            {'name': 'Test Estate Property', 'status': 'sold'},
            {'name': 'Test Estate Property 2', 'status': 'sold'},
        ])

        with self.assertRaises(UserError):
            self.properties.change_status_to_cancelled()
