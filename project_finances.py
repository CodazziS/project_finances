from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp
from lxml import etree as ET


class project_finances(osv.Model):
    _inherit = 'account.analytic.account'

    def _count_planned_amount(self, cr, uid, ids, field_name, arg, context):
        res = {}
        record = self.browse(cr, uid, ids, context=context)
        for data in record:
            planned_amount = 0
            cross = data.crossovered_budget_line
            for line in cross:
                planned_amount += line.planned_amount
            res[data.id] = planned_amount
        return res

    def _count_practical_amount(self, cr, uid, ids, field_name, arg, context):
        res = {}
        record = self.browse(cr, uid, ids, context=context)
        for data in record:
            practical_amount = 0
            cross = data.crossovered_budget_line
            for line in cross:
                practical_amount += line.practical_amount
            res[data.id] = practical_amount
        return res

    _columns = {
        'planned_amount': fields.function(_count_planned_amount,
        string="Planned amount",
        type="float",
        digits_compute=dp.get_precision('Amount')),
        'practical_amount': fields.function(_count_practical_amount,
        string="Practical amount",
        type="float",
        digits_compute=dp.get_precision('Amount')),
    }


class project_finances_project(osv.Model):
    _inherit = 'project.project'

    _columns = {
        'thematic': fields.char('Project Thematic'),
        'area': fields.char('Intervention area'),
    }