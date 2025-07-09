# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class PurchaseRequisitionRfqComparator(models.Model):
    _inherit = 'purchase.requisition'
    _description = 'Purchase Agreement RFQ Comparator'

    def action_open_rfq_comparison(self):
        self.ensure_one()
        return {
            'name': "Purchase RFQ Comparator",
            'type': 'ir.actions.client',
            'tag': 'purchase_rfq_comparator.MyClientAction',
            'target': 'new',
            'flags': {'header': False, 'footer': False},
            'context': {
                'dialog_size': 'extra-large',
            },
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
                """
                Devuelve la información del producto, incluyendo si tiene el mejor precio entre todas las órdenes.
                Ahora compara el mejor precio de cada producto (por product_id) entre todas las RFQs.
                """
                return {
                    "id": line.product_id.id,
                    "row_index": row_index,
                    "name": line.product_id.display_name,
                    "qty": line.product_qty,
                    "price": line.price_unit,
                    "subtotal": line.price_subtotal,
                    "times": line.date_planned.strftime('%d/%m/%y') if line.date_planned else "",
                }

            def get_ranking_by_amount(purchase_list, current_purchase):
                sorted_purchases = sorted(purchase_list, key=lambda x: x.amount_total)
                return sorted_purchases.index(current_purchase) + 1

            def get_ranking_by_delivery_time(purchase_list, current_purchase):
                # Obtener la fecha de entrega más temprana de cada orden de compra
                def get_earliest_delivery_date(purchase):
                    if not purchase.order_line:
                        return None
                    delivery_dates = [line.date_planned for line in purchase.order_line if line.date_planned]
                    return min(delivery_dates) if delivery_dates else None
                
                # Filtrar órdenes que tienen fechas de entrega válidas
                purchases_with_dates = [(p, get_earliest_delivery_date(p)) for p in purchase_list]
                purchases_with_dates = [(p, date) for p, date in purchases_with_dates if date]
                
                if not purchases_with_dates:
                    return None
                
                # Ordenar por fecha de entrega (más temprana primero)
                sorted_purchases = sorted(purchases_with_dates, key=lambda x: x[1])
                current_earliest = get_earliest_delivery_date(current_purchase)
                
                if current_earliest:
                    for i, (p, date) in enumerate(sorted_purchases):
                        if p.id == current_purchase.id:
                            return i + 1
                return None

            ranking_amount = get_ranking_by_amount(requisition.purchase_ids, purchase)
            ranking_delivery = get_ranking_by_delivery_time(requisition.purchase_ids, purchase)
            
            def get_ranking_class(rank):
                if rank == 1:
                    return 'alert-success'
                elif rank == 2:
                    return 'alert-warning'
                return 'alert-danger'

            ranking_class = get_ranking_class(ranking_amount)
            
            # Optimización: Precalcular el menor precio unitario por producto en todas las compras
            # para evitar bucles anidados por cada línea de orden.
            # Creamos un dict: {product_id: min_price}
            min_price_per_product = {}
            for purchase_obj in requisition.purchase_ids:
                for line_obj in getattr(purchase_obj, 'order_line', []):
                    product_id = getattr(line_obj.product_id, 'id', None)
                    price_unit = getattr(line_obj, 'price_unit', None)
                    if product_id is not None and price_unit is not None:
                        if product_id not in min_price_per_product or price_unit < min_price_per_product[product_id]:
                            min_price_per_product[product_id] = price_unit

            # Crear un diccionario de productos usando row_index como clave
            products_dict = {}
            for index, line in enumerate(purchase.order_line):
                key = f"{line.product_id.id}_{index}"
                products_dict[key] = get_product_info(line, index)
                product_id = line.product_id.id
                min_price = min_price_per_product.get(product_id)
                products_dict[key]["is_best_price"] = (line.price_unit == min_price)

            purchase_data = {
                "id": purchase.id,
                "name": purchase.name,
                "supplier": purchase.partner_id.name,
                "supplier_id": purchase.partner_id.id,
                "state": purchase.state,
                "state_class": get_state_class(purchase.state),
                "state_text": state_mapping.get(purchase.state, purchase.state),
                "products": products_dict,
                "notes": purchase.notes,
                "amount_total": purchase.amount_total,
                "ranking_amount": ranking_amount,
                "ranking_delivery": ranking_delivery,
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
        formatted = lang_obj.format('%.2f', value, grouping=True)
        return '%s %s' % (currency.symbol, formatted)