from odoo import api,fields,models


class Training(models.Model):
    _name="training"



    session_ids = fields.One2many('session', 'formation_id')

    name = fields.Char(required=1)
    price = fields.Float(required=1)
    category = fields.Char(required=1)
