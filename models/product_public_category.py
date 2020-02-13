# -*- coding: utf-8 -*-

from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)

class ProductPublicCategory(models.Model):
    _inherit = 'product.public.category'

    lazada_category_id = fields.Char(string='Category Lazada ID', help='ID Danh mục sản phẩm Lazada tương ứng')
