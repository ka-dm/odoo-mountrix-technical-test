# -*- coding: utf-8 -*-
{
    'name': "Purchase RFQ Comparator",

    'summary': """
        Allows efficient and detailed comparison and analysis of supplier 
        quotations for better decision making.""",

    'description': """
        Module for comparing supplier quotations that includes:
        * Side-by-side comparison of quotations
    """,

    'author': "Kevodoo",
    'website': "https://www.kevodoo.com",

    'category': 'Purchase/Analysis',
    'version': '18.0.1.0.1',

    'depends': [
        'base',
        'purchase',
        'purchase_requisition',
        'stock',
    ],

    'data': [
        # 'security/ir.model.access.csv',
        'views/purchase_requisition_views.xml',
        'report/report_purchase_rfq_comparator_template.xml',
        'report/report_purchase_rfq_comparator_action.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'purchase_rfq_comparator/static/src/js/report.js',
            'purchase_rfq_comparator/static/src/xml/**/*',
        ],
    },


    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
