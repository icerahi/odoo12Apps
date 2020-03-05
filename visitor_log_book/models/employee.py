
from odoo import fields,models,api,_

class Department(models.Model):
    _name = 'employee.department'
    name = fields.Char(string="Name ")

class Position(models.Model):
    _name = 'employee.position'
    name = fields.Char(string='Name')

class Employee(models.Model):
    _inherit = 'hr.employee'
    name = fields.Char(string='Name',required=True)
    work_phone = fields.Char(string='Work Phone',required=True)
    work_email = fields.Char(string='Work Email',required=True)

    # getting name and phone as many2one field view
    def name_get(self):
        list = []
        for f in self:
            list.append((f.id, '%s (%s)' % (f.name, f.work_phone)))
        return list

    @api.constrains('work_phone')
    def check_phone_validation(self):
        result = self.env['hr.employee'].search([('work_phone', '=', self.work_phone)])
        if len(result)>1:
            raise Warning('This Phone Number Already Register in our record book!')

    @api.constrains('work_email')
    def check_email_validation(self):
        result = self.env['hr.employee'].search([('work_email', '=', self.work_email)])
        if len(result) > 1:
            raise Warning('This Email Already Register in our record book!')
