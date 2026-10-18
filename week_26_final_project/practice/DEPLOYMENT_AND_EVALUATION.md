# Локальный запуск и приемка проекта

## Готовый baseline

В `Practice_Week_26.ipynb` выполните Restart Kernel → Run All. Получаются EDA, baseline comparison,
validation threshold, held-out test metrics, bootstrap interval и inference example.
Для запуска без Jupyter из practice:

```bash
python capstone_cli.py --minutes-open 50 --affected-users 10 --category access --channel portal
```

CLI реально обучает небольшой pipeline на первых 360 строках, выбирает threshold на следующих
120 и предсказывает один новый input. Test-часть не участвует в выборе. Повторное обучение быстрое
и устраняет необходимость загрузки pickle. Если сохраняете модель, загружайте только доверенные
артефакты своей команды и фиксируйте совместимые версии библиотек.
[Model persistence](https://scikit-learn.org/stable/model_persistence.html)

## Приемка

- Все notebooks выполняются с чистого ядра и локальными файлами.
- Schema неверного input отвергается; final_resolution_minutes не поступает в модель.
- Train/validation/test разделены по времени, preprocess.fit использует train.
- Baseline, новая модель и выбранный threshold имеют объясненную метрику.
- Demo возвращает вероятность, threshold, решение и пометку synthetic baseline.
- README дает одну воспроизводимую команду; нет ключей и обязательных платных сервисов.

[Common pitfalls](https://scikit-learn.org/stable/common_pitfalls.html)
· [Evaluation](https://scikit-learn.org/stable/modules/model_evaluation.html)

## Если выбран другой трек

ML: правильный split, baseline и leakage audit обязательны. RAG: отдельные retrieval и answer
tests, sources и abstention. Copilot/n8n: actual observed runs или явный offline simulator,
контракт tool, session isolation, ошибки и отсутствие неразрешенных side effects.

## Переход к серверу

Для учебной защиты достаточно локального CLI. Для веб-демо вынесите predict в функцию,
загружайте модель один раз при старте, добавьте schema validation, health endpoint, timeout,
ограничение размера запроса и доступ только учебной группе. Проверьте app на новых test cases.
Облачное размещение требует выбранной площадки, secrets setup и отдельной наблюдаемой проверки;
этот комплект не заявляет, что облачная публикация уже выполнена.

## Рубрика финального проекта — 100 баллов

| Критерий | Баллы |
|---|---:|
| Проблема, данные и EDA | 15 |
| Baseline и метод без утечки | 25 |
| Честная оценка, ошибки, uncertainty | 25 |
| Работающий интерфейс и воспроизводимость | 20 |
| Защита, ограничения, следующие шаги | 15 |

Порог прохождения: 60/100 по учебной рубрике. Критические ошибки (test leakage, выдуманные live
результаты, неработающее основное demo) требуют исправления соответствующей части независимо
от суммарного балла. Это авторская оценочная рубрика курса, не официальный регламент программы.
