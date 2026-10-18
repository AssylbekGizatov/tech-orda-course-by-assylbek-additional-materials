# Неделя 25 — n8n: AI-агент с инструментами

**Tech Orda course authored by Gizatov A. S.**

## Цели и нагрузка

AI-ноды, agent, tools, память, end-to-end тесты и наблюдаемость.

По календарному плану: **4 академических часа = 180 минут**, два занятия по 90 минут.
В каждом занятии **36 минут теории + 54 минуты практики**; итого **40% / 60%**.
Домашняя работа — ориентировочно **180 минут самостоятельной работы**, сверх аудиторных часов.

| Занятие | Точная тема календарного плана | Теория | Практика | Что делаем руками |
|---|---|---:|---:|---|
| 1 | AI-ноды, agent, tools и память | 36 мин | 54 мин | Реализуем tools и подключаем реальный AI Agent workflow |
| 2 | End-to-end кейс и наблюдаемость | 36 мин | 54 мин | Проверяем memory, trace и качество end-to-end ответов |

## Как провести неделю

На теоретическую часть отведите 6 минут на повторение, 20 минут на основные идеи и формулы,
10 минут на разбор диаграмм и вопросы. Практические 54 минуты: 10 минут на данные и постановку,
30 минут на код и эксперимент, 10 минут на проверку, 4 минуты на интерпретацию результата.
В материалах с облачной частью эти 54 минуты можно пройти в учебной среде по vendor lab;
offline notebook остается обязательной подготовкой и резервом при отсутствии доступа.

## Содержимое

- [presentations/README.md](presentations/README.md) — скачанные университетские PDF, официальные инструкции, выбранные страницы и время изучения.
- `practice/Practice_Week_25.ipynb` — основной разобранный практикум с комментариями и проверками.
- `datasets/` — локальные данные, словарь полей и происхождение.
- `homework/Homework_Week_25.md` — задания и рубрика на 100 баллов.
- `homework/Homework_Week_25_Starter.ipynb` — незаполненная, запускаемая заготовка.

Запуск: откройте notebook в окружении из корневого README и выполните **Restart Kernel → Run All**.
Данные ищутся относительно корня репозитория; абсолютные пути не требуются.
`practice/n8n_ai_agent_course_helper.json` — реальный импортируемый Agent workflow, `N8N_AI_AGENT_LAB.md` — credentials/model setup и приемка. Live inference не выполнялся.

## На что смотреть преподавателю

Реализуем tools и подключаем реальный AI Agent workflow. Проверяем memory, trace и качество end-to-end ответов.
Студент должен объяснять выбор метрики, читать фактический вывод и называть ограничение подхода.
Одного успешного запуска ячеек для понимания темы недостаточно.

## Проверенные первичные источники

Проверены при подготовке 18 октября 2026 года; интерфейсы сервисов могут изменяться.

- [n8n: AI Agent](https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.agent/)
- [n8n: Custom Code Tool](https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.toolcode/)
- [n8n: Simple Memory](https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.memorybufferwindow/)
- [n8n: OpenAI Chat Model](https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.lmchatopenai/)
