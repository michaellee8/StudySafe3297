SELECT svr.venue_id, svr.entry_datetime, svr.exit_datetime
FROM studysafe_venue sve
         JOIN studysafe_visitingrecord svr on sve.id = svr.venue_id
         JOIN studysafe_member sm on sm.id = svr.member_id
WHERE sm.hku_id = '3036222333'
  AND svr.entry_datetime <= '2022-04-19 17:55:20'
  AND svr.exit_datetime >= '2022-04-19 15:55:20'