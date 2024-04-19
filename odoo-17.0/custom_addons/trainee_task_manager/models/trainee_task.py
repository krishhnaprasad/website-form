from odoo import models, fields, api

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TraineeTask(models.Model):
    _name = "trainee.task.management"
    _rec_name = 'task_name'

    task_name = fields.Char(string="Task Name")
    task_description = fields.Text(string="Description")
    task_duration = fields.Float(string="Duration in hours")
    task_difficulty = fields.Selection([('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')],
                                       string="Difficulty")
    task_completed = fields.Boolean(string="Completed")
    total_duration = fields.Float(string="Total Duration (minutes)", compute='_compute_duration', store=True)

    def button_comment(self):
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'trainee.comment',
            'name': 'comment tab',
            'target': 'new',
        }

    def marked_as_done(self):
        self.task_completed = True

    @api.depends('task_duration')
    def _compute_duration(self):
        for rec in self:
            if rec.task_duration:
                rec.total_duration = rec.task_duration * 60

    @api.onchange('task_difficulty')
    def _auto_description(self):
        for rec in self:
            if rec.task_difficulty == "easy":
                rec.task_description = "This task is relatively easy."

            elif rec.task_difficulty == "medium":
                rec.task_description = "This task requires some effort."

            else:
                rec.task_description = "This task is challenging."
