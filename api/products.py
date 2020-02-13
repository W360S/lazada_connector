from .sdk.base import *
import xml.etree.ElementTree as ET
from odoo.modules.module import get_module_resource
import urllib.parse
import logging

_logger = logging.getLogger(__name__)

class Product:

    API_URL = 'https://api.lazada.vn/rest'
    app_key = ''
    app_secret = ''
    access_token = ''

    def __init__(self, app_key, app_secret, access_token):
        self.app_key = app_key
        self.app_secret = app_secret
        self.access_token = access_token
        self.client = LazopClient(self.API_URL, app_key, app_secret)
        self.xml_path = get_module_resource('lazada_connector', 'api/xmls/products')

    def _getXmlPath(self, path):
        return self.xml_path + '/' + path

    def _getXmlSku(self, params):
        seller_sku = params.get('seller_sku', '')
        color_family = params.get('color_family', '')
        size = params.get('size', '')
        quantity = params.get('quantity', '')
        price = params.get('price', '')
        package_length = params.get('package_length', '')
        package_height = params.get('package_height', '')
        package_weight = params.get('package_weight', '')
        package_width = params.get('package_width', '')
        package_content = params.get('package_content', '')
        images = params.get('images', [])
        attribute_xml = '<SellerSku>' + seller_sku + '</SellerSku><color_family>' + color_family + '</color_family><size>' + size + '</size><quantity>' + str(quantity) + '</quantity><price>' + str(price) + '</price><package_length>' + str(package_length) + '</package_length><package_height>' + str(package_height) + '</package_height><package_weight>' + str(package_weight) + '</package_weight><package_width>' + str(package_width) + '</package_width><package_content>' + str(package_content) + '</package_content>'
        image_xml = ''
        for image in images:
            image_xml += '<Image>' + urllib.parse.quote(image) + '</Image>'
        return '<Sku>' + attribute_xml + '<Images>' + image_xml + '</Images>' + '</Sku>'

    def createSubElement(parent, tag, attrib={}, text=None, nsmap=None, **extra):
        result = ET.SubElement(parent, tag, attrib, nsmap, **extra)
        result.text = text
        return result

    # Use this API to retrieve all product brands in the system.
    def getBrands(self, offset=0, limit=100):
        request = LazopRequest('/brands/get', 'GET')
        request.add_api_param('offset', offset)
        request.add_api_param('limit', limit)
        response = self.client.execute(request)
        return response.body

    # Use this API to get a list of attributes for a specified product category.
    def getCategoryAttributes(self, category_id):
        request = LazopRequest('/category/attributes/get', 'GET')
        request.add_api_param('primary_category_id', category_id)
        response = self.client.execute(request)
        return response.body

    # Get product's category suggestion by product title
    def getCategorySuggestion(self, field, value):
        request = LazopRequest('/product/category/suggestion/get', 'GET')
        request.add_api_param(field, value)
        response = self.client.execute(request, self.access_token)
        return response.body

    # Use this API to retrieve the list of all product categories in the system.
    def getCategoryTree(self):
        request = LazopRequest('/category/tree/get', 'GET')
        response = self.client.execute(request)
        return response.body

    # Get single product by ItemId or SellerSku.
    def getProductItem(self, item_id, seller_sku):
        request = LazopRequest('/product/item/get', 'GET')
        request.add_api_param('item_id', item_id)
        request.add_api_param('seller_sku', seller_sku)
        response = self.client.execute(request, self.access_token)
        return response.body

    # Use this API to get detailed information of the specified products.
    def getProducts(self, params):
        request = LazopRequest('/products/get', 'GET')
        request.add_api_param('filter', 'live')
        for key in params:
            request.add_api_param(key, params[key])
        if 'offset' not in params:
            request.add_api_param('offset', '0')
        if 'limit' not in params:
            request.add_api_param('limit', '10')
        response = self.client.execute(request, self.access_token)
        return response.body

    def createProduct(self, params):
        tree = ET.parse(self._getXmlPath('create_product.xml'))
        root = tree.getroot()
        root.find('./Product/PrimaryCategory').text = params.get('primary_category')
        root.find('./Product/Attributes/name').text = params.get('name')
        root.find('./Product/Attributes/short_description').text = params.get('short_description')
        root.find('./Product/Attributes/description').text = params.get('description')
        root.find('./Product/Attributes/model').text = params.get('model')
        skus = root.find('./Product/Skus')
        for variant_params in params.get('variants'):
            sku = ET.fromstring(self._getXmlSku(variant_params))
            skus.append(sku)

        xml = ET.tostring(root, encoding='utf8', method='xml')
        xml = xml.decode('utf-8').replace('\n', '')

        request = LazopRequest('/product/create')
        request.add_api_param('payload', xml)
        response = self.client.execute(request, self.access_token)
        return response.body

    def updateProduct(self, params):
        tree = ET.parse(self._getXmlPath('create_product.xml'))
        root = tree.getroot()
        root.find('./Product/PrimaryCategory').text = params.get('primary_category')
        root.find('./Product/Attributes/name').text = params.get('name')
        root.find('./Product/Attributes/short_description').text = params.get('short_description')
        root.find('./Product/Attributes/description').text = params.get('description')
        root.find('./Product/Attributes/model').text = params.get('model')
        skus = root.find('./Product/Skus')
        for variant_params in params.get('variants'):
            sku = ET.fromstring(self._getXmlSku(variant_params))
            skus.append(sku)

        xml = ET.tostring(root, encoding='utf8', method='xml')
        xml = xml.decode('utf-8').replace('\n', '')

        request = LazopRequest('/product/update')
        request.add_api_param('payload', xml)
        response = self.client.execute(request, self.access_token)
        return response.body

    # Use this API to remove an existing product, some SKUs in one product, or all SKUs in one product. System supports a maximum number of 50 SellerSkus in one request.
    def removeProduct(self, seller_sku_list):
        request = LazopRequest('/product/remove')
        request.add_api_param('seller_sku_list', seller_sku_list)
        response = self.client.execute(request, self.access_token)
        return response.body

    # Use this API to get the quality control status of items being listed.
    def getQcStatus(self, params):
        request = LazopRequest('/product/qc/status/get', 'GET')
        for key in params:
            request.add_api_param(key, params[key])
        if 'offset' not in params:
            request.add_api_param('offset', '0')
        if 'limit' not in params:
            request.add_api_param('limit', '10')
        response = self.client.execute(request, self.access_token)
        return response.body

    # Use this API to get the returned information from the system for the MigrateImages API.
    def getResponse(self, batch_id):
        request = LazopRequest('/image/response/get', 'GET')
        request.add_api_param('batch_id', batch_id)
        response = self.client.execute(request, self.access_token)
        return response.body

    # Use this API to migrate a single image from an external site to Lazada site. Allowed image formats are JPG and PNG. The maximum size of an image file is 1MB.
    def migrateImage(self, image_url):
        tree = ET.parse(self._getXmlPath('migrate_image.xml'))
        root = tree.getroot()
        url = root.find('./Image/Url')
        url.text = image_url
        xml = ET.tostring(root, encoding='utf8', method='xml')
        xml = xml.decode('utf-8').replace('\n', '')
        request = LazopRequest('/image/migrate')
        request.add_api_param('payload', xml)
        response = self.client.execute(request, self.access_token)
        _logger.info(response.body)
        if response.body.get('batch_id'):
            _logger.info(batch_id)
            image = self.getResponse(response.get('batch_id'))
            if image.get('data', {}).get('image'):
                return image.get('data', {}).get('image', {}).get('url')
        return False

    # Use this API to migrate multiple images from an external site to Lazada site. Allowed image formats are JPG and PNG. The maximum size of an image file is 1MB. A single call can migrate 8 images at most.
    def migrateImages(self, image_urls):
        tree = ET.parse(self._getXmlPath('migrate_images.xml'))
        root = tree.getroot()
        images = root.find('./Images')
        for url in image_urls:
            ET.SubElement(images, 'Url', {}).text = url
        xml = ET.tostring(root, encoding='utf8', method='xml')
        xml = xml.decode('utf-8').replace('\n', '')
        request = LazopRequest('/images/migrate')
        request.add_api_param('payload', xml)
        response = self.client.execute(request, self.access_token)
        if response.body.get('batch_id'):
            images = self.getResponse(response.body.get('batch_id'))
            if images.get('data', {}).get('images'):
                return [image.get('url') for image in images.get('data', {}).get('images')]
        return []

    # Use this API to set the images for an existing product by associating one or more image URLs with it.
    def setImages(self, seller_sku, image_urls):
        tree = ET.parse(self._getXmlPath('set_images.xml'))
        root = tree.getroot()
        images = root.find('./Product/Skus/Sku/Images')
        sku = root.find('./Product/Skus/Sku/SellerSku')
        sku.text = seller_sku
        for url in image_urls:
            ET.SubElement(images, 'Image', {}).text = url
        xml = ET.tostring(root, encoding='utf8', method='xml')
        xml = xml.decode('utf-8').replace('\n', '')
        _logger.info(xml)
        request = LazopRequest('/images/set')
        request.add_api_param('payload', xml)
        response = self.client.execute(request, self.access_token)
        if response.get('data'):
            return response.body
        else:
            return response.get('message')
        return False
