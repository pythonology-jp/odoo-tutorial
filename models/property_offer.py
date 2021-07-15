from odoo import api, models, fields
from odoo.exceptions import UserError
import datetime


class PropertyOfferModel(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property Offer description'

    price = fields.Float()
    status = fields.Selection(selection=[
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ])
    partner_id = fields.Many2one('res.partner', string='Partner')
    property_id = fields.Many2one('estate.property', string='Property')

    _sql_constraints = [
        ('check_positive_price', 'CHECK(price >= 0)',
         'The offer price should be greater than 0.')
    ]
    validity = fields.Integer(compute='_compute_validity', inverse='_inverse_validity')
    deadline_date = fields.Date(required=True)

    @api.depends('create_date', 'deadline_date')
    def _compute_validity(self):
        for record in self:
            if record.create_date and record.deadline_date:
                delta = record.deadline_date - record.create_date.date()
                record.validity = delta.days
            else:
                record.validity = 0

    def _inverse_validity(self):
        for record in self:
            if record.create_date:
                record.deadline_date = record.create_date + datetime.timedelta(days=record.validity)
            else:
                record.deadline_date = datetime.date.today() + datetime.timedelta(days=record.validity)

    def accept_offer(self):
        for record in self:
            if record.property_id.status != 'open':
                raise UserError('Sold or Cancelled property cannot accept offer.')
            record.property_id.partner_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.status = 'sold'
            record.status = 'accepted'

    def refuse_offer(self):
        for record in self:
            if record.property_id.status != 'open':
                raise UserError('Sold or Cancelled property cannot accept offer.')
            record.status = 'refused'
