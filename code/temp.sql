SELECT COUNT("form_studentdetailedinfo"."studentdetailedinfobase_ptr_id") AS "better_rank"
FROM "form_studentdetailedinfo"
GROUP BY "form_studentdetailedinfo"."studentdetailedinfobase_ptr_id"
;