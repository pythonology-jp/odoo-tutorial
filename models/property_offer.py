from odoo import api, models, fields
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
    # validity = fields.Integer(compute='_compute_validity', inverse='_inverse_validity')
    # deadline_date = fields.Date()
    #
    # @api.depends('create_date', 'deadline_date')
    # def _compute_validity(self):
    #     for record in self:
    #         if record.create_date:
    #             delta = record.deadline_date - record.create_date
    #             record.validity = delta.days
    #         else:
    #             record.validity = 0
    #
    # def _inverse_validity(self):
    #     for record in self:
    #         record.deadline_date = record.create_date + datetime.timedelta(days=record.validity)
