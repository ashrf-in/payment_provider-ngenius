# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request
from odoo.tools import mute_logger

from odoo.addons.payment.logging import get_payment_logger
from odoo.addons.payment_ni_ngenius import const

_logger = get_payment_logger(__name__, const.SENSITIVE_KEYS)


class NGeniusController(http.Controller):
    _return_url = '/payment/ngenius/return'
    _webhook_url = '/payment/ngenius/webhook'

    @http.route(_return_url, type='http', methods=['GET'], auth='public', csrf=False)
    def ngenius_return(self, **data):
        """Process the payment data sent by N-Genius after redirection from payment.

        :param dict data: The payment data, including the reference and order ref.
        """
        # Get transaction reference from URL (we included it in the redirect URL)
        reference = data.get('reference')
        order_ref = data.get('ref')  # N-Genius order reference
        
        # Find transaction by reference or by provider_reference (order ref)
        tx_sudo = None
        if reference:
            tx_sudo = request.env['payment.transaction'].sudo().search([
                ('reference', '=', reference),
                ('provider_code', '=', 'ngenius'),
            ], limit=1)
        
        if not tx_sudo and order_ref:
            tx_sudo = request.env['payment.transaction'].sudo().search([
                ('provider_reference', '=', order_ref),
                ('provider_code', '=', 'ngenius'),
            ], limit=1)
        
        if not tx_sudo:
            _logger.warning("N-Genius: No transaction found for reference=%s, order_ref=%s", reference, order_ref)
            with mute_logger('werkzeug'):
                return request.redirect('/payment/status')
        
        # Fetch order details from N-Genius API
        try:
            order_ref_to_fetch = order_ref or tx_sudo.provider_reference
            if order_ref_to_fetch:
                access_token = tx_sudo.provider_id._ngenius_get_access_token()
                outlet_ref = tx_sudo.provider_id.ngenius_outlet_ref
                endpoint = const.ORDER_DETAIL_ENDPOINT.format(
                    outlet_ref=outlet_ref, order_ref=order_ref_to_fetch
                )
                order_data = tx_sudo.provider_id._ngenius_make_request(
                    'GET', endpoint, access_token=access_token
                )
                
                # Process the payment data
                payment_data = {
                    'reference': tx_sudo.reference,
                    'order_data': order_data,
                }
                tx_sudo._process('ngenius', payment_data)
            else:
                _logger.warning("N-Genius: No order reference to fetch - cannot verify payment")
                tx_sudo._set_error("Payment could not be verified - no order reference")
        except ValidationError as e:
            _logger.exception("Failed to process the return from N-Genius")
            tx_sudo._set_error(str(e))
        except Exception as e:
            _logger.exception("Unexpected error processing N-Genius return")
            tx_sudo._set_error("Payment processing failed: %s" % str(e))

        # Redirect the user to the status page
        with mute_logger('werkzeug'):
            return request.redirect('/payment/status')

    @http.route(_webhook_url, type='http', methods=['POST'], auth='public', csrf=False)
    def ngenius_webhook(self):
        """Process the payment data sent by N-Genius to the webhook.

        :return: An empty string to acknowledge the notification.
        :rtype: str
        """
        event = request.get_json_data()
        
        try:
            # Extract transaction reference and order data
            reference = event.get('merchantOrderReference')
            if reference:
                tx_sudo = request.env['payment.transaction'].sudo()._search_by_reference(
                    'ngenius', {'reference': reference}
                )
                
                # Process the webhook data
                payment_data = {
                    'reference': reference,
                    'order_data': event,
                }
                tx_sudo._process('ngenius', payment_data)
        except ValidationError:
            _logger.exception("Unable to process the webhook; skipping to acknowledge")
        
        return request.make_json_response('')
