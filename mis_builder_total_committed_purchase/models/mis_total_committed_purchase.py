# Copyright 2017 ACSONE SA/NV
# Copyright 2022 Camptocamp SA (https://www.camptocamp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, tools
from odoo.modules.module import get_module_resource


class MisTotalCommittedPurchase(models.Model):

    _name = "mis.total.committed.purchase"
    _description = "MIS Total Purchase Commitment"
    _auto = False

    name = fields.Char()
    account_id = fields.Many2one(comodel_name="account.account")
    company_id = fields.Many2one(comodel_name="res.company")
    product_id = fields.Many2one(comodel_name="product.product")
    purchase_order_id = fields.Many2one(comodel_name="purchase.order")
    credit = fields.Float()
    debit = fields.Float()
    date = fields.Date()

    analytic_account_ids = fields.Many2many(
        comodel_name="account.analytic.account",
        relation="mis_total_committed_purchase_analytic_account_rel",
        column1="mis_total_committed_purchase_id",
        column2="analytic_account_id",
        string="Analytic Accounts",
    )

    def init(self):

        with open(
            get_module_resource(
                "mis_builder_total_committed_purchase",
                "data",
                "mis_total_committed_purchase.sql",
            )
        ) as f:
            tools.drop_view_if_exists(self.env.cr, "mis_total_committed_purchase")
            self.env.cr.execute(f.read())

        with open(
            get_module_resource(
                "mis_builder_total_committed_purchase",
                "data",
                "mis_total_committed_purchase_analytic_account_rel.sql",
            )
        ) as f2:
            # Create many2many relation for account.analytic.account
            tools.drop_view_if_exists(
                self.env.cr, "mis_total_committed_purchase_analytic_account_rel"
            )
            self.env.cr.execute(f2.read())
