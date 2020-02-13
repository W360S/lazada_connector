# -*- coding: utf-8 -*-

from odoo import models, fields
import logging

_logger = logging.getLogger(__name__)


class LazadaConnectorSetting(models.Model):

    _name = 'lazada_connector.settings'
    _description = 'Setting for lazada API'

    app_id = fields.Char(string="Client ID")
    app_secret = fields.Char(string="Client Secret")
    access_token = fields.Char(string="Access Token")

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    lazada = fields.Many2one(
        'lazada_connector.settings',
        string='Lazada API Settings',
        default=lambda self: self.env['lazada_connector.settings'].search([], limit=1)
    )

    lazada_connector_app_id = fields.Char(related='lazada.app_id', string='App ID', readonly=False)
    lazada_connector_app_secret = fields.Char(related='lazada.app_secret', string='App Secret', readonly=False)
    lazada_connector_access_token = fields.Char(related='lazada.access_token', string='Secret Key', readonly=False)

    def sync_lazada_categories(self):
        self.env.ref('lazada_connector.action_load_primary_category').run()
