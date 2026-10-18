# Дополнительные материалы — Week 23

**Copilot Studio: интеграции и оценка**

Здесь сохранены полные исходные PDF университетских лекций и, где требуется, официальная документация разработчиков. Учебный маршрут ниже выбирает конкретные части под два 90-минутных занятия недели.

## Как изучать

20 мин концептуальных слайдов +20–25 мин выбранных Microsoft Learn разделов. Настройка connections и test cases — практическая часть.

**Нумерация страниц:** все диапазоны ниже — физические страницы PDF, первая страница файла считается 1. Номера в нижнем колонтитуле оригинала иногда отличаются.

**Язык:** исходные материалы преимущественно английские; русские объяснения, код, задания и словари данных находятся в соседних папках.

## Университетские презентации

### [Berkeley_Enterprise_Agent_Workflows.pdf](Berkeley_Enterprise_Agent_Workflows.pdf)

**Agents for Enterprise Workflows — CS294/194-196 Lecture 7 (2024)**  
UC Berkeley LLM Agents course; guest lecturer Nicolas Chapados, ServiceNow. Полный файл: **72 стр.**

**Выбранный фрагмент:** PDF-страницы 6–9, 14, 16, 21–22, 33, 35, 38, 40, 43, 47, 58: API-агенты, workflows, tools/memory, критерии качества, воспроизводимость и сценарий доступа к знаниям.  
**Время:** около 20 мин. **Уровень:** Доступная концептуальная выборка; обучение агентов и исследовательские benchmarks — углубление.

**Связь с неделей:** Связь M365/внешних источников с проверяемыми действиями: вход→проверка прав→источник→результат→тест. Обсудите, какой фактический результат должен остаться после вызова action.

Лекция ServiceNow в UC Berkeley описывает корпоративные принципы. Она не документирует Microsoft365. Доступ, connections и публикация Copilot выполняются по официальным Microsoft Learn snapshots и отдельной лабораторной.

[Официальная страница курса](https://rdi.berkeley.edu/llm-agents/f24) · [Прямая загрузка оригинала](https://rdi.berkeley.edu/llm-agents/assets/agentworkflows.pdf)

**Права:** Copyright 2024 ServiceNow, Inc. All rights reserved. No open redistribution license stated; original notices retained.

## Официальная документация — сохранённые страницы

Это HTML/Markdown-снимки документации, а не слайды. Они скачаны 18.10.2026 с сайтов самих разработчиков; основной текст сохранён локально. Внешние изображения, стили и переходы в HTML могут обращаться к сети. Для установленной у вас версии сервиса сверяйте актуальный оригинал.

| Локальный файл | Что читать | Примерное время | Оригинал |
|---|---|---:|---|
| [Microsoft_Agent_Flow.html](Microsoft_Agent_Flow.html) | Prerequisites; Create a new agent flow from the Flows page; Manage which connections are used by the flow | 15 мин | [Microsoft Learn](https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-flow-create) |
| [Microsoft_Publish_Channels.html](Microsoft_Publish_Channels.html) | Publish the latest content; Test your agent; Configure channels; Channel experience reference table | 12 мин | [Microsoft Learn](https://learn.microsoft.com/en-us/microsoft-copilot-studio/publication-fundamentals-publish-channels) |
| [Microsoft_End_User_Authentication.html](Microsoft_End_User_Authentication.html) | Choose an authentication option; Required user sign in and agent sharing | 10 мин | [Microsoft Learn](https://learn.microsoft.com/en-us/microsoft-copilot-studio/configuration-end-user-authentication) |

Разделы справочника выбираются по текущему упражнению; времена отдельных файлов не прибавляются автоматически к обязательной нагрузке.

- **Create a flow for an agent:** Настоящий action через agent flow, inputs/outputs и настройка connections.
- **Publish your agent:** Проверка и публикация в доступный канал, включая Teams/M365 при доступности в tenant.
- **Configure end-user authentication:** Сопоставить право пользователя и доступ к источнику; не приравнивать agent-owner connection к разрешению любого пользователя.

Исходные copyright/attribution notices документации сохранены. Условия дальнейшего использования проверяются по оригинальному сайту; наличие локальной копии не меняет владельца прав.

## Проверка понимания

Для action запишите вход, источник, действующего пользователя, ожидаемый выход и негативный тест. Сверьте live результаты отдельно от локальной SQLite-иллюстрации.

Далее: [Practice Week 23](../practice/Practice_Week_23.ipynb) · [Homework Week 23](../homework/Homework_Week_23.md) · [Данные и происхождение](../datasets/DATA_DICTIONARY.md).

## Проверка файлов и авторство

PDF сохранены без изменения страниц и титров. Проверены сигнатура PDF, число страниц, извлекаемый текст и выборочные отрисованные страницы с графиками/схемами/формулами. В каталоге ресурсов репозитория записаны исходные URL, размеры и SHA-256.

Отбор и русская учебная навигация относятся к этому курсу. Авторство оригинальных лекций принадлежит указанным преподавателям и организациям; включение материалов не означает партнёрство или одобрение курса университетом.
