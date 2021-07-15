from odoo import models, fields


class PropertyTypeModel(models.Model):
    _name = 'estate.property.type'
    _description = 'Property type description'

    name = fields.Char()

    _sql_constraints = [
        ('check_unique_name', 'UNIQUE(name)',
         'The property name should be unique.')
    ]
