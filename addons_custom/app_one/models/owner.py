from odoo import models,fields

class Owner(models.Model):
    _name = 'owner'

    name = fields.Char(required=1)
    phone = fields.Char()
    address = fields.Char()
    user_id = fields.Many2one('res.users', 'User')
    real_estate_ids = fields.One2many('real.estate','owner_id')
