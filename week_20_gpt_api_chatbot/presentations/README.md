# Дополнительные материалы — Week 20

**GPT API и чат-бот на Python**

Здесь сохранены полные исходные PDF университетских лекций и, где требуется, официальная документация разработчиков. Учебный маршрут ниже выбирает конкретные части под два 90-минутных занятия недели.

## Как изучать

20 мин университетской схемы +20–30 мин нужных разделов OpenAI в пределах теории. Код API разбирается в практические 54 мин каждого занятия.

**Нумерация страниц:** все диапазоны ниже — физические страницы PDF, первая страница файла считается 1. Номера в нижнем колонтитуле оригинала иногда отличаются.

**Язык:** исходные материалы преимущественно английские; русские объяснения, код, задания и словари данных находятся в соседних папках.

## Университетские презентации

### [MIT_Large_Language_Models_II.pdf](MIT_Large_Language_Models_II.pdf)

**Large Language Models II — 15.773 Hands-on Deep Learning (2024)**  
MIT; Rama Ramakrishnan. Полный файл: **115 стр.**

**Выбранный фрагмент:** PDF-страницы 12, 14, 17, 19, 40, 47, 49–50, 56–58, 77–80: instruction-following, диалоговый формат, способы адаптации и ограничение контекстного окна.  
**Время:** около 20 мин. **Уровень:** Начальный концептуальный фрагмент; RLHF и LoRA в полном PDF для углубления.

**Связь с неделей:** Основа для объяснения того, что API получает инструкции/историю и возвращает ответ. Это университетская концептуальная презентация; текущий синтаксис SDK, аутентификация и ошибки изучаются по сохранённой документации OpenAI.

Историческая лестница GPT/GPT-2/GPT-3 и примеры ChatGPT относятся к лекции 2024. Выбор актуальной доступной модели выполняется в LIVE_API_LAB.md через переменную окружения, без жёстко зашитого устаревшего model ID.

[Официальная страница курса](https://ocw.mit.edu/courses/15-773-hands-on-deep-learning-spring-2024/lists/lecture-notes/) · [Прямая загрузка оригинала](https://ocw.mit.edu/courses/15-773-hands-on-deep-learning-spring-2024/mit15_773_s24_lec10.pdf)

**Права:** MIT OpenCourseWare; CC BY-NC-SA 4.0 except separately credited third-party material; original notices retained

## Официальная документация — сохранённые страницы

Это HTML/Markdown-снимки документации, а не слайды. Они скачаны 18.10.2026 с сайтов самих разработчиков; основной текст сохранён локально. Внешние изображения, стили и переходы в HTML могут обращаться к сети. Для установленной у вас версии сервиса сверяйте актуальный оригинал.

| Локальный файл | Что читать | Примерное время | Оригинал |
|---|---|---:|---|
| [OpenAI_Python_SDK.html](OpenAI_Python_SDK.html) | Usage: Responses API и Chat Completions; Handling errors; Retries; Timeouts | 15 мин | [OpenAI](https://developers.openai.com/api/reference/python) |
| [OpenAI_Error_Codes.html](OpenAI_Error_Codes.html) | API errors; Python library error types | 8 мин | [OpenAI](https://developers.openai.com/api/docs/guides/error-codes) |
| [OpenAI_Migrate_to_Responses.html](OpenAI_Migrate_to_Responses.html) | About the Responses API; Migrating from Chat Completions; Incremental rollout checklist | 8 мин | [OpenAI](https://developers.openai.com/api/docs/guides/migrate-to-responses) |

Разделы справочника выбираются по текущему упражнению; времена отдельных файлов не прибавляются автоматически к обязательной нагрузке.

- **Python SDK reference: Responses and Chat Completions:** Актуальные import, OPENAI_API_KEY, responses.create/chat.completions.create и обработка сетевых/API ошибок.
- **API error codes and handling:** Отличать 401/403 от 429 и 5xx; выбирать понятное сообщение пользователю и ограниченный retry.
- **Migrate to the Responses API:** Chat Completions сохранён для темы силлабуса; для новых приложений сопоставить с текущим Responses API.

Исходные copyright/attribution notices документации сохранены. Условия дальнейшего использования проверяются по оригинальному сайту; наличие локальной копии не меняет владельца прав.

## Проверка понимания

Покажите путь: env key→request→response→validation→history. Объясните, почему ошибочный запрос не должен оставлять половину диалоговой пары в истории.

Далее: [Practice Week 20](../practice/Practice_Week_20.ipynb) · [Homework Week 20](../homework/Homework_Week_20.md) · [Данные и происхождение](../datasets/DATA_DICTIONARY.md).

## Проверка файлов и авторство

PDF сохранены без изменения страниц и титров. Проверены сигнатура PDF, число страниц, извлекаемый текст и выборочные отрисованные страницы с графиками/схемами/формулами. В каталоге ресурсов репозитория записаны исходные URL, размеры и SHA-256.

Отбор и русская учебная навигация относятся к этому курсу. Авторство оригинальных лекций принадлежит указанным преподавателям и организациям; включение материалов не означает партнёрство или одобрение курса университетом.
