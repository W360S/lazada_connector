# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2019-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Niyas Raphy and Sreejith P (odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

{
    'name': 'Lazada Connector',
    'version': '1.0',
    'summary': 'Synchonous products, variants to Lazada.',
    'category': 'Inventory',
    'author': 'TGCC Techno solutions',
    'maintainer': 'TGCC Techno Solutions',
    'company': 'TGCC Techno Solutions',
    'website': 'https://www.thegioichocon.com',
    'depends': ['base', 'product', 'website_sale'],
    'data': [
        'views/res_config_settings.xml',
        'views/product_public_category.xml',
        'views/product_action.xml',
        'views/sync_data.xml',
        'security/ir.model.access.csv',
        'data/settings.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
