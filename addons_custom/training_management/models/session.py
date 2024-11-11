from odoo import api,fields,models

from odoo.exceptions import ValidationError

from odoo import exceptions


class Session(models.Model):
    _name = "session"


    formation_id = fields.Many2one('training', string='Formation')
    room_ids = fields.Many2many('room', string='Rooms')
    candidate_ids = fields.Many2many('candidate', string="Candidates")
    trainer_ids = fields.Many2many('trainer', string='Trainers')

    name= fields.Char(required=True)
    number_participant = fields.Integer(compute='_compute_number_participant')
    start_date= fields.Date(required=True)
    end_date = fields.Date(required=True)
    duration = fields.Integer(compute='_compute_duration', store=1 ,string="Duration (in Days)")
    state = fields.Selection([
        ('draft','Draft'),
        ('in_progress','In Progress'),
        ('finished','Finished'),

    ],default='draft')

    category= fields.Char(related='formation_id.category')

    _sql_constraints = [
        ('check_end_date', 'CHECK(end_date > start_date)',
         'The end date must be later than the start date.')
    ]

    # -------------------------------------------------------------------------
    # COMPUTE METHODS
    # -------------------------------------------------------------------------

    @api.depends('end_date','start_date')
    def _compute_duration(self):
       for rec in self:
           if rec.start_date and rec.end_date :
               start_date=fields.Date.from_string(rec.start_date)
               end_date=fields.Date.from_string(rec.end_date)
               rec.duration=(end_date-start_date).days
           else:
               rec.duration= 0

    @api.depends('candidate_ids')
    def _compute_number_participant(self):
        for rec in self :
            rec.number_participant=len(rec.candidate_ids)



    # -------------------------------------------------------------------------
    # Constrains METHODS
    # -------------------------------------------------------------------------

    @api.constrains('room_ids', 'start_date', 'end_date')
    def _check_room_availability(self):
        for session in self:
            for room in session.room_ids:
                overlapping_sessions = self.env['session'].search([
                    ('id', '!=', session.id),
                    ('room_ids', 'in', room.id),
                    ('start_date', '<=', session.end_date),
                    ('end_date', '>=', session.start_date),
                ])
                if overlapping_sessions:
                    raise exceptions.ValidationError(
                        f"La salle '{room.name}' est déjà réservée pour une autre session durant la période sélectionnée."
                    )

    @api.constrains('candidate_ids')
    def _check_number_participant(self):
        for session in self:
            print('number_participant changed')
            number_places=0
            rooms = self.room_ids
            for room in rooms :
               print(room.number_places)
               number_places = number_places + room.number_places
            if number_places < session.number_participant:
                raise exceptions.ValidationError('le nombre de participant est supérieur au nombre de places')


    def check_one_session(self, current_user):
        start_date = fields.Date.from_string(self.start_date)
        end_date = fields.Date.from_string(self.end_date)
        list_session_ids = current_user.session_ids

        for session in list_session_ids:

            session_start_date = fields.Date.from_string(session.start_date)
            session_end_date = fields.Date.from_string(session.end_date)

            if (session_start_date <= end_date) and (session_end_date >= start_date):

                return True


            return False


    def action_subscription(self):
        current_user = self.env["candidate"].search([('user_id', '=', self.env.user.id)], limit= 1)
        if current_user:
            list_candidate_ids = self.candidate_ids.ids
            if not current_user in list_candidate_ids:
                list_candidate_ids.append(current_user.id)
                if self.check_one_session(current_user):
                    raise ValidationError('overlapping session')
                self.write({'candidate_ids': [(6,0, list_candidate_ids)]})







    def action_cancellation(self):
        current_user = self.env["candidate"].search([('user_id', '=', self.env.user.id)], limit=1)
        if current_user:
            list_candidate_ids = self.candidate_ids.ids
            if current_user.id in list_candidate_ids:
                self.write({
                    'candidate_ids': [(3, current_user.id)]
                })





