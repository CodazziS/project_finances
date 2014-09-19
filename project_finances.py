from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp
from lxml import etree as ET


class project_finances(osv.Model):
    _inherit = 'account.analytic.account'

    def _check_amount(self, amount_expected, parent_id):
        if parent_id.id > 0:
            childrens = parent_id.child_complete_ids

            if parent_id.amount_expected > 0:
                total_amount = amount_expected
                for children in childrens:
                    total_amount += children.amount_expected
                if total_amount > parent_id.amount_expected:
                    return True
            return False

    def _count_amount(self, cr, uid, ids, field_name, arg, context):
        res = {}
        record = self.browse(cr, uid, ids, context=context)
        for data in record:
            amount = 0
            #res_str = dict(self.pool.get('project_logical_framework.logical_framework').fields_get(cr, uid, allfields=['type'], context=context)['type']['selection'])[data.type]
            #res_str += "\n" + data.logique
            res[data.id] = amount
        
        return res

    def _verify_fields(self, cr, uid, ids, field_name, args, context=None):
        record = self.browse(cr, uid, ids, context=context)
        for data in record:
            return self._check_amount(data.amount_expected, data.parent_id)

    _columns = {
        'amount_expected': fields.float(
            'Amount expected',
            digits_compute=dp.get_precision('Amount')),
        'test_amount': fields.function(_count_amount,
            string="[TEST] Amount expected",
            type="float",
            digits_compute=dp.get_precision('Amount')),
        'amount_overload': fields.function(_verify_fields, type="boolean"),
     }
    _defaults = {
        'amount_expected': 0,
    }

class project_finances_project(osv.Model):
    _inherit = 'project.project'

    def _onchange_amount_expected(
        self,
        cr,
        uid,
        ids,
        parent=None,
        amount_expected=0):
        if parent:
            aaa_obj = self.pool.get("account.analytic.account")
            parent_brw = aaa_obj.browse(cr, uid, parent)
            return {'value': {'amount_overload': aaa_obj
                ._check_amount(amount_expected, parent_brw)}}
        return {'value': {'amount_overload': False}}

    _columns = {
        'thematic': fields.char('Project Thematic'),
        'area': fields.char('Intervention area'),
    }