from odoo import models, fields, api, _, exceptions


class Designation(models.Model):
    _name = 'visitor.designation'
    name = fields.Char(string="Name ")

class Company(models.Model):
    _name = 'visitor.company'

    name = fields.Char(string='Name')

class Visitor(models.Model):
    _name = 'visitor_log_book.visitor'
    #_inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char('Visitor Phone',required=True)
    phone = fields.Char(string='Visitor Name',required=True)
    company = fields.Many2one('visitor.company')
    designation = fields.Many2one('visitor.designation')
    nid = fields.Char(string='NID(National ID)')
    visitor_id = fields.Char(string='Visitor ID',required=True,copy=False,index=True,default=lambda self:_('New'))
    total_visit = fields.Integer(string='Total Visites',compute='get_total_count')

    def get_total_count(self):
        count=self.env['visitor_log_book.checkinout'].search_count([('visitor','=',self.id)])
        self.total_visit=count

        #getting name and phone as many2one field view
    def name_get(self):
        list = []
        for f in self:
            list.append((f.id, '%s (%s)' % (f.name, f.phone)))
        return list

    @api.multi
    def get_total_visit(self):
        return {
            'name': 'All Visits',
            'res_model': 'visitor_log_book.checkinout',
            'domain': [('visitor', '=', self.id)],
            'view_type': 'form',
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

    @api.multi
    def redirect_checkin(self):
        return {
            'name':'Visitor CheckIn',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'visitor_log_book.checkinout',

            #passing default value for the form
            'context':{'default_visitor':self.id},
            'target':'new',
        }

    @api.model
    def create(self, vals_list):
        if vals_list.get('visitor_id',_('New')) == 'New':
            vals_list['visitor_id']=self.env['ir.sequence'].next_by_code('visitor_id.sequence') or _('New')


        result=super(Visitor, self).create(vals_list)

        contact = self.env['res.partner'].create({'phone':result['name'],'name':result['phone'], #phone & name exchange for need
                                                  'function':result['designation']['name']})
        return result


    @api.constrains('name')
    def check_phone_validation(self):
         result = self.env['visitor_log_book.visitor'].search([('name', '=', self.name)])
         if len(result)>1:
             raise Warning('This Phone Number Already Register in our record book!')




class InheritContact(models.Model):
    _inherit = 'res.partner'
    property_account_receivable_id=fields.Many2one('account.account',required=False)
    property_account_payable_id=fields.Many2one('account.account',required=False)
