-- CREATE OR REPLACE FUNCTION add_two_number(
-- 	first integer,
-- 	second integer)
--     RETURNS integer
--     LANGUAGE 'plpgsql'
-- AS $$
-- begin
--     return first + second;
-- end;
-- $$;

-- create or replace function add_two_number(x int, y int, out result int)
-- language 'plpgsql'
-- as $$
-- begin
--     result = x + y;
-- end;
-- $$;


-- TODO: write function to calculate consine sim
with summary as (
    select 
        src.value as src_value, 
        susp.value as susp_value,
        add_two_number(src.value, susp.value) as result
    from susp, source as src
)
select 
    *
from 
    summary
where 
result > 80;


