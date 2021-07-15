from odoo import models, fields


class PropertyTagModel(models.Model):
    _name = 'estate.property.tag'
    _description = 'Property tag description'
    _order = 'name asc'

    name = fields.Char()
    color = fields.Integer(default=0)

    _sql_constraints = [
        ('check_unique_name', 'UNIQUE(name)',
         'Property tag should be unique.')
    ]
