CREATE OR REPLACE VIEW mis_total_committed_purchase_tag_rel AS(
    SELECT
        po_mcp.id AS mis_total_committed_purchase_id,
        jsonb_object_keys(po_rel.analytic_distribution) as account_analytic_tag_id

    FROM 
        purchase_order_line AS po_rel
        INNER JOIN mis_total_committed_purchase AS po_mcp ON
        po_rel.analytic_distribution ? (po_mcp.res_id || '')

    WHERE CAST(po_mcp.res_model AS VARCHAR) = 'purchase.order.line'

    UNION ALL

    SELECT
        inv_mcp.id AS mis_total_committed_purchase_id,
        jsonb_object_keys(inv_rel.analytic_distribution) as account_analytic_tag_id

    FROM account_move_line AS inv_rel
        INNER JOIN mis_total_committed_purchase AS inv_mcp ON
        inv_rel.analytic_distribution ? (inv_mcp.res_id || '')

    WHERE CAST(inv_mcp.res_model AS VARCHAR) = 'account.move.line'
)
