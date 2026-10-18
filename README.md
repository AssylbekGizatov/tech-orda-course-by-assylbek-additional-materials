# Tech Orda course authored by Gizatov A. S.

Дополнительные учебные материалы к курсу **Data Science, Machine Learning и AI для начинающих**: университетские лекции, практикумы на русском языке, локальные данные и домашние задания на каждую неделю. Материалы собраны по исходному силлабусу и дополняют основную презентацию преподавателя.

**Начните с [настройки среды](SETUP.md), затем откройте [неделю 01](week_01_intro_ds_ai/README.md).** Преподавателю пригодятся [календарный план](00_course_admin/CALENDAR.md) и [руководство по проведению занятий](00_course_admin/INSTRUCTOR_GUIDE.md).

## Программа и часы

| Параметр | Объём |
|---|---|
| Продолжительность | **26 недель** |
| Аудиторная нагрузка | **104 академических часа** по 45 минут = **78 астрономических часов** |
| Занятия | **52 занятия** по 90 минут, два занятия в неделю |
| Нагрузка недели | **4 академических часа** = 180 минут |
| Теория и практика | **40% / 60%**: 36 минут теории + 54 минуты практики на занятие |
| Самостоятельная работа | Отдельные оценки времени в недельных Homework; сверх аудиторных часов |

Основание — [оригинальный силлабус](00_course_admin/original_syllabus.pdf). Его **15 модулей** распределены между 26 неделями с сохранением часов: сначала Python, SQL и описательная аналитика; затем предобработка, классические модели, ансамбли, оценка и нейросети; далее LLM, API, Copilot Studio, n8n и итоговый проект. Модули по шесть часов могут переходить через границу недели. Точная привязка каждого занятия к модулю находится в [календарном плане](00_course_admin/CALENDAR.md), а данные плана — в [course_plan.json](course_plan.json).

Распределение 36/54 минуты — методическая реализация общей пропорции силлабуса. Конкретные даты занятий не заданы: исходный документ указывает месяц старта, но не дни недели. Полные внешние лекции могут быть глубже уровня курса; в недельных маршрутах выделены фрагменты, подходящие начинающим.

## Все 26 недель

Ссылка в первом столбце открывает план недели. Ссылка в последнем — разобранный практикум; данные, презентации и Homework лежат рядом с ним в той же недельной папке.

| Неделя | Тема | Конкретная практика и результат |
|---:|---|---|
| [01](week_01_intro_ds_ai/README.md) | Введение в Data Science и AI | [Анализ обращений службы поддержки](week_01_intro_ds_ai/practice/01_reproducible_data_analysis.ipynb): задача, единица наблюдения, статистики ожидания и воспроизводимый отчёт |
| [02](week_02_python_numpy/README.md) | Python и NumPy | [Энергопотребление здания](week_02_python_numpy/practice/01_python_numpy_energy.ipynb): структуры Python, массивы, broadcasting, расчёт потребления и стоимости |
| [03](week_03_pandas_files/README.md) | pandas, CSV и JSON | [Аудит заказов магазина](week_03_pandas_files/practice/01_pandas_orders_audit.ipynb): типы, фильтрация, объединение файлов и проверенный отчёт по городам |
| [04](week_04_sql_basics/README.md) | SQL: SELECT, JOIN, GROUP BY | [Аналитика магазина в SQLite](week_04_sql_basics/practice/01_sql_store_analytics.ipynb): выручка, клиенты без заказов и контроль числа строк после JOIN |
| [05](week_05_sql_windows_eda/README.md) | Оконные функции и начало EDA | [Динамика четырёх магазинов](week_05_sql_windows_eda/practice/01_sql_windows_descriptive_eda.ipynb): LAG, скользящие показатели, распределения и описательная статистика |
| [06](week_06_eda_visualization/README.md) | Визуализация и корреляции | [Исследование доставок](week_06_eda_visualization/practice/01_visualization_correlation.ipynb): matplotlib, seaborn, Plotly, сравнение групп и ограничения корреляции |
| [07](week_07_storytelling_cleaning/README.md) | Data storytelling и очистка | [От грязных данных к сообщению для руководителя](week_07_storytelling_cleaning/practice/01_storytelling_data_cleaning.ipynb): пропуски, дубликаты, выбросы и журнал изменений |
| [08](week_08_preprocessing_pipelines/README.md) | Признаки и pipelines | [Предобработка объявлений без утечки](week_08_preprocessing_pipelines/practice/01_leakage_safe_preprocessing.ipynb): imputation, encoding, scaling и ColumnTransformer/Pipeline |
| [09](week_09_linear_regression/README.md) | Линейная регрессия | [Модель от формулы до прогноза](week_09_linear_regression/practice/01_linear_regression_from_scratch.ipynb): MSE, gradient descent, least squares, регуляризация и остатки |
| [10](week_10_logistic_knn/README.md) | Логистическая регрессия и kNN | [Вероятность, расстояние и порог решения](week_10_logistic_knn/practice/01_logistic_regression_and_knn.ipynb): сравнение моделей, масштабирование и ошибки классификации |
| [11](week_11_trees_svm/README.md) | Деревья решений и SVM | [Два способа построить границу](week_11_trees_svm/practice/01_decision_trees_and_svm.ipynb): глубина дерева, impurity, margin и ядра |
| [12](week_12_random_forest/README.md) | Bagging и Random Forest | [Усреднение деревьев и OOB](week_12_random_forest/practice/01_bagging_random_forest_oob.ipynb): устойчивость ансамбля, bias/variance и сравнение с одиночным деревом |
| [13](week_13_boosting_tuning/README.md) | Gradient Boosting, XGBoost, LightGBM | [Бустинг и промежуточный проект](week_13_boosting_tuning/practice/01_boosting_xgboost_lightgbm_midterm.ipynb): ручное исправление остатков, реальные библиотеки, одинаковый бюджет подбора и честный test |
| [14](week_14_clustering_dimensions/README.md) | K-Means, DBSCAN, PCA, t-SNE | [Структура данных Wine](week_14_clustering_dimensions/practice/01_clustering_pca_tsne.ipynb): кластеризация без передачи классов алгоритму, снижение размерности и интерпретация проекций |
| [15](week_15_evaluation_cv/README.md) | Метрики и кросс-валидация | [Как не переоценить модель](week_15_evaluation_cv/practice/01_metrics_cv_and_overfitting.ipynb): baseline, метрики, CV, переобучение и независимая проверка |
| [16](week_16_explainability_nn/README.md) | SHAP, LIME и первый нейрон | [Объяснение предсказания и ограничения объяснения](week_16_explainability_nn/practice/01_shap_lime_and_neuron.ipynb): реальные SHAP/LIME, активации и loss |
| [17](week_17_backprop_frameworks/README.md) | Backpropagation, PyTorch, Keras/TensorFlow | Одинаковые локальные цифры 8×8: [NumPy и проверка производных](week_17_backprop_frameworks/practice/01_backpropagation_numpy.ipynb), [обучение в PyTorch](week_17_backprop_frameworks/practice/02_pytorch_digits_training.ipynb), [обучение в TensorFlow/Keras](week_17_backprop_frameworks/practice/03_tensorflow_keras_digits_training.ipynb) |
| [18](week_18_dl_llm_intro/README.md) | Валидация нейросети и принципы LLM | [MLP, checkpoint и численный attention](week_18_dl_llm_intro/practice/Practice_Week_18.ipynb): train/validation/test, регуляризация, токены, causal mask и heatmap |
| [19](week_19_prompt_engineering/README.md) | Prompt Engineering | [Zero/few-shot и проверяемый evaluator](week_19_prompt_engineering/practice/Practice_Week_19.ipynb): инструкции, корректность JSON, класс, подтверждение ответа и раздельные dev/test |
| [20](week_20_gpt_api_chatbot/README.md) | GPT API и чат-бот на Python | [Контракт API, ошибки и история](week_20_gpt_api_chatbot/practice/Practice_Week_20.ipynb): offline-проверка parser/retry; отдельно — настоящий API-клиент и live-лабораторная |
| [21](week_21_context_memory/README.md) | Контекст, память и retrieval | [Локальный поиск с источниками](week_21_context_memory/practice/Practice_Week_21.ipynb): TF-IDF, Recall@k, отказ при отсутствии факта, память отдельных сессий и optional RAG-клиент |
| [22](week_22_copilot_basics/README.md) | Copilot Studio: основы | [Агент, topics и переменные](week_22_copilot_basics/practice/Practice_Week_22.ipynb): Python-симулятор диалога и отдельная пошаговая лабораторная в Copilot Studio |
| [23](week_23_copilot_integrations/README.md) | Copilot Studio: интеграции и оценка | [Источники, права и actions](week_23_copilot_integrations/practice/Practice_Week_23.ipynb): локальная SQLite-иллюстрация доступа плюс Microsoft 365/agent flows/test/publish lab |
| [24](week_24_n8n_workflows/README.md) | n8n: workflow, HTTP, SQL, ошибки | [Проверяемый поток данных](week_24_n8n_workflows/practice/Practice_Week_24.ipynb): JSON, валидация, идемпотентный SQL, локальный HTTP-сервер и четыре импортируемых workflow |
| [25](week_25_n8n_ai_agents/README.md) | n8n: AI-агент с инструментами | [Tools, память и полный сценарий](week_25_n8n_ai_agents/practice/Practice_Week_25.ipynb): контракты инструментов, журнал результатов, offline-симулятор и настоящий импортируемый AI Agent workflow |
| [26](week_26_final_project/README.md) | Финальный проект и защита | [Приоритизация заявок](week_26_final_project/practice/Practice_Week_26.ipynb): EDA, временное разбиение, baseline, цена FP/FN, анализ ошибок, работающий CLI и шаблон защиты |

## Как устроена папка недели

| Путь | Что внутри |
|---|---|
| `README.md` | Два занятия, часы, цели, предварительные знания и порядок работы |
| `presentations/` | Скачанные внешние лекции; README с источниками, выбранными страницами, уровнем и временем изучения |
| `practice/` | Разобранные `.ipynb` с комментариями, формулами, таблицами, графиками и проверками; при необходимости — скрипты и vendor labs |
| `datasets/` | Локальные данные и словарь/происхождение в `README.md` или `DATA_DICTIONARY.md` |
| `homework/` | `Homework_Week_XX.md`: задачи, подсказки, ожидаемый результат и рубрика; рядом — незаполненный notebook-стартер |

В большинстве недель один основной практикум. На неделе 17 их три: NumPy, PyTorch и TensorFlow/Keras, поэтому всего **28 разобранных практических ноутбуков** на 26 недель. Каждая неделя содержит отдельный Homework и стартер.

## Быстрый запуск

Рекомендуем **Python 3.12**. Скачайте или клонируйте весь репозиторий и откройте терминал в его корне — в папке, где лежит этот README. Для первого блока курса достаточно базовых зависимостей. Подробности, установка расширений и разбор типичных ошибок — в [SETUP.md](SETUP.md).

**macOS / Linux, bash или zsh:**

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-core.txt jupyterlab
python -m jupyter lab
```

**Windows, PowerShell:**

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-core.txt jupyterlab
.\.venv\Scripts\python.exe -m jupyter lab
```

В JupyterLab откройте нужную папку `practice/`, затем notebook. Выберите Python из созданного окружения и выполните **Kernel → Restart Kernel and Run All Cells**. В сохранённой копии уже есть результаты контрольного исполнения; повторный запуск показывает результат вашей среды. Интернет нужен для первоначальной установки пакетов; локальные практикумы используют приложенные данные и CPU.

| Файл зависимостей | Когда нужен |
|---|---|
| [requirements-core.txt](requirements-core.txt) | Python/NumPy/pandas/SQL, графики, scikit-learn и Jupyter kernel; базовая часть и offline-практика AI-интеграций |
| [requirements-ml.txt](requirements-ml.txt) | Полный набор для всех 54 ноутбуков, включая XGBoost, LightGBM, SHAP, LIME, PyTorch и TensorFlow; включает core |
| [00_course_admin/requirements-qa-lock.txt](00_course_admin/requirements-qa-lock.txt) | Зафиксированные версии контрольной Linux x86_64 / CPU-среды; используется базовыми файлами как constraints |

Перед неделями 13, 16 и 17 установите полный набор: `python -m pip install -r requirements-ml.txt` в активном окружении. Для Windows без активации используйте `.\.venv\Scripts\python.exe` вместо `python`. JupyterLab — отдельно устанавливаемый интерфейс; контрольный прогон проверял код в Jupyter kernels, а не работу UI на каждой операционной системе. Наличие подходящих wheels для полного DL-набора на другой платформе нужно проверять при установке; воспроизводимый референс описан в [SETUP.md](SETUP.md).

## Как использовать дополнительные лекции

Основная презентация преподавателя задаёт ход занятия. Внешние материалы помогают раскрыть отдельную тему через формулу, диаграмму, график или более подробный пример. Начинайте с `presentations/README.md` соответствующей недели: там указан основной маршрут и факультативные части. **Полная скачанная презентация и обязательный фрагмент для студента имеют разный объём.**

Для LLM и агентных систем университетские лекции объясняют принципы; текущие API и интерфейсы Copilot/n8n изучаются по официальной документации разработчиков. Сохранённые HTML/Markdown-страницы явно обозначены как документация. Исторические названия моделей, цены, дедлайны университетских курсов и скриншоты интерфейсов не считаются текущими условиями этого курса.

Общая навигация: [каталог материалов](RESOURCE_CATALOG.md), [машиночитаемый каталог с источниками и SHA-256](RESOURCE_CATALOG.json), [авторство и условия использования](THIRD_PARTY_NOTICES.md). Университетские файлы сохраняют исходное авторство и титры; название этого репозитория относится к организации курса и его учебному сопровождению.

## Домашние работы и оценивание

Работа недели начинается с `Homework_Week_XX.md`: прочитайте задачи, критерии на 100 баллов, подсказки и ожидаемый формат сдачи. Затем откройте notebook-стартер рядом. Его имя может оканчиваться на `_starter`, `_Starter` или просто `Homework_Week_XX.ipynb`; точная ссылка есть в README недели.

**Успешный Run All стартера означает исправную заготовку. Домашняя работа остаётся незавершённой, пока студент не реализовал TODO, не построил нужные результаты и не написал выводы.** Полный практикум служит примером метода; самостоятельное задание требует своего эксперимента и объяснения.

Силлабус задаёт **12 оцениваемых домашних работ**, промежуточный проект, финальную защиту и активность. В репозитории есть **26 недельных заданий**; предложенная схема объединяет их в 12 сдач, сохраняя веса силлабуса: **40% / 20% / 35% / 5%**. Полная схема, сроки и критерии находятся в [ASSESSMENT.md](00_course_admin/ASSESSMENT.md). Проходной результат — не менее 70/100 с обязательной защитой финального проекта. Промежуточный проект подготовлен к неделе 13; завершение и защита финального — к неделе 26.

## Что работает offline, а что проверяется в сервисе

Все 54 ноутбука запускаются на CPU с локальными данными после установки зависимостей. В классическом ML и DL используются реальные вычисления и библиотеки. В API/Copilot/n8n части, моделирующие внешний сервис, прямо помечены как **fixture** или **симуляция**. Например, набор авторских ответов в неделе 19 проверяет evaluator, а не измеряет эффективность prompt на живой LLM; численный attention в неделе 18 не является предобученной языковой моделью.

| Реальная интеграция | Где выполнить |
|---|---|
| OpenAI API: ключ через окружение, Chat Completions и Responses, история и ошибки | [Неделя 20: LIVE_API_LAB.md](week_20_gpt_api_chatbot/practice/LIVE_API_LAB.md) и [live_api_chatbot.py](week_20_gpt_api_chatbot/practice/live_api_chatbot.py) |
| Ответ с найденным контекстом через API | [Неделя 21: live_rag.py](week_21_context_memory/practice/live_rag.py); сначала локальная оценка retrieval в основном практикуме |
| Создание Copilot-агента, knowledge, topics и переменные | [Неделя 22: COPILOT_STUDIO_LAB.md](week_22_copilot_basics/practice/COPILOT_STUDIO_LAB.md) |
| Microsoft 365, agent flows, права, тестирование и публикация | [Неделя 23: COPILOT_INTEGRATIONS_LAB.md](week_23_copilot_integrations/practice/COPILOT_INTEGRATIONS_LAB.md) |
| Импорт workflow, HTTP, Postgres и error workflow в n8n | [Неделя 24: N8N_LAB.md](week_24_n8n_workflows/practice/N8N_LAB.md) |
| Настоящий AI Agent с tools, model и memory в n8n | [Неделя 25: N8N_AI_AGENT_LAB.md](week_25_n8n_ai_agents/practice/N8N_AI_AGENT_LAB.md) |
| Воспроизводимая локальная демонстрация финального проекта | [Неделя 26: DEPLOYMENT_AND_EVALUATION.md](week_26_final_project/practice/DEPLOYMENT_AND_EVALUATION.md) и [capstone_cli.py](week_26_final_project/practice/capstone_cli.py) |

Для live-лабораторных нужны разрешённые учебные аккаунты, доступные сервисы и собственные credentials. Их настройка описана отдельно; ключи не входят в учебные файлы. При сборке платные API-вызовы, работа в Copilot Studio и выполнение n8n в пользовательском аккаунте не проводились. Offline-тест не подтверждает доступность модели, лицензии, подключения или опубликованного агента: в сдаче фиксируется фактический статус live-проверки.

## Проверка качества и воспроизводимость

Контрольный прогон от **18 октября 2026 года**: **54/54 ноутбука успешно исполнены** в отдельных настоящих Jupyter kernels через `nbclient` на CPU. Результаты сохранены в `.ipynb`.

| Проверка | Зафиксированный результат |
|---|---:|
| Разобранные практикумы | **28** |
| Исполнимые незаполненные стартеры Homework | **26** |
| Исполненные кодовые ячейки | **500** |
| Сохранённые PNG-выводы | **90** |
| Ноутбуки с успешным контрольным исполнением | **54 из 54** |
| Ошибки исполнения в финальном прогоне | **0** |

Доказательства: [подробный отчёт по файлам и SHA-256](00_course_admin/validation_all.json), [версии интерпретатора и пакетов](00_course_admin/validation_all_versions.json), [полный lock среды](00_course_admin/requirements-qa-lock.txt). Проверенная платформа — **Python 3.12.14, Linux x86_64, CPU**. В проверку входят настоящий XGBoost/LightGBM, SHAP/LIME и обучение в PyTorch/TensorFlow, а также исполнимость заготовок; это не подтверждение выполнения студентом Homework и не тест живых облачных сервисов.

Численные проверки, проверки данных и отсутствие ошибок исполнения дополняют преподавательскую оценку. Для завершения темы студент должен объяснить выбор данных, смысл хотя бы одной формулы, одного графика и одного ограничения результата.

## Документы курса

- [Исходный силлабус](00_course_admin/original_syllabus.pdf) — первоисточник содержания, нагрузки и правил оценивания.
- [Календарный план](00_course_admin/CALENDAR.md) — 15 модулей, 52 занятия и 26 недель.
- [Оценивание](00_course_admin/ASSESSMENT.md) — 12 сдач, промежуточный проект, итоговая защита и недельные рубрики.
- [Руководство преподавателя](00_course_admin/INSTRUCTOR_GUIDE.md) — подготовка занятия, использование лекций, организация практики и критерии проверки.
- [Настройка среды](SETUP.md) — первый запуск, уровни зависимостей и диагностика проблем.
- [Каталог ресурсов](RESOURCE_CATALOG.md) и [сведения об авторстве](THIRD_PARTY_NOTICES.md) — источники дополнительных материалов и условия их использования.
