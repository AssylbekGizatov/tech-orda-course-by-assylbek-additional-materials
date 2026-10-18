# Реальная лабораторная: Course Helper в Copilot Studio

**Статус:** сервис не запускался при сборке. Нужна учебная учетная запись, разрешенная среда
и доступ к Copilot Studio. Python simulator не заменяет проверку UI. Два занятия по 54 минуты
практики: агент+knowledge, затем topic+переменные. Используем только вымышленные файлы недели.

## Занятие 1: агент и knowledge

1. Откройте [Copilot Studio](https://copilotstudio.microsoft.com/), выберите учебную environment.
   Запишите ее имя и тип лицензии без секретов. Для описанного canvas нужен standard harness;
   если включен New experience, переключитесь на стандартный опыт согласно текущему quickstart.
2. Создайте агента с названием **Course Helper Lab**. Описание: «Помогает студентам с домашней
   работой и готовит черновики запросов на консультации по фиктивной учебной базе».
3. На Overview проверьте Instructions: отвечать по базе, уточнять недостающие данные,
   честно сообщать о черновике, не обещать календарную запись.
4. В Knowledge выберите добавление файла, загрузите `../datasets/course_knowledge.txt`.
   Дождитесь состояния готовности источника. Если обработка еще идет, не оценивайте ответ как финальный.
5. В Test your agent спросите «Куда сдать домашнюю?», затем вопрос вне базы: «Какой курс валют?».
   Проверьте содержание, ссылки на knowledge и честное отсутствие ответа вне источника.

[Microsoft quickstart](https://learn.microsoft.com/en-us/microsoft-copilot-studio/fundamentals-get-started)
· [Knowledge sources](https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-copilot-studio)

## Занятие 2: topic, slots и условие

6. Topics → Add a topic → From blank. Название **Consultation Lab**.
   Для classic orchestration добавьте 6 фраз из `consultation_trigger_phrases.txt`.
   Для generative orchestration опишите назначение topic; не ожидайте полного совпадения механики trigger phrases.
7. Добавьте Question: «Выберите тему». Варианты Python, ML, Project; переменная `Topic.Subject`.
8. Добавьте Question для дня Tuesday/Thursday, переменная `Topic.Day`.
9. Добавьте Boolean-вопрос подтверждения, переменная `Topic.Confirmed`.
   Condition: при true покажите черновик, при false сообщение об отмене. Никаких календарных connectors пока нет.
10. Save. Запустите новую test-session и проверьте полную ветку, неподходящий день, отмену и повторный старт.
    Убедитесь, что значения старой test-session не подменили новый выбор.

[Microsoft: topics and authoring canvas](https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-create-edit-topics)

## Дополнительная заготовка YAML

`topic_consultation.yaml` показывает минимальный topic с текстовым slot и подтверждением; он короче
полной canvas-лабораторной и не содержит день/валидацию выбора. Можно открыть новый topic → More →
Open code editor, вставить YAML, Save, вернуться на canvas и дополнить. Microsoft отмечает ограничения
создания сложных topics только через YAML; сохранение и тест в вашей версии обязательны.

## Что сдавать

Таблицу 12 тестов: input, expected topic, observed topic, response, source, passed/failed.
Приложите 3 скриншота без учетных данных: knowledge Ready, topic canvas, успешный test-run.
Зафиксируйте дату и orchestration mode. Если лицензия недоступна, сдайте simulator, agent_spec,
схему topic и пометку **copilot_studio: not_run**. Публикация рассматривается на следующей неделе.
