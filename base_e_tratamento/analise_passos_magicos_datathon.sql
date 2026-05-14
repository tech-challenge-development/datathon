-- Análise de defasagem --

Select ra,
       defasagem,
       ian
from base;

Select
    origem,
    ian,
    count(*)
from base
group by 1,2;

With alunos_full as (
    Select ra
    from public.base
    group by ra
    having count(distinct origem) = 3
)

Select
    b.origem,
    ian,
    count(*) qtd_alunos
from base b
right join alunos_full af
    on b.ra = af.ra
group by 1,2;


-- Análise de IDA --

Select
    origem,
    avg(ida)
from base
group by 1;

Select
    por,
    mat,
    ing,
    ida
from base
where origem = 'base2022';

With alunos_full as (
    Select ra
    from public.base
    group by ra
    having count(distinct origem) = 3
)

Select
    b.origem,
    avg(por),
    avg(mat),
    avg(ing),
    (avg(por) + avg(mat) + avg(ing)) / 3,
    avg(b.ida)
from base b
right join alunos_full af
    on b.ra = af.ra
group by 1;

With alunos_full as (
    Select ra
    from public.base
    group by ra
    having max(case when origem = 'base2022' then 1 else 0 end) = 1
       and max(case when origem = 'base2023' then 1 else 0 end) = 1
       and max(case when origem = 'base2024' then 1 else 0 end) = 1
)

Select
    b.origem,
    round(avg(b.ida)::numeric, 6) ida_medio,
    count(*) filter (where b.por is not null) n_por_nao_nulo,
    count(*) filter (where b.mat is not null) n_mat_nao_nulo,
    count(*) filter (where b.ing is not null) n_ing_nao_nulo
from public.base b
join alunos_full af
    on af.ra = b.ra
where b.origem in ('base2022', 'base2023', 'base2024')
group by b.origem
order by b.origem;

With alunos_full as (
    Select ra
    from public.base
    group by ra
    having max(case when origem = 'base2022' then 1 else 0 end) = 1
       and max(case when origem = 'base2023' then 1 else 0 end) = 1
       and max(case when origem = 'base2024' then 1 else 0 end) = 1
)

Select
    b.origem,
    count(*) n_registros,
    round(avg((b.por + b.mat) / 3.0)::numeric, 6) media_soma_sobre_3
from public.base b
join alunos_full a
    on a.ra = b.ra
where b.origem in ('base2022', 'base2023', 'base2024')
  and b.por is not null
  and b.mat is not null
  and b.ing is null
group by b.origem
order by b.origem;

With alunos_full as (
    Select ra
    from public.base
    group by ra
    having max(case when origem = 'base2022' then 1 else 0 end) = 1
       and max(case when origem = 'base2023' then 1 else 0 end) = 1
       and max(case when origem = 'base2024' then 1 else 0 end) = 1
)

Select
    b.origem,
    count(*) n_registros,
    round(avg((b.por + b.mat + b.ing) / 3.0)::numeric, 6) media_soma_sobre_3
from public.base b
join alunos_full a
    on a.ra = b.ra
where b.origem in ('base2022', 'base2023', 'base2024')
  and b.por is not null
  and b.mat is not null
  and b.ing is not null
group by b.origem
order by b.origem;

Select
    origem,
    avg(por) por,
    avg(mat) mat,
    avg(ing) ing
from base
group by 1;

Select origem, 'POR'::text disciplina, por nota
from public.base
where por is not null

union all

Select origem, 'MAT'::text, mat
from public.base
where mat is not null

union all

Select origem, 'ING'::text, ing
from public.base
where ing is not null

order by origem, disciplina;

Select
    left(fase,1),
    avg(ida)
from base
group by 1;

Select
    fase,
    avg(ida)
from base
group by 1;

With base_rotulo as (
    Select
        ida,
        case
            when fase is null then null::text
            when upper(btrim(fase)) = 'ALFA' then 'ALFA'
            when fase ~ '[0-9]' then substring(fase from '[0-9]+')
            else null::text
        end fase_rotulo
    from public.base
)

Select
    fase_rotulo,
    coalesce(avg(ida), 0) avg_ida
from base_rotulo
group by fase_rotulo
order by
    case when fase_rotulo = 'ALFA' then 1 else 0 end,
    fase_rotulo nulls last;


-- Análise de correlação entre engajamento, IDA e IPV --

Select
    origem,
    corr(ieg, ida) pearson_ieg_ida,
    count(*) n
from base
where ieg is not null
  and ida is not null
group by origem;

Select
    origem,
    corr(ieg, ipv) pearson_ieg_ipv,
    count(*) n
from base
where ieg is not null
  and ipv is not null
group by origem;

Select
    atingiu_pv,
    avg(ieg) media_ieg,
    stddev(ieg) desvio_ieg,
    count(*) n
from base
where origem = 'base2022'
  and atingiu_pv is not null
  and ieg is not null
group by 1;


-- Análise de autoavaliação --

Select
    'IAA' indicador,
    round(avg(iaa)::numeric, 3) media,
    round(percentile_cont(0.5) within group (order by iaa)::numeric, 3) mediana,
    round(stddev(iaa)::numeric, 3) desvio_padrao,
    count(*) filter (where iaa is null) nulos
from base

union all

Select
    'IDA',
    round(avg(ida)::numeric, 3),
    round(percentile_cont(0.5) within group (order by ida)::numeric, 3),
    round(stddev(ida)::numeric, 3),
    count(*) filter (where ida is null)
from base

union all

Select
    'IEG',
    round(avg(ieg)::numeric, 3),
    round(percentile_cont(0.5) within group (order by ieg)::numeric, 3),
    round(stddev(ieg)::numeric, 3),
    count(*) filter (where ieg is null)
from base;

Select
    origem ano,
    round(corr(iaa, ida)::numeric, 4) correlacao_iaa_ida,
    count(*) filter (where iaa is not null and ida is not null) n
from base
group by 1
order by 1;

With corr_base as (
    Select
        origem,
        corr(iaa, ida) r,
        count(*) filter (where iaa is not null and ida is not null) n
    from base
    group by 1
)

Select
    origem ano,
    round(r::numeric, 4) correlacao,
    n,
    round((r * sqrt(n - 2) / sqrt(1 - r * r))::numeric, 4) t_stat
from corr_base
order by 1;

With gap as (
    Select (iaa - ida) diff_iaa_ida
    from base
    where iaa is not null
      and ida is not null
)

Select
    'Superestimam (IAA - IDA > 1.5)' grupo,
    count(*) filter (where diff_iaa_ida > 1.5) qtd_alunos,
    round(count(*) filter (where diff_iaa_ida > 1.5)::numeric / count(*) * 100, 1) percentual
from gap

union all

Select
    'Relativamente coerentes (|IAA - IDA| <= 1.5)',
    count(*) filter (where abs(diff_iaa_ida) <= 1.5),
    round(count(*) filter (where abs(diff_iaa_ida) <= 1.5)::numeric / count(*) * 100, 1)
from gap

union all

Select
    'Subestimam (IAA - IDA < -1.5)',
    count(*) filter (where diff_iaa_ida < -1.5),
    round(count(*) filter (where diff_iaa_ida < -1.5)::numeric / count(*) * 100, 1)
from gap;

With gap as (
    Select (iaa - ida) diff_iaa_ida
    from base
    where iaa is not null
      and ida is not null
      and origem = 'base2024'
)

Select
    'Superestimam (IAA - IDA > 1.5)' grupo,
    count(*) filter (where diff_iaa_ida > 1.5) qtd_alunos,
    round(count(*) filter (where diff_iaa_ida > 1.5)::numeric / count(*) * 100, 1) percentual
from gap

union all

Select
    'Relativamente coerentes (|IAA - IDA| <= 1.5)',
    count(*) filter (where abs(diff_iaa_ida) <= 1.5),
    round(count(*) filter (where abs(diff_iaa_ida) <= 1.5)::numeric / count(*) * 100, 1)
from gap

union all

Select
    'Subestimam (IAA - IDA < -1.5)',
    count(*) filter (where diff_iaa_ida < -1.5),
    round(count(*) filter (where diff_iaa_ida < -1.5)::numeric / count(*) * 100, 1)
from gap;

With gap as (
    Select (iaa - ida) diff_iaa_ida
    from base
    where iaa is not null
      and ida is not null
)

Select
    'Superestimam (IAA - IDA > 1.5)' grupo,
    count(*) filter (where diff_iaa_ida > 1.5) qtd_alunos,
    round(count(*) filter (where diff_iaa_ida > 1.5)::numeric / count(*) * 100, 1) percentual
from gap

union all

Select
    'Relativamente coerentes (|IAA - IDA| <= 1.5)',
    count(*) filter (where abs(diff_iaa_ida) <= 1.5),
    round(count(*) filter (where abs(diff_iaa_ida) <= 1.5)::numeric / count(*) * 100, 1)
from gap

union all

Select
    'Subestimam (IAA - IDA < -1.5)',
    count(*) filter (where diff_iaa_ida < -1.5),
    round(count(*) filter (where diff_iaa_ida < -1.5)::numeric / count(*) * 100, 1)
from gap;

Select
    origem ano,
    round(avg(iaa - ida)::numeric, 3) gap_medio,
    round(percentile_cont(0.5) within group (order by iaa - ida)::numeric, 3) gap_mediana
from base
where iaa is not null
  and ida is not null
group by 1
order by 1;

With gap as (
    Select (iaa - ida) diff_iaa_ieg
    from base
    where iaa is not null
      and ida is not null
)

Select
    'Superestimam engajamento (IAA - IEG > 0.5)' grupo,
    count(*) filter (where diff_iaa_ieg > 0.5) qtd_alunos
from gap

union all

Select
    'Alinhados (|IAA - IEG| <= 0.5)',
    count(*) filter (where abs(diff_iaa_ieg) <= 0.5)
from gap

union all

Select
    'Subestimam engajamento (IAA - IEG < -0.5)',
    count(*) filter (where diff_iaa_ieg < -0.5)
from gap;

Select
    origem ano,
    round(corr(iaa, ieg)::numeric, 4) correlacao_iaa_ieg,
    count(*) filter (where iaa is not null and ieg is not null) n
from base
group by 1
order by 1;

With gap as (
    Select (iaa - ieg) diff_iaa_ieg
    from base
    where iaa is not null
      and ieg is not null
)

Select
    count(*) filter (where diff_iaa_ieg > 0.5) superestimam,
    count(*) filter (where abs(diff_iaa_ieg) <= 0.5) alinhados,
    count(*) filter (where diff_iaa_ieg < -0.5) subestimam
from gap;


-- Análise de aspectos psicossociais --

Select
    round(avg(ips)::numeric, 3) media,
    round(percentile_cont(0.5) within group (order by ips)::numeric, 3) mediana,
    round(stddev(ips)::numeric, 3) desvio_padrao,
    min(ips) minimo,
    max(ips) maximo,
    count(*) filter (where ips is null) nulos
from base;

Select
    origem ano,
    round(avg(ips)::numeric, 3) media_ips,
    round(avg(ida)::numeric, 3) media_ida,
    round(avg(ian)::numeric, 3) media_ian,
    round(avg(ieg)::numeric, 3) media_ieg,
    count(*) n
from base
where ips is not null
group by 1
order by 1;

Select
    origem ano,
    round(corr(ips, ida)::numeric, 4) corr_ips_ida,
    round(corr(ips, ieg)::numeric, 4) corr_ips_ieg,
    count(*) filter (where ips is not null and ida is not null) n_ida,
    count(*) filter (where ips is not null and ieg is not null) n_ieg
from base
group by 1
order by 1;

With quartis as (
    Select
        ips,
        ntile(4) over (order by ips) quartil
    from base
    where ips is not null
)

Select
    quartil,
    round(min(ips)::numeric, 2) minimo,
    round(max(ips)::numeric, 2) maximo,
    count(*) n
from quartis
group by 1
order by 1;

Select
    round(ips::numeric, 1) valor_ips,
    count(*) qtd_alunos,
    round(count(*) * 100.0 / sum(count(*)) over (), 1) percentual
from base
where ips is not null
group by round(ips::numeric, 1)
order by valor_ips;

Select
    case
        when ips <= 3.8 then '1. Crítico (≤ 3.8)'
        when ips <= 5.6 then '2. Baixo (3.9–5.6)'
        when ips <= 7.5 then '3. Médio (5.7–7.5)'
        when ips >  7.5 then '4. Alto (> 7.5)'
    end faixa_ips,
    count(*) qtd_alunos,
    round(count(*) * 100.0 / sum(count(*)) over (), 1) percentual,
    round(avg(ida)::numeric, 3) media_ida,
    round(avg(ieg)::numeric, 3) media_ieg,
    round(avg(iaa)::numeric, 3) media_iaa
from base
where ips is not null
group by 1
order by 1;

Select
    case when defasagem < 0 then 'Em Risco' else 'Sem Risco' end grupo,
    round(avg(ips)::numeric, 3) media_ips,
    round(percentile_cont(0.5) within group (order by ips)::numeric, 3) mediana_ips,
    count(*) n
from base
where ips is not null
  and defasagem is not null
group by grupo;

Select
    a.ra,
    a.origem ano_atual,
    a.ips ips_atual,
    a.ida ida_atual,
    a.ieg ieg_atual,
    b.origem ano_anterior,
    b.ips ips_anterior,
    b.ida ida_anterior,
    b.ieg ieg_anterior,
    round((a.ips - b.ips)::numeric, 3) delta_ips,
    round((a.ida - b.ida)::numeric, 3) delta_ida,
    round((a.ieg - b.ieg)::numeric, 3) delta_ieg
from base a
join base b
    on a.ra = b.ra
    and a.origem > b.origem
where a.ips is not null
  and b.ips is not null
order by 1,2;


-- Avaliação psicopedagógica --

Select
    ian,
    count(*) qtd_alunos,
    round(count(*) * 100.0 / sum(count(*)) over(), 1) percentual,
    round(avg(defasagem)::numeric, 3) defasagem_media
from base
group by 1
order by 1;

Select
    ian,
    count(*) n,
    round(avg(ipp)::numeric, 3) media_ipp,
    round(percentile_cont(0.5) within group (order by ipp)::numeric, 3) mediana_ipp,
    round(stddev(ipp)::numeric, 3) std_ipp
from base
where ipp is not null
group by 1
order by 1;

Select
    origem ano,
    count(*) total_alunos,
    count(ipp) com_ipp,
    count(*) - count(ipp) sem_ipp,
    round((count(*) - count(ipp)) * 100.0 / count(*), 1) pct_nulos
from base
group by 1
order by 1;

Select
    case
        when ian = 2.5  then 'IAN Crítico (2.5)'
        when ian = 5.0  then 'IAN Parcial (5.0)'
        when ian = 10.0 then 'IAN Adequado (10.0)'
    end nivel_ian,
    count(*) total,
    count(*) filter (where ipp >= 7.5) ipp_alto,
    count(*) filter (where ipp < 7.5) ipp_baixo,
    round(avg(ipp)::numeric, 3) media_ipp
from base
where ipp is not null
group by 1
order by 1;

Select
    origem ano,
    count(*) filter (where ipp is not null) n_valido,
    round(corr(ipp, ian)::numeric, 4) corr_ipp_ian
from base
where ipp is not null
group by 1
order by 1;


-- Análise de ponto de virada --

Select
    round(avg(ipv)::numeric, 3) media,
    round(percentile_cont(0.5) within group (order by ipv)::numeric, 3) mediana,
    round(stddev(ipv)::numeric, 3) desvio_padrao,
    count(*) filter (where ipv is null) nulos
from base;

Select
    origem ano,
    round(avg(ipv)::numeric, 3) media_ipv,
    round(percentile_cont(0.5) within group (order by ipv)::numeric, 3) mediana_ipv,
    count(*) n
from base
where ipv is not null
group by 1
order by 1;

Select
    origem ano,
    'IDA' indicador,
    round(corr(ipv, ida)::numeric, 4) correlacao,
    count(*) filter (where ipv is not null and ida is not null) n
from base
group by 1

union all

Select origem, 'IEG', round(corr(ipv, ieg)::numeric, 4),
    count(*) filter (where ipv is not null and ieg is not null)
from base
group by origem

union all

Select origem, 'IPP', round(corr(ipv, ipp)::numeric, 4),
    count(*) filter (where ipv is not null and ipp is not null)
from base
group by origem

union all

Select origem, 'IAA', round(corr(ipv, iaa)::numeric, 4),
    count(*) filter (where ipv is not null and iaa is not null)
from base
group by origem

union all

Select origem, 'IPS', round(corr(ipv, ips)::numeric, 4),
    count(*) filter (where ipv is not null and ips is not null)
from base
group by origem

union all

Select origem, 'IAN', round(corr(ipv, ian)::numeric, 4),
    count(*) filter (where ipv is not null and ian is not null)
from base
group by origem

order by ano, indicador;


-- Análise de impactos sobre o INDE --

With tercis as (
    Select
        inde_24,
        ntile(3) over (order by ida) ida_t,
        ntile(3) over (order by ieg) ieg_t,
        ntile(3) over (order by ips) ips_t,
        ntile(3) over (order by ipp) ipp_t,
        ntile(3) over (order by ipv) ipv_t
    from base
    where origem = 'PEDE2024'
      and fase not in ('FASE 8', '8F', '8E', '8D', '8B', '8A')
      and ida    is not null
      and ieg    is not null
      and ips    is not null
      and ipp    is not null
      and ipv    is not null
      and inde_24 is not null
)

Select
    'IDA' indicador,
    round(avg(inde_24) filter (where ida_t = 1)::numeric, 3) baixo,
    round(avg(inde_24) filter (where ida_t = 2)::numeric, 3) medio,
    round(avg(inde_24) filter (where ida_t = 3)::numeric, 3) alto
from tercis

union all

Select 'IEG',
    round(avg(inde_24) filter (where ieg_t = 1)::numeric, 3),
    round(avg(inde_24) filter (where ieg_t = 2)::numeric, 3),
    round(avg(inde_24) filter (where ieg_t = 3)::numeric, 3)
from tercis

union all

Select 'IPV',
    round(avg(inde_24) filter (where ipv_t = 1)::numeric, 3),
    round(avg(inde_24) filter (where ipv_t = 2)::numeric, 3),
    round(avg(inde_24) filter (where ipv_t = 3)::numeric, 3)
from tercis

union all

Select 'IPP',
    round(avg(inde_24) filter (where ipp_t = 1)::numeric, 3),
    round(avg(inde_24) filter (where ipp_t = 2)::numeric, 3),
    round(avg(inde_24) filter (where ipp_t = 3)::numeric, 3)
from tercis

union all

Select 'IPS',
    round(avg(inde_24) filter (where ips_t = 1)::numeric, 3),
    round(avg(inde_24) filter (where ips_t = 2)::numeric, 3),
    round(avg(inde_24) filter (where ips_t = 3)::numeric, 3)
from tercis;

With tercis as (
    Select
        inde_24,
        case ntile(3) over (order by ida)
            when 1 then 'Baixo' when 2 then 'Médio' else 'Alto' end ida,
        case ntile(3) over (order by ieg)
            when 1 then 'Baixo' when 2 then 'Médio' else 'Alto' end ieg,
        case ntile(3) over (order by ipv)
            when 1 then 'Baixo' when 2 then 'Médio' else 'Alto' end ipv,
        case ntile(3) over (order by ipp)
            when 1 then 'Baixo' when 2 then 'Médio' else 'Alto' end ipp,
        case ntile(3) over (order by ips)
            when 1 then 'Baixo' when 2 then 'Médio' else 'Alto' end ips
    from base
    where origem   = 'PEDE2024'
      and fase not in ('FASE 8', '8F', '8E', '8D', '8B', '8A')
      and ida      is not null
      and ieg      is not null
      and ips      is not null
      and ipp      is not null
      and ipv      is not null
      and inde_24  is not null
)

Select
    ida, ieg, ipv, ipp, ips,
    round(avg(inde_24)::numeric, 3) inde_medio,
    count(*) n
from tercis
group by ida, ieg, ipv, ipp, ips
order by inde_medio desc
limit 10;


-- Avaliação da efetividade do programa pela métrica de Pedras --

Select
    'PEDE2022' ano,
    pedra_22 pedra,
    count(*) qtd,
    round(count(*) * 100.0 / sum(count(*)) over (), 1) percentual
from base
where pedra_22 is not null
  and origem = 'PEDE2022'
group by pedra_22

union all

Select
    'PEDE2023',
    pedra_23,
    count(*),
    round(count(*) * 100.0 / sum(count(*)) over (), 1)
from base
where pedra_23 is not null
  and origem = 'PEDE2023'
group by pedra_23

union all

Select
    'PEDE2024',
    pedra_24,
    count(*),
    round(count(*) * 100.0 / sum(count(*)) over (), 1)
from base
where pedra_24 is not null
  and origem = 'PEDE2024'
group by pedra_24

order by ano, pedra;

With pares as (
    Select
        pedra_22,
        pedra_24,
        case
            when pedra_24 in ('TOPÁZIO','TOPAZIO')
             and pedra_22 in ('AMETISTA','ÁGATA','AGATA','QUARTZO') then 'Melhorou'
            when pedra_24 in ('AMETISTA')
             and pedra_22 in ('ÁGATA','AGATA','QUARTZO')            then 'Melhorou'
            when pedra_24 in ('ÁGATA','AGATA')
             and pedra_22 in ('QUARTZO')                            then 'Melhorou'
            when replace(upper(pedra_24), 'AGATA', 'ÁGATA') = replace(upper(pedra_22), 'AGATA', 'ÁGATA') then 'Permaneceu'
            else 'Piorou'
        end movimento
    from base
    where pedra_22 is not null
      and pedra_24 is not null
      and pedra_24 <> 'INCLUIR'
)

Select
    movimento,
    count(*) qtd,
    round(count(*) * 100.0 / sum(count(*)) over (), 1) percentual
from pares
group by movimento
order by qtd desc;

Select
    pedra_24 pedra,
    round(avg(inde_24)::numeric, 3) inde_medio,
    count(*) n
from base
where pedra_24 is not null
  and pedra_24 <> 'INCLUIR'
  and inde_24  is not null
group by pedra_24
order by inde_medio;

Select
    pedra_22,
    pedra_23,
    pedra_24,
    count(*) n
from base
where pedra_22 is not null
  and pedra_23 is not null
  and pedra_24 is not null
  and pedra_24 <> 'INCLUIR'
group by pedra_22, pedra_23, pedra_24
order by n desc
limit 10;