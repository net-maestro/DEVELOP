SELECT
s.agreement,
s.name,
sa.name,
ha.name,
pn.name
FROM clients s
JOIN addr_houses ha on ha.id = s.house
JOIN addr_streets sa on sa.id = ha.street
JOIN addr_cities ca on ca.id = sa.city
LEFT JOIN addr_groups gr on gr.id = ha.group_id
LEFT JOIN client_prices pr on pr.agreement = s.id and pr.time_stop is null
LEFT JOIN bill_prices pn on pn.id = pr.price
WHERE s.agreement in (51004, 51005, 51010, 51012, 51020, 51029, 51033, 51034, 51035, 51036, 51037, 51038, 51043, 51044, 51046, 51047, 51048, 51054, 51057, 51061, 51067, 51069, 51071, 51073, 51076, 51078, 51081, 51090, 51093, 51101, 51102, 51105, 51111, 51118, 51125, 51129, 51130, 51131, 51144, 51145, 51147, 52008, 53038, 53079, 53146, 53305, 53400) AND  pn.id in (13,14,19,32,38,48,49,52,59,60,61,64,65) 





SELECT
s.agreement,
s.name,
sa.name,
ha.name
FROM clients s
JOIN addr_houses ha on ha.id = s.house
JOIN addr_streets sa on sa.id = ha.street
JOIN addr_cities ca on ca.id = sa.city
LEFT JOIN addr_groups gr on gr.id = ha.group_id
LEFT JOIN client_prices pr on pr.agreement = s.id and pr.time_stop is null
LEFT JOIN bill_prices pn on pn.id = pr.price
WHERE s.agreement in (51004, 51005, 51010, 51012, 51020, 51029, 51033, 51034, 51035, 51036, 51037, 51038, 51043, 51044, 51046, 51047, 51048, 51054, 51057, 51061, 51067, 51069, 51071, 51073, 51076, 51078, 51081, 51090, 51093, 51101, 51102, 51105, 51111, 51118, 51125, 51129, 51130, 51131, 51144, 51145, 51147, 52008, 53038, 53079, 53146, 53305, 53400) AND pn.name='Білий IP'
