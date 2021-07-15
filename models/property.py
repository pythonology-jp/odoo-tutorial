from odoo import api, models, fields
from odoo.exceptions import ValidationError


class PropertyModel(models.Model):
    _name = 'estate.property'
    _description = 'Property Description'

    name = fields.Char()
    description = fields.Text()
    postcode = fields.Char()
    date_available = fields.Date()
    expected_price = fields.Float()
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection=[
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])

    # Compute fields
    total_area = fields.Integer(compute='_compute_total_area', inverse='_inverse_total_area')
    best_price = fields.Float(compute='_compute_best_price')

    # Relation fields
    property_type_id = fields.Many2one('estate.property.type', string='Property type')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')

    _sql_constraints = [
        ('check_positive_expected_price', 'CHECK(expected_price >= 0)',
         'The expected price should be greater than 0.'),
        ('check_positive_selling_price', 'CHECK(selling_price >= 0)',
         'The selling price should be greater than 0.'),
    ]

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    def _inverse_total_area(self):
        for record in self:
            record.garden_area = record.total_area - record.living_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(offer.price for offer in record.offer_ids) if record.offer_ids else 0

    @api.onchange('garden')
    def _onchange_garden(self):
        return {
            'warning': {
                'title': 'Warning',
                'message': ('This option is not supported for Authorize.net', 'ABC'),
            }
        }

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price < 0.9 * record.expected_price:
                raise ValidationError('Selling price cannot be lower than 90% of the expected price.')
