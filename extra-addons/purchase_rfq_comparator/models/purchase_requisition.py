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
                Returns product information, including whether it has the best price among all orders.
                Now compares the best price of each product (by product_id) among all RFQs.
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
                # Get the earliest delivery date of each purchase order
                def get_earliest_delivery_date(purchase):
                    if not purchase.order_line:
                        return None
                    delivery_dates = [line.date_planned for line in purchase.order_line if line.date_planned]
                    return min(delivery_dates) if delivery_dates else None
                
                # Filter orders that have valid delivery dates
                purchases_with_dates = [(p, get_earliest_delivery_date(p)) for p in purchase_list]
                purchases_with_dates = [(p, date) for p, date in purchases_with_dates if date]
                
                if not purchases_with_dates:
                    return None
                
                # Sort by delivery date (earliest first)
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
            
            # Optimization: Precalculate the minimum unit price per product across all purchases
            # to avoid nested loops for each order line.
            # Create a dict: {product_id: min_price}
            min_price_per_product = {}
            for purchase_obj in requisition.purchase_ids:
                for line_obj in getattr(purchase_obj, 'order_line', []):
                    product_id = getattr(line_obj.product_id, 'id', None)
                    price_unit = getattr(line_obj, 'price_unit', None)
                    if product_id is not None and price_unit is not None:
                        if product_id not in min_price_per_product or price_unit < min_price_per_product[product_id]:
                            min_price_per_product[product_id] = price_unit

            # Create a products dictionary using row_index as key
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
    
    def action_buy_optimal(self):
        self.ensure_one()
        action = self.env.ref('purchase.purchase_rfq').read()[0]
        action['domain'] = [('requisition_id', '=', self.id)]
        action['context'] = {'default_requisition_id': self.id}

        # Get all RFQs (purchase orders) related to this requisition
        rfqs = self.purchase_ids.filtered(lambda x: x.state in ['draft', 'sent', 'to approve', 'purchase'])
        if rfqs:
            # Take one (the first one)
            main_rfq = rfqs[0]
            # The others as alternatives
            alternative_rfqs = rfqs - main_rfq
            # Assign alternatives to the alternative_po_ids field
            main_rfq.alternative_po_ids = [(6, 0, alternative_rfqs.ids)]

        # For each requisition line, find the purchase.order.line with the lowest unit price
        for line in self.line_ids:
            # Search for all purchase order lines related to this requisition line
            polines = self.env['purchase.order.line'].search([
                ('order_id', 'in', self.purchase_ids.ids),
                ('product_id', '=', line.product_id.id),
            ])
            if polines:
                # Find the line with the lowest unit price
                best_line = min(polines, key=lambda l: l.price_unit)
                # Execute the 'action_choose' action on that line
                best_line.action_choose()

        # Confirm orders that have ordered products (>0) and cancel those with qty 0
        for po in self.purchase_ids:
            # If any line has quantity > 0, confirm the order
            has_qty = any(line.product_qty > 0 for line in po.order_line)
            if has_qty:
                if po.state in ['draft', 'sent', 'to approve']:
                    # Confirm the purchase order skipping the alternatives check
                    po.with_context(skip_alternative_check=True).button_confirm()
            else:
                if po.state not in ['cancel', 'done']:
                    po.button_cancel()

        return action