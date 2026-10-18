# Дополнительные материалы — Week 24

**n8n: основы workflow**

Здесь сохранены полные исходные PDF университетских лекций и, где требуется, официальная документация разработчиков. Учебный маршрут ниже выбирает конкретные части под два 90-минутных занятия недели.

## Как изучать

20 мин университетских слайдов +20–25 мин документации по нужным nodes. Импорт и отладка workflow занимают практические 108 мин недели.

**Нумерация страниц:** все диапазоны ниже — физические страницы PDF, первая страница файла считается 1. Номера в нижнем колонтитуле оригинала иногда отличаются.

**Язык:** исходные материалы преимущественно английские; русские объяснения, код, задания и словари данных находятся в соседних папках.

## Университетские презентации

### [Stanford_CS329S_Data_Engineering.pdf](Stanford_CS329S_Data_Engineering.pdf)

**CS329S Lecture 3: Data Engineering (2021)**  
Stanford University; Chip Huyen. Полный файл: **86 стр.**

**Выбранный фрагмент:** PDF-страницы 12–13, 15–16, 20, 22–29, 43–48: источники/сериализация/JSON, OLTP/OLAP, ETL, schema, HTTP request/response и события.  
**Время:** около 20 мин. **Уровень:** Выбранный Data engineering101 — начальный. Streaming infrastructure и programmatic labeling вне основного маршрута.

**Связь с неделей:** Подготовка к n8n: различать item/JSON, преобразование, SQL-запрос, триггер и сетевой ответ; понять, почему API может вернуть ошибку.

Оригинальный PDF экспортирован из публичной Google Slides, на которую ссылается официальный syllabus Stanford CS329S2021. Названия n8n-узлов и импорт workflow изучаются по документации n8n и N8N_LAB.md.

[Официальная страница курса](https://stanford-cs329s.github.io/2021/syllabus.html) · [Прямая загрузка оригинала](https://docs.google.com/presentation/d/18oX1JpMJrUBjcrhenxijpyYB3ppZ9rSN9Qrimgp-qBM/export/pdf)

**Права:** No formal redistribution license stated on the source page; original author and copyright notices retained

## Официальная документация — сохранённые страницы

Это HTML/Markdown-снимки документации, а не слайды. Они скачаны 18.10.2026 с сайтов самих разработчиков; основной текст сохранён локально. Внешние изображения, стили и переходы в HTML могут обращаться к сети. Для установленной у вас версии сервиса сверяйте актуальный оригинал.

| Локальный файл | Что читать | Примерное время | Оригинал |
|---|---|---:|---|
| [n8n_Import_Export.md](n8n_Import_Export.md) | From the Editor UI menu; Copy-Paste | 5 мин | [n8n](https://docs.n8n.io/workflows/export-import/) |
| [n8n_HTTP_Request.md](n8n_HTTP_Request.md) | Node parameters: Method, URL, Authentication, Send Headers; Node options: Response, Timeout | 12 мин | [n8n](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/) |
| [n8n_Postgres.md](n8n_Postgres.md) | Operations: Execute Query; Use query parameters | 10 мин | [n8n](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.postgres/) |
| [n8n_Error_Handling.md](n8n_Error_Handling.md) | How do I set up an error workflow?; What data does an error workflow receive? | 8 мин | [n8n](https://docs.n8n.io/flow-logic/error-handling/) |

Разделы справочника выбираются по текущему упражнению; времена отдельных файлов не прибавляются автоматически к обязательной нагрузке.

- **Export and import workflows:** Импорт настоящих workflow JSON в practice; credentials добавляются отдельно.
- **HTTP Request node:** GET к локальному fixture server, разбор response и контролируемая обработка 503.
- **Postgres node:** SQL с параметрами, отдельно от SQL-синтаксиса; импортируемый узел использует безопасный placeholder.
- **Error handling:** Error Trigger, статус выполнения и отладка отдельного error workflow.

Исходные copyright/attribution notices документации сохранены. Условия дальнейшего использования проверяются по оригинальному сайту; наличие локальной копии не меняет владельца прав.

## Проверка понимания

Для каждого node укажите входной JSON, выходной JSON и вариант ошибки. Проверьте идемпотентность повторного запуска и SQL-параметры.

Далее: [Practice Week 24](../practice/Practice_Week_24.ipynb) · [Homework Week 24](../homework/Homework_Week_24.md) · [Данные и происхождение](../datasets/DATA_DICTIONARY.md).

## Проверка файлов и авторство

PDF сохранены без изменения страниц и титров. Проверены сигнатура PDF, число страниц, извлекаемый текст и выборочные отрисованные страницы с графиками/схемами/формулами. В каталоге ресурсов репозитория записаны исходные URL, размеры и SHA-256.

Отбор и русская учебная навигация относятся к этому курсу. Авторство оригинальных лекций принадлежит указанным преподавателям и организациям; включение материалов не означает партнёрство или одобрение курса университетом.
