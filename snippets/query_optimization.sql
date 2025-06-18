/*
PostgreSQL Optimization Example
Demonstrates index strategy for performance improvement
*/

-- Partial index for frequent queries
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_orders_active 
ON orders (customer_id, last_updated)
WHERE status = 'active';

-- Optimized JOIN pattern using CTE
EXPLAIN ANALYZE
WITH recent_orders AS MATERIALIZED (
  SELECT id, total, customer_id
  FROM orders
  WHERE created_at > CURRENT_DATE - INTERVAL '30 days'
    AND status = 'shipped'
)
SELECT o.id, o.total, c.email 
FROM recent_orders o
JOIN customers c USING (customer_id);