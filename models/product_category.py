# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.addons.lazada_connector.api.products import Product
import logging

_logger = logging.getLogger(__name__)


class LazadaConnectorCategory(models.Model):

    _name = 'lazada_connector.primary_categories'
    _description = 'Primary Categories of Lazada'

    parent_id = fields.Many2one('lazada_connector.primary_categories', index=True, ondelete='set null', string='Parent ID')
    category_id = fields.Char(string="Category ID")
    name = fields.Char(string="Name")
    fullname = fields.Char(compute='_compute_fullname', string="Full Name", store=True)
    leaf = fields.Boolean(default=False, string="Leaf")

    @api.depends('name')
    def _compute_fullname(self):
        for record in self:
            record.fullname = self._get_fullname(record)

    def _get_fullname(self, record):
        if record.parent_id and record.parent_id.name:
            return "%s > %s" % (self._get_fullname(record.parent_id), record.name)
        else:
            return record.name

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, record.fullname))
        return result

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=20):
        args = args or []
        domain_name = [('fullname', 'ilike', name)]
        recs = self.search(domain_name + args, limit=limit)
        return recs.name_get()

    def load_primary_categories(self):
        setting = self.env['lazada_connector.settings'].search([], limit=1)
        if not setting.app_id or not setting.app_secret or not setting.access_token:
            raise ValidationError('Vui lòng cài đặt Lazada API Token trước')
        productApi = Product(setting.app_id, setting.app_secret, setting.access_token)

        primary_categories = productApi.getCategoryTree()
        # _logger.info(primary_categories)
        if primary_categories.get('code') == '0':
            self._create_or_update_category_list(primary_categories.get('data'))

    def _create_or_update_category_list(self, categories, parent_id=''):
        for category in categories:
            exit_category = self.search([('category_id', '=', category.get('category_id'))], limit=1)
            if exit_category:
                if category.get('children') and len(category.get('children')):
                    self._create_or_update_category_list(category.get('children'), exit_category.id)
            else:
                new_category = self.create({
                    'category_id': category.get('category_id'),
                    'parent_id': parent_id,
                    'name': category.get('name'),
                    'leaf': True if str(category.get('leaf')) == 'True' else False
                })
                if category.get('children') and len(category.get('children')):
                    self._create_or_update_category_list(category.get('children'), new_category.id)
        return True
