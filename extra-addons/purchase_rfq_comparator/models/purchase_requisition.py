# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseRequisitionRfqComparator(models.Model):
    _inherit = 'purchase.requisition'
    _description = 'Purchase Agreement RFQ Comparator'

    def action_open_rfq_comparison(self):
        self.ensure_one()
        return {
            'name': "ANÁLISIS COMPARATIVO DE PROVEEDORES",
            'type': 'ir.actions.client',
            'tag': 'purchase_rfq_comparator.MyClientAction',
            'target': 'new',
            'flags': {'header': False, 'footer': False},
        }

    @api.model
    def get_rfq_comparator_data(self, req_id):

        requisition = self.browse(req_id) if req_id else []

        purchases_info = []
        pruducts_info = []

        for purchase in requisition.purchase_ids:
            state_mapping = {
                'draft': 'SdP',
                'sent': 'SdP enviada',
                'to approve': 'A aprobar',
                'purchase': 'Pedido de compra',
                'done': 'Bloqueada',
                'cancel': 'Cancelado'
            }
            
            def get_state_class(state):
                if state == 'draft':
                    return 'alert-info'
                elif state in ['sent', 'to approve']:
                    return 'alert-warning'
                elif state in ['purchase', 'done']:
                    return 'alert-success'
                return 'alert-danger'

            def get_product_info(line, row_index):
                return {
                    "id": line.product_id.id,
                    "row_index": row_index,
                    "name": line.product_id.display_name,
                    "qty": line.product_qty,
                    "price": line.price_unit,
                    "subtotal": line.price_subtotal,
                    "times": line.date_planned or "",
                    
                }

            def get_ranking_by_amount(purchase_list, current_purchase):
                sorted_purchases = sorted(purchase_list, key=lambda x: x.amount_total)
                return sorted_purchases.index(current_purchase) + 1

            ranking = get_ranking_by_amount(requisition.purchase_ids, purchase)
            def get_ranking_class(rank):
                if rank == 1:
                    return 'alert-success'
                elif rank == 2:
                    return 'alert-warning'
                return 'alert-danger'

            ranking_class = get_ranking_class(ranking)
            
            # Crear un diccionario de productos usando row_index como clave
            products_dict = {}
            for index, line in enumerate(purchase.order_line):
                key = f"{line.product_id.id}_{index}"
                products_dict[key] = get_product_info(line, index)

            purchase_data = {
                "id": purchase.id,
                "name": purchase.name,
                "supplier": purchase.partner_id.name,
                "state": purchase.state,
                "state_class": get_state_class(purchase.state),
                "state_text": state_mapping.get(purchase.state, purchase.state),
                "products": products_dict,
                "notes": purchase.notes,
                "amount_total": purchase.amount_total,
                "ranking": ranking,
                "ranking_class": ranking_class
            }
                
            purchases_info.append(purchase_data)

        for index, line in enumerate(requisition.line_ids):
            pruducts_info.append({
                "row_index": index,
                "id": line.product_id.id,
                "name": line.product_id.display_name,
                "description": line.product_description_variants or "",
                "qty": line.product_qty,
            })

        return {
            "name": requisition.name,
            "proyect": requisition.x_studio_proyecto.name if hasattr(requisition, 'x_studio_proyecto') and requisition.x_studio_proyecto else "",
            "purchases": purchases_info,
            "pruducts": pruducts_info
        }

    def print_rfq_comparator(self):
        report_name = 'purchase_rfq_comparator.report_purchase_rfq_comparator'
        return self.env.ref(report_name).report_action(self)
    
    @api.model
    def format_amount(self, value):
        if not value:
            return ''
        lang = self.env.user.lang or 'es_CO'
        lang_obj = self.env['res.lang']._lang_get(lang)
        currency = self.env.company.currency_id
        formatted = lang_obj.format('%.2f', value, grouping=True, monetary=True)
        return '%s %s' % (currency.symbol, formatted)