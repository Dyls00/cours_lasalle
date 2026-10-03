-- ============================================================================
-- MODULE 2.2 : SQL ANALYTIQUE, MANIPULATION JSON/UNNEST & WINDOW FUNCTIONS
-- ============================================================================

-- 1. CTE + MANIPULATION DE CHAMPS IMBRIQUÉS (STRUCT & UNNEST SUR ARRAYS)
WITH raw_data AS (
    SELECT
        'evt_101' AS event_id,
        'usr_882' AS user_id,
        TIMESTAMP('2026-09-29 10:00:00') AS event_timestamp,
        STRUCT('iOS' AS os, 'Safari' AS browser) AS device,
        [
            STRUCT('laptop-pro' AS item_id, 1299.99 AS price),
            STRUCT('mouse-wireless' AS item_id, 49.99 AS price)
        ] AS cart_items
)
SELECT
    event_id,
    user_id,
    device.os AS device_os,
    item.item_id,
    item.price
FROM
    raw_data,
    UNNEST(cart_items) AS item;

-- ----------------------------------------------------------------------------
-- 2. WINDOW FUNCTIONS : DÉDUPLICATION ET CALCUL DE CUMUL SÉQUENTIEL
-- ----------------------------------------------------------------------------
WITH user_activity AS (
    SELECT 'usr_100' AS user_id, TIMESTAMP('2026-09-29 10:00:00') AS ts, 50.0 AS amount UNION ALL
    SELECT 'usr_100', TIMESTAMP('2026-09-29 10:15:00'), 30.0 UNION ALL
    SELECT 'usr_100', TIMESTAMP('2026-09-29 10:15:00'), 30.0 UNION ALL -- Doublon exact
    SELECT 'usr_200', TIMESTAMP('2026-09-29 11:00:00'), 120.0
),
deduplicated AS (
    SELECT
        *,
        ROW_NUMBER() OVER(PARTITION BY user_id, ts, amount ORDER BY ts) AS row_num
    FROM user_activity
)
SELECT
    user_id,
    ts,
    amount,
    SUM(amount) OVER(PARTITION BY user_id ORDER BY ts ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total
FROM deduplicated
WHERE row_num = 1;
