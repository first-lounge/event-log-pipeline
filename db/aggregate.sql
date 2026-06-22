-- 1) 이벤트 타입별 발생 횟수 
select event_type, count(*) as cnt
from events
group by event_type
order by cnt desc;

-- 2) 시간대별 이벤트 추이
select date_trunc('day', event_time) as daily, event_type, count(*) as cnt
from events
group by daily, event_type
order by daily, event_type;

-- 3) 전체 대비 에러 비율
select 
	ROUND(100.0 * count(*) / (select count(*) from events), 2) as total_ratio
from error;

-- 4) 에러별 비율
select 
	error_code, 
	error_msg,
	ROUND(100.0 * count(*) / (select count(*) from events), 2) as ratio_per_error
from error
group by error_code, error_msg
order by ratio_per_error desc;

-- 5) 페이지뷰 TOP N
select page_name, count(*) as cnt
from events
where event_type='page_view'
group by page_name
order by cnt desc
limit 10;