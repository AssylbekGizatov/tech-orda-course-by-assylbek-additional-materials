# Дополнительные материалы — Week 25

**n8n: AI-агент с инструментами**

Здесь сохранены полные исходные PDF университетских лекций и, где требуется, официальная документация разработчиков. Учебный маршрут ниже выбирает конкретные части под два 90-минутных занятия недели.

## Как изучать

20 мин университетских слайдов +20–25 мин документации. Остальное время теории — разбор tool contracts; практическая часть — импорт, credentials и end-to-end тест.

**Нумерация страниц:** все диапазоны ниже — физические страницы PDF, первая страница файла считается 1. Номера в нижнем колонтитуле оригинала иногда отличаются.

**Язык:** исходные материалы преимущественно английские; русские объяснения, код, задания и словари данных находятся в соседних папках.

## Университетские презентации

### [Stanford_CS224N_LLM_Agents.pdf](Stanford_CS224N_LLM_Agents.pdf)

**CS224N Lecture 14: Reasoning and Agents (2024)**  
Stanford University; Shikhar Murty. Полный файл: **75 стр.**

**Выбранный фрагмент:** PDF-страницы 38–44, 49–50, 53–55, 71–75: действие/наблюдение/среда, агентный цикл, проверка в sandbox и падение качества при длинных задачах.  
**Время:** около 20 мин. **Уровень:** Начальный концептуальный маршрут по агентам; обучение policy/RL и multimodal модели — факультатив.

**Связь с неделей:** Основа для AI Agent + tools + memory в n8n и объяснение, зачем ограничивать инструменты, число шагов и оценивать полную цепочку.

Схемы и графики относятся к исследовательским системам 2024. Инструкции по текущим AI-узлам находятся в официальной документации. В лабораторной наблюдаемость означает tool inputs/outputs/status, а не запрос скрытых рассуждений модели.

[Официальная страница курса](https://web.stanford.edu/class/cs224n/) · [Прямая загрузка оригинала](https://web.stanford.edu/class/cs224n/slides/cs224n-spr2024-lecture14-agents-shikhar-updated.pdf)

**Права:** No formal redistribution license stated on the source page; original author and copyright notices retained

## Официальная документация — сохранённые страницы

Это HTML/Markdown-снимки документации, а не слайды. Они скачаны 18.10.2026 с сайтов самих разработчиков; основной текст сохранён локально. Внешние изображения, стили и переходы в HTML могут обращаться к сети. Для установленной у вас версии сервиса сверяйте актуальный оригинал.

| Локальный файл | Что читать | Примерное время | Оригинал |
|---|---|---:|---|
| [n8n_AI_Agent.md](n8n_AI_Agent.md) | AI Agent — вводная часть и обязательное подключение tool | 7 мин | [n8n](https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.agent/) |
| [n8n_Code_Tool.md](n8n_Code_Tool.md) | Node parameters: Description, Language, JavaScript/Python | 8 мин | [n8n](https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.toolcode/) |
| [n8n_Simple_Memory.md](n8n_Simple_Memory.md) | Node parameters: Session Key, Context Window Length | 7 мин | [n8n](https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.memorybufferwindow/) |
| [n8n_OpenAI_Chat_Model.md](n8n_OpenAI_Chat_Model.md) | Node parameters: Credential, Model; Node options | 10 мин | [n8n](https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.lmchatopenai/) |

Разделы справочника выбираются по текущему упражнению; времена отдельных файлов не прибавляются автоматически к обязательной нагрузке.

- **AI Agent node:** Назначение AI Agent root node; соединения tools/model/memory.
- **Code Tool node:** Назначение инструмента, схема входа и проверяемый результат; параметры сверять с установленной версиейUI.
- **Simple Memory node:** Разделение сессий и границы короткой памяти; это не база знаний.
- **OpenAI Chat Model node:** Реальный credential и доступная модель выбираются в интерфейсе; fixture не подтверждает live доступ.

Исходные copyright/attribution notices документации сохранены. Условия дальнейшего использования проверяются по оригинальному сайту; наличие локальной копии не меняет владельца прав.

## Проверка понимания

Сравните намерение агента с фактическими tool inputs/outputs и final result. Измерьте success rate на наборе сценариев; отдельно отмечайте live и fixture результаты.

Далее: [Practice Week 25](../practice/Practice_Week_25.ipynb) · [Homework Week 25](../homework/Homework_Week_25.md) · [Данные и происхождение](../datasets/DATA_DICTIONARY.md).

## Проверка файлов и авторство

PDF сохранены без изменения страниц и титров. Проверены сигнатура PDF, число страниц, извлекаемый текст и выборочные отрисованные страницы с графиками/схемами/формулами. В каталоге ресурсов репозитория записаны исходные URL, размеры и SHA-256.

Отбор и русская учебная навигация относятся к этому курсу. Авторство оригинальных лекций принадлежит указанным преподавателям и организациям; включение материалов не означает партнёрство или одобрение курса университетом.
