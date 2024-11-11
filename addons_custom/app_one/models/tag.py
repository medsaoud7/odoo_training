from odoo import models,fields

class Tag(models.Model):
    _name='tag'

    name = fields.Char(required=1)
    real_estate_ids = fields.Many2many('real.estate',string="Properties")
