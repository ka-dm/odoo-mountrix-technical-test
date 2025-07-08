# -*- coding: utf-8 -*-
# from odoo import http


# class PurchaseRfqComparator(http.Controller):
#     @http.route('/purchase_rfq_comparator/purchase_rfq_comparator', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/purchase_rfq_comparator/purchase_rfq_comparator/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('purchase_rfq_comparator.listing', {
#             'root': '/purchase_rfq_comparator/purchase_rfq_comparator',
#             'objects': http.request.env['purchase_rfq_comparator.purchase_rfq_comparator'].search([]),
#         })

#     @http.route('/purchase_rfq_comparator/purchase_rfq_comparator/objects/<model("purchase_rfq_comparator.purchase_rfq_comparator"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('purchase_rfq_comparator.object', {
#             'object': obj
#         })
