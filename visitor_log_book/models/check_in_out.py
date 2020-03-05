from odoo import models,fields,api,_
from datetime import datetime

class CheckInOut(models.Model):
    _name='visitor_log_book.checkinout'
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name = 'vi_phone'

    @api.onchange('visitor')
    def based_on_visitor(self):
        result = self.env['visitor_log_book.visitor'].search([('id','=',self.visitor.id)])
        if result:
            self.visitor_id=result.visitor_id
            self.company = result.company.name
            self.designation = result.designation.name
            self.vi_phone = result.phone
            self.nid = result.nid




    # @api.onchange('nid')
    # def based_on_nid(self):
    #     for f in self:
    #         return {'domain': {'visitor': [('nid', '=', f.nid)]}}

    visitor = fields.Many2one('visitor_log_book.visitor',string='Visitor Phone',required=True)
    visitor_id = fields.Char(string='Visitor ID',required=True)
    card_no = fields.Char(string='Card No')
    company = fields.Char(string='Company')
    designation = fields.Char(string='Designation')
    purpose = fields.Selection([('official','Official'),('personal','Personal')],default='official')
    nid = fields.Char(string='NID(National ID')
    vi_phone = fields.Char(string='Visitor Name')

    @api.onchange('desired_person')
    def based_on_desired_person(self):
        result = self.env['hr.employee'].search([('id', '=', self.desired_person.id)])
        if result:
            self.em_phone = result.work_phone
            self.email = result.work_email
            self.department = result.department_id.name
            self.position = result.job_id.name

    @api.onchange('em_phone')
    def based_on_em_phone(self):
        result = self.env['hr.employee'].search([('work_phone', '=', self.em_phone)])
        print(result)
        print(result.name)
        if result:
            self.desired_person = result.id
            self.email = result.work_email
            self.department = result.department_id.name
            self.position = result.job_id.name

    @api.onchange('email')
    def based_on_email(self):
        result = self.env['hr.employee'].search([('work_email', '=', self.email)])
        if result:
            self.desired_person = result.id
            self.em_phone = result.work_phone
            self.department = result.department_id.name
            self.position = result.job_id.name

    # @api.onchange('employee_id')
    # def based_on_employee_id(self):
    #     result = self.env['visitor_log_book.employee'].search([('employee_id', '=', self.employee_id)])
    #     if result:
    #         self.desired_person = result.id
    #         self.email = result.work_email
    #         self.department = result.department.name
    #         self.position = result.position.name
    #         self.em_phone = result.work_phone

    desired_person = fields.Many2one('hr.employee', string='Name')#for purpose
    department = fields.Char(string='Department')
    position = fields.Char(string='Position')
    em_phone = fields.Char(string='Phone',required=True) #for purpose
    email = fields.Char(string='Email',required=True)

    check_in = fields.Datetime(string='Checkin Time',required=True,default = fields.Datetime.now)
    check_out = fields.Datetime(string='Checkout Time')
    state = fields.Selection([('checkin','CheckIn'),('checkout','CheckOut')],readonly=True)
    is_checkout = fields.Boolean(string='Is Checkout',default=True)



    def checkout_btn(self):
        for f in self:
            f.state='checkout'
            f.check_out=datetime.now()



    @api.model
    def create(self, vals_list):
        result=super(CheckInOut, self).create(vals_list)
        if result['is_checkout']==True:
            result['state']='checkin'
            result['is_checkout']=False

            #for descuss notification

        return result







            
