# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.addons.lazada_connector.api.products import Product
from odoo.addons.lazada_connector.helpers.util import get_image_url
import logging

_logger = logging.getLogger(__name__)


class ProductTemplateWizard(models.TransientModel):
    _name = 'lazada_connector.sync_product_template_wizard'
    _description = 'Synchonous product to Lazada'

    product_template_ids = fields.Many2many('product.template', 'lazada_connector_sync_product_template_relation_wizard', 'sync_product_template_wizard_id', 'product_temlate_id', string='Danh sách sản phẩm')

    def sync_product_template_list(self):
        setting = self.env['lazada_connector.settings'].search([], limit=1)
        if not setting.app_id or not setting.app_secret or not setting.access_token:
            raise ValidationError('Vui lòng cài đặt Lazada API Token trước')
        productApi = Product(setting.app_id, setting.app_secret, setting.access_token)

        for record in self.product_template_ids:
            if not record.package_weight or not record.package_width or not record.package_length or not record.package_height:
                raise ValidationError('Vui lòng nhập đủ kích thước cho sản phẩm')
            if not record.primary_category_id and not record.primary_category_id.category_id:
                raise ValidationError('Sản phẩm chưa có thông tin Lazada Primary Category hoặc thông tin không hợp lệ.')
            if not record.model:
                raise ValidationError('Vui lòng nhập Lazada Model cho sản phẩm')
            variants = []
            for product in record.product_variant_ids:
                product_images = [get_image_url(image, 'image_1920', 1920) for image in product.product_template_image_ids]
                if len(product_images):
                    product_images = productApi.migrateImages(product_images)
                color_family = ' '.join([attr.name for attr in product.product_template_attribute_value_ids])
                variants.append({
                    'seller_sku': product.barcode if product.barcode else record.barcode,
                    'color_family': color_family if color_family else 'Mặc định',
                    'quantity': int(product.qty_available),
                    'price': int(product.lst_price),
                    'images': product_images,
                    'package_weight': record.package_weight,
                    'package_width': record.package_width,
                    'package_length': record.package_length,
                    'package_height': record.package_height
                })
            data = {
                'primary_category': record.primary_category_id.category_id,
                'name': record.name,
                'short_description': record.short_description,
                'description': record.description,
                'model': record.model,
                'variants': variants
            }
            response = productApi.updateProduct(data) if record.lazada_item_id else productApi.createProduct(data)
            if response:
                if response.get('code') == '500' and len(response.get('detail')):
                    raise ValidationError(response.get('message') + ': ' + response.get('detail')[0].get('message'))
                elif response.get('code') == 'IllegalAccessToken':
                    raise ValidationError('Lazada Token không đúng hoặc đã hết hạn.')
                elif response.get('code') == '0':
                    if not record.lazada_item_id and response.get('data').get('item_id'):
                        record.write({'lazada_item_id': response.get('data').get('item_id')})
                else:
                    pass
