/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

const { Component, useState, onWillStart } = owl;

export class MyClientAction extends Component {
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.state = useState({
            data: {},
            req_id: this.props.action.context.active_id || 0,
        });

        onWillStart(this.onWillStart);   
    }

    async onWillStart() {
        await this._fetchData();
    }

    async _fetchData() {
        this.state.data = await this.orm.call(
            'purchase.requisition',
            'get_rfq_comparator_data',
            [this.state.req_id],
            {},
        );

        this.state.data = this.state.data || {};
    }

    printPDF() {

        this.action.doAction({
            type: 'ir.actions.report',
            report_type: 'qweb-pdf',
            report_name: 'purchase_rfq_comparator.report_purchase_rfq_comparator',
            report_file: 'purchase_rfq_comparator.report_purchase_rfq_comparator',
            data:  {
                req_id: this.state.req_id,
            },
        });        
    }

    formatAmount(value) {
        if (!value) return '';
        return new Intl.NumberFormat('es-CO', {
            style: 'currency',
            currency: 'COP',
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
        }).format(value);
    }

    cleanHtmlText(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.innerHTML = text;
        return div.textContent || div.innerText || '';
    }

}

MyClientAction.template = "purchase_rfq_comparator.clientaction";

registry.category("actions").add("purchase_rfq_comparator.MyClientAction", MyClientAction);