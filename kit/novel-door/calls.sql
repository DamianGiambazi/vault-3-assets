-- calls.sql — what crossed the boundary, and how did the reader work? DuckDB audits the server's own call log.
-- Run from C:\Dev\novel-door :   duckdb -bail -f calls.sql
-- An archived log (off camera):   duckdb -bail -cmd "SET VARIABLE log = 'C:/path/calls-R2.jsonl'" -f calls.sql

.mode box
.maxwidth 120
SET VARIABLE log = coalesce(getvariable('log'), 'calls.jsonl');

-- 1. Every call the client made, in order.
SELECT ts, tool, left(coalesce(args->>'question', args->>'word', args->>'chapter', args->>'title'), 60) AS asked,
       chapters, chars_out
FROM read_json(getvariable('log'), columns = {ts: 'VARCHAR', tool: 'VARCHAR', args: 'JSON', chapters: 'INTEGER[]', chars_out: 'BIGINT', vector_in_output: 'BOOLEAN'}) ORDER BY ts;

-- 2. Per tool: how often, how much text left the machine, which chapters were opened.
SELECT tool, count(*) AS calls, sum(chars_out) AS chars_out,
       list_sort(list_distinct(flatten(list(chapters)))) AS chapters_touched
FROM read_json(getvariable('log'), columns = {ts: 'VARCHAR', tool: 'VARCHAR', args: 'JSON', chapters: 'INTEGER[]', chars_out: 'BIGINT', vector_in_output: 'BOOLEAN'}) GROUP BY tool ORDER BY calls DESC;

-- 3. The reader's strategy (Performance Edition, prediction P2): did it search, or read the whole book?
SELECT 'READER  reads=' || count(*) FILTER (WHERE tool = 'read_chapter')
       || '  chapters_read=' || coalesce(len(list_distinct(flatten(list(chapters) FILTER (WHERE tool = 'read_chapter')))), 0) || '/24'
       || '  meaning_searches=' || count(*) FILTER (WHERE tool = 'search_by_meaning')
       || '  keyword_searches=' || count(*) FILTER (WHERE tool = 'keyword_search')
       || CASE WHEN coalesce(len(list_distinct(flatten(list(chapters) FILTER (WHERE tool = 'read_chapter')))), 0) >= 20
               THEN '  -> READ_WHOLE_BOOK' ELSE '  -> SELECTIVE_READER' END AS strategy
FROM read_json(getvariable('log'), columns = {ts: 'VARCHAR', tool: 'VARCHAR', args: 'JSON', chapters: 'INTEGER[]', chars_out: 'BIGINT', vector_in_output: 'BOOLEAN'});

-- 4. The firewall: text only. A single vector in any reply fails the audit.
SELECT CASE WHEN count(*) FILTER (WHERE vector_in_output) = 0
            THEN 'FIREWALL_HELD  calls=' || count(*) || '  vectors_out=0  chars_out=' || sum(chars_out)
            ELSE error('FIREWALL_BREACH  vectors_out=' || count(*) FILTER (WHERE vector_in_output)) END AS verdict
FROM read_json(getvariable('log'), columns = {ts: 'VARCHAR', tool: 'VARCHAR', args: 'JSON', chapters: 'INTEGER[]', chars_out: 'BIGINT', vector_in_output: 'BOOLEAN'});
