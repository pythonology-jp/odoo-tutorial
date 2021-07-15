from odoo import models, fields


class PropertyTypeModel(models.Model):
    _name = 'estate.property.type'
    _description = 'Property type description'
    _order = 'sequence'

    name = fields.Char()
    sequence = fields.Integer('Sequence', default=1, help="Used to order property types. Lower is better.")

    # Relation fields
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')

    _sql_constraints = [
        ('check_unique_name', 'UNIQUE(name)',
         'The property name should be unique.')
    ]
