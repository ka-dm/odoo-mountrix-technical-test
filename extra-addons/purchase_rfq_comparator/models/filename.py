from odoo import models, fields, api
import io
import json
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class DynamicPurchaseReport(models.Model):
    _name = "dynamic.purchase.report"
    purchase_report = fields.Char(string="Purchase Report")
    date_from = fields.Datetime(string="Date From")
    date_to = fields.Datetime(string="Date to")
    report_type = fields.Selection([
        ('report_by_order', 'Report By Order'),
        ('report_by_product', 'Report By Product')], default='report_by_order')

    @api.model
    def purchase_report(self, option):
        orders = self.env['purchase.order'].search([])
        report_values = self.env['dynamic.purchase.report'].search(
            [('id', '=', option[0])])
        data = {

            'report_type': report_values.report_type,
            'model': self,
        }
        if report_values.date_from:
            data.update({
                'date_from': report_values.date_from,
            })
        if report_values.date_to:
            data.update({
                'date_to': report_values.date_to,
            })
        filters = self.get_filter(option)
        report = self._get_report_values(data)
        lines = self._get_report_values(data).get('PURCHASE')
        return {
            'name': "Purchase Orders",
            'type': 'ir.actions.client',
            'tag': 's_r',
            'orders': data,
            'filters': filters,
            'report_lines': lines,
        }


def get_filter(self, option):
    data = self.get_filter_data(option)
    filters = {}
    if data.get('report_type') == 'report_by_order':
        filters['report_type'] = 'Report By Order'
    return filters


def get_filter_data(self, option):
    r = self.env['dynamic.purchase.report'].search([('id', '=', option[0])])
    default_filters = {}
    filter_dict = {
        'report_type': r.report_type,
    }
    filter_dict.update(default_filters)
    return filter_dict

def _get_report_sub_lines(self, data, report, date_from, date_to):
   report_sub_lines = []
   new_filter = None
   if data.get('report_type') == 'report_by_order':
       query = '''
                select l.name,l.date_order,l.partner_id,l.amount_total,l.notes,l.user_id,res_partner.name as partner,
                         res_users.partner_id as user_partner,sum(purchase_order_line.product_qty),l.id as id,
                        (SELECT res_partner.name as salesman FROM res_partner WHERE res_partner.id = res_users.partner_id)
                        from purchase_order as l
                        left join res_partner on l.partner_id = res_partner.id
                        left join res_users on l.user_id = res_users.id
                        left join purchase_order_line on l.id = purchase_order_line.order_id
                         '''
       term = 'Where '
       if data.get('date_from'):
           query += "Where l.date_order >= '%s' " % data.get('date_from')
           term = 'AND '
       if data.get('date_to'):
           query += term + "l.date_order <= '%s' " % data.get('date_to')
       query += "group by l.user_id,res_users.partner_id,res_partner.name,l.partner_id,l.date_order,l.name,l.amount_total,l.notes,l.id"
       self._cr.execute(query)
       report_by_order = self._cr.dictfetchall()
       report_sub_lines.append(report_by_order)
   elif data.get('report_type') == 'report_by_product':
       query = '''
       select l.amount_total,sum(purchase_order_line.product_qty) as qty, purchase_order_line.name as product, purchase_order_line.price_unit,product_product.default_code,product_category.name
                from purchase_order as l
                left join purchase_order_line on l.id = purchase_order_line.order_id
               
 left join product_product on purchase_order_line.product_id = product_product.id
                left join product_template on purchase_order_line.product_id = product_template.id
                left join product_category on product_category.id = product_template.categ_id
                          '''
       term = 'Where '
       if data.get('date_from'):
           query += "Where l.date_order >= '%s' " % data.get('date_from')
           term = 'AND '
       if data.get('date_to'):
           query += term + "l.date_order <= '%s' " % data.get('date_to')
       query += "group by l.amount_total,purchase_order_line.name,purchase_order_line.price_unit,purchase_order_line.product_id,product_product.default_code,product_template.categ_id,product_category.name"
       self._cr.execute(query)
       report_by_product = self._cr.dictfetchall()
       report_sub_lines.append(report_by_product)
   return report_sub_lines

def _get_report_values(self, data):
   docs = data['model']
   date_from = data.get('date_from')
   date_to = data.get('date_to')
   if data['report_type'] == 'report_by_order_detail':
       report = ['Report By Order Detail']
   elif data['report_type'] == 'report_by_product':
       report = ['Report By Product']
   elif data['report_type'] == 'report_by_categories':
       report = ['Report By Categories']
   elif data['report_type'] == 'report_by_purchase_representative':
       report = ['Report By Purchase Representative']
   elif data['report_type'] == 'report_by_state':
       report = ['Report By State']
   else:
       report = ['Report By Order']
   if data.get('report_type'):
       report_res = \
           self._get_report_sub_lines(data, report, date_from, date_to)[0]
   else:
      
 report_res = self._get_report_sub_lines(data, report, date_from,
                                               date_to)
   return {
       'doc_ids': self.ids,
       'docs': docs,
       'PURCHASE': report_res,
   }
