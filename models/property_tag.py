from odoo import models, fields


class PropertyTagModel(models.Model):
    _name = 'estate.property.tag'
    _description = 'Property tag description'

    name = fields.Char()

    _sql_constraints = [
        ('check_unique_name', 'UNIQUE(name)',
         'Property tag should be unique.')
    ]
