# Реальная лабораторная n8n: workflow → HTTP → SQL → errors

**Проверка поставки:** JSON структурно проверен, JavaScript узлов проверяется отдельно;
фактический импорт и выполнение n8n/Postgres еще не проводились. Все workflow `active=false`,
credentials и instance IDs отсутствуют. Версии узлов опираются на текущие официальные определения n8n.

## 1. Импорт без credentials — 25 минут

1. Откройте свою учебную n8n instance. Создайте новый workflow; меню справа → Import from File.
   Выберите `n8n_offline_fixture.json`, сохраните. После импорта должны быть 4 связанных узла.
2. Execute workflow. Просмотрите input/output каждого узла, особенно Validate and Transform.
   Summary ожидает input_rows=8, accepted_rows=5, rejected_rows=3, high_priority=2.
   Здесь rejected включает 2 невалидные строки и 1 дубликат.
3. Измените в Synthetic Items одну минуту на отрицательную и повторите; проверьте reason.
   Верните исходный fixture. No-credential run выполняется целиком внутри n8n.

[Import/export](https://docs.n8n.io/build/manage-workflows/export-and-import.md)

## 2. Настоящий локальный HTTP — 25 минут

4. В терминале запустите `python local_fixture_server.py`. Импортируйте `n8n_http_fixture.json`.
   Если n8n установлен на той же машине, URL `http://127.0.0.1:8765/tickets` подходит.
5. Если n8n в Docker, localhost контейнера отличается от хоста. Разрешите доступ только в учебной
   сети: запустите fixture server с `--host 0.0.0.0`, используйте `host.docker.internal:8765`
   при доступной настройке Docker; на Linux может потребоваться host-gateway mapping.
   n8n Cloud не видит локальный localhost: используйте первый fixture workflow или отдельный
   доступный учебный HTTP endpoint; не публикуйте сервер автоматически.
6. Выполните workflow, сравните Summary с первым. Это уже реальный HTTP к синтетическим данным.
   Затем путь `/simulate-503`: HTTP Request должен завершиться ошибкой, не возвращая «успех».
   В Settings узла изучите Retry On Fail, ограничьте max attempts; верните `/tickets`.

[HTTP Request](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/)

## 3. Read-only Postgres — 30 минут

7. В выделенной учебной БД выполните `postgres_setup.sql`. Создайте/select-only role средствами
   администратора. В n8n Credentials создайте Postgres connection; секреты хранятся в credentials,
   не в workflow JSON. Не используйте рабочую БД.
8. Импортируйте `n8n_postgres_readonly.json`. В Read Postgres выберите credential. Проверьте
   Operation=Execute Query, запрос с `$1`, Options → Query Parameters=`={{ [$json.category] }}`.
9. Execute workflow: billing возвращает N102 и N106. Измените category на строку
   `billing' OR 1=1--`: должно вернуться 0 строк. Не вставляйте значение в SQL конкатенацией.

[Postgres parameters](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.postgres/)

## 4. Ошибки и наблюдаемость — 28 минут

10. Импортируйте `n8n_error_handler.json`, сохраните. В основном workflow Settings → Error workflow
    выберите его вручную: ID зависит от instance и намеренно отсутствует в экспортируемом JSON.
11. Изучите Executions и отличие ручного/автоматического запуска. Error Trigger не проверяется
    обычным ручным Execute как входные данные; автоматический error workflow проверяйте только
    на разрешенном учебном trigger. Для offline-проверки используйте notebook и пример входного payload.
12. В отчете перечислите входные строки, причины отказов, повторную загрузку, read-only SQL и live-status
    каждого компонента. Экспортируя свою версию, удалите credentials references и приватные URL.

[Error workflows](https://docs.n8n.io/build/flow-logic/handle-errors-gracefully.md)

**Результат:** workflow JSON, 4 screenshots ключевых outputs, таблица expected/observed,
отдельные статусы n8n engine / HTTP / Postgres / Error Trigger. Никаких внешних сообщений не отправляется.
