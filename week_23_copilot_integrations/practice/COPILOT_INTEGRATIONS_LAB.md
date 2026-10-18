# Реальная лабораторная: knowledge + read-only tool + тестовый канал

**Статус поставки:** Microsoft 365, SharePoint, agent flows и публикация не вызывались.
Пройдите в разрешенной учебной среде; названия UI соответствуют standard harness из документации
на 18.10.2026. Учетные права и лицензии влияют на доступность. Базовый маршрут offline бесплатен.

## Занятие 1: M365 knowledge и разграничение доступа

1. Создайте/выберите отдельный учебный SharePoint site; загрузите `sharepoint_demo_policy.txt`.
   Используйте тестовых пользователей A и B, согласованных администратором. Рабочие документы не нужны.
2. В агенте недели 22 откройте Knowledge → Add knowledge → SharePoint. Укажите учебный site/file.
   Проверьте обработку источника и доступ account, под которым работает агент.
3. В Settings/Security/Authentication оставьте Microsoft authentication для внутреннего канала.
   Не переключайте No authentication ради обхода ошибки доступа.
4. Спросите о допустимых статусах, запишите source citation. Проверьте пользователя без доступа:
   источник не должен раскрываться. Отдельно проверьте права на file и на сам агент.

[Knowledge authentication](https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-copilot-studio)
· [End-user authentication](https://learn.microsoft.com/en-us/microsoft-copilot-studio/configuration-end-user-authentication)

## Занятие 2: action/tool и тестовая публикация

5. Подготовьте учебный SharePoint list `CourseRequests`: RequestId (text), Topic (text), Status (text).
   Внесите 4 фиктивные строки из CSV. Для проверки доступа настройте item permissions в учебной среде;
   текстовое поле OwnerId само по себе правами доступа не управляет.
6. Copilot Studio → Flows → New flow → Agent flow. Название **LookupRequestLab**.
   На **When an agent calls the flow** добавьте text input `requestId`.
7. Между trigger и **Respond to the agent** добавьте read-only SharePoint Get items.
   Ограничьте результат учебным list и requestId, не выполняйте Update/Create/Delete.
   Для простого курса допустимо получить маленький list доступных пользователю строк и
   отфильтровать requestId через Filter array; не применяйте этот способ к большим производственным спискам.
8. Добавьте условие: одна разрешенная строка → вернуть ее Status и RequestId;
   иначе result=`not_found_or_forbidden`. На ответе выключите asynchronous response.
   Configure run-only/user connection так, чтобы запрос использовал подходящие user credentials;
   maker connection без нужного ограничения может раскрыть лишние данные.
9. Опубликуйте учебный flow, добавьте его агенту как tool. В topic вызовите инструмент,
   передайте `Topic.RequestId`, отобразите output без обещания записи календаря.
   Пройдите все cases из CSV реальными пользователями, не подменяя identity текстом запроса.

[Create flow as tool](https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-flow-create)

10. При наличии разрешения преподавателя и прав публикации: Publish агента, затем Channels →
    Teams/Microsoft 365, выберите доступный внутренний учебный канал. Установите/откройте агента
    под тестовым пользователем, проверьте тот же набор cases и номер опубликованной версии.
    Изменение draft не обновляет опубликованную версию до повторного Publish.
    При trial или запрете tenant зафиксируйте точный этап `blocked/not_run` и завершите test-pane часть.

[Publish and channels](https://learn.microsoft.com/en-us/microsoft-copilot-studio/publication-fundamentals-publish-channels)

## Что сдавать

Схему вход/выход инструмента, flow canvas, 6 observed результатов, контроль доступа для A/B,
source citation и тест канала. Без реального доступа — SQLite-эквивалент, матрицу permissions,
план UI и статусы not_run. Не добавляйте connection strings, tenant secrets или реальные user данные.
