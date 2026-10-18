# Данные недели 24

                 `http_response_fixture.json`: source — author_synthetic_fixture; tickets — 8 объектов.
                 ticket_id: N + 3 цифры; category: access/billing/schedule/other;
                 minutes_open: неотрицательное integer в минутах. В fixture намеренно есть 1 точный дубликат,
                 отрицательная длительность и пустой ID. После проверки 5 уникальных валидных строк.
                 Priority high задается учебным порогом >=60 минут. Данные не получены из внешнего HTTP API.
                 Локальный сервер при запуске лишь обслуживает этот авторский fixture.
