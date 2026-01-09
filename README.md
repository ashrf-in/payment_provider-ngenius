# N-Genius Payment Provider for Odoo

![Odoo Version](https://img.shields.io/badge/Odoo-19.0-blue)
![License](https://img.shields.io/badge/License-LGPL--3-green)
![N-Genius](https://img.shields.io/badge/N--Genius-Network%20International-orange)

A robust payment provider module for Odoo 19 that integrates **N-Genius** payment gateway by [Network International](https://www.network.ae).

## Features

✅ **Card Payments** - Accept Visa, Mastercard, and American Express  
✅ **3D Secure (3DS2)** - Full EMV 3DS authentication with strict ECI validation  
✅ **Sandbox & Production** - Easy switching between environments  
✅ **Refund Support** - Process full refunds through the Odoo interface  
✅ **Webhook Notifications** - Real-time payment status updates  
✅ **Hosted Payment Page** - Secure redirect-based payment flow

## Installation

1. Copy the `payment_ni_ngenius` folder to your Odoo addons directory
2. Update the app list: **Apps → Update Apps List**
3. Install the module: Search for "N-Genius" and click **Install**

## Configuration

1. Go to **Invoicing → Configuration → Payment Providers**
2. Select **N-Genius** and click **Activate**
3. Configure your credentials:
   - **API Key**: Your N-Genius API key from the merchant portal
   - **Outlet Reference**: Your outlet reference ID
4. Select **Test Mode** for sandbox or **Enabled** for production
5. **Save** and you're ready to accept payments!

## API Credentials

Get your credentials from the N-Genius merchant portal:

- **Sandbox**: https://merchant.sandbox.ngenius-payments.com
- **Production**: https://merchant.ngenius-payments.com

## 3D Secure Validation

This module implements strict 3DS authentication:

| ECI Value | Card Brand | Meaning                      | Result      |
| --------- | ---------- | ---------------------------- | ----------- |
| 05        | Visa       | Fully Authenticated          | ✅ Success  |
| 02        | Mastercard | Fully Authenticated          | ✅ Success  |
| 06        | Visa       | Attempted, Not Authenticated | ❌ Declined |
| 01        | Mastercard | Attempted, Not Authenticated | ❌ Declined |
| 07        | Visa       | Not Enrolled                 | ❌ Declined |
| 00        | Mastercard | Not Enrolled                 | ❌ Declined |

## Supported Currencies

The module supports all currencies enabled in your N-Genius outlet, including:

- AED, USD, EUR, GBP, SAR, and 50+ more

## Test Cards (Sandbox)

| Card Number         | Brand      | Result       |
| ------------------- | ---------- | ------------ |
| 4111 1111 1111 1111 | Visa       | Success      |
| 5200 0000 0000 0007 | Mastercard | Success      |
| 4000 0000 0000 0002 | Visa       | 3DS Required |

## Requirements

- Odoo 19.0 (Enterprise or Community)
- `payment` module (auto-installed)
- `account_payment` module (auto-installed)
- Active N-Genius merchant account

## Support

- **Author**: Ashraf
- **Website**: [www.ashrf.in](https://www.ashrf.in)
- **GitHub**: [github.com/ashrf-in](https://github.com/ashrf-in)
- **Issues**: Report bugs on GitHub

## License

This module is licensed under LGPL-3. See [LICENSE](LICENSE) for details.

## Changelog

### Version 19.0.1.0.0

- Initial release for Odoo 19
- Full 3DS2 authentication with ECI validation
- Card payments (Visa, Mastercard, Amex)
- Refund support
- Webhook notifications
- Sandbox and Production environments
