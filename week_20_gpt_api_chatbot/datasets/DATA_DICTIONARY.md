# Данные недели 20

                 `synthetic_http_events.csv` — 5 агрегированных категорий, всего 90 придуманных событий.
                 status_code: HTTP-статус; category: смысл; retry: учебная политика; count: число событий.
                 Для 429 различайте временный rate limit и exhausted quota: CSV упрощает это различие.

                 `chat_completion_fixture.json` — вручную составленный пример формы Chat Completions.
                 choices/message/content и usage соответствуют объясняемому контракту;
                 model имеет значение fixture-not-a-real-model. 30/14/44 tokens придуманы для parser-test,
                 не получены из API и не характеризуют стоимость. Авторские fixtures для учебного использования.
