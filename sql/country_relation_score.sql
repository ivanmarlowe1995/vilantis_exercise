
create or replace view edw.country_relation_score as 
with base_table as(
	select
		w1.id, 
		w1.description,
		w2.nicename  as country
	from 
		edw.country_relation_revised  w1 
		join edw.dim_country w2
	    on 
	   		w1.description like '%' || w2.nicename || '%' and w1.description <> w2.nicename
--	   		or w1.description like w2.nicename || ' %' and w1.description <> w2.nicename
),
agg_tbl as (
	select
		t1.id,
		t1.description,
		t1.country,
		t2.country_count
	from
		base_table t1
	inner join
		(select
			id,
			description,
			count(1) country_count
		from base_table
			group by 1,2
		) t2
	on t1.id = t2.id
),
gen_tbl_1 as (
	select
		*
	from
		agg_tbl
	where 
		country_count = 2
),
gen_tbl_2 as (
	select
		*
	from
		agg_tbl
	where 
		country_count > 2
),
final_gen_tbl_2 as (
	select
		id,
		country
	from
		(
			select
				id,
				country_similar country,
				count(1) country_count
			from
				(
					select
						a.id,
						a.country,
						b.country country_similar
					from
						gen_tbl_2 a
					left join gen_tbl_2 b on a.id = b.id and a.country like '%'||b.country||'%'
				) a
			group by 1, 2
		) a 
		where country_count = 1
),
tbl_gen_combined as (
	select 
		id,
		country
	from 
		gen_tbl_1
	union all
	select
		id,
		country
	from
		final_gen_tbl_2
),
tbl_relationships as (
	select
		md5(a.country_rel_a||', '||a.country_rel_b) country_id,
		a.country_rel_a country_a,
		a.country_rel_b country_b,
		substring(max(b.date_created)::varchar, 1, 19) date_updated,
		sum(b.rep_change) relationship_score
	from
		(
			select
				a.id,
				max(a.country_rel_a) country_rel_a,
				max(a.country_rel_b) country_rel_b
			from
				(
					select
						id,
						case when rn = 1 then country else null end as country_rel_a,
						case when rn = 2 then country else null end as country_rel_b
					from
						(
							select
								id,
								country,
								row_number() over(partition by id order by country asc) rn
							from
								tbl_gen_combined 
						) a
				) a
			group by 1
		) a
	inner join 
		edw.country_relation_revised b 
	on 
		a.id = b.id
	group by 1, 2, 3
	order by relationship_score desc
) 
select * from tbl_relationships
