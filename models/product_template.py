# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.addons.lazada_connector.api.products import Product
import logging

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    primary_category_id = fields.Many2one('lazada_connector.primary_categories', ondelete='cascade', string='Primary Category')
    model = fields.Char(string='Model')
    short_description = fields.Text(string='Short Description')
    package_weight = fields.Integer(string='Package Weight')
    package_width = fields.Integer(string='Package Width')
    package_height = fields.Integer(string='Package Height')
    package_length = fields.Integer(string='Package Length')
    lazada_item_id = fields.Char(string='Lazada ID')
