from odoo import api, models, fields
from odoo.exceptions import ValidationError, UserError


class PropertyModel(models.Model):
    _name = 'estate.property'
    _description = 'Property Description'
    _order = 'id desc'

    name = fields.Char()
    description = fields.Text()
    postcode = fields.Char()
    date_available = fields.Date()
    expected_price = fields.Float()
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    number_floor = fields.Integer(required = False)
    total_room = fields.Integer(required=False)
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
    status = fields.Selection(selection=[
        ('open', 'Open'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled'),
    ], required=True, default='open')

    type_roof = fields.Selection(selection=[
        ('stone coated steel', 'Stone Coated Steel'),
        ('metal roofing', 'Metal roofing'),
        ('rubber slate', 'Rubber Slate'),
        ('clay and concrete tiles', 'Clay and Concrete Tiles'),
        ('solar tiles', 'Solar Tiles'),
    ], required=False, default='solar tiles')

    # Compute fields
    total_area = fields.Integer(compute='_compute_total_area', inverse='_inverse_total_area')
    best_price = fields.Float(compute='_compute_best_price')

    # Relation fields
    property_type_id = fields.Many2one('estate.property.type', string='Property type')
    property_tag_ids = fields.Many2many('estate.property.tag', string='Property tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    user_id = fields.Many2one('res.users', string='Salesman')
    partner_id = fields.Many2one('res.partner', string='Buyer')

    _sql_constraints = [
        ('check_positive_expected_price', 'CHECK(expected_price >= 0)',
         'The expected price should be greater than 0.'),
        ('check_positive_selling_price', 'CHECK(selling_price >= 0)',
         'The selling price should be greater than 0.'),
    ]

    @api.depends('living_area', 'garden_area', 'number_floor')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area * record.number_floor + record.garden_area

    def _inverse_total_area(self):
        for record in self:
            record.garden_area = record.total_area - record.living_area * record.number_floor

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(offer.price for offer in record.offer_ids) if record.offer_ids else 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None
        # return {
        #     'warning': {
        #         'title': 'Warning',
        #         'message': ('This option is not supported for Authorize.net', 'ABC'),
        #     }
        # }

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price < 0.9 * record.expected_price:
                raise ValidationError('Selling price cannot be lower than 90% of the expected price.')

    def change_status_to_sold(self):
        for record in self:
            if record.status == 'cancelled':
                raise UserError('Cancelled property cannot be sold.')
            else:
                record.status = 'sold'

    def change_status_to_cancelled(self):
        for record in self:
            if record.status == 'sold':
                raise UserError('Sold property cannot be cancelled.')
            else:
                record.status = 'cancelled'
