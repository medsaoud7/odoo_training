from datetime import date
from odoo import api,fields,models


class Room(models.Model):
    _name = 'room'

    session_ids=fields.Many2many('session',string='Sessions')

    name= fields.Char(required=1)
    number_places=fields.Integer(required=1)
    free=fields.Boolean(default=True,compute='_compute_free')

    # -------------------------------------------------------------------------
    # COMPUTE METHODS
    # -------------------------------------------------------------------------

    @api.depends('session_ids')
    def _compute_free(self):
        for room in self:
            is_free = True
            for session in room.session_ids:
                start_date = fields.Date.from_string(session.start_date)
                end_date = fields.Date.from_string(session.end_date)

                if start_date <= fields.Date.today() <= end_date:
                    is_free = False
                    break

            room.free = is_free


    @api.model
    def check_free(self):
        rooms = self.env['room'].search([])
        for room in rooms:
            is_free = True
            for session in room.session_ids:
                start_date = fields.Date.from_string(session.start_date)
                end_date = fields.Date.from_string(session.end_date)

                if start_date <= fields.Date.today() <= end_date:
                    is_free = False
                    break

            room.free = is_free











