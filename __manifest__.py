# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Payment Provider: N-Genius',
    'version': '19.0.1.0.0',
    'category': 'Accounting/Payment Providers',
    'sequence': 350,
    'summary': "Accept card payments via N-Genius by Network International.",
    'description': """
N-Genius Payment Provider for Odoo
==================================

This module integrates the N-Genius payment gateway by Network International 
into Odoo, enabling merchants to accept card payments securely.

Features:
- Card payments (Visa, Mastercard, American Express)
- 3D Secure (3DS2) authentication with strict ECI validation
- Sandbox and Production environment support
- Refund support
- Webhook notifications
- Hosted Payment Page (redirect flow)

For more information, visit: https://www.network.ae/en/solutions/partners/n-genius
    """,
    'depends': ['payment', 'account_payment'],
    'data': [
        'views/payment_provider_views.xml',
        'views/payment_ngenius_templates.xml',
        'data/account_payment_method_data.xml',
        'data/payment_provider_data.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'payment_provider_ngenius/static/src/**/*',
        ],
    },
    'author': 'Ashraf',
    'website': 'https://www.ashrf.in',
    'maintainer': 'Ashraf',
    'support': 'hi@ashrf.in',
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
    'images': ['static/description/icon.png'],
}
