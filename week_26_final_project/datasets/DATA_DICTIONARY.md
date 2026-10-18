# Данные недели 26

                 `service_tickets.csv`: 600 синтетических заявок, seed 126, временной шаг 2 часа.
                 Авторский генератор использует logistic risk с шумным Bernoulli target. Это не реальные
                 service desk logs и не сведения о студентах или организациях.

                 | Поле | Тип | Смысл / доступность |
                 |---|---|---|
                 | ticket_id | str | Уникальный ID, не признак |
                 | opened_at | datetime | Условное время, для temporal split |
                 | minutes_open | int 0..120 | Возраст заявки в triage, доступен |
                 | affected_users | int 1..45 | Затронутые пользователи, доступен |
                 | category | str | access/billing/schedule/other |
                 | channel | str | portal/chat/email |
                 | breach_sla | int 0/1 | Target: нарушение SLA |
                 | final_resolution_minutes | int | Известен после исхода; намеренный leakage trap |

                 Logistic logit = -3.2 + .022*minutes_open + .025*affected_users + .5*(access) + .3*(email).
                 Target случайно генерируется из соответствующей вероятности. Outcome duration >120 при target=1.
                 Стоимость FN=5, FP=1 — отдельное учебное допущение, не оцененная стоимость компании.
                 Генератор — scripts/build_weeks_18_26.py/build26; авторские данные для учебного использования.
