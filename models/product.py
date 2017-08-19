# -*- coding: utf-8 -*-
###############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2017 Humanytek (<www.humanytek.com>).
#    Manuel Márquez <manuel@humanytek.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from openerp import api, models
from openerp.exceptions import ValidationError
from openerp.tools.translate import _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def _validate_limit_suppliers(
        self, limit_suppliers, product_number_suppliers):
        """Validates that number of suppliers does not exceed the limit"""

        if limit_suppliers >= 0:
            if product_number_suppliers > limit_suppliers:
                raise ValidationError(_(
                    'You can not add more than %s vendors' % limit_suppliers))

    @api.model
    def create(self, vals):

        IrConfigParameter = self.env['ir.config_parameter']
        exists_parameter_number_suppliers = IrConfigParameter.search([
            ('key', '=', 'product_limit_number_suppliers')
            ])
        if exists_parameter_number_suppliers:
            limit_suppliers = int(exists_parameter_number_suppliers[0].value)

            self._validate_limit_suppliers(
                limit_suppliers, len(vals.get('seller_ids')))

        return super(ProductTemplate, self).create(vals)

    @api.multi
    def write(self, vals):

        IrConfigParameter = self.env['ir.config_parameter']
        exists_parameter_number_suppliers = IrConfigParameter.search([
            ('key', '=', 'product_limit_number_suppliers')
            ])
        if exists_parameter_number_suppliers:
            limit_suppliers = int(exists_parameter_number_suppliers[0].value)

            if 'seller_ids' in vals:
                self._validate_limit_suppliers(
                    limit_suppliers, len(vals.get('seller_ids')))

        return super(ProductTemplate, self).write(vals)
