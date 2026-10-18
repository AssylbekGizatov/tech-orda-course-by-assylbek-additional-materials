# Реальная лабораторная: n8n AI Agent + tools + memory

**Статус:** JSON и код контрактов подготовлены; платная модель и n8n engine не запускались.
Этот workflow содержит настоящий AI Agent, не Python-симуляцию. Для исполнения нужен доступ
к n8n с соответствующими узлами и выбранный разрешенный модельный провайдер.
JSON не содержит API key, credentials IDs, личных webhook URL или активных публикаций.

## Занятие 1 — 54 минуты

1. Импортируйте `n8n_ai_agent_course_helper.json` через Import from File. Должны появиться:
   Course Chat, Course Agent, Select OpenAI Model, Session Memory, Course Policy, Sum Numbers,
   Validate Response. Проверьте main/ai_languageModel/ai_memory/ai_tool связи.
2. Если ваш n8n не знает Agent v3.1, обновите учебную instance либо пересоздайте Agent через UI
   актуальной версии и подключите те же sub-nodes. Не понижайте до deprecated Agent v1.
3. В Select OpenAI Model выберите созданный вами OpenAI credential. Ключ вводится только в
   Credentials. В поле Model замените SELECT_AVAILABLE_MODEL_IN_UI реальной доступной моделью.
   Узел показывает доступные аккаунту модели; проверьте бюджет до первого вызова.
4. Откройте Course Policy: это read-only функция на синтетическом JSON. Вход — один ключ
   schedule/homework/project. В Sum Numbers вход — строка чисел через запятую, максимум 10.
   Оба инструмента возвращают JSON string; arbitrary code из пользовательского текста не исполняется.
5. Откройте тестовый Chat, спросите «Когда у нас занятия?» и «Сложи 12, 5 и 3».
   В trace проверьте фактический tool call и итог 20. Наличие ответа без вызова нужного tool — отдельная ошибка.

[AI Agent](https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.agent/)
· [Custom Code Tool](https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.toolcode/)
· [OpenAI model](https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.lmchatopenai/)

## Занятие 2 — 54 минуты

6. Продолжите «А когда сдавать домашнюю?» и проверьте источник homework. Затем начните новую
   chat session и убедитесь, что предыдущий диалог не появился в ее памяти.
7. Session Memory использует sessionId от Course Chat и 3 последних взаимодействия.
   Это учебная Simple Memory для одиночного процесса; в queue mode используйте поддерживаемую
   внешнюю память и проверяйте правильный session key. Не передавайте один фиксированный key всем.
8. Выполните негативные сценарии: неизвестная политика, сумма с текстом, вопрос без доступного tool,
   просьба отправить email. Агент должен уточнить/сообщить ограничение; workflow ничего не отправляет.
9. Поставьте max iterations=3. Изучите историю Executions: input, выбранный tool, tool result,
   final response, ошибки. Фиксируйте observable tool trace; скрытые внутренние рассуждения не нужны.
10. На 12 отдельно написанных natural-language кейсах измерьте правильность выбора инструмента,
     правильность ответа, число отказов, actual usage если доступен, latency и число tool calls.
     Не подставляйте результаты детерминированного simulator из notebook как результаты LLM.

[Simple Memory](https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.memorybufferwindow/)

## Сдача

Экспорт после удаления credentials references, таблица observed outcomes, 3 примера trace,
2 примера ошибок и описание session isolation. Сервис не нужно публиковать наружу.
Если учетной записи нет, сдайте notebook с контрактами, JSON и 12-кейсный план live-проверки,
явно указав **n8n_llm_agent: not_run**. Этот статус честнее вымышленных метрик.
