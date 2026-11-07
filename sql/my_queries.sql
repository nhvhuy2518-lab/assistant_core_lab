-- F3: Các topic nhận nhiều thumbs-down (-1) nhất
-- Thành viên 5 - Nguyên

SELECT i.topic,
       COUNT(*) AS thumbs_down_count
FROM interaction i
JOIN feedback f
    ON f.request_id = i.request_id
WHERE f.rating = -1
  AND i.topic IS NOT NULL
GROUP BY i.topic
ORDER BY thumbs_down_count DESC, i.topic;

-- H2: Tỷ lệ câu trả lời chưa giải quyết
-- hoặc sử dụng phương án dự phòng theo intent
-- Thành viên 5 - Nguyên

SELECT intent,
       COUNT(*) AS total_requests,
       SUM(
           CASE
               WHEN resolved = 0 OR degraded = 1
               THEN 1 ELSE 0
           END
       ) AS fallback_count,
       ROUND(
           100.0 * SUM(
               CASE
                   WHEN resolved = 0 OR degraded = 1
                   THEN 1 ELSE 0
               END
           ) / COUNT(*),
           1
       ) AS fallback_pct
FROM interaction
GROUP BY intent
ORDER BY fallback_pct DESC;

-- =====================================================
-- F3: ACTUAL QUERY RESULTS
-- Database: assistant.db (300 seeded interactions)
-- =====================================================
-- topic     | thumbs_down_count
-- H26-4.2   | 8
-- H26-5.3   | 8
-- H26-7.2   | 2

-- Analysis:
-- H26-4.2 and H26-5.3 received the most negative
-- feedback, with 8 thumbs-down each.


-- =====================================================
-- H2: ACTUAL QUERY RESULTS
-- Database: assistant.db (300 seeded interactions)
-- =====================================================
-- intent    | total_requests | fallback_count | fallback_pct
-- unknown   | 26             | 26             | 100.0
-- rule      | 140            | 34             | 24.3
-- greeting  | 26             | 2              | 7.7
-- office    | 47             | 1              | 2.1
-- fee       | 61             | 1              | 1.6

-- Analysis:
-- Unknown has the highest fallback rate (100%).
-- Among other intents, rule has the highest fallback
-- rate (24.3%), indicating room for improvement.