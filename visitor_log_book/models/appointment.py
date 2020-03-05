from odoo import fields,api,models,_

class Appointment(models.Model):
    _name = 'appointment'
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name = 'appointment_date'

    @api.onchange('employee')
    def based_on_employee(self):
        result = self.env['hr.employee'].search([('id', '=', self.employee.id)])
        if result:
            self.em_phone = result.work_phone
            self.email = result.work_email
            self.department = result.department_id.name
            self.position = result.job_id.name

    @api.onchange('em_phone')
    def based_on_em_phone(self):
        result = self.env['hr.employee'].search([('work_phone', '=', self.em_phone)])
        if result:
            self.employee = result.id
            self.email = result.work_email
            self.department = result.department_id.name
            self.position = result.job_id.name

    @api.onchange('email')
    def based_on_email(self):
        result = self.env['hr.employee'].search([('work_email', '=', self.email)])
        if result:
            self.employee = result.id
            self.em_phone = result.work_phone
            self.department = result.department_id.name
            self.position = result.job_id.name


    employee = fields.Many2one('hr.employee',string='Employee Name')
    department = fields.Char(string='Department')
    position = fields.Char(string='Job Position')
    em_phone = fields.Char(string='Phone Number')
    email = fields.Char(string='Email')

##### auto load visitor information

    @api.onchange('visitor')
    def based_on_visitor(self):
        result = self.env['visitor_log_book.visitor'].search([('id', '=', self.visitor.id)])
        if result:
            self.visitor_id = result.visitor_id
            self.company = result.company.name
            self.designation = result.designation.name
            self.vi_phone = result.phone
            self.nid = result.nid

    @api.onchange('vi_phone')
    def based_on_vi_phone(self):
        result=self.env['visitor_log_book.visitor'].search([('phone','=',self.vi_phone)])
        if result:
            self.visitor = result.id
            self.visitor_id = result.visitor_id
            self.company = result.company.name
            self.designation = result.designation.name
            self.nid = result.nid


    @api.onchange('visitor_id')
    def based_on_visitor_id(self):
        result = self.env['visitor_log_book.visitor'].search([('visitor_id', '=', self.visitor_id)])
        if result:
            self.visitor = result.id
            self.nid = result.nid
            self.company = result.company.name
            self.designation = result.designation.name
            self.vi_phone = result.phone


    visitor = fields.Many2one('visitor_log_book.visitor',string='Visitor Phone')
    visitor_id = fields.Char(string='Visitor ID',required=True)
    company = fields.Char(string='Company')
    designation = fields.Char(string='Designation')
    purpose = fields.Selection([('official','Official'),('personal','Personal')],default='official')
    nid = fields.Char(string='NID(National ID)')
    vi_phone = fields.Char(string='Visitor Name ')
    appointment_date=fields.Datetime(string='Appointment Date',required=True)
    state = fields.Selection([('pending','Pending'),('done','Done')])


        #auto checkin when click button with data.
    def checkin_from_appointment(self):

        for f in self:
            if f.state== 'pending':
                f.state='done'
            values={
                'visitor':f.visitor.id,
                'vi_phone':f.vi_phone,
                'company':f.company,
                'designation':f.designation,
                'nid':f.nid,
                'visitor_id':f.visitor_id,

                'desired_person':f.employee.id,
                'em_phone':f.em_phone,
                'email':f.email,
                'department':f.department,
                'position':f.position,


            }
            new_checkin=f.env['visitor_log_book.checkinout'].create(values)
            context = dict(f.env.context)
            return {
                'type':'ir.actions.act_window',
                'view_type':'form',
                'view_mode':'form',
                'res_model':'visitor_log_book.checkinout',
                'res_id':new_checkin.id,
            }


    @api.model
    def create(self, vals_list):
        result = super(Appointment, self).create(vals_list)
        result['state'] = 'pending'
        return result











