from odoo import api,fields,models


class Candidate(models.Model):
    _name = 'candidate'

    session_ids = fields.Many2many('session', string="Sessions")
    user_id = fields.Many2one('res.users', 'User')
    name=fields.Char(required=1)
    number_ins=fields.Integer(required=1)


