# Дополнительные материалы — Week 22

**Microsoft Copilot Studio: основы**

Здесь сохранены полные исходные PDF университетских лекций и, где требуется, официальная документация разработчиков. Учебный маршрут ниже выбирает конкретные части под два 90-минутных занятия недели.

## Как изучать

15 мин университетских понятий +25–30 мин Microsoft Learn; остальное изучается по ходу практических 108 мин. Полная исследовательская лекция необязательна.

**Нумерация страниц:** все диапазоны ниже — физические страницы PDF, первая страница файла считается 1. Номера в нижнем колонтитуле оригинала иногда отличаются.

**Язык:** исходные материалы преимущественно английские; русские объяснения, код, задания и словари данных находятся в соседних папках.

## Университетские презентации

### [Berkeley_LLM_Agent_History.pdf](Berkeley_LLM_Agent_History.pdf)

**History of LLM Agents (2024)**  
UC Berkeley LLM Agents course; guest lecturer Shunyu Yao. Полный файл: **71 стр.**

**Выбранный фрагмент:** PDF-страницы 3–7, 9, 11–16, 67–68: agent/environment/action/observation, rule-based диалог, knowledge retrieval, tools и участие пользователя.  
**Время:** около 15 мин. **Уровень:** Начальный концептуальный обзор. Исследовательские алгоритмы в полном PDF необязательны.

**Связь с неделей:** Понятия для Copilot Studio: агент, знание, тема, внешнее действие. Интерфейс Copilot и порядок кликов изучаются по Microsoft Learn и нашей лабораторной.

Это гостевая лекция Shunyu Yao в UC Berkeley, не презентация Microsoft и не инструкция по Copilot Studio. Схемы используются для понимания; соответствие реальному сервису проверяется отдельно в COPILOT_STUDIO_LAB.md.

[Официальная страница курса](https://rdi.berkeley.edu/llm-agents/f24) · [Прямая загрузка оригинала](https://rdi.berkeley.edu/llm-agents/assets/llm_agent_history.pdf)

**Права:** No formal redistribution license stated on the source page; original author and copyright notices retained

## Официальная документация — сохранённые страницы

Это HTML/Markdown-снимки документации, а не слайды. Они скачаны 18.10.2026 с сайтов самих разработчиков; основной текст сохранён локально. Внешние изображения, стили и переходы в HTML могут обращаться к сети. Для установленной у вас версии сервиса сверяйте актуальный оригинал.

| Локальный файл | Что читать | Примерное время | Оригинал |
|---|---|---:|---|
| [Microsoft_Create_Agent.html](Microsoft_Create_Agent.html) | Create an agent; Improve your agent; Publish your agent | 12 мин | [Microsoft Learn](https://learn.microsoft.com/en-us/microsoft-copilot-studio/fundamentals-get-started) |
| [Microsoft_Topics.html](Microsoft_Topics.html) | Selecting the right topic to respond to a user; Node types; Create a topic; Edit a topic; Test and publish | 15 мин | [Microsoft Learn](https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-create-edit-topics) |
| [Microsoft_Knowledge.html](Microsoft_Knowledge.html) | Supported knowledge sources; Source authentication; Add and manage knowledge for generative answers | 10 мин | [Microsoft Learn](https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-copilot-studio) |

Разделы справочника выбираются по текущему упражнению; времена отдельных файлов не прибавляются автоматически к обязательной нагрузке.

- **Quickstart: Create and deploy an agent:** Реальный интерфейс создания агента; проходить вместе с COPILOT_STUDIO_LAB.md.
- **Create and edit topics:** Триггеры, вопросы, переменные и ветвления; локальный state-machine simulator иллюстрирует эти понятия.
- **Knowledge in Copilot Studio:** Выбор источника знаний и пользовательская аутентификация.

Исходные copyright/attribution notices документации сохранены. Условия дальнейшего использования проверяются по оригинальному сайту; наличие локальной копии не меняет владельца прав.

## Проверка понимания

Нарисуйте один topic с trigger→question→variable→condition→answer. Повторите его в Copilot Studio по лабораторной и сохраните подтверждение реального запуска.

Далее: [Practice Week 22](../practice/Practice_Week_22.ipynb) · [Homework Week 22](../homework/Homework_Week_22.md) · [Данные и происхождение](../datasets/DATA_DICTIONARY.md).

## Проверка файлов и авторство

PDF сохранены без изменения страниц и титров. Проверены сигнатура PDF, число страниц, извлекаемый текст и выборочные отрисованные страницы с графиками/схемами/формулами. В каталоге ресурсов репозитория записаны исходные URL, размеры и SHA-256.

Отбор и русская учебная навигация относятся к этому курсу. Авторство оригинальных лекций принадлежит указанным преподавателям и организациям; включение материалов не означает партнёрство или одобрение курса университетом.
