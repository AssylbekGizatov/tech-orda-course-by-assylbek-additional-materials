#!/usr/bin/env python3
"""Build the original Russian practical materials for course weeks 01–08.

All tabular datasets in this file are synthetic. Run from any working directory:
    python scripts/build_weeks_01_08.py
The script intentionally does not download or copy third-party course material.
"""
from __future__ import annotations

import csv
import datetime as dt
import json
import math
import random
import sqlite3
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = json.loads((ROOT / "course_plan.json").read_text(encoding="utf-8"))


def clean(text):
    return textwrap.dedent(text).strip() + "\n"


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": clean(text).splitlines(True)}


def code(text):
    return {"cell_type": "code", "metadata": {}, "execution_count": None,
            "outputs": [], "source": clean(text).splitlines(True)}


def save_notebook(path, cells, week, purpose="practice"):
    for i, cell in enumerate(cells):
        cell["id"] = f"w{week:02d}-{purpose}-{i:02d}"
    notebook = {
        "nbformat": 4, "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.11"},
            "course": {"week": week, "language": "ru", "purpose": purpose,
                       "dataset_type": "synthetic", "network_required": False,
                       "instructor": "Gizatov A. S."},
        },
        "cells": cells,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def save_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def dataset_readme(week, text):
    path = ROOT / PLAN[week - 1]["folder"] / "datasets" / "README.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    intro = clean(f"""
        # Данные недели {week:02d}

        **Происхождение:** оригинальные синтетические учебные данные, созданные специально
        для этого практикума. Это не реальные данные компаний, городов, клиентов или студентов.
        Денежная единица в примерах — тенге (KZT), но числа не описывают цены рынка.
        Персональные данные отсутствуют. Генератор: [`scripts/build_weeks_01_08.py`](../../scripts/build_weeks_01_08.py).
        Случайность задаётся отдельным `random.Random(seed)` для каждой недели; файлы уже включены,
        поэтому для лабораторной не нужны сеть или повторная генерация.

        """)
    path.write_text(intro + "\n" + clean(text), encoding="utf-8")


def setup(week, imports=""):
    folder = PLAN[week - 1]["folder"]
    imports = imports.replace("\n", "\n        ")
    return code(f"""
        from pathlib import Path
        import sys
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        from IPython.display import display
        {imports}

        SEED = 42
        rng = np.random.default_rng(SEED)
        plt.rcParams.update({{"figure.figsize": (8, 4), "axes.grid": True,
                             "grid.alpha": 0.2, "figure.dpi": 100}})

        def locate_week():
            "Работает из practice/, homework/, папки недели и корня репозитория."
            current = Path.cwd().resolve()
            for parent in (current, *current.parents):
                for candidate in (parent, parent / {folder!r}):
                    if candidate.name == {folder!r} and (candidate / "datasets").is_dir():
                        return candidate
            raise FileNotFoundError("Откройте notebook внутри полного клона репозитория.")

        WEEK_DIR = locate_week()
        DATA_DIR = WEEK_DIR / "datasets"
        print("Python:", sys.version.split()[0], "| NumPy:", np.__version__, "| pandas:", pd.__version__)
        print("Рабочая неделя:", WEEK_DIR.name)
        """)


def sources_cell(sources):
    return md("## Документация и дальнейшее чтение\n\n"
              + "\n".join(f"- [{label}]({url})" for label, url in sources)
              + "\n\nКод, объяснения и синтетические примеры в этой лабораторной подготовлены для курса; "
                "это не копия университетского ноутбука. Дополнительные лекции находятся в `../presentations/`. "
                "Документация проверена 18 октября 2026 года; версии среды закреплены на уровне репозитория.")


def make_homework(week, loading, tasks, hours, hints, checks):
    folder = ROOT / PLAN[week - 1]["folder"]
    title = PLAN[week - 1]["title"]
    task_md = "\n\n".join(
        f"### {i}. {task['title']} — {task['points']} баллов\n\n{task['description']}"
        for i, task in enumerate(tasks, 1)
    )
    rubric = "\n".join(f"| {i}. {t['title']} | {t['points']} |" for i, t in enumerate(tasks, 1))
    document = f"""# Homework Week {week:02d} — {title}

**Оценка самостоятельной работы:** {hours} астрономических часа; это рекомендация автора практикума,
а не дополнительные контактные часы силлабуса. **Рекомендуемый дедлайн:** 7 дней после занятий недели.
Задание рассчитано на начинающего после лабораторной. Оно развивает материал, а не требует обучения
моделей, которые ещё не разбирались на занятии.

## Что сдавать

- Скопируйте [`Homework_Week_{week:02d}.ipynb`](Homework_Week_{week:02d}.ipynb) в `Surname_Week_{week:02d}.ipynb`.
- Завершите TODO, подпишите графики, добавьте объяснения в Markdown и выполните `Restart Kernel → Run All`.
- В конце укажите 3–5 выводов с числами, одно ограничение анализа и используемые источники/помощь инструментов.
- Представьте notebook с сохранёнными выводами. Большие скриншоты кода не заменяют исполняемые ячейки.
- Не изменяйте исходные файлы `datasets/`: создавайте копии DataFrame и сохраняйте свои результаты отдельно.

## Задания

{task_md}

## Критерии оценки

| Часть | Максимум |
|---|---:|
{rubric}
| **Итого** | **100** |

Внутри каждой части 60% баллов даются за корректность результата и соблюдение условия,
25% — за воспроизводимость, подписи и проверки, 15% — за объяснение решения своими словами.
Незаполненный TODO не является решением, даже если starter выполняется без ошибок.
Эта рубрика оценивает недельную работу; вклад в итоговую оценку курса определяется общей схемой курса.

## Подсказки без готового решения

{hints}

## Самопроверка перед сдачей

{checks}
"""
    (folder / "homework").mkdir(parents=True, exist_ok=True)
    (folder / "homework" / f"Homework_Week_{week:02d}.md").write_text(document, encoding="utf-8")
    cells = [md(f"""# Homework Week {week:02d} — {title}

        **Starter, не готовое решение.** Все `None`, пустые SQL-строки и TODO нужно заменить
        собственным решением. Ячейки намеренно не выбрасывают исключения до заполнения:
        успешный запуск пустого starter не означает, что домашняя работа выполнена.

        Полные условия и рубрика: [Homework_Week_{week:02d}.md](Homework_Week_{week:02d}.md).
        Имя: **TODO**. Дата: **TODO**. Время работы: **TODO**.
        """), setup(week, "import sqlite3\nimport json"), code(loading)]
    for i, task in enumerate(tasks, 1):
        cells.extend([md(f"## {i}. {task['title']} ({task['points']} баллов)\n\n{task['description']}"),
                      code(task["starter"]),
                      md("**Моё объяснение и результат:** TODO. Укажите проверяемый вывод и его ограничение.")])
    cells.append(md("""## Перед сдачей

        Выполните notebook заново в чистом kernel. Убедитесь, что в ответах не остались TODO,
        все значения рассчитаны кодом, графики имеют единицы измерения, а выводы относятся
        только к этому синтетическому набору. Перечислите использованные источники и помощь.
        """))
    save_notebook(folder / "homework" / f"Homework_Week_{week:02d}.ipynb", cells, week, "homework")


def week_readme(week, notebook_name, outcomes, prerequisites, steps, sources):
    plan = PLAN[week - 1]
    folder = ROOT / plan["folder"]
    rows = "\n".join(f"| {i} | {s['module']} | {s['topic']} | 2 | 36 | 54 |" for i, s in enumerate(plan["sessions"], 1))
    source_lines = "\n".join(f"- [{label}]({url})" for label, url in sources)
    content = f"""# Неделя {week:02d} — {plan['title']}

**Преподаватель курса:** Gizatov A. S. / Ғизатов Асылбек Серікұлы.
**Уровень:** beginner, объяснения и задания на русском; API и дополнительные лекции преимущественно на английском.

## Место в силлабусе и часы

Неделя содержит **4 академических часа = 180 минут контактной работы**: два занятия по 90 минут.
По силлабусу 1 академический час = 45 минут. Соотношение **40% теории / 60% практики**
даёт **72 минуты теории и 108 минут практики**. Самостоятельная работа вынесена отдельно.
Понедельная разбивка — методическая организация модулей исходного силлабуса, не официальная календарная дата.

| Занятие | Модуль | Точная тема | Акад. часы | Теория, мин | Практика, мин |
|---|---:|---|---:|---:|---:|
{rows}
| **Всего** | | | **4** | **72** | **108** |

### План каждого занятия на 90 минут

| Интервал | Формат | Назначение |
|---|---|---|
| 0–18 | Теория | Постановка задачи, понятия, рисунок или формула |
| 18–45 | Практика | Пример с преподавателем, запуск и объяснение кода |
| 45–63 | Теория | Разбор наблюдений, границы метода и типичная ошибка |
| 63–90 | Практика | Самостоятельное изменение примера, проверки и разбор результатов |

{steps}

## Что студент сможет сделать

{outcomes}

## Что знать до занятия

{prerequisites}

## Файлы недели

- [`practice/{notebook_name}`](practice/{notebook_name}) — полный разобранный практикум с кодом, описательной аналитикой, графиками и проверками.
- [`datasets/README.md`](datasets/README.md) — происхождение, словарь полей и ограничения данных.
- [`homework/Homework_Week_{week:02d}.md`](homework/Homework_Week_{week:02d}.md) — задания, время, подсказки и рубрика на 100 баллов.
- [`homework/Homework_Week_{week:02d}.ipynb`](homework/Homework_Week_{week:02d}.ipynb) — исполняемый starter с незавершёнными TODO.
- [`presentations/`](presentations/) — подобранные дополнительные лекции и сведения об источниках. Основную презентацию преподавателя эти материалы дополняют.

## Как работать

Установите общую среду из корня репозитория и откройте полный клон в JupyterLab.
Выполните `Restart Kernel → Run All` сверху вниз. Лабораторная работает на CPU, без API-ключей,
скачивания данных и подключения к сети; пути ищутся относительно клона, а не компьютера автора.
Часть кода можно разбирать заранее, но результаты и вопросы следует обсуждать в аудитории.

## Документация для самостоятельной проверки

{source_lines}

Данные в практикуме синтетические. Выводы относятся к учебному примеру и не являются статистикой рынка или города.
"""
    (folder / "README.md").write_text(content, encoding="utf-8")


def build_week_01():
    week = 1
    folder = ROOT / PLAN[week - 1]["folder"]
    rnd = random.Random(101)
    rows = []
    for i in range(150):
        channel = rnd.choice(["chat", "email", "phone"])
        category = rnd.choice(["access", "payment", "technical"])
        wait = max(1.0, rnd.gauss({"chat": 8, "email": 35, "phone": 13}[channel], 4))
        duration = max(3, rnd.gauss(18 + (category == "technical") * 25, 9))
        rows.append({"ticket_id": f"T{i+1:04d}", "created_date": str(dt.date(2026, 1, 1) + dt.timedelta(days=i // 5)),
                     "channel": channel, "category": category,
                     "wait_minutes": round(wait, 1), "resolution_minutes": round(duration, 1),
                     "satisfaction": min(5, max(1, round(5 - wait / 19 + rnd.gauss(0, 0.6))))})
    save_csv(folder / "datasets" / "support_tickets.csv", rows)
    dataset_readme(1, """Seed: `101`. Файл `support_tickets.csv`: **150 строк, 7 полей**, одна строка — одно обращение.

| Поле | Тип / единицы | Смысл |
|---|---|---|
| ticket_id | string | Уникальный синтетический идентификатор обращения |
| created_date | ISO-дата | Дата поступления; 5 обращений за каждый из 30 дней |
| channel | category | chat / email / phone |
| category | category | access / payment / technical |
| wait_minutes | float, минуты | Ожидание первого ответа, положительное |
| resolution_minutes | float, минуты | Длительность решения, положительная |
| satisfaction | integer, 1–5 | Синтетическая порядковая оценка |

Пропусков и дубликатов нет. Канал связан с ожиданием по правилу генератора;
это учебная закономерность, а не доказательство превосходства канала в реальном бизнесе.
Категория и длительность решения известны на разных этапах: длительность нельзя использовать,
если прогноз строится до решения обращения.""")
    sources = [("JupyterLab: работа с notebooks", "https://jupyterlab.readthedocs.io/en/stable/user/notebook.html"),
               ("Python: вводный учебник", "https://docs.python.org/3/tutorial/"),
               ("Pro Git: основы Git", "https://git-scm.com/book/en/v2/Getting-Started-Git-Basics")]
    cells = [
        md("""# Неделя 01. От бизнес-вопроса к воспроизводимому анализу

        **Кейс:** учебная служба поддержки хочет понять, сколько пользователи ждут ответа.
        Мы пройдём маленький цикл Data Science: вопрос → таблица → проверка → число → график → вывод.
        Первую модель ещё не обучаем: сначала нужно определить, что мы вообще измеряем.

        **Цель:** отличить анализ, ML и AI-систему; запустить Jupyter; прочитать небольшой CSV;
        сделать первый численный вывод и проверить воспроизводимость. Все данные синтетические.
        """),
        md("""## 1. Что такое задача, наблюдение и признак

        Data Science объединяет работу с данными, статистику и предметную постановку задачи.
        ML учится отображать признаки в прогноз по примерам. AI-система может включать ML,
        правила, интерфейс и действия. У этих терминов есть пересечения; одно не заменяет другое.

        В таблице одна **строка** — обращение; `channel` — признак;
        `wait_minutes` можно сделать **целевой переменной**, если прогноз нужен при поступлении.
        Сначала спрашиваем: кому нужен результат, в какой момент он используется и что считается успехом?
        """),
        setup(1, "import hashlib\nimport json"),
        md("""## 2. Notebook — это исполняемый документ

        Markdown-ячейка содержит объяснение; Code-ячейка меняет состояние kernel.
        `Shift+Enter` запускает ячейку. Ошибка выполнения требует исправления причины,
        а не скрытия ячейки. В конце используйте **Restart Kernel → Run All**:
        это проверяет, что результат не зависит от забытых переменных.
        """),
        code("""
        data_path = DATA_DIR / "support_tickets.csv"
        tickets = pd.read_csv(data_path, parse_dates=["created_date"])
        display(tickets.head(8))
        print("Строк:", len(tickets), "| Столбцов:", len(tickets.columns))
        """),
        md("""## 3. Не путать измерение с интерпретацией

        `wait_minutes` — количественная величина с единицей измерения.
        `satisfaction` — порядковая шкала от 1 до 5: разница между 1 и 2 не обязана
        значить то же, что между 4 и 5. Идентификатор обращения не является полезной числовой мерой.
        Словарь полей находится в `../datasets/README.md`.
        """),
        code("""
        schema = pd.DataFrame({"dtype": tickets.dtypes.astype(str),
                               "missing": tickets.isna().sum(),
                               "unique_values": tickets.nunique()})
        display(schema)
        # Это проверка контракта нашего конкретного учебного CSV.
        assert tickets["ticket_id"].is_unique
        assert tickets["wait_minutes"].gt(0).all()
        assert tickets["satisfaction"].between(1, 5).all()
        """),
        md(r"""## 4. Среднее и медиана отвечают на разные вопросы

        Среднее: $\bar{x}=\frac{1}{n}\sum_{i=1}^n x_i$.
        Медиана — центральное значение упорядоченной выборки (для чётного $n$ — среднее двух центральных).
        Большое ожидание одного клиента влияет на среднее сильнее, чем на медиану.
        Поэтому в отчёте покажем обе величины и объём выборки.
        """),
        code("""
        waits = tickets["wait_minutes"]
        summary = pd.Series({"n": len(waits), "mean_minutes": waits.mean(),
                             "median_minutes": waits.median(), "min_minutes": waits.min(),
                             "p90_minutes": waits.quantile(0.90), "max_minutes": waits.max()})
        display(summary.round(2).to_frame("value"))
        # Вручную проверяем формулу среднего, не полагаясь на красивую таблицу.
        manual_mean = sum(waits) / len(waits)
        assert np.isclose(manual_mean, waits.mean())
        """),
        md("""## 5. Распределение показывает то, что скрывает одно число

        Гистограмма считает, сколько обращений попало в каждый интервал ожидания.
        Вертикальные линии показывают среднее и медиану. Нельзя считать 90-й процентиль
        обещанием, что ровно 90% будущих обращений будут быстрее: это описание этой выборки.
        """),
        code("""
        fig, ax = plt.subplots()
        ax.hist(waits, bins=15, color="#277DA1", edgecolor="white")
        ax.axvline(waits.mean(), color="#F94144", label=f"Среднее {waits.mean():.1f}")
        ax.axvline(waits.median(), color="#43AA8B", linestyle="--", label=f"Медиана {waits.median():.1f}")
        ax.set(xlabel="Ожидание первого ответа, минуты", ylabel="Число обращений",
               title="Синтетическая поддержка: распределение ожидания")
        ax.legend()
        plt.tight_layout()
        plt.show()
        """),
        md("""## 6. Переходим от общего среднего к группам

        Сравним каналы по одинаковым метрикам. Число обращений `n` обязательно:
        одинаковое среднее при 3 и 300 наблюдениях имеет разную устойчивость.
        Пока это описательное сравнение. Каналы могут отличаться типом задач и нагрузкой.
        """),
        code("""
        by_channel = tickets.groupby("channel").agg(
            n=("ticket_id", "size"), mean_wait=("wait_minutes", "mean"),
            median_wait=("wait_minutes", "median"), p90_wait=("wait_minutes", lambda s: s.quantile(0.9)))
        display(by_channel.round(2))
        assert by_channel["n"].sum() == len(tickets)
        ax = by_channel["median_wait"].sort_values().plot.barh(color="#277DA1")
        ax.set(xlabel="Медиана ожидания, минуты", ylabel="Канал", title="Сравнение каналов в учебном наборе")
        plt.tight_layout()
        plt.show()
        """),
        md("""## 7. Избегаем ошибки среднего от средних

        Если группы разного размера, общий показатель нужно взвесить по числу обращений.
        Простое среднее трёх средних отвечает на вопрос о «среднем канале»,
        а взвешенное — о «среднем обращении».
        """),
        code("""
        unweighted = by_channel["mean_wait"].mean()
        weighted = np.average(by_channel["mean_wait"], weights=by_channel["n"])
        print(f"Среднее средних: {unweighted:.2f} мин")
        print(f"Взвешенное среднее: {weighted:.2f} мин")
        assert np.isclose(weighted, waits.mean())
        """),
        md("""## 8. Переводим идеи в правильные типы задач

        | Вопрос | Тип задачи | Что требуется |
        |---|---|---|
        | Сколько ждали в январе? | Описательная аналитика | Исторические обращения |
        | Сколько будет ждать новое обращение? | Регрессия | Признаки, известные при поступлении |
        | Какую категорию назначить тексту? | Классификация | Тексты и проверенные метки |
        | Какие группы обращений похожи? | Кластеризация | Признаки и критерий полезности групп |
        | Сформировать ответ сотруднику | Генеративная AI-система | Контекст, проверка ответа и правила использования |

        Пока мы реализовали первую строку. Доступность данных, смысл метрики и цена ошибки
        важнее выбора звучного названия алгоритма.
        """),
        code("""
        # Проверяем простое правило сервиса: доля обращений с ожиданием более 20 минут.
        # Порог 20 выбран как учебное условие, а не как найденный отраслевой стандарт.
        threshold = 20.0
        tickets = tickets.assign(long_wait=tickets["wait_minutes"] > threshold)
        long_wait_share = tickets["long_wait"].mean()
        print(f"Дольше {threshold:.0f} минут: {tickets['long_wait'].sum()} из {len(tickets)} ({long_wait_share:.1%})")
        assert 0 <= long_wait_share <= 1
        """),
        md("""## 9. Простейшая контрольная точка перед будущим ML

        Предположим, прогноз нужен для более поздних обращений. Первые 100 строк используем
        как историю, последние 50 — как будущую проверку. Постоянный прогноз равен медиане истории.
        Это baseline: ориентир, с которым позже сравним обучаемые модели.
        Медиана и ошибка не должны вычисляться по одним и тем же наблюдениям.
        Здесь нет обещания качества: 50 синтетических обращений — только демонстрация процедуры.
        """),
        code("""
        history = tickets.iloc[:100].copy()
        future = tickets.iloc[100:].copy()
        baseline = history["wait_minutes"].median()
        errors = (future["wait_minutes"] - baseline).abs()
        print(f"Постоянный прогноз: {baseline:.2f} мин; MAE на следующих 50 обращениях: {errors.mean():.2f} мин")
        assert history["created_date"].max() < future["created_date"].min()
        assert set(history["ticket_id"]).isdisjoint(future["ticket_id"])
        """),
        md("""## 10. Воспроизводимость: данные, код и окружение

        Seed задаёт последовательность псевдослучайных чисел, но не заменяет версии библиотек,
        исходный файл и порядок запуска ячеек. Хеш файла помогает обнаружить случайное изменение данных.
        Он не доказывает, что сами данные правильные.
        """),
        code("""
        sample_a = np.random.default_rng(SEED).choice(tickets["ticket_id"], size=5, replace=False)
        sample_b = np.random.default_rng(SEED).choice(tickets["ticket_id"], size=5, replace=False)
        assert np.array_equal(sample_a, sample_b)
        run_manifest = {"dataset": data_path.name, "sha256": hashlib.sha256(data_path.read_bytes()).hexdigest(),
                        "rows": len(tickets), "seed": SEED, "python": sys.version.split()[0],
                        "numpy": np.__version__, "pandas": pd.__version__}
        print(json.dumps(run_manifest, ensure_ascii=False, indent=2))
        """),
        md("""## 11. Git, Colab и карьерные роли

        Git хранит историю изменений файлов. Notebook хранит и код, и выводы, поэтому перед коммитом
        проверьте, что в нём нет токенов, персональных данных или случайных огромных результатов.
        Локально можно выполнить `git status`, затем добавить **конкретный свой файл** и создать commit.
        Репозиторий курса приватный: для Colab потребуется авторизация доступа к GitHub либо загрузка
        полного архива. Один ipynb без соседней папки `datasets` работать не обязан.

        Аналитик объясняет наблюдения; Data Scientist ставит и проверяет модели; ML Engineer организует
        обучение и применение; AI Engineer строит систему вокруг моделей. В небольшой команде роли пересекаются.
        После этого практикума напишите, какие действия вы уже смогли сделать самостоятельно.
        """),
        code("""
        # Итоговый отчёт использует вычисленные значения, а не числа, набранные вручную.
        print(f"Изучено {len(tickets)} синтетических обращений.")
        print(f"Медиана ожидания: {waits.median():.1f} мин; 90-й процентиль: {waits.quantile(0.9):.1f} мин.")
        print(f"Доля долгих ожиданий по учебному порогу: {long_wait_share:.1%}.")
        print("Ограничение: каналы не распределялись случайно, поэтому различие не является причинным эффектом.")
        """),
        md("""## Вопросы для обсуждения

        1. Почему `resolution_minutes` может стать утечкой при прогнозе в момент поступления?
        2. Какие два дополнительных поля помогли бы понять причины долгого ожидания?
        3. Почему вывод «добавим чат — время ожидания обязательно снизится» не следует из графика?
        4. Что нужно сохранить, чтобы одногруппник повторил расчёт через месяц?

        Теперь переходите к [Homework Week 01](../homework/Homework_Week_01.md).
        """), sources_cell(sources)]
    save_notebook(folder / "practice" / "01_reproducible_data_analysis.ipynb", cells, 1)
    tasks = [
        {"title": "Паспорт задачи", "points": 15, "description": "Сформулируйте один описательный и один прогнозный вопрос для поддержки. Для прогнозного укажите пользователя результата, момент прогноза, цель, 3 допустимых признака и один недопустимый будущий признак. Не обучайте модель.", "starter": "# TODO: заполните паспорт собственными формулировками.\nproblem_card = None\nif problem_card is not None:\n    display(problem_card)"},
        {"title": "Контракт исходных данных", "points": 20, "description": "Проверьте число строк, уникальность ticket_id, диапазон satisfaction, пропуски и допустимые каналы. Добавьте минимум 4 понятных assert и объясните, какую ошибку ловит каждый.", "starter": "# TODO: вычислите проверки, затем добавьте собственные assert.\ndata_contract = None\nif data_contract is not None:\n    display(data_contract)"},
        {"title": "Описание длительности решения", "points": 25, "description": "Для resolution_minutes вычислите n, среднее, медиану, p75, p90, минимум и максимум. Сделайте группировку по category с n и медианой. Сверьте общее среднее со взвешенным средним групп.", "starter": "# TODO: используйте resolution_minutes, а не разобранный wait_minutes.\nresolution_summary = None\ncategory_summary = None\nif resolution_summary is not None:\n    display(resolution_summary)"},
        {"title": "Один график — один вопрос", "points": 20, "description": "Постройте гистограмму длительности решения с медианой и график медиан по категориям. Укажите единицы и источник; сформулируйте два численных наблюдения без причинных утверждений.", "starter": "# TODO: создайте два графика и сохраните ссылки на Figure в список.\nfigures = []\nprint('Графиков создано:', len(figures))"},
        {"title": "Воспроизводимость и вывод", "points": 20, "description": "Выберите 6 обращений с собственным фиксированным seed; покажите, что повторный выбор совпадает. Сформируйте manifest с seed, версиями и SHA-256 CSV. Напишите 100–150 слов: вывод, ограничение, следующий сбор данных.", "starter": "# TODO: создайте свой manifest; итоговый текст разместите в Markdown ниже.\nmanifest = None\nif manifest is not None:\n    display(manifest)"},
    ]
    make_homework(1, 'tickets = pd.read_csv(DATA_DIR / "support_tickets.csv", parse_dates=["created_date"])\ndisplay(tickets.head())', tasks, "2–3", "- `describe` можно дополнить `quantile`; единицы не исчезают при усреднении.\n- Взвешенное среднее использует размеры групп, а не число категорий.\n- Для повторения выборки создайте новый генератор с тем же seed.", "- CSV остался исходным; путь относительный.\n- Run All выполняется в чистом kernel.\n- Во всех групповых таблицах есть n; в выводах нет обобщения на реальные компании.")
    week_readme(1, "01_reproducible_data_analysis.ipynb", "- Различить описательную, прогнозную и генеративную задачу.\n- Определить единицу наблюдения, признаки и момент прогноза.\n- Проверить CSV, вычислить описательные метрики и построить два графика.\n- Сохранить воспроизводимый notebook и объяснить назначение Git.", "- Уверенно открывать файлы и пользоваться браузером.\n- Предварительное программирование не требуется: первая лабораторная проходит с преподавателем.", "**Занятие 1:** разделы 1–8: постановка задачи, таблица, описательная аналитика.\n\n**Занятие 2:** повторный запуск, разделы 9–11, manifest, Git/Colab и самостоятельный вывод.", sources)


def build_week_02():
    folder = ROOT / PLAN[1]["folder"]
    rnd = random.Random(202)
    rows = []
    for day in range(1, 61):
        temp = round(7 + 9 * math.sin(day / 10) + rnd.gauss(0, 2), 1)
        rows.append({"day": day, "heating_kwh": round(max(1, 80 - 3 * temp + rnd.gauss(0, 7)), 2),
                     "cooling_kwh": round(max(0, 1.3 * (temp - 10) + rnd.gauss(3, 2)), 2),
                     "lighting_kwh": round(rnd.uniform(15, 25), 2),
                     "equipment_kwh": round(rnd.uniform(30, 60), 2), "temperature_c": temp})
    save_csv(folder / "datasets" / "daily_energy.csv", rows)
    dataset_readme(2, """Seed: `202`. `daily_energy.csv`: **60 строк, 6 полей**, один день учебного здания.

| Поле | Тип / единицы | Смысл |
|---|---|---|
| day | int, 1–60 | Номер дня, не календарная дата |
| heating_kwh | float, кВт·ч | Потребление отопления |
| cooling_kwh | float, кВт·ч | Потребление охлаждения |
| lighting_kwh | float, кВт·ч | Потребление освещения |
| equipment_kwh | float, кВт·ч | Потребление оборудования |
| temperature_c | float, °C | Наружная температура |

Пропуски отсутствуют. Потребление неотрицательное, порядок дней фиксирован.
Тариф в notebook — вымышленное условие упражнения, не официальный тариф электроэнергии.""")
    sources = [("Python: структуры данных", "https://docs.python.org/3/tutorial/datastructures.html"),
               ("NumPy: руководство для начинающих", "https://numpy.org/doc/stable/user/absolute_beginners.html"),
               ("NumPy: broadcasting", "https://numpy.org/doc/stable/user/basics.broadcasting.html")]
    cells = [md("""# Неделя 02. Python и NumPy на данных энергопотребления

        **Кейс:** сравнить потребление четырёх систем здания за 60 дней, рассчитать стоимость
        и проверить, что векторизованная реализация совпадает с понятным циклом.
        Данные и тарифы синтетические. Здесь важны единицы, форма массивов и правильность расчёта.
        """), setup(2, "import csv\nfrom time import perf_counter"),
        md("""## 1. Список словарей: сначала понятные структуры Python

        Список сохраняет порядок элементов; словарь связывает имя поля со значением.
        CSV хранит текст, поэтому значения нужно преобразовать в числа явно.
        Одна запись — один день. `with` закрывает файл даже при исключении.
        """),
        code("""
        with (DATA_DIR / "daily_energy.csv").open(encoding="utf-8", newline="") as handle:
            raw_records = list(csv.DictReader(handle))
        records = [{key: float(value) for key, value in row.items()} for row in raw_records]
        for record in records:
            record["day"] = int(record["day"])
        display(records[:3])
        assert len(records) == 60
        """),
        md("""## 2. Функция превращает правило в проверяемый объект

        Стоимость равна потреблению, умноженному на тариф. Отрицательное потребление для этого
        упражнения не допускается. Вместо молчаливого исправления входа функция сообщает ошибку.
        Docstring объясняет входы и возвращаемое значение.
        """),
        code("""
        def energy_cost(kwh, tariff=25.0):
            "Стоимость в KZT для неотрицательных kWh и тарифа KZT/kWh."
            if kwh < 0 or tariff < 0:
                raise ValueError("Потребление и тариф должны быть неотрицательными")
            return kwh * tariff

        assert energy_cost(10, 20) == 200
        assert energy_cost(0) == 0
        rejected = False
        try:
            energy_cost(-1)
        except ValueError:
            rejected = True
        assert rejected, "Недопустимое отрицательное потребление должно отклоняться"
        print("Проверены обычный случай, ноль и недопустимый вход.")
        """),
        md("""## 3. Цикл, comprehension и множества

        Сначала явно суммируем четыре системы. Comprehension удобен для короткого преобразования;
        сложные ветвления лучше оставить в функции. Множество хранит уникальные элементы,
        поэтому подходит для проверки, что номера дней не повторяются.
        """),
        code("""
        systems = ["heating_kwh", "cooling_kwh", "lighting_kwh", "equipment_kwh"]
        daily_totals_loop = []
        for row in records:
            total = 0.0
            for system in systems:
                total += row[system]
            daily_totals_loop.append(total)

        daily_totals_comp = [sum(row[name] for name in systems) for row in records]
        cold_days = [row["day"] for row in records if row["temperature_c"] < 0]
        unique_days = {row["day"] for row in records}
        # float-суммирование может отличаться на округление; сравниваем с малым допуском.
        assert np.allclose(daily_totals_loop, daily_totals_comp, rtol=1e-12, atol=1e-12)
        assert len(unique_days) == len(records)
        print("Дни ниже 0 °C:", cold_days)
        """),
        md(r"""## 4. Матрица: строки — дни, столбцы — системы

        $X\in\mathbb{R}^{60\times4}$: $X_{ij}$ — энергия системы $j$ в день $i$.
        `shape` показывает размеры, `dtype` — тип каждого элемента.
        В отличие от вложенных списков, NumPy позволяет применять операции ко всему массиву.
        """),
        code("""
        X = np.array([[row[name] for name in systems] for row in records], dtype=np.float64)
        days = np.array([row["day"] for row in records])
        temperature = np.array([row["temperature_c"] for row in records])
        print("Форма X:", X.shape, "| dtype:", X.dtype, "| байт:", X.nbytes)
        display(pd.DataFrame(X[:5], columns=systems))
        assert X.shape == (60, 4)
        assert np.isfinite(X).all() and (X >= 0).all()
        """),
        md("""## 5. Оси и описательная статистика

        `axis=0` сворачивает дни: получаем число для каждой системы.
        `axis=1` сворачивает системы: получаем число для каждого дня.
        Стандартное отклонение с `ddof=1` использует знаменатель n−1;
        для описания всех 60 наблюдений можно явно выбрать `ddof=0`. Не смешивайте соглашения.
        """),
        code("""
        daily_totals = X.sum(axis=1)
        system_totals = X.sum(axis=0)
        summary = pd.DataFrame({"mean_kwh": X.mean(axis=0), "median_kwh": np.median(X, axis=0),
                                "sample_std_kwh": X.std(axis=0, ddof=1),
                                "p90_kwh": np.quantile(X, 0.9, axis=0),
                                "total_kwh": system_totals}, index=systems)
        display(summary.round(2))
        assert np.allclose(daily_totals, daily_totals_loop)
        assert np.isclose(daily_totals.sum(), system_totals.sum())
        """),
        md("""## 6. Срезы, маски и копии

        Маска — массив True/False, по которому выбираются строки. Базовый срез часто является
        представлением исходной памяти: изменение среза может изменить исходный массив.
        Для независимого эксперимента используйте `.copy()`.
        """),
        code("""
        warm_mask = temperature > 12
        print("Тёплых дней:", warm_mask.sum())
        print("Среднее потребление в тёплые дни:", X[warm_mask].sum(axis=1).mean().round(2))

        demo = np.array([10.0, 20.0, 30.0])
        view = demo[:2]
        view[0] = 99.0
        assert demo[0] == 99.0
        independent = demo[:2].copy()
        independent[0] = -1.0
        assert demo[0] == 99.0
        print("Срез изменил исходник; копия — нет.")
        """),
        md(r"""## 7. Broadcasting: сравниваем формы до вычисления

        Пусть тарифы $t\in\mathbb{R}^{4}$. Произведение `X * t` имеет форму `(60, 4)`:
        NumPy сопоставляет последние размеры, равные либо друг другу, либо 1.
        А `X @ t` даёт вектор из 60 стоимостей: $c_i=\sum_j X_{ij}t_j$.
        Тарифы ниже намеренно различаются как упражнение, а не описание платёжной политики.
        """),
        code("""
        tariffs = np.array([24.0, 28.0, 22.0, 26.0])  # KZT / kWh, учебное условие
        costs_by_system = X * tariffs
        daily_cost = X @ tariffs
        assert costs_by_system.shape == X.shape
        assert daily_cost.shape == (len(X),)
        assert np.allclose(daily_cost, costs_by_system.sum(axis=1))
        print("Стоимость за 60 дней:", round(daily_cost.sum(), 2), "KZT")
        """),
        md(r"""## 8. Стандартизация как упражнение с broadcasting

        $z_{ij}=(x_{ij}-\mu_j)/\sigma_j$. Средние и стандартные отклонения имеют форму `(4,)`.
        Если столбец постоянный, деление на ноль нельзя игнорировать: заменим его масштаб на 1.
        **Пока это описание данного набора.** Для ML параметры позже будем вычислять только на train.
        """),
        code("""
        mean = X.mean(axis=0)
        std = X.std(axis=0, ddof=0)
        safe_std = np.where(std == 0, 1.0, std)
        Z = (X - mean) / safe_std
        assert np.allclose(Z.mean(axis=0), 0, atol=1e-12)
        nonconstant = std > 0
        assert np.allclose(Z[:, nonconstant].std(axis=0), 1)
        reconstructed = Z * safe_std + mean
        assert np.allclose(reconstructed, X)
        print("Стандартизация и обратное преобразование проверены.")
        """),
        md("""## 9. Графики отвечают на разные вопросы

        Линия показывает изменения по порядку дней; scatter показывает связь температуры
        с энергией отопления. Связь специально встроена в генератор. По этому примеру
        нельзя оценивать экономию реального здания.
        """),
        code("""
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        axes[0].plot(days, daily_totals, color="#277DA1", label="Всего")
        axes[0].set(xlabel="День", ylabel="Энергия, кВт·ч", title="Потребление за 60 дней")
        axes[0].legend()
        axes[1].scatter(temperature, X[:, 0], alpha=0.75, color="#F8961E")
        axes[1].set(xlabel="Температура, °C", ylabel="Отопление, кВт·ч", title="Учебная связь температуры и отопления")
        plt.tight_layout()
        plt.show()
        """),
        md("""## 10. Сравниваем реализации, затем измеряем время

        Правильный ответ важнее скорости. Используем небольшой воспроизводимый массив,
        сравниваем цикл и матричную операцию на одинаковом входе. Одно измерение времени
        зависит от нагрузки машины и не является строгим benchmark; поэтому скорость не проверяется assert.
        """),
        code("""
        benchmark_X = np.random.default_rng(SEED).uniform(0, 100, size=(20000, 4))

        start = perf_counter()
        loop_cost = np.array([sum(value * tariff for value, tariff in zip(row, tariffs))
                              for row in benchmark_X])
        loop_seconds = perf_counter() - start
        start = perf_counter()
        vector_cost = benchmark_X @ tariffs
        vector_seconds = perf_counter() - start
        assert np.allclose(loop_cost, vector_cost)
        display(pd.DataFrame({"implementation": ["Python loop", "NumPy @"],
                              "elapsed_seconds": [loop_seconds, vector_seconds]}))
        """),
        md("""## 11. Мини-кейс: бюджет и сценарий экономии

        Предположим, только освещение потребляет на 15% меньше, а остальные системы не меняются.
        Сначала копируем массив, затем считаем стоимость тем же тарифом. Это сценарный расчёт
        при заданном допущении, а не прогноз реального эффекта мероприятия.
        """),
        code("""
        scenario = X.copy()
        scenario[:, 2] *= 0.85
        scenario_cost = scenario @ tariffs
        saving = daily_cost.sum() - scenario_cost.sum()
        analytical_saving = X[:, 2].sum() * tariffs[2] * 0.15
        assert np.isclose(saving, analytical_saving)
        assert np.array_equal(X[:, [0, 1, 3]], scenario[:, [0, 1, 3]])
        print(f"Экономия в учебном сценарии: {saving:,.2f} KZT ({saving / daily_cost.sum():.1%} бюджета).")
        """),
        md("""## Обсуждение и перенос навыка

        - Почему `X.mean(axis=0)` имеет 4 числа, а `X.mean(axis=1)` — 60?
        - Какая форма нужна тарифу по дням: `(60,)` или `(60, 1)`, чтобы умножить каждый день отдельно?
        - Почему скорость исполнения не должна заменять проверку размерностей и единиц?
        - Что изменится в стандартизации, если завтра появятся новые наблюдения?

        Домашняя работа: [Homework Week 02](../homework/Homework_Week_02.md).
        """), sources_cell(sources)]
    save_notebook(folder / "practice" / "01_python_numpy_energy.ipynb", cells, 2)
    tasks = [
        {"title": "Функция и структуры Python", "points": 20, "description": "Реализуйте функцию total_energy(record), которая суммирует только 4 энергетических поля. Добавьте docstring, проверку отрицательных значений и три теста: обычный день, нули, недопустимый вход. Не суммируйте day или temperature_c.", "starter": "def total_energy(record):\n    # TODO: реализуйте контракт функции.\n    return None\n\n# TODO: добавьте тесты после реализации.\nfunction_ready = False"},
        {"title": "Оси и фильтрация", "points": 20, "description": "Соберите X размера 60×4, рассчитайте максимум и p75 по каждой системе. Найдите дни, когда суммарная энергия выше 75-го процентиля, и выведите их номера, температуру и потребление.", "starter": "# TODO: соберите массив и таблицу отфильтрованных дней.\nX = None\nhigh_energy_days = None\nif high_energy_days is not None:\n    display(high_energy_days)"},
        {"title": "Broadcasting по дням", "points": 25, "description": "Пусть в дни, кратные 7, тариф для всех систем 30 KZT/kWh, иначе 24. Рассчитайте матрицу стоимости с broadcasting по дням, затем итог. Сверьте с Python-циклом через np.allclose и объясните форму тарифа.", "starter": "# TODO: дневной тариф должен иметь корректную форму для broadcasting.\nday_tariff = None\nvector_cost = None\nloop_cost = None"},
        {"title": "Устойчивая стандартизация", "points": 20, "description": "Напишите функцию standardize_columns(X), возвращающую Z, средние и масштабы; обработайте постоянный столбец. Проверьте обратное преобразование и конечность Z на маленькой матрице с постоянным столбцом.", "starter": "def standardize_columns(values):\n    # TODO: не делите на ноль при постоянном столбце.\n    return None\n\n# TODO: создайте собственные проверки на маленьких данных."},
        {"title": "Сценарий и визуальный вывод", "points": 15, "description": "Рассчитайте сценарий: отопление −10%, оборудование +5%, остальные системы без изменений. Постройте сравнение общей энергии по дням и сообщите, увеличился или снизился бюджет при постоянных тарифах лабораторной. Обозначьте допущения.", "starter": "# TODO: сохраните исходный X и создайте отдельный сценарий.\nscenario_summary = None\nif scenario_summary is not None:\n    display(scenario_summary)"},
    ]
    make_homework(2, 'frame = pd.read_csv(DATA_DIR / "daily_energy.csv")\nrecords = frame.to_dict("records")\nsystems = ["heating_kwh", "cooling_kwh", "lighting_kwh", "equipment_kwh"]\ndisplay(frame.head())', tasks, "3–4", "- Разделите выбор энергетических столбцов и вычисление суммы.\n- Для тарифа по строкам полезен `reshape(-1, 1)`.\n- Изменение сценария выполняйте на `.copy()`.\n- Тест должен проверять независимое ожидаемое значение или свойство, не повторять ту же формулу второй раз.", "- У всех массивов проверены формы.\n- Цикл и векторизованная версия совпадают.\n- Есть тест постоянного столбца и ошибочного входа.\n- В выводе приведены KZT и кВт·ч, а не просто числа.")
    week_readme(2, "01_python_numpy_energy.ipynb", "- Использовать списки, словари, множества, функции и comprehension.\n- Читать shape, dtype и оси матрицы NumPy.\n- Реализовать маски, broadcasting, стандартизацию и сценарный расчёт.\n- Проверять векторизацию через независимый цикл и простые граничные случаи.", "- Пройти неделю 01; уметь запускать Code/Markdown-ячейки.\n- Знать сумму, среднее и смысл процентов.", "**Занятие 1:** разделы 1–4, Python-функция, структуры и контракт входов.\n\n**Занятие 2:** разделы 5–11, NumPy, broadcasting, проверка скорости и сценарий.", sources)


def build_week_03():
    folder = ROOT / PLAN[2]["folder"]
    rnd = random.Random(303)
    customers = [{"customer_id": i, "city": rnd.choice(["Atyrau", "Astana", "Aktau"]),
                  "segment": rnd.choice(["individual", "small_business"])} for i in range(1, 41)]
    folder.joinpath("datasets").mkdir(parents=True, exist_ok=True)
    (folder / "datasets" / "customers.json").write_text(json.dumps(customers, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    rows = []
    prices = {"keyboard": 14000, "mouse": 6500, "headset": 18000, "webcam": 23000}
    for i in range(180):
        product = rnd.choice(list(prices))
        status = rnd.choices(["completed", "processing", "cancelled"], weights=[8, 1, 1])[0]
        rows.append({"order_id": 1001 + i, "customer_id": 999 if i == 37 else rnd.randint(1, 38),
                     "ordered_at": str(dt.date(2026, 2, 1) + dt.timedelta(days=i // 6)),
                     "product": product, "unit_price_kzt": prices[product], "quantity": rnd.randint(1, 4),
                     "status": status, "shipping_days": rnd.randint(1, 7) if status == "completed" else ""})
    rows.extend([dict(rows[11]), dict(rows[75])])
    save_csv(folder / "datasets" / "orders.csv", rows)
    dataset_readme(3, """Seed: `303`. `orders.csv`: **182 строки**, из них **180 уникальных заказов + 2 точных дубля**.
`customers.json`: **40 клиентов**, JSON-массив объектов.

| Файл / поле | Тип / единицы | Смысл |
|---|---|---|
| orders.order_id | int | Ключ заказа; два полных дубля добавлены намеренно |
| orders.customer_id | int | Ссылка на клиента; ID 999 отсутствует в справочнике намеренно |
| orders.ordered_at | ISO-дата | Дата заказа |
| orders.product | category | keyboard / mouse / headset / webcam |
| orders.unit_price_kzt | int, KZT | Зафиксированная цена одной единицы в заказе |
| orders.quantity | int, 1–4 | Количество единиц |
| orders.status | category | completed / processing / cancelled |
| orders.shipping_days | float, дни / missing | Длительность доставки для completed; иначе неизвестна |
| customers.customer_id | int | Уникальный ключ справочника |
| customers.city | category | Atyrau / Astana / Aktau — вымышленные клиенты |
| customers.segment | category | individual / small_business |

Учебное определение выручки: `quantity × unit_price_kzt` только для `completed`.
Возвраты, скидки, налог и валютная переоценка не моделируются. Нельзя трактовать пропуск
длительности ещё не завершённого заказа как нулевую длительность.""")
    sources = [("pandas: вводные учебники", "https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html"),
               ("pandas: GroupBy", "https://pandas.pydata.org/docs/user_guide/groupby.html"),
               ("pandas: merge и join", "https://pandas.pydata.org/docs/user_guide/merging.html")]
    cells = [md("""# Неделя 03. pandas: от двух файлов к проверенному отчёту

        **Кейс:** интернет-магазин просит отчёт по завершённым заказам и городам.
        CSV содержит заказы, JSON — клиентов. В поставке намеренно есть два точных дубля
        и неизвестный клиент. Сначала проверяем данные, затем считаем деньги.

        **Результат:** воспроизводимая загрузка, фильтрация, `groupby`, безопасный `merge`,
        проверка потерь строк и один компактный аналитический отчёт. Все данные синтетические.
        """), setup(3, "import json\nfrom tempfile import TemporaryDirectory"),
        md("""## 1. Читаем CSV и JSON с явным смыслом типов

        pandas DataFrame — таблица с именами столбцов и индексом строк. Дата не должна оставаться
        произвольной строкой, если нужны календарные вычисления. Идентификатор — ключ,
        даже если хранится целым числом. `shipping_days` имеет пропуски по смыслу процесса.
        """),
        code("""
        raw_orders = pd.read_csv(DATA_DIR / "orders.csv", parse_dates=["ordered_at"])
        with (DATA_DIR / "customers.json").open(encoding="utf-8") as handle:
            customers = pd.DataFrame(json.load(handle))
        display(raw_orders.head())
        display(customers.head())
        print("Orders:", raw_orders.shape, "| Customers:", customers.shape)
        """),
        md("""## 2. Профиль качества до изменений

        `duplicated()` сравнивает все столбцы, а `duplicated('order_id')` — только ключ.
        Это разные вопросы: одинаковый ID с разным количеством нельзя молча удалить как точную копию.
        В нашем CSV повторы полные; сохраняем исходный DataFrame для аудита.
        """),
        code("""
        quality = pd.DataFrame({"dtype": raw_orders.dtypes.astype(str),
                                "missing": raw_orders.isna().sum(), "nunique": raw_orders.nunique()})
        display(quality)
        print("Точных дублей:", raw_orders.duplicated().sum())
        display(raw_orders.loc[raw_orders.duplicated("order_id", keep=False)].sort_values("order_id"))
        orders = raw_orders.drop_duplicates().copy()
        assert len(raw_orders) == 182 and len(orders) == 180
        assert orders["order_id"].is_unique and customers["customer_id"].is_unique
        """),
        md("""## 3. Индекс, loc и iloc

        `iloc` выбирает по позиции, `loc` — по меткам или логической маске.
        Индекс удобен для поиска, но не заменяет проверку уникальности бизнес-ключа.
        При назначении используем `.loc` или `.assign`, без цепочек вида `df[mask][column] = ...`.
        """),
        code("""
        indexed = orders.set_index("order_id", verify_integrity=True)
        display(indexed.loc[[1001, 1002], ["product", "quantity", "status"]])
        display(indexed.iloc[:3, :4])
        selected = orders.loc[(orders["quantity"] >= 3) & (orders["status"] == "completed"),
                              ["order_id", "product", "quantity"]]
        display(selected.head())
        assert selected["quantity"].ge(3).all()
        """),
        md(r"""## 4. Производные величины и границы метрики

        Для заказа $i$: $v_i=q_i p_i$ (количество × цена).
        **Выручкой этого упражнения** считаем сумму $v_i$ только завершённых заказов.
        Для остальных строк выручка равна 0 по нашему определению, но shipping_days остаётся неизвестной.
        Это иллюстрирует, почему разные столбцы требуют разных правил обработки пропусков.
        """),
        code("""
        orders = orders.assign(order_value_kzt=orders["quantity"] * orders["unit_price_kzt"])
        orders["revenue_kzt"] = orders["order_value_kzt"].where(orders["status"].eq("completed"), 0)
        orders["weekday"] = orders["ordered_at"].dt.dayofweek  # 0 = понедельник
        assert orders["quantity"].gt(0).all() and orders["unit_price_kzt"].ge(0).all()
        assert orders.loc[orders["status"].ne("completed"), "revenue_kzt"].eq(0).all()
        display(orders[["order_id", "status", "order_value_kzt", "revenue_kzt", "shipping_days"]].head(8))
        """),
        md("""## 5. Группируем с именованными агрегатами

        `size` считает строки группы, а `count` — непустые значения выбранного столбца.
        Для длительности доставки явно показываем число доступных измерений.
        Средний чек ниже относится только к завершённым заказам, а не ко всем созданным.
        """),
        code("""
        completed = orders.loc[orders["status"].eq("completed")].copy()
        by_product = completed.groupby("product").agg(
            completed_orders=("order_id", "size"), units=("quantity", "sum"),
            revenue_kzt=("revenue_kzt", "sum"), mean_order_kzt=("revenue_kzt", "mean"),
            shipping_observations=("shipping_days", "count"), median_shipping=("shipping_days", "median"))
        display(by_product.round(2))
        assert by_product["revenue_kzt"].sum() == completed["revenue_kzt"].sum()
        display(orders.groupby("status").agg(rows=("order_id", "size"), known_shipping=("shipping_days", "count")))
        """),
        md("""## 6. Объединение many-to-one: одна строка заказа — один клиент

        `validate='many_to_one'` требует уникальность ключа справа.
        `indicator=True` показывает, какие строки не нашли пару.
        LEFT JOIN сохраняет все заказы, поэтому неизвестного клиента можно заметить и разобрать.
        INNER JOIN удалил бы его молча, если не сравнить число строк и сумму выручки.
        """),
        code("""
        merged = orders.merge(customers, on="customer_id", how="left",
                              validate="many_to_one", indicator=True)
        assert len(merged) == len(orders)
        assert merged["revenue_kzt"].sum() == orders["revenue_kzt"].sum()
        unmatched = merged.loc[merged["_merge"].eq("left_only"), ["order_id", "customer_id", "revenue_kzt"]]
        display(unmatched)
        assert unmatched["customer_id"].tolist() == [999]
        merged["city_report"] = merged["city"].fillna("UNKNOWN")
        """),
        md("""## 7. Проверка защищает от размножения строк

        Если в справочнике две записи одного клиента, один заказ при join может превратиться в две строки.
        Покажем ошибку на отдельной испорченной копии, не меняя исходный справочник.
        `try/except` здесь нужен, чтобы учебный notebook продолжился после ожидаемой ошибки контракта.
        """),
        code("""
        bad_customers = pd.concat([customers, customers.iloc[[0]]], ignore_index=True)
        blocked = False
        try:
            orders.merge(bad_customers, on="customer_id", how="left", validate="many_to_one")
        except pd.errors.MergeError as exc:
            blocked = True
            print("Ожидаемая защита:", type(exc).__name__)
        assert blocked, "Дублирование ключа справочника должно блокироваться"
        assert customers["customer_id"].is_unique
        """),
        md("""## 8. Описательная аналитика после join

        Отчёт должен сохранить неизвестные значения отдельной группой.
        Для каждого города показываем число заказов, завершённые заказы и выручку.
        Доля завершений имеет знаменатель «все созданные заказы города», а средний чек —
        «только завершённые заказы». Эти знаменатели нельзя подменять друг другом.
        """),
        code("""
        merged["is_completed"] = merged["status"].eq("completed")
        by_city = merged.groupby("city_report").agg(
            all_orders=("order_id", "size"), completed_orders=("is_completed", "sum"),
            completion_rate=("is_completed", "mean"), revenue_kzt=("revenue_kzt", "sum"))
        by_city["mean_completed_order_kzt"] = by_city["revenue_kzt"].div(by_city["completed_orders"].replace(0, np.nan))
        display(by_city.round(2))
        assert by_city["all_orders"].sum() == len(orders)
        assert by_city["revenue_kzt"].sum() == completed["revenue_kzt"].sum()
        """),
        md("""## 9. Сводная таблица и временная агрегация

        `pivot_table` строит двумерную сводку. `resample` агрегирует даты по календарной частоте.
        Нулевую выручку в дне без завершённых заказов здесь можно указать явно,
        поскольку файл покрывает весь заданный период. Для неполной выгрузки ноль мог бы вводить в заблуждение.
        """),
        code("""
        city_product = merged.pivot_table(index="city_report", columns="product", values="revenue_kzt",
                                          aggfunc="sum", fill_value=0)
        daily = orders.set_index("ordered_at")["revenue_kzt"].resample("D").sum()
        display(city_product)
        assert city_product.to_numpy().sum() == orders["revenue_kzt"].sum()
        assert daily.sum() == orders["revenue_kzt"].sum()
        """),
        md("""## 10. Графики: значение, единица и подпись ограничения

        Сравнение выручки не является рейтингом эффективности: группы могут отличаться размером.
        Поэтому рядом с денежным показателем в отчёте оставляем число заказов.
        Линия по дням — описание 30 синтетических дней, не оценка сезонности.
        """),
        code("""
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        (by_city["revenue_kzt"].sort_values() / 1000).plot.barh(ax=axes[0], color="#277DA1")
        axes[0].set(xlabel="Выручка, тыс. KZT", ylabel="Город", title="Только завершённые заказы")
        (daily / 1000).plot(ax=axes[1], color="#43AA8B", marker=".")
        axes[1].set(xlabel="Дата", ylabel="Выручка, тыс. KZT", title="Синтетическая динамика")
        plt.tight_layout()
        plt.show()
        """),
        md("""## 11. Экспорт и round-trip проверка

        CSV не хранит все типы pandas, поэтому после повторного чтения проверяем значения и ключи.
        Используем временную папку, чтобы лабораторная не перезаписывала исходные данные.
        Такой тест ловит случайное сохранение индекса как лишнего столбца или потерю строк.
        """),
        code("""
        export = by_city.reset_index()
        with TemporaryDirectory() as temp_dir:
            report_path = Path(temp_dir) / "city_report.csv"
            export.to_csv(report_path, index=False, encoding="utf-8")
            restored = pd.read_csv(report_path)
        assert restored.columns.tolist() == export.columns.tolist()
        assert restored["city_report"].tolist() == export["city_report"].tolist()
        assert np.allclose(restored["revenue_kzt"], export["revenue_kzt"])
        print("CSV round-trip: структура, ключи и выручка сохранены.")
        """),
        md("""## Что должно попасть в финальный вывод

        1. Сколько исходных строк было, сколько точных дублей удалено и почему.
        2. Сколько заказов не нашли клиента и как они отражены в отчёте.
        3. Что в этом упражнении означает «выручка» и какие бизнес-процессы отсутствуют.
        4. Какие суммы независимо сошлись после группировки и join.

        Переходите к [Homework Week 03](../homework/Homework_Week_03.md).
        """), sources_cell(sources)]
    save_notebook(folder / "practice" / "01_pandas_orders_audit.ipynb", cells, 3)
    tasks = [
        {"title": "Проверка поставки", "points": 20, "description": "Составьте таблицу количества строк, точных дублей, повторов order_id, пропусков и допустимых статусов. Удалите только точные дубли в копии. Докажите, что противоречащих записей одного order_id после этого нет.", "starter": "# TODO: исходные raw_orders и customers не меняйте.\naudit = None\norders = None\nif audit is not None:\n    display(audit)"},
        {"title": "Сегменты клиентов", "points": 25, "description": "Выполните LEFT JOIN с validate и indicator. Постройте отчёт по segment: все заказы, completed, completion_rate, units_completed и revenue_kzt. Неизвестный сегмент сохраните отдельно. Сверьте общие итоги до и после join.", "starter": "# TODO: сначала проверьте cardinality, затем агрегируйте.\nsegment_report = None\nif segment_report is not None:\n    display(segment_report)"},
        {"title": "Доставка и неполные наблюдения", "points": 20, "description": "Для завершённых заказов посчитайте медиану и p90 shipping_days по product с числом доступных наблюдений. Объясните, почему нельзя заменить все пропуски shipping_days нулями. Постройте график.", "starter": "# TODO: используйте корректный фильтр и подпишите единицу «дни».\nshipping_report = None\nif shipping_report is not None:\n    display(shipping_report)"},
        {"title": "Сводная и дни недели", "points": 20, "description": "Сделайте pivot_table выручки segment×product и отчёт по weekday с числом календарных дат, заказов и выручкой на день. Объясните, почему сравнение только сумм по дням недели может быть нечестным.", "starter": "# TODO: явно посчитайте число календарных дат в каждой группе.\nsegment_product = None\nweekday_report = None"},
        {"title": "Экспорт и бизнес-вывод", "points": 15, "description": "Сохраните один отчёт в CSV в своей папке, прочитайте его обратно и проверьте схему, ключи и сумму. Напишите 120–180 слов с двумя численными выводами, одним риском качества и одним следующим вопросом.", "starter": "# TODO: экспортируйте свой результат после завершения предыдущих частей.\nexport_verified = False\nprint('Экспорт проверен:', export_verified)"},
    ]
    make_homework(3, 'raw_orders = pd.read_csv(DATA_DIR / "orders.csv", parse_dates=["ordered_at"])\ncustomers = pd.read_json(DATA_DIR / "customers.json")\ndisplay(raw_orders.head())', tasks, "3–4", "- `groupby(..., dropna=False)` либо отдельный UNKNOWN сохраняет неизвестную группу.\n- `size` и `count` могут различаться.\n- Выручка должна использовать completed; количество созданных заказов — все статусы.\n- Число дат можно получить после удаления дублей дат, а не подсчётом строк заказов.", "- Не потерян customer_id 999.\n- Join не увеличил количество уникальных заказов.\n- Выручка сходится по исходнику, группам и pivot.\n- Пустая доставка не стала «мгновенной доставкой».")
    week_readme(3, "01_pandas_orders_audit.ipynb", "- Загрузить CSV и JSON с понятной схемой.\n- Использовать loc, iloc, assign, groupby, pivot_table и даты.\n- Проверить cardinality объединения и объяснить LEFT/INNER JOIN.\n- Сделать описательный отчёт с сохранением неизвестных групп и контрольными суммами.", "- Неделя 02: списки, словари, функции, логические условия, NumPy.\n- Неделя 01: единица наблюдения и среднее/медиана.", "**Занятие 1:** разделы 1–5: чтение, индекс, фильтрация, производные поля и группировки.\n\n**Занятие 2:** разделы 6–11: JSON-справочник, merge, аудит, сводные и экспорт.", sources)


def build_week_04():
    folder = ROOT / PLAN[3]["folder"]
    rnd = random.Random(404)
    customers = [{"customer_id": i, "city": rnd.choice(["Atyrau", "Astana", "Aktau"]),
                  "joined_on": str(dt.date(2025, 11, 1) + dt.timedelta(days=rnd.randint(0, 50)))}
                 for i in range(1, 27)]
    products = [{"product_id": i + 1, "product_name": name, "category": category, "catalog_price_kzt": price}
                for i, (name, category, price) in enumerate([
                    ("Keyboard", "accessories", 14000), ("Mouse", "accessories", 6500),
                    ("Webcam", "video", 23000), ("Headset", "audio", 18000),
                    ("Microphone", "audio", 32000), ("Stand", "accessories", 9000)])]
    orders, items = [], []
    for i in range(1, 181):
        orders.append({"order_id": i, "customer_id": rnd.randint(1, 22),
                       "ordered_on": str(dt.date(2026, 3, 1) + dt.timedelta(days=(i - 1) // 6)),
                       "status": rnd.choices(["paid", "cancelled", "refunded"], [8, 1, 1])[0]})
        for product in rnd.sample(products, rnd.randint(1, 3)):
            items.append({"line_id": len(items) + 1, "order_id": i, "product_id": product["product_id"],
                          "quantity": rnd.randint(1, 4),
                          "unit_price_kzt": product["catalog_price_kzt"] - rnd.choice([0, 0, 500])})
    tables = {"customers": customers, "products": products, "orders": orders, "order_items": items}
    for name, table in tables.items():
        save_csv(folder / "datasets" / f"{name}.csv", table)
    con = sqlite3.connect(":memory:")
    con.executescript("""
        PRAGMA foreign_keys = ON;
        CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, city TEXT NOT NULL, joined_on TEXT NOT NULL);
        CREATE TABLE products(product_id INTEGER PRIMARY KEY, product_name TEXT NOT NULL,
                              category TEXT NOT NULL, catalog_price_kzt INTEGER NOT NULL CHECK(catalog_price_kzt >= 0));
        CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
                            ordered_on TEXT NOT NULL, status TEXT NOT NULL CHECK(status IN ('paid','cancelled','refunded')));
        CREATE TABLE order_items(line_id INTEGER PRIMARY KEY, order_id INTEGER NOT NULL REFERENCES orders(order_id),
                                 product_id INTEGER NOT NULL REFERENCES products(product_id),
                                 quantity INTEGER NOT NULL CHECK(quantity > 0),
                                 unit_price_kzt INTEGER NOT NULL CHECK(unit_price_kzt >= 0));
    """)
    for name, table in tables.items():
        placeholders = ",".join("?" for _ in table[0])
        con.executemany(f"INSERT INTO {name} VALUES ({placeholders})", [tuple(row.values()) for row in table])
    con.commit()
    with sqlite3.connect(folder / "datasets" / "store.sqlite") as target:
        con.backup(target)
    con.close()
    dataset_readme(4, f"""Seed: `404`. Готовая SQLite-база `store.sqlite` плюс CSV-снимки всех таблиц.

| Таблица | Строк | Поля и смысл |
|---|---:|---|
| customers | 26 | customer_id PK; city; joined_on — ISO-дата регистрации |
| products | 6 | product_id PK; product_name; category; catalog_price_kzt — справочная цена |
| orders | 180 | order_id PK; customer_id FK; ordered_on ISO; status paid/cancelled/refunded |
| order_items | {len(items)} | line_id PK; order_id FK; product_id FK; quantity; unit_price_kzt — цена при покупке |

Одна строка `order_items` — позиция заказа, не целый заказ. Клиенты 23–26 намеренно не имеют заказов.
Все внешние ключи корректны; одна покупка может содержать несколько продуктов.
Денежные поля — целые KZT, без налогов, доставки и валютного обмена.
Выручка упражнения = `SUM(quantity * unit_price_kzt)` только для заказов `paid`.
У refunded вся сумма исключается; частичные возвраты не моделируются.
Используйте цену позиции, а не текущую справочную цену `catalog_price_kzt`.
В лабораторной база открывается read-only; ваши эксперименты не меняют исходник.""")
    sources = [("SQLite: SELECT", "https://www.sqlite.org/lang_select.html"),
               ("Python: sqlite3 и параметры запросов", "https://docs.python.org/3/library/sqlite3.html"),
               ("pandas: сравнение с SQL", "https://pandas.pydata.org/docs/getting_started/comparison/comparison_with_sql.html")]
    cells = [md("""# Неделя 04. SQL: запросы, группировки и корректные JOIN

        **Кейс:** финансовый аналитик должен получить выручку магазина и клиентов без заказов.
        В отличие от плоской таблицы недели 03, здесь нормализованная SQLite-база из четырёх таблиц.
        Учимся отличать заказ от позиции, выбирать правильный ключ и сверять суммы независимым способом.
        Данные синтетические; SQL выполняется локально без сервера.
        """), setup(4, "import sqlite3"),
        md("""## 1. Открываем базу только для чтения и изучаем схему

        `customers → orders → order_items ← products` — связи по ключам.
        Один клиент имеет много заказов; один заказ — много позиций.
        При любом JOIN заранее спрашиваем, сколько строк должно получиться.
        CSV рядом с базой позволяет проверить результат независимо от SQL.
        """),
        code("""
        db_path = DATA_DIR / "store.sqlite"
        connection = sqlite3.connect(db_path.resolve().as_uri() + "?mode=ro", uri=True)

        def query(sql, params=None):
            "Выполнить SELECT и вернуть DataFrame; данные передаются параметрами."
            return pd.read_sql_query(sql, connection, params=params)

        display(query("SELECT name, sql FROM sqlite_master WHERE type = 'table' ORDER BY name"))
        print("SQLite:", sqlite3.sqlite_version)
        assert connection.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
        assert connection.execute("PRAGMA foreign_key_check").fetchall() == []
        """),
        md("""## 2. SELECT, WHERE, ORDER BY, LIMIT

        SQL описывает, какие данные нужны. Без `ORDER BY` порядок результата не гарантирован.
        Сначала выберем нужные столбцы и статус, затем явно упорядочим по дате и ID.
        Второй ключ делает порядок однозначным при совпадении дат.
        """),
        code("""
        paid_preview = query('''
            SELECT order_id, customer_id, ordered_on, status
            FROM orders
            WHERE status = 'paid'
            ORDER BY ordered_on, order_id
            LIMIT 8
        ''')
        display(paid_preview)
        assert paid_preview["status"].eq("paid").all()
        """),
        md("""## 3. Агрегация и GROUP BY

        `GROUP BY` сворачивает строки: на каждый статус остаётся одна строка.
        `COUNT(*)` считает строки; `MIN/MAX` показывают границы дат.
        В SQLite можно написать неоднозначный неагрегированный столбец; в учебном SQL
        придерживаемся переносимого правила: каждый выбранный столбец либо в GROUP BY, либо агрегирован.
        """),
        code("""
        status_summary = query('''
            SELECT status, COUNT(*) AS orders_n,
                   MIN(ordered_on) AS first_day, MAX(ordered_on) AS last_day
            FROM orders
            GROUP BY status
            ORDER BY orders_n DESC, status
        ''')
        display(status_summary)
        assert status_summary["orders_n"].sum() == 180
        """),
        md("""## 4. WHERE фильтрует строки; HAVING — результат группировки

        Найдём клиентов с минимум 5 оплаченными заказами. Сначала WHERE убирает неоплаченные,
        затем GROUP BY считает, а HAVING оставляет группы по агрегату.
        Порог 5 — учебное бизнес-условие, не статистическое правило.
        """),
        code("""
        repeat_customers = query('''
            SELECT customer_id, COUNT(*) AS paid_orders
            FROM orders
            WHERE status = 'paid'
            GROUP BY customer_id
            HAVING COUNT(*) >= 5
            ORDER BY paid_orders DESC, customer_id
        ''')
        display(repeat_customers)
        assert repeat_customers["paid_orders"].ge(5).all()
        """),
        md("""## 5. JOIN меняет единицу строки

        После соединения orders с order_items строкой становится позиция заказа.
        Поэтому `COUNT(*)` считает позиции, а `COUNT(DISTINCT order_id)` — заказы.
        Для суммы используем цену, зафиксированную при покупке: цена справочника могла измениться.
        """),
        code("""
        line_preview = query('''
            SELECT o.order_id, i.line_id, p.product_name, i.quantity,
                   i.unit_price_kzt, i.quantity * i.unit_price_kzt AS line_value_kzt
            FROM orders AS o
            JOIN order_items AS i ON i.order_id = o.order_id
            JOIN products AS p ON p.product_id = i.product_id
            WHERE o.status = 'paid'
            ORDER BY o.order_id, i.line_id
            LIMIT 10
        ''')
        display(line_preview)
        counts = query('''
            SELECT COUNT(*) AS paid_lines, COUNT(DISTINCT o.order_id) AS paid_orders
            FROM orders AS o JOIN order_items AS i ON i.order_id = o.order_id
            WHERE o.status = 'paid'
        ''')
        display(counts)
        assert counts.loc[0, "paid_lines"] >= counts.loc[0, "paid_orders"]
        """),
        md(r"""## 6. Выручка и средний чек

        Выручка $R=\sum_{i\in\text{paid lines}}q_i p_i$.
        Средний чек $A=R/N_{\text{paid orders}}$, не $R/N_{\text{lines}}$.
        `1.0 *` обеспечивает вещественное деление. Сравним города с числом клиентов и заказов.
        """),
        code("""
        city_revenue = query('''
            SELECT c.city, COUNT(DISTINCT o.order_id) AS paid_orders,
                   COUNT(DISTINCT o.customer_id) AS paying_customers,
                   SUM(i.quantity * i.unit_price_kzt) AS revenue_kzt,
                   1.0 * SUM(i.quantity * i.unit_price_kzt) / COUNT(DISTINCT o.order_id) AS mean_order_kzt
            FROM customers AS c
            JOIN orders AS o ON o.customer_id = c.customer_id
            JOIN order_items AS i ON i.order_id = o.order_id
            WHERE o.status = 'paid'
            GROUP BY c.city
            ORDER BY revenue_kzt DESC, c.city
        ''')
        display(city_revenue.round(2))
        """),
        md("""## 7. LEFT JOIN и клиенты без заказов

        LEFT JOIN сохраняет левую таблицу. Для отсутствующей пары поля справа становятся NULL.
        Используем `IS NULL`, а не `= NULL`. Если после LEFT JOIN поставить в WHERE условие
        на правую таблицу, строки без пары часто исчезают. Условие «только paid» следует
        помещать в ON, если нам нужны и клиенты с нулём оплат.
        """),
        code("""
        no_orders = query('''
            SELECT c.customer_id, c.city
            FROM customers AS c
            LEFT JOIN orders AS o ON o.customer_id = c.customer_id
            WHERE o.order_id IS NULL
            ORDER BY c.customer_id
        ''')
        display(no_orders)
        assert set(no_orders["customer_id"]) == {23, 24, 25, 26}
        all_customers = query('''
            SELECT c.customer_id, COUNT(o.order_id) AS paid_orders
            FROM customers AS c
            LEFT JOIN orders AS o ON o.customer_id = c.customer_id AND o.status = 'paid'
            GROUP BY c.customer_id
            ORDER BY c.customer_id
        ''')
        assert len(all_customers) == 26
        assert all_customers.loc[all_customers["customer_id"].ge(23), "paid_orders"].eq(0).all()
        """),
        md("""## 8. Подзапрос: сначала чек заказа, потом распределение

        Для описательной статистики нам нужна одна строка на заказ. Подзапрос агрегирует позиции,
        а внешний SELECT описывает полученные чеки. Медиану и квантили добавим в pandas,
        чтобы не зависеть от необязательных SQLite-расширений.
        """),
        code("""
        order_totals = query('''
            SELECT o.order_id, o.ordered_on, SUM(i.quantity * i.unit_price_kzt) AS order_total_kzt
            FROM orders AS o JOIN order_items AS i ON i.order_id = o.order_id
            WHERE o.status = 'paid'
            GROUP BY o.order_id, o.ordered_on
            ORDER BY o.order_id
        ''')
        sql_summary = query('''
            SELECT COUNT(*) AS n, AVG(order_total_kzt) AS mean_kzt,
                   MIN(order_total_kzt) AS min_kzt, MAX(order_total_kzt) AS max_kzt
            FROM (
                SELECT o.order_id, SUM(i.quantity * i.unit_price_kzt) AS order_total_kzt
                FROM orders AS o JOIN order_items AS i ON i.order_id = o.order_id
                WHERE o.status = 'paid'
                GROUP BY o.order_id
            ) AS totals
        ''')
        display(sql_summary.round(2))
        display(order_totals["order_total_kzt"].describe(percentiles=[0.25, 0.5, 0.9]).round(2))
        assert np.isclose(sql_summary.loc[0, "mean_kzt"], order_totals["order_total_kzt"].mean())
        """),
        md("""## 9. Параметры запроса отделяют SQL от данных

        Значение фильтра передаём через `params`, не вставляем f-строкой в SQL.
        Это решает и проблему кавычек в строках, и риск превращения данных в часть запроса.
        Параметры предназначены для значений; имена таблиц и столбцов выбирают из известного списка.
        """),
        code("""
        chosen_city = "Atyrau"
        chosen = query('''
            SELECT customer_id, city FROM customers WHERE city = ? ORDER BY customer_id
        ''', params=(chosen_city,))
        display(chosen)
        assert chosen["city"].eq(chosen_city).all()
        unusual = query("SELECT customer_id FROM customers WHERE city = ?", params=("Atyrau' OR 1=1 --",))
        assert unusual.empty  # Строка остаётся значением; она не изменила смысл WHERE.
        """),
        md("""## 10. Независимая сверка SQL против CSV+pandas

        Совпадение красивых чисел не достаточно: сверяем количество уникальных заказов и выручку.
        Вторая реализация читает отдельные CSV-снимки, проверяет cardinality и повторяет
        бизнес-определение paid. Это помогает поймать неверный JOIN или знаменатель.
        """),
        code("""
        csv_orders = pd.read_csv(DATA_DIR / "orders.csv")
        csv_items = pd.read_csv(DATA_DIR / "order_items.csv")
        csv_customers = pd.read_csv(DATA_DIR / "customers.csv")
        joined = (csv_items.merge(csv_orders, on="order_id", validate="many_to_one")
                  .merge(csv_customers, on="customer_id", validate="many_to_one"))
        paid = joined.loc[joined["status"].eq("paid")].copy()
        paid["value"] = paid["quantity"] * paid["unit_price_kzt"]
        reference = paid.groupby("city")["value"].sum().sort_index()
        actual = city_revenue.set_index("city")["revenue_kzt"].sort_index()
        pd.testing.assert_series_equal(actual, reference, check_names=False)
        assert paid["order_id"].nunique() == counts.loc[0, "paid_orders"]
        assert order_totals["order_total_kzt"].sum() == actual.sum()
        print("SQL и pandas: выручка по каждому городу и количество заказов совпали.")
        """),
        md("""## 11. Визуальный отчёт и закрытие соединения

        Гистограмма чеков помогает увидеть разброс, а столбцы выручки — сравнить объём.
        Объём нельзя называть эффективностью без информации о затратах и размере аудитории.
        После всех запросов соединение закрываем; для повтора запускаем notebook сверху.
        """),
        code("""
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        axes[0].hist(order_totals["order_total_kzt"] / 1000, bins=12, color="#277DA1", edgecolor="white")
        axes[0].set(xlabel="Чек, тыс. KZT", ylabel="Оплаченные заказы", title="Распределение размера заказа")
        axes[1].bar(city_revenue["city"], city_revenue["revenue_kzt"] / 1000, color="#43AA8B")
        axes[1].set(xlabel="Город", ylabel="Выручка, тыс. KZT", title="Выручка в синтетической базе")
        plt.tight_layout()
        plt.show()
        connection.close()
        """),
        md("""## Контрольные вопросы

        - В какой момент `COUNT(*)` перестаёт считать заказы?
        - Почему `COUNT(o.order_id)` после LEFT JOIN даёт 0, а `COUNT(*)` — 1 для клиента без заказов?
        - Чем фильтр правой таблицы в ON отличается от такого же фильтра в WHERE?
        - Почему цена справочника не всегда подходит для расчёта исторической выручки?

        Дальше: [Homework Week 04](../homework/Homework_Week_04.md).
        """), sources_cell(sources)]
    save_notebook(folder / "practice" / "01_sql_store_analytics.ipynb", cells, 4)
    tasks = [
        {"title": "Фильтр и группировка", "points": 15, "description": "SQL-запросом получите число paid/cancelled/refunded по каждой дате. Отдельно найдите даты минимум с 5 оплаченными заказами через HAVING. Покажите детерминированный порядок результатов.", "starter": "# TODO: после заполнения выполните через pd.read_sql_query.\nstatus_by_day_sql = ''\nif status_by_day_sql.strip():\n    display(pd.read_sql_query(status_by_day_sql, connection))"},
        {"title": "Категории товаров", "points": 25, "description": "Для каждой category вычислите оплаченные позиции, уникальные paid-заказы, проданные единицы и выручку. Объясните, почему сумма уникальных заказов категорий может быть больше общего числа заказов.", "starter": "category_sql = ''  # TODO: напишите JOIN и корректные агрегаты.\nif category_sql.strip():\n    display(pd.read_sql_query(category_sql, connection))"},
        {"title": "Все клиенты, включая нули", "points": 25, "description": "Сформируйте SQL-таблицу всех 26 клиентов с числом paid-заказов и paid-выручкой, включая нули. Избегайте размножения счётчика заказов после JOIN с позициями. Проверьте клиентов 23–26.", "starter": "customer_sql = ''  # TODO: продумайте уровень агрегации до JOIN.\nif customer_sql.strip():\n    display(pd.read_sql_query(customer_sql, connection))"},
        {"title": "Подзапрос и проверка", "points": 20, "description": "Найдите оплаченные заказы с суммой выше среднего оплаченного чека, используя подзапрос. Независимо проверьте множество order_id и общую сумму в pandas по CSV.", "starter": "above_average_sql = ''  # TODO: сравнивайте заказ с заказом, не с позицией.\nabove_average = None\nif above_average_sql.strip():\n    above_average = pd.read_sql_query(above_average_sql, connection)\n    display(above_average)"},
        {"title": "График и объяснение SQL-ошибки", "points": 15, "description": "Постройте график выручки по category с единицами. На маленьком самостоятельно придуманном примере объясните ошибку COUNT(*) после LEFT JOIN и покажите исправленный запрос. Все фильтры по внешним значениям передавайте параметрами.", "starter": "# TODO: график строится по вашему SQL-результату.\nexplanation_example = None\nif explanation_example is not None:\n    display(explanation_example)"},
    ]
    make_homework(4, 'db_path = DATA_DIR / "store.sqlite"\nconnection = sqlite3.connect(db_path.resolve().as_uri() + "?mode=ro", uri=True)\ndisplay(pd.read_sql_query("SELECT name FROM sqlite_master WHERE type = \'table\' ORDER BY name", connection))', tasks, "3–4", "- После JOIN с позициями используйте COUNT(DISTINCT ...) либо предварительную агрегацию.\n- COALESCE может заменить неизвестную сумму нулём, когда отсутствие покупок действительно означает 0.\n- Сумма разных групп по DISTINCT не всегда аддитивна.\n- Для подзапроса сначала постройте одну строку на заказ.", "- База открыта read-only и не изменена.\n- Все 26 клиентов сохранены.\n- Чеки сравниваются на одном уровне детализации.\n- Есть независимая проверка SQL против CSV+pandas.")
    week_readme(4, "01_sql_store_analytics.ipynb", "- Написать SELECT, WHERE, ORDER BY, GROUP BY и HAVING.\n- Соединить 4 таблицы по ключам и объяснить единицу строки.\n- Сохранить клиентов без заказов при LEFT JOIN.\n- Использовать подзапросы и параметры, сверить SQL с pandas.", "- Неделя 03: DataFrame, groupby, merge, ключи и контрольные суммы.\n- Базовые типы Python; SQL-сервер или облачная учётная запись не нужны.", "**Занятие 1:** разделы 1–4: схема, SELECT, фильтры и GROUP BY/HAVING.\n\n**Занятие 2:** разделы 5–11: JOIN, NULL, подзапросы, параметры и независимая сверка.", sources)


def build_week_05():
    folder = ROOT / PLAN[4]["folder"]
    rnd = random.Random(505)
    stores = [{"store_id": i + 1, "store_name": name} for i, name in enumerate(["North", "South", "East", "West"])]
    rows = []
    for store in stores:
        for day in range(35):
            promotion = int(day % 7 in (4, 5))
            orders = max(5, round(30 + 6 * store["store_id"] + 0.2 * day + 9 * promotion + rnd.gauss(0, 5)))
            ticket = round(4500 + 120 * store["store_id"] + rnd.gauss(0, 450))
            rows.append({"store_id": store["store_id"], "sale_date": str(dt.date(2026, 4, 1) + dt.timedelta(days=day)),
                         "orders_n": orders, "revenue_kzt": orders * ticket, "promotion": promotion})
    save_csv(folder / "datasets" / "daily_sales.csv", rows)
    save_csv(folder / "datasets" / "stores.csv", stores)
    con = sqlite3.connect(":memory:")
    con.executescript("""
        CREATE TABLE stores(store_id INTEGER PRIMARY KEY, store_name TEXT NOT NULL);
        CREATE TABLE daily_sales(store_id INTEGER NOT NULL REFERENCES stores(store_id), sale_date TEXT NOT NULL,
                                 orders_n INTEGER NOT NULL CHECK(orders_n > 0),
                                 revenue_kzt INTEGER NOT NULL CHECK(revenue_kzt >= 0),
                                 promotion INTEGER NOT NULL CHECK(promotion IN (0,1)),
                                 PRIMARY KEY(store_id, sale_date));
    """)
    con.executemany("INSERT INTO stores VALUES (?,?)", [tuple(row.values()) for row in stores])
    con.executemany("INSERT INTO daily_sales VALUES (?,?,?,?,?)", [tuple(row.values()) for row in rows])
    con.commit()
    with sqlite3.connect(folder / "datasets" / "sales.sqlite") as target:
        con.backup(target)
    con.close()
    dataset_readme(5, """Seed: `505`. `sales.sqlite` и CSV-снимки `daily_sales.csv`, `stores.csv`.
Таблица daily_sales: **140 строк = 4 магазина × 35 последовательных дней**; пропусков дат нет.

| Поле | Тип / единицы | Смысл |
|---|---|---|
| store_id | int, 1–4 | Ключ магазина; имя в stores.store_name |
| sale_date | ISO-дата | Дата: 2026-04-01…2026-05-05 |
| orders_n | positive int | Завершённые заказы за день |
| revenue_kzt | nonnegative int, KZT | Дневная выручка |
| promotion | 0 / 1 | Синтетический признак акции |

Первичный ключ составной: (store_id, sale_date). Строка — магазин-день.
Суммы по дням нельзя считать независимыми случайными наблюдениями без дополнительных допущений.
Акции связаны с определёнными днями по правилу генератора; корреляция не оценивает причинный эффект акции.""")
    sources = [("SQLite: оконные функции", "https://www.sqlite.org/windowfunctions.html"),
               ("pandas: rolling", "https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rolling.html"),
               ("NumPy: standard deviation", "https://numpy.org/doc/stable/reference/generated/numpy.std.html")]
    cells = [md("""# Неделя 05. SQL-окна и первый системный EDA

        **Кейс:** описать 35 дней работы четырёх магазинов: изменение к прошлому дню,
        скользящее среднее, накопленную выручку и разброс показателей.
        Первая половина недели завершает SQL, вторая открывает модуль EDA.
        Вся база синтетическая и доступна локально.
        """), setup(5, "import sqlite3"),
        md("""## 1. Контракт временной таблицы

        Окно `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` означает три строки, а не автоматически три дня.
        В этом наборе на каждый магазин есть ровно одна строка каждого дня — сначала это докажем.
        Для таблицы с пропусками календаря понадобился бы явный календарь и отдельное правило заполнения.
        """),
        code("""
        connection = sqlite3.connect((DATA_DIR / "sales.sqlite").resolve().as_uri() + "?mode=ro", uri=True)
        def query(sql, params=None):
            return pd.read_sql_query(sql, connection, params=params)

        sales = query("SELECT * FROM daily_sales ORDER BY store_id, sale_date")
        sales["sale_date"] = pd.to_datetime(sales["sale_date"])
        assert not sales.duplicated(["store_id", "sale_date"]).any()
        assert len(sales) == 140
        for _, group in sales.groupby("store_id"):
            expected = pd.date_range(group["sale_date"].min(), group["sale_date"].max(), freq="D")
            assert group["sale_date"].tolist() == expected.tolist()
        display(sales.head())
        """),
        md("""## 2. Окно сохраняет строки, GROUP BY сворачивает

        `SUM(revenue) OVER (PARTITION BY store_id)` добавляет итог магазина к каждой его строке.
        С ним можно вычислить долю дня в итоговой выручке магазина.
        Сумма дневных долей по магазину должна равняться 1.
        """),
        code("""
        shares = query('''
            SELECT store_id, sale_date, revenue_kzt,
                   SUM(revenue_kzt) OVER (PARTITION BY store_id) AS store_total_kzt,
                   1.0 * revenue_kzt / SUM(revenue_kzt) OVER (PARTITION BY store_id) AS revenue_share
            FROM daily_sales
            ORDER BY store_id, sale_date
        ''')
        display(shares.head(7))
        assert len(shares) == len(sales)
        assert np.allclose(shares.groupby("store_id")["revenue_share"].sum(), 1)
        """),
        md("""## 3. LAG: изменение к предыдущей строке

        Предыдущего дня у первой строки нет: NULL означает отсутствие сравнения, а не нулевую выручку.
        CTE `WITH previous AS (...)` позволяет сначала вычислить lag, затем использовать его в формуле.
        `NULLIF(previous, 0)` защищает от деления на ноль, если появится день с нулевой выручкой.
        """),
        code("""
        changes = query('''
            WITH previous AS (
                SELECT store_id, sale_date, revenue_kzt,
                       LAG(revenue_kzt) OVER (PARTITION BY store_id ORDER BY sale_date) AS previous_revenue
                FROM daily_sales
            )
            SELECT *, revenue_kzt - previous_revenue AS change_kzt,
                   100.0 * (revenue_kzt - previous_revenue) / NULLIF(previous_revenue, 0) AS change_pct
            FROM previous
            ORDER BY store_id, sale_date
        ''')
        display(changes.head(6))
        assert changes["previous_revenue"].isna().sum() == 4
        """),
        md(r"""## 4. Скользящее и накопленное окно

        Скользящее среднее для $t\ge3$: $m_t=(x_t+x_{t-1}+x_{t-2})/3$.
        В первых двух строках используем доступные 1 или 2 наблюдения.
        Накопленная сумма $S_t=\sum_{i=1}^t x_i$ должна расти при неотрицательной выручке.
        Указываем frame явно, чтобы смысл не зависел от default `RANGE`.
        """),
        code("""
        windows = query('''
            SELECT store_id, sale_date, revenue_kzt,
                   AVG(revenue_kzt) OVER (
                       PARTITION BY store_id ORDER BY sale_date
                       ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
                   ) AS rolling_3_rows,
                   SUM(revenue_kzt) OVER (
                       PARTITION BY store_id ORDER BY sale_date
                       ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                   ) AS cumulative_revenue
            FROM daily_sales
            ORDER BY store_id, sale_date
        ''')
        display(windows.head(6))
        assert windows.groupby("store_id")["cumulative_revenue"].diff().dropna().ge(0).all()
        """),
        md("""## 5. ROW_NUMBER и DENSE_RANK

        `ROW_NUMBER` нумерует строки; для выбора одной последней записи задаём однозначный порядок.
        `DENSE_RANK` даёт одинаковый ранг равным значениям без пропусков следующих рангов.
        Рейтинг выручки за день отражает объём магазина, а не его эффективность.
        """),
        code("""
        latest = query('''
            WITH ranked AS (
                SELECT *, ROW_NUMBER() OVER (PARTITION BY store_id ORDER BY sale_date DESC) AS row_n
                FROM daily_sales
            )
            SELECT store_id, sale_date, revenue_kzt FROM ranked WHERE row_n = 1 ORDER BY store_id
        ''')
        daily_rank = query('''
            SELECT store_id, sale_date, revenue_kzt,
                   DENSE_RANK() OVER (PARTITION BY sale_date ORDER BY revenue_kzt DESC) AS revenue_rank
            FROM daily_sales ORDER BY store_id, sale_date
        ''')
        display(latest)
        assert len(latest) == 4 and latest["sale_date"].nunique() == 1
        """),
        md("""## 6. Независимая реализация в pandas

        Сортировка и границы групп должны совпадать с SQL. `shift` — аналог LAG;
        `rolling(..., min_periods=1)` повторяет наши короткие начальные окна.
        Сравнение NaN требует `equal_nan=True`: отсутствие прошлого дня ожидаемо.
        """),
        code("""
        reference = pd.read_csv(DATA_DIR / "daily_sales.csv").sort_values(["store_id", "sale_date"]).reset_index(drop=True)
        by_store = reference.groupby("store_id")["revenue_kzt"]
        assert np.allclose(changes["previous_revenue"], by_store.shift(1), equal_nan=True)
        rolling_ref = by_store.transform(lambda s: s.rolling(3, min_periods=1).mean())
        assert np.allclose(windows["rolling_3_rows"], rolling_ref)
        assert np.allclose(windows["cumulative_revenue"], by_store.cumsum())
        ranks_ref = reference.groupby("sale_date")["revenue_kzt"].rank(method="dense", ascending=False)
        assert np.array_equal(daily_rank["revenue_rank"], ranks_ref)
        print("Проверены LAG, rolling, cumulative sum и dense rank во всех 140 строках.")
        """),
        md(r"""## 7. EDA: центр, разброс и форма распределения

        Среднее описывает центр, стандартное отклонение — разброс вокруг среднего:
        $s=\sqrt{\frac{1}{n-1}\sum_i(x_i-\bar{x})^2}$.
        IQR = Q75 − Q25 описывает среднюю половину наблюдений и меньше зависит от крайних значений.
        Коэффициент вариации $CV=s/\bar{x}$ имеет смысл для положительной величины с осмысленным нулём.
        Не превращаем описательный CV в вывод о статистической значимости.
        """),
        code("""
        summary = sales.groupby("store_id")["revenue_kzt"].agg(["size", "mean", "median", "std", "min", "max"])
        quantiles = sales.groupby("store_id")["revenue_kzt"].quantile([0.25, 0.75]).unstack()
        summary["iqr_kzt"] = quantiles[0.75] - quantiles[0.25]
        summary["cv"] = summary["std"] / summary["mean"]
        display(summary.round(2))
        one_store = sales.loc[sales["store_id"].eq(1), "revenue_kzt"].to_numpy()
        manual_std = np.sqrt(((one_store - one_store.mean()) ** 2).sum() / (len(one_store) - 1))
        assert np.isclose(manual_std, summary.loc[1, "std"])
        """),
        md("""## 8. Гистограмма и эмпирическая функция распределения

        Гистограмма зависит от границ интервалов. ECDF показывает долю наблюдений ≤ x
        без выбора ширины интервала. Для повторяющихся значений ступеньки накладываются;
        график всё равно представляет эмпирическое распределение.
        """),
        code("""
        sorted_revenue = np.sort(one_store)
        ecdf = np.arange(1, len(sorted_revenue) + 1) / len(sorted_revenue)
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        axes[0].hist(one_store / 1000, bins=8, color="#277DA1", edgecolor="white")
        axes[0].set(xlabel="Выручка, тыс. KZT", ylabel="Дни", title="Магазин 1: распределение")
        axes[1].step(sorted_revenue / 1000, ecdf, where="post", color="#43AA8B")
        axes[1].set(xlabel="Выручка, тыс. KZT", ylabel="Доля дней ≤ x", ylim=(0, 1.05), title="ECDF")
        plt.tight_layout()
        plt.show()
        assert np.all(np.diff(ecdf) >= 0) and ecdf[-1] == 1
        """),
        md("""## 9. Сглаживание не создаёт новые наблюдения

        Сравним исходный ряд и rolling mean. Сглаживание подавляет быстрые изменения,
        но соседние точки начинают использовать общие данные. Их нельзя считать независимыми.
        Для прогноза следующего дня окно должно опираться только на прошлые значения;
        наше окно с текущим днём используется для описания уже завершённого дня.
        """),
        code("""
        w = windows.loc[windows["store_id"].eq(1)].copy()
        w["sale_date"] = pd.to_datetime(w["sale_date"])
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(w["sale_date"], w["revenue_kzt"] / 1000, alpha=0.6, marker=".", label="Дневная выручка")
        ax.plot(w["sale_date"], w["rolling_3_rows"] / 1000, linewidth=2.5, label="Среднее по 3 строкам")
        ax.set(xlabel="Дата", ylabel="Выручка, тыс. KZT", title="Магазин 1: исходный и сглаженный ряд")
        ax.legend()
        fig.autofmt_xdate()
        plt.tight_layout()
        plt.show()
        """),
        md("""## 10. Средний чек: правильное взвешивание

        Среднее дневных средних чеков придаёт одинаковый вес дню с 10 и 100 заказами.
        Средний чек всех заказов за период равен суммарной выручке / числу заказов.
        Число дней и число заказов — разные единицы наблюдения.
        """),
        code("""
        sales["daily_mean_ticket"] = sales["revenue_kzt"] / sales["orders_n"]
        ticket_report = sales.groupby("store_id").agg(
            revenue=("revenue_kzt", "sum"), orders=("orders_n", "sum"),
            mean_of_daily_means=("daily_mean_ticket", "mean"))
        ticket_report["weighted_mean_ticket"] = ticket_report["revenue"] / ticket_report["orders"]
        display(ticket_report.round(2))
        for store_id, group in sales.groupby("store_id"):
            assert np.isclose(np.average(group["daily_mean_ticket"], weights=group["orders_n"]),
                              ticket_report.loc[store_id, "weighted_mean_ticket"])
        connection.close()
        """),
        md("""## Короткий итог для аналитика

        Укажите магазин с максимальной суммой, магазин с максимальной вариативностью,
        и почему это могут быть разные магазины. Объясните, почему нельзя объявить
        акцию причиной роста только по группировке `promotion`.

        Домашняя работа: [Homework Week 05](../homework/Homework_Week_05.md).
        """), sources_cell(sources)]
    save_notebook(folder / "practice" / "01_sql_windows_descriptive_eda.ipynb", cells, 5)
    tasks = [
        {"title": "Окно предыдущих семи дней", "points": 25, "description": "SQL-запросом рассчитайте среднюю выручку предыдущих 7 строк без текущего дня для каждого магазина. Для первого дня результат должен быть NULL. Объясните разницу с окном, включающим текущий день, если результат нужен как признак прогноза.", "starter": "past_week_sql = ''  # TODO: текущий день не должен входить в frame.\nif past_week_sql.strip():\n    display(pd.read_sql_query(past_week_sql, connection).head(10))"},
        {"title": "Рейтинг и совпадения", "points": 20, "description": "Найдите 3 дня с максимальной выручкой каждого магазина через ROW_NUMBER с детерминированным tie-breaker. На маленькой таблице с равными суммами сравните ROW_NUMBER, RANK и DENSE_RANK.", "starter": "top_days_sql = ''  # TODO: сначала rank в CTE, затем фильтр.\nif top_days_sql.strip():\n    display(pd.read_sql_query(top_days_sql, connection))"},
        {"title": "Независимая сверка окон", "points": 20, "description": "По CSV воспроизведите семидневное прошлое окно и top-3 в pandas. Проверьте все значения, порядок и начальные NaN; отдельно убедитесь, что окна не смешивают магазины.", "starter": "# TODO: SQL и pandas должны совпасть построчно.\nwindow_verified = False\nprint('Сверка завершена:', window_verified)"},
        {"title": "Распределение среднего чека", "points": 20, "description": "Для каждого магазина опишите дневной средний чек: n, mean, median, sample std, IQR. Постройте ECDF двух магазинов на общей шкале. Не выдавайте 35 дневных средних за распределение чеков отдельных заказов.", "starter": "# TODO: сначала определите единицу наблюдения.\nticket_summary = None\nif ticket_summary is not None:\n    display(ticket_summary)"},
        {"title": "Акции и ограничения", "points": 15, "description": "Сравните дни с акцией и без по числу дней, числу заказов и выручке на магазин-день. Напишите 150 слов: наблюдение с числами, два возможных смешивающих фактора и какие данные нужны для причинного вывода.", "starter": "# TODO: сравнение является описательным, не оценкой эффекта.\npromotion_report = None\nif promotion_report is not None:\n    display(promotion_report)"},
    ]
    make_homework(5, 'connection = sqlite3.connect((DATA_DIR / "sales.sqlite").resolve().as_uri() + "?mode=ro", uri=True)\nsales = pd.read_csv(DATA_DIR / "daily_sales.csv", parse_dates=["sale_date"])\ndisplay(sales.head())', tasks, "3–4", "- SQL frame `... AND 1 PRECEDING` исключает текущую строку.\n- В pandas сначала shift внутри группы, затем rolling.\n- Для одинаковых значений добавьте дату как tie-breaker только в ROW_NUMBER.\n- ECDF по дням и ECDF по заказам отвечают на разные вопросы.", "- Первый день не получил выдуманное прошлое.\n- Ни одно окно не пересекает store_id.\n- Все SQL-результаты сверены, не только первые 5 строк.\n- Сравнение акций не объявлено причинным экспериментом.")
    week_readme(5, "01_sql_windows_descriptive_eda.ipynb", "- Объяснить PARTITION BY, ORDER BY и оконный frame.\n- Реализовать LAG, rolling, cumulative sum и ранжирование.\n- Сверить оконные SQL-операции с pandas.\n- Описать центр, разброс, ECDF и корректное взвешивание метрик.", "- Неделя 04: SELECT, JOIN, агрегирование и подзапросы.\n- Недели 02–03: NumPy, pandas, индексы и даты.", "**Занятие 1, модуль 3:** разделы 1–6: оконные функции и интеграция SQL+pandas.\n\n**Занятие 2, модуль 4:** разделы 7–10: описательная статистика, распределения и начальный EDA.", sources)


def build_week_06():
    folder = ROOT / PLAN[5]["folder"]
    rnd = random.Random(606)
    rows = []
    for i in range(240):
        traffic = rnd.choice(["off_peak", "peak"])
        weather = rnd.choices(["dry", "rain"], [3, 1])[0]
        distance = rnd.uniform(1, 18)
        load = rnd.randint(1, 6)
        duration = 10 + 2.4 * distance + 9 * (traffic == "peak") + 7 * (weather == "rain") + 1.5 * load + rnd.gauss(0, 4)
        rows.append({"delivery_id": f"D{i+1:04d}", "day": str(dt.date(2026, 5, 1) + dt.timedelta(days=i // 8)),
                     "region": rnd.choice(["North", "Center", "South"]), "traffic": traffic, "weather": weather,
                     "distance_km": round(distance, 2), "batch_orders": load,
                     "delivery_minutes": round(max(5, duration), 2)})
    confounded = []
    for mode, lo, hi, intercept in [("dense_center", 1, 5, 45), ("express_road", 8, 12, 8)]:
        for _ in range(50):
            distance = rnd.uniform(lo, hi)
            confounded.append({"route_type": mode, "distance_km": round(distance, 3),
                               "minutes": round(intercept + 3 * distance + rnd.gauss(0, 1.2), 3)})
    save_csv(folder / "datasets" / "deliveries.csv", rows)
    save_csv(folder / "datasets" / "confounding_demo.csv", confounded)
    dataset_readme(6, """Seed: `606`. `deliveries.csv`: **240 строк**, одна строка — доставка.

| Поле | Тип / единицы | Смысл |
|---|---|---|
| delivery_id | string | Уникальный ключ |
| day | ISO-дата | 30 дней, 8 доставок в день |
| region | category | North / Center / South |
| traffic | category | off_peak / peak |
| weather | category | dry / rain |
| distance_km | float, км | Дистанция 1–18 км |
| batch_orders | int, 1–6 | Число заказов в маршруте |
| delivery_minutes | float, минуты | Положительная синтетическая длительность |

`confounding_demo.csv`: **100 строк**, 50 `dense_center` и 50 `express_road`.
Поля: route_type, distance_km, minutes. Правило специально создаёт положительную связь
дистанции и времени внутри групп, но отрицательную общую корреляцию из-за различий групп.
Это демонстрация смешения, а не наблюдение о реальной дорожной сети.
В обоих файлах нет пропусков; эффект погоды и нагрузки задан генератором, не измерен экспериментально.""")
    sources = [("Matplotlib: pyplot tutorial", "https://matplotlib.org/stable/tutorials/pyplot.html"),
               ("seaborn: статистические зависимости", "https://seaborn.pydata.org/tutorial/relational.html"),
               ("Plotly: отображение фигур", "https://plotly.com/python/renderers/"),
               ("Plotly: автономный HTML", "https://plotly.com/python/interactive-html-export/")]
    cells = [md("""# Неделя 06. EDA: графики, корреляция и честные выводы

        **Кейс:** описать длительность доставок и проверить, меняет ли разбиение на группы
        интерпретацию общей корреляции. Освоим matplotlib, seaborn и Plotly на одной задаче.
        Все файлы синтетические и локальные. Для интерактивного графика не используется CDN.

        **Результат:** несколько графиков с понятным вопросом, проверенная описательная таблица,
        сравнение Pearson/Spearman и воспроизводимый пример смешения факторов.
        """), setup(6, "import seaborn as sns\nimport plotly.express as px\nimport json\nfrom tempfile import TemporaryDirectory"),
        md("""## 1. Перед графиком проверяем единицу строки

        Одна строка — доставка; расстояние в км, время в минутах. Дневной средний показатель
        был бы другой единицей наблюдения. Начнём с профиля данных, количества категорий и диапазонов.
        Не выбираем только удобные строки, чтобы график выглядел аккуратнее.
        """),
        code("""
        deliveries = pd.read_csv(DATA_DIR / "deliveries.csv", parse_dates=["day"])
        assert deliveries["delivery_id"].is_unique and len(deliveries) == 240
        assert deliveries.notna().all().all()
        assert deliveries["distance_km"].gt(0).all() and deliveries["delivery_minutes"].gt(0).all()
        display(deliveries.head())
        display(deliveries[["distance_km", "batch_orders", "delivery_minutes"]].describe().round(2))
        display(pd.crosstab(deliveries["traffic"], deliveries["weather"], margins=True))
        """),
        md("""## 2. Выбор графика следует за вопросом

        | Вопрос | График | Что подписать |
        |---|---|---|
        | Как распределено время? | Histogram / ECDF | Интервалы, n, минуты |
        | Как время связано с расстоянием? | Scatter | Единицы обеих осей, группы |
        | Как отличаются группы? | Boxplot + число наблюдений | Медиана, диапазон, n |
        | Как менялся показатель по датам? | Line | Агрегация, даты, единица |
        | Какие линейные связи есть? | Correlation heatmap | Метод и выбор числовых полей |

        Цвет должен иметь значение. Не кодируем десять несущественных категорий, если вопрос только о двух.
        """),
        code("""
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        axes[0].hist(deliveries["delivery_minutes"], bins=16, color="#277DA1", edgecolor="white")
        axes[0].axvline(deliveries["delivery_minutes"].median(), color="#F94144", linestyle="--", label="Медиана")
        axes[0].set(xlabel="Длительность, минуты", ylabel="Доставки", title="Распределение, n = 240")
        axes[0].legend()
        axes[1].scatter(deliveries["distance_km"], deliveries["delivery_minutes"], alpha=0.55, s=24)
        axes[1].set(xlabel="Расстояние, км", ylabel="Длительность, минуты", title="Расстояние и время")
        plt.tight_layout()
        plt.show()
        """),
        md("""## 3. seaborn: групповой scatter и boxplot

        Разделим время пик/вне пика. Boxplot показывает медиану, квартильный интервал и точки
        за пределами стандартных усов; эти точки не автоматически ошибочные.
        В сопроводительной таблице оставим n, среднее, медиану и p90.
        """),
        code("""
        traffic_summary = deliveries.groupby("traffic").agg(
            n=("delivery_id", "size"), mean=("delivery_minutes", "mean"),
            median=("delivery_minutes", "median"), p90=("delivery_minutes", lambda s: s.quantile(0.9)))
        display(traffic_summary.round(2))
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        sns.scatterplot(data=deliveries, x="distance_km", y="delivery_minutes", hue="traffic", alpha=0.7, ax=axes[0])
        axes[0].set(xlabel="Расстояние, км", ylabel="Длительность, минуты", title="Группы трафика")
        sns.boxplot(data=deliveries, x="traffic", y="delivery_minutes", color="#90BE6D", ax=axes[1])
        axes[1].set(xlabel="Трафик", ylabel="Длительность, минуты", title="Распределения внутри групп")
        plt.tight_layout()
        plt.show()
        assert traffic_summary["n"].sum() == len(deliveries)
        """),
        md("""## 4. Plotly: интерактивное исследование тех же данных

        Наведите курсор, чтобы увидеть ID, погоду и нагрузку. Легенда позволяет скрывать группы;
        двойной щелчок возвращает масштаб. Используем `plotly_mimetype`: данные и спецификация
        сохраняются в notebook, а JupyterLab/VS Code используют свой renderer.
        Статические графики выше остаются читаемыми в просмотрщиках без Plotly.
        """),
        code("""
        interactive = px.scatter(
            deliveries, x="distance_km", y="delivery_minutes", color="traffic",
            hover_data=["delivery_id", "weather", "batch_orders"],
            labels={"distance_km": "Расстояние, км", "delivery_minutes": "Длительность, минуты", "traffic": "Трафик"},
            title="Синтетические доставки: изучите отдельные наблюдения", template="plotly_white")
        # Явный MIME renderer не подключает внешнюю CDN-библиотеку.
        interactive.show(renderer="plotly_mimetype")
        assert sum(len(trace.x) for trace in interactive.data) == len(deliveries)
        """),
        md("""## 5. Автономный HTML и проверка экспорта

        Для отправки графика вне notebook можно сохранить HTML с JavaScript внутри файла:
        `include_plotlyjs=True`. Это увеличивает файл, зато для открытия не нужен интернет.
        Здесь демонстрация идёт во временной папке; для собственного отчёта выберите свою папку результатов.
        """),
        code("""
        with TemporaryDirectory() as temp_dir:
            html_path = Path(temp_dir) / "delivery_scatter.html"
            interactive.write_html(html_path, include_plotlyjs=True, full_html=True, auto_open=False)
            html = html_path.read_text(encoding="utf-8")
            assert "Plotly.newPlot" in html and html_path.stat().st_size > 1000000
            # Нет внешнего script src: библиотека включена в этот HTML.
            from html.parser import HTMLParser
            class ScriptSources(HTMLParser):
                def __init__(self):
                    super().__init__()
                    self.sources = []
                def handle_starttag(self, tag, attrs):
                    if tag == "script":
                        self.sources.extend(value for key, value in attrs if key == "src")
            parser = ScriptSources()
            parser.feed(html)
            assert not parser.sources
            print("Автономный HTML сформирован:", round(html_path.stat().st_size / 1024 / 1024, 2), "MiB")
        """),
        md(r"""## 6. Pearson и Spearman

        Pearson измеряет линейную связь:
        $r=\frac{\sum_i(x_i-\bar{x})(y_i-\bar{y})}{\sqrt{\sum_i(x_i-\bar{x})^2\sum_i(y_i-\bar{y})^2}}$.
        Spearman применяет корреляцию к рангам и отражает монотонную связь.
        Ни одна из этих величин не доказывает причинность; коэффициент также не заменяет scatter.
        """),
        code("""
        numeric = deliveries[["distance_km", "batch_orders", "delivery_minutes"]]
        pearson = numeric.corr(method="pearson")
        spearman = numeric.corr(method="spearman")
        display(pearson.round(3))
        display(spearman.round(3))
        x = numeric["distance_km"].to_numpy()
        y = numeric["delivery_minutes"].to_numpy()
        manual_r = ((x - x.mean()) * (y - y.mean())).sum() / np.sqrt(((x - x.mean()) ** 2).sum() * ((y - y.mean()) ** 2).sum())
        assert np.isclose(manual_r, pearson.loc["distance_km", "delivery_minutes"])
        assert np.allclose(np.diag(pearson), 1) and np.allclose(pearson, pearson.T)
        """),
        md("""## 7. Heatmap и нелинейный контрпример

        У корреляции диапазон от −1 до 1, поэтому сохраняем общую цветовую шкалу.
        Низкая корреляция не означает отсутствие зависимости: симметричная парабола —
        детерминированная зависимость с почти нулевым Pearson.
        """),
        code("""
        nonlinear_x = np.linspace(-3, 3, 101)
        nonlinear_y = nonlinear_x ** 2
        nonlinear_r = np.corrcoef(nonlinear_x, nonlinear_y)[0, 1]
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        sns.heatmap(pearson, annot=True, fmt=".2f", vmin=-1, vmax=1, center=0, cmap="vlag", ax=axes[0])
        axes[0].set_title("Pearson: фиксированная шкала")
        axes[1].scatter(nonlinear_x, nonlinear_y, s=18, color="#F8961E")
        axes[1].set(xlabel="x", ylabel="x²", title=f"Зависимость есть, Pearson = {nonlinear_r:.3f}")
        plt.tight_layout()
        plt.show()
        assert abs(nonlinear_r) < 1e-10
        """),
        md("""## 8. Смешение групп может перевернуть знак

        Отдельный учебный файл содержит медленные короткие маршруты по плотному центру и
        быстрые длинные маршруты по скоростной дороге. Внутри каждого типа увеличение дистанции
        увеличивает время, но смешанная таблица может показать отрицательную связь.
        Не следует переводить такое наблюдение в совет «чем дальше ехать, тем быстрее доедем».
        """),
        code("""
        confounded = pd.read_csv(DATA_DIR / "confounding_demo.csv")
        overall_r = confounded["distance_km"].corr(confounded["minutes"])
        grouped_r = pd.Series({name: g["distance_km"].corr(g["minutes"])
                               for name, g in confounded.groupby("route_type")}, name="within_group_pearson")
        display(grouped_r.to_frame())
        print("Общая корреляция:", round(overall_r, 3))
        assert overall_r < 0 and grouped_r.gt(0).all()
        fig, ax = plt.subplots()
        sns.scatterplot(data=confounded, x="distance_km", y="minutes", hue="route_type", ax=ax)
        ax.set(xlabel="Дистанция, км", ylabel="Время, минуты", title="Синтетический пример смешения факторов")
        plt.tight_layout()
        plt.show()
        """),
        md("""## 9. Сравниваем группы с одинаковым определением показателя

        Добавим долю доставок дольше 60 минут. Порог — учебное условие. Процент всегда сопровождаем
        числителем и знаменателем. В реальном отчёте нужно уточнить, одинаково ли собираются
        наблюдения в разных группах и нет ли пропущенных доставок.
        """),
        code("""
        deliveries = deliveries.assign(over_60=deliveries["delivery_minutes"] > 60)
        report = deliveries.groupby(["traffic", "weather"]).agg(
            n=("delivery_id", "size"), over_60_n=("over_60", "sum"),
            over_60_share=("over_60", "mean"), median_minutes=("delivery_minutes", "median"),
            median_distance=("distance_km", "median"))
        display(report.round(3))
        assert np.allclose(report["over_60_share"], report["over_60_n"] / report["n"])
        """),
        md("""## 10. Формулируем вывод без лишней уверенности

        Хорошая структура: **наблюдение с числом → ограничение → следующий проверяемый вопрос**.
        Например: «В этой выборке медиана в группе X равна ... при n=...; группы различаются
        длиной маршрута, поэтому это не оценка эффекта трафика; сравним похожие маршруты».
        Не называем различие статистически значимым: в этой неделе статистический тест не проводился.
        """),
        code("""
        for name, row in traffic_summary.iterrows():
            print(f"{name}: n={int(row['n'])}, медиана={row['median']:.1f} мин, p90={row['p90']:.1f} мин.")
        print("Ограничение: данные синтетические; показанные отношения заданы генератором.")
        print("Следующий вопрос: сохраняется ли различие при одинаковом расстоянии и погоде?")
        """), sources_cell(sources)]
    save_notebook(folder / "practice" / "01_visualization_correlation.ipynb", cells, 6)
    tasks = [
        {"title": "План анализа и профиль", "points": 15, "description": "Сформулируйте 3 вопроса по погоде, нагрузке и длительности. Для каждого выберите график и единицу наблюдения. Проверьте диапазоны, пропуски и численность комбинаций traffic×weather×region.", "starter": "# TODO: сформулируйте вопросы до построения графиков.\nanalysis_plan = None\nquality_profile = None"},
        {"title": "Три разных графика", "points": 25, "description": "Постройте ECDF длительности по погоде, scatter дистанции и времени с цветом погоды и boxplot длительности по batch_orders. Добавьте подписи единиц, n и объясните выбор каждого графика.", "starter": "# TODO: не копируйте одну и ту же визуализацию с разными цветами.\nfigures = []\nprint('Готовых графиков:', len(figures))"},
        {"title": "Интерактивный отчёт", "points": 20, "description": "Создайте Plotly scatter с hover по ID и региону, цветом погоды и фасетами traffic. Сохраните автономный HTML с include_plotlyjs=True в свою папку. Проверьте число наблюдений во всех traces.", "starter": "# TODO: импортируйте plotly.express и создайте собственную Figure.\ninteractive_figure = None\nif interactive_figure is not None:\n    interactive_figure.show(renderer='plotly_mimetype')"},
        {"title": "Корреляция и группа", "points": 25, "description": "Вычислите Pearson и Spearman между batch_orders и delivery_minutes в целом и внутри traffic. Укажите n групп. На confounding_demo.csv самостоятельно воспроизведите смену знака и объясните её без причинного утверждения.", "starter": "# TODO: сначала таблица коэффициентов с n, затем интерпретация.\ncorrelation_report = None\nif correlation_report is not None:\n    display(correlation_report)"},
        {"title": "Записка аналитику", "points": 15, "description": "Напишите 150–200 слов с тремя численными наблюдениями, двумя ограничениями и предложением нового сбора данных. Укажите, какой из ваших графиков лучше всего отвечает на главный вопрос и почему.", "starter": "# TODO: вычислите числа, которые используете в записке; текст — в Markdown.\nkey_numbers = None\nif key_numbers is not None:\n    display(key_numbers)"},
    ]
    make_homework(6, 'deliveries = pd.read_csv(DATA_DIR / "deliveries.csv", parse_dates=["day"])\nconfounded = pd.read_csv(DATA_DIR / "confounding_demo.csv")\ndisplay(deliveries.head())', tasks, "3–4", "- Для фасетов Plotly есть facet_col; hover_data добавляет поля без новой оси.\n- ECDF: сортировка + последовательность 1/n…1.\n- Метод corr можно задать явно.\n- Низкая корреляция не исключает нелинейную связь; посмотрите scatter.", "- Сохранены все 240 доставок либо описан точный фильтр.\n- Графики читаются без устного пояснения.\n- HTML не требует CDN.\n- Нет заявлений о причинности или значимости без соответствующего исследования.")
    week_readme(6, "01_visualization_correlation.ipynb", "- Выбирать histogram, ECDF, scatter, boxplot и line по вопросу.\n- Создавать matplotlib/seaborn-графики и автономную Plotly-фигуру.\n- Рассчитать и проверить Pearson/Spearman.\n- Объяснить смешение факторов, нулевую корреляцию при нелинейности и границы группового сравнения.", "- Неделя 05: распределения, стандартное отклонение, квантили.\n- Недели 02–03: NumPy и pandas, группировки и маски.", "**Занятие 1:** разделы 1–5: matplotlib, seaborn, Plotly и автономный экспорт.\n\n**Занятие 2:** разделы 6–10: корреляции, групповые сравнения, смешение и вывод.", sources)


def build_week_07():
    folder = ROOT / PLAN[6]["folder"]
    rnd = random.Random(707)
    rows = []
    variants = {"center": ["Center", " center ", "CENTER"], "north": ["North", "NORTH ", "north"],
                "south": ["South", " south", "SOUTH"]}
    for i in range(150):
        district = rnd.choice(list(variants))
        source = rnd.choice(["web", "phone", "mobile"])
        response = round(max(2, rnd.gauss({"center": 45, "north": 60, "south": 80}[district], 18)), 1)
        cost = round(max(0, rnd.gauss(18000, 6500)))
        if rnd.random() < (0.24 if source == "phone" else 0.06):
            response = ""
        if i % 17 == 0:
            cost = ""
        rows.append({"request_id": f"R{i+1:04d}", "created_at": (dt.datetime(2026, 6, 1, 8) + dt.timedelta(hours=i * 4)).isoformat(),
                     "district": rnd.choice(variants[district]), "source": source,
                     "priority": rnd.choice(["low", "medium", "high"]),
                     "status": rnd.choices(["open", "closed"], [1, 3])[0],
                     "response_minutes": response, "cost_kzt": cost})
    rows[12]["cost_kzt"] = -500
    rows[41]["cost_kzt"] = -1000
    rows[54]["cost_kzt"] = "unknown"
    rows[25]["response_minutes"] = -8
    rows[99]["response_minutes"] = "not_recorded"
    rows[77]["response_minutes"] = 2200.0  # Реальное для учебного сценария редкое долгое ожидание.
    rows[88]["created_at"] = "2026-99-99"
    rows.extend(dict(rows[i]) for i in [3, 19, 42, 77, 110])
    save_csv(folder / "datasets" / "service_requests_dirty.csv", rows)
    summary = [{"month": month, "requests_n": n, "over_60_n": late}
               for month, n, late in [("2026-01", 120, 36), ("2026-02", 150, 42), ("2026-03", 180, 45), ("2026-04", 160, 32)]]
    save_csv(folder / "datasets" / "storytelling_monthly.csv", summary)
    rules = {"exact_duplicates": "Remove exact copies; conflicting request_id requires review.",
             "response_minutes": "Parse numeric; nonpositive or unparseable -> missing; high positive values retained.",
             "cost_kzt": "Parse numeric; negative or unparseable -> missing; zero is allowed.",
             "created_at": "Parse ISO datetime; invalid -> NaT and quality flag.",
             "district": "Strip whitespace and lowercase; map center/north/south to canonical labels.",
             "outliers": "IQR rule is descriptive flag only; do not delete observations automatically.",
             "imputation": "Sensitivity analysis only; do not treat filled observations as measured values."}
    (folder / "datasets" / "cleaning_rules.json").write_text(json.dumps(rules, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    dataset_readme(7, """Seed: `707`. `service_requests_dirty.csv`: **155 строк = 150 обращений + 5 точных дублей**.

| Поле | Тип / единицы | Смысл и намеренные проблемы |
|---|---|---|
| request_id | string | ID обращения; повторы полных строк намеренные |
| created_at | ISO datetime / string | В одной строке некорректная дата 2026-99-99 |
| district | category/string | center/north/south с пробелами и разным регистром |
| source | category | web / phone / mobile; phone чаще не имеет времени ответа |
| priority | category | low / medium / high |
| status | category | open / closed — состояние на момент выгрузки |
| response_minutes | numeric text / missing | Есть пропуски, −8, not_recorded и корректное редкое 2200 |
| cost_kzt | numeric text / missing | Есть пропуски, две отрицательные суммы и unknown |

`cleaning_rules.json` фиксирует учебные правила качества. Большое положительное время 2200 минут
считается допустимым редким событием по условию; его нельзя автоматически удалять.
Исходные данные намеренно грязные. Нормализованный файл не подменяет исходник.

`storytelling_monthly.csv` — **отдельный синтетический демонстрационный агрегат за 4 месяца**,
не агрегация service_requests_dirty.csv. Поля: month, requests_n — все обращения,
over_60_n — обращения с ожиданием >60 минут. Все длительности для этого демонстрационного агрегата известны.
Он показывает, почему число опозданий и их доля могут меняться по-разному.""")
    sources = [("pandas: missing data", "https://pandas.pydata.org/docs/user_guide/missing_data.html"),
               ("pandas: duplicates", "https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop_duplicates.html"),
               ("pandas: to_numeric", "https://pandas.pydata.org/docs/reference/api/pandas.to_numeric.html"),
               ("seaborn: распределения", "https://seaborn.pydata.org/tutorial/distributions.html")]
    cells = [md("""# Неделя 07. Data storytelling и очистка без потери смысла

        **Занятие 1:** как превратить график в проверяемое сообщение для руководителя.
        **Занятие 2:** как обнаружить пропуски, дубли, ошибки формата и редкие наблюдения,
        сохранив журнал решений. Все примеры синтетические.

        Итог — аккуратный аналитический вывод, исходные данные без изменений,
        очищенная копия и проверки того, что ни одна строка не исчезла незаметно.
        """), setup(7, "import json\nimport seaborn as sns"),
        md("""## 1. Storytelling начинается с решения, которое предстоит принять

        Аудитория: руководитель службы. Вопрос: уменьшилась ли доля обращений с долгим ожиданием?
        Нужна доля с прозрачным знаменателем, а не только абсолютное число задержек.
        Первые четыре строки ниже — отдельный демонстрационный агрегат; к грязной выгрузке июня
        они не относятся. Смешивать эти два источника в одном временном тренде нельзя.
        """),
        code("""
        monthly = pd.read_csv(DATA_DIR / "storytelling_monthly.csv")
        monthly["over_60_share"] = monthly["over_60_n"] / monthly["requests_n"]
        assert monthly["over_60_n"].le(monthly["requests_n"]).all()
        display(monthly)
        """),
        md("""## 2. Абсолютное число и доля могут рассказывать разные истории

        На первом графике — нагрузка долгими обращениями. На втором — доля от всех обращений.
        Столбцы начинаются от нуля; подписи n показывают знаменатель. Заголовок сообщает,
        что именно измерено, без обещаний о причине изменения.
        """),
        code("""
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        axes[0].bar(monthly["month"], monthly["over_60_n"], color="#277DA1")
        axes[0].set(xlabel="Месяц", ylabel="Обращения", title="Число ожиданий дольше 60 минут")
        bars = axes[1].bar(monthly["month"], monthly["over_60_share"] * 100, color="#43AA8B")
        for bar, row in zip(bars, monthly.itertuples()):
            axes[1].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.8,
                         f"{row.over_60_share:.0%}\\nn={row.requests_n}", ha="center", va="bottom", fontsize=9)
        axes[1].set(xlabel="Месяц", ylabel="Доля обращений, %", ylim=(0, 40), title="Доля долгих ожиданий снизилась в примере")
        plt.tight_layout()
        plt.show()
        """),
        md("""## 3. Проценты и процентные пункты

        Падение с 30% до 20% — это −10 процентных пунктов, а относительное изменение равно −33,3%.
        Эти величины описывают одно изменение на разных шкалах. В выводе укажите, какая шкала используется.
        Мы описываем данные; чтобы объяснить причину, нужны сведения о нагрузке, персонале и процессе.
        """),
        code("""
        first = monthly.iloc[0]
        last = monthly.iloc[-1]
        change_pp = 100 * (last["over_60_share"] - first["over_60_share"])
        relative_change = last["over_60_share"] / first["over_60_share"] - 1
        print(f"В синтетическом примере доля снизилась с {first['over_60_share']:.0%} до {last['over_60_share']:.0%}.")
        print(f"Изменение: {change_pp:.1f} п.п.; относительное изменение: {relative_change:.1%}.")
        print("Причина не установлена; следующий шаг — проверить состав обращений и изменения процесса.")
        assert np.isclose(change_pp, -10)
        """),
        md("""## 4. Новая поставка: сначала аудит, затем очистка

        Загружаем сырую июньскую выгрузку как есть. Не перезаписываем её и не удаляем строки
        глобальным `dropna()`. Для каждого преобразования фиксируем, что оно изменяет и почему.
        Сначала удалим только точные повторы; конфликтующие записи одного ID потребовали бы разбора.
        """),
        code("""
        raw = pd.read_csv(DATA_DIR / "service_requests_dirty.csv")
        original = raw.copy(deep=True)
        rules = json.loads((DATA_DIR / "cleaning_rules.json").read_text(encoding="utf-8"))
        display(raw.head())
        display(pd.DataFrame({"dtype": raw.dtypes.astype(str), "missing": raw.isna().sum()}))
        exact_duplicates = int(raw.duplicated().sum())
        clean_data = raw.drop_duplicates().copy()
        assert exact_duplicates == 5 and len(clean_data) == 150
        assert clean_data["request_id"].is_unique
        audit_rows = [{"step": "raw", "rows": len(raw), "affected": 0},
                      {"step": "remove_exact_duplicates", "rows": len(clean_data), "affected": exact_duplicates}]
        """),
        md("""## 5. Ошибка формата и пропуск — разные причины неизвестности

        `errors='coerce'` превращает неразбираемые значения в missing, но важно сохранить флаг причины.
        Отрицательная стоимость по условию недопустима; нулевая допустима.
        Неположительное время ответа недопустимо. Большое положительное время не является ошибкой само по себе.
        """),
        code("""
        for column in ["response_minutes", "cost_kzt"]:
            parsed = pd.to_numeric(clean_data[column], errors="coerce")
            clean_data[column + "_parse_error"] = clean_data[column].notna() & parsed.isna()
            clean_data[column + "_was_missing"] = clean_data[column].isna()
            clean_data[column] = parsed

        clean_data["invalid_cost"] = clean_data["cost_kzt"].lt(0)
        clean_data["invalid_response"] = clean_data["response_minutes"].le(0)
        clean_data.loc[clean_data["invalid_cost"], "cost_kzt"] = np.nan
        clean_data.loc[clean_data["invalid_response"], "response_minutes"] = np.nan
        parsed_dates = pd.to_datetime(clean_data["created_at"], errors="coerce")
        clean_data["invalid_created_at"] = parsed_dates.isna()
        clean_data["created_at"] = parsed_dates
        flag_columns = [c for c in clean_data if c.endswith("_parse_error") or c.startswith("invalid_")]
        display(clean_data[flag_columns].sum().to_frame("affected_rows"))
        audit_rows.append({"step": "parse_and_flag_invalid", "rows": len(clean_data),
                           "affected": int(clean_data[flag_columns].any(axis=1).sum())})
        """),
        md("""## 6. Нормализация категорий не должна угадывать смысл

        Убираем пробелы и приводим регистр, затем сопоставляем с явным словарём.
        Неизвестные значения нужно показать отдельно, а не автоматически относить к популярной группе.
        Сохраняем исходное написание для проверки преобразования.
        """),
        code("""
        clean_data["district_raw"] = clean_data["district"]
        normalized = clean_data["district"].str.strip().str.lower()
        district_map = {"center": "Center", "north": "North", "south": "South"}
        clean_data["district"] = normalized.map(district_map)
        assert clean_data["district"].notna().all()
        display(clean_data[["district_raw", "district"]].drop_duplicates().sort_values("district"))
        assert set(clean_data["district"]) == {"Center", "North", "South"}
        """),
        md("""## 7. Пропуски изучаем по источнику

        Доля missing может различаться по способу сбора данных. Это предупреждает,
        что анализ только полных строк способен изменить состав выборки.
        По одной таблице нельзя надёжно определить механизм MCAR/MAR/MNAR; здесь описываем наблюдаемое.
        """),
        code("""
        clean_data["response_missing"] = clean_data["response_minutes"].isna()
        missing_by_source = clean_data.groupby("source").agg(
            requests=("request_id", "size"), missing_n=("response_missing", "sum"),
            missing_share=("response_missing", "mean"), observed_n=("response_minutes", "count"))
        display(missing_by_source.round(3))
        assert (missing_by_source["requests"] == missing_by_source["missing_n"] + missing_by_source["observed_n"]).all()
        ax = (missing_by_source["missing_share"] * 100).plot.bar(color="#F8961E")
        ax.set(xlabel="Источник", ylabel="Доля неизвестного времени, %", title="Качество измерения отличается по источникам")
        plt.tight_layout()
        plt.show()
        """),
        md(r"""## 8. IQR — флаг для проверки, не автоматическое удаление

        $IQR=Q_{0.75}-Q_{0.25}$. Обычная эвристика отмечает $x<Q_1-1.5IQR$ или $x>Q_3+1.5IQR$.
        Она не знает бизнес-смысла. В условии этого набора 2200 минут — допустимое редкое ожидание.
        Сохраняем его и сравниваем устойчивую медиану со средним. Порог вычислен для EDA всей выгрузки;
        в ML обучаемые пороги должны оцениваться только по train.
        """),
        code("""
        observed = clean_data["response_minutes"].dropna()
        q1, q3 = observed.quantile([0.25, 0.75])
        iqr = q3 - q1
        low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        clean_data["response_iqr_flag"] = (clean_data["response_minutes"] < low) | (clean_data["response_minutes"] > high)
        display(clean_data.loc[clean_data["response_iqr_flag"], ["request_id", "response_minutes", "source", "district"]])
        assert clean_data.loc[clean_data["request_id"].eq("R0078"), "response_minutes"].iloc[0] == 2200
        assert clean_data.loc[clean_data["request_id"].eq("R0078"), "response_iqr_flag"].iloc[0]
        print(f"Среднее {observed.mean():.1f} мин; медиана {observed.median():.1f} мин; флагов {clean_data['response_iqr_flag'].sum()}.")
        """),
        md("""## 9. Честный отчёт по районам

        Для медианы используем доступные измерения; рядом указываем все обращения и число наблюдений.
        Неизвестное время не приравниваем к нулю и не считаем быстрым ответом.
        График на общей оси показывает медиану, а подписи n раскрывают покрытие измерениями.
        """),
        code("""
        district_report = clean_data.groupby("district").agg(
            all_requests=("request_id", "size"), observed_n=("response_minutes", "count"),
            mean_minutes=("response_minutes", "mean"), median_minutes=("response_minutes", "median"),
            p90_minutes=("response_minutes", lambda s: s.quantile(0.9)))
        district_report["coverage"] = district_report["observed_n"] / district_report["all_requests"]
        display(district_report.round(2))
        ordered = district_report.sort_values("median_minutes")
        fig, ax = plt.subplots()
        bars = ax.barh(ordered.index, ordered["median_minutes"], color="#277DA1")
        for bar, (_, row) in zip(bars, ordered.iterrows()):
            ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                    f"n={int(row['observed_n'])}/{int(row['all_requests'])}", va="center")
        ax.set(xlabel="Медиана первого ответа, минуты", ylabel="Район",
               title="Только доступные измерения; покрытие указано рядом")
        ax.set_xlim(0, ordered["median_minutes"].max() * 1.4)
        plt.tight_layout()
        plt.show()
        """),
        md("""## 10. Импутация меняет данные, поэтому проверяем чувствительность

        Замена пропусков медианой может быть полезной инженерной операцией, но не восстанавливает
        реально измеренное значение. Покажем два сценария заполнения и сравним число наблюдений,
        среднее и разброс. Они не становятся двумя независимыми исследованиями.
        Исходный очищенный столбец оставим с пропусками.
        """),
        code("""
        available = clean_data["response_minutes"]
        global_fill = available.fillna(available.median())
        source_medians = clean_data.groupby("source")["response_minutes"].transform("median")
        source_fill = available.fillna(source_medians)
        sensitivity = pd.DataFrame({
            name: {"n_values": values.count(), "mean": values.mean(), "median": values.median(), "std": values.std(ddof=1)}
            for name, values in {"observed_only": available, "global_median_fill": global_fill,
                                 "source_median_fill": source_fill}.items()
        }).T
        display(sensitivity.round(2))
        assert available.isna().sum() == clean_data["response_missing"].sum()
        print("Импутация показана как анализ чувствительности; очищенный исходник не заполнен.")
        """),
        md("""## 11. Проверяем контракт и журнал решений

        Проверки должны защищать смысл: ключи уникальны, данные не потеряны, допустимый редкий случай
        сохранён, причины неизвестных значений не исчезли, оригинал не изменился.
        В финальном отчёте нельзя скрывать, что некоторые даты и значения остались неизвестными.
        """),
        code("""
        pd.testing.assert_frame_equal(raw, original)
        assert clean_data["request_id"].is_unique and len(clean_data) == len(raw) - exact_duplicates
        assert clean_data["cost_kzt"].dropna().ge(0).all()
        assert clean_data["response_minutes"].dropna().gt(0).all()
        assert clean_data["invalid_cost"].sum() == 2
        assert clean_data["invalid_created_at"].sum() == 1
        assert clean_data["response_minutes_parse_error"].sum() == 1
        assert clean_data["cost_kzt_parse_error"].sum() == 1
        assert district_report["all_requests"].sum() == len(clean_data)
        audit_rows.append({"step": "final_clean_copy_with_flags", "rows": len(clean_data),
                           "affected": int(clean_data["response_missing"].sum())})
        display(pd.DataFrame(audit_rows))
        print("Контракт выполнен; исходный CSV не изменён.")
        """),
        md("""## 12. Итоговая записка: что известно и чего не хватает

        Укажите число удалённых точных дублей, долю известного времени, медианы по районам
        и роль редкого ожидания 2200 минут. Предложите проверку процесса сбора в phone-канале.
        Не делайте вывод, что район или канал сам по себе вызывает задержку.

        Домашняя работа: [Homework Week 07](../homework/Homework_Week_07.md).
        """), sources_cell(sources)]
    save_notebook(folder / "practice" / "01_storytelling_data_cleaning.ipynb", cells, 7)
    tasks = [
        {"title": "Сообщение руководителю", "points": 20, "description": "По storytelling_monthly.csv создайте один график и записку на 80–120 слов: изменение доли долгих ожиданий в п.п. и относительных %, динамика нагрузки и одно ограничение. Не смешивайте этот агрегат с июньскими обращениями.", "starter": "# TODO: выберите один главный вопрос и визуализацию.\nstory_metrics = None\nif story_metrics is not None:\n    display(story_metrics)"},
        {"title": "Функция очистки с аудитом", "points": 25, "description": "Напишите clean_requests(frame), возвращающую очищенную копию и audit DataFrame. Используйте cleaning_rules.json, сохраните flags и исходник. Проверьте идемпотентность значений основных полей: повторная очистка уже очищенных данных не меняет их.", "starter": "def clean_requests(frame):\n    # TODO: верните (clean_copy, audit), не меняя frame.\n    return None\n\ncleaned = None\naudit = None"},
        {"title": "Стоимость и покрытие", "points": 20, "description": "Для priority рассчитайте число всех обращений, число известных cost_kzt, coverage, median и p90 стоимости. Постройте график с покрытием. Объясните, почему неизвестная стоимость не равна нулевой.", "starter": "# TODO: отчёт должен явно показывать измеренные и неизвестные значения.\ncost_report = None\nif cost_report is not None:\n    display(cost_report)"},
        {"title": "Редкое событие и чувствительность", "points": 20, "description": "Сравните mean/median/p90 времени с сохранением всех допустимых наблюдений и в отдельном сценарии без IQR-флагов. Не удаляйте строки из основного набора. Объясните влияние удаления R0078 и почему результат не является исправлением ошибки.", "starter": "# TODO: два сценария нужны для анализа чувствительности.\nsensitivity_report = None\nif sensitivity_report is not None:\n    display(sensitivity_report)"},
        {"title": "Контракт и аналитическая записка", "points": 15, "description": "Добавьте не менее 6 проверок: число строк, уникальность, допустимость чисел, сохранность редкого события, неизменность оригинала, согласованность знаменателей. Напишите 150 слов с ограничениями и предложением улучшения сбора данных.", "starter": "# TODO: проверки должны соответствовать вашим правилам и выявлять нарушения.\ncontract_checks = None\nif contract_checks is not None:\n    display(contract_checks)"},
    ]
    make_homework(7, 'raw = pd.read_csv(DATA_DIR / "service_requests_dirty.csv")\nmonthly = pd.read_csv(DATA_DIR / "storytelling_monthly.csv")\nrules = json.loads((DATA_DIR / "cleaning_rules.json").read_text(encoding="utf-8"))\ndisplay(raw.head())', tasks, "3–4", "- Флаги нужно сохранить до преобразования строки в число.\n- Повторная очистка должна учитывать уже существующие флаги и канонические категории.\n- IQR не определяет бизнес-допустимость.\n- Сравнивайте coverage как observed/all, не как долю после удаления пропусков.", "- Исходник остался неизменным.\n- R0078 сохранён в основном наборе.\n- Нельзя перепутать 10 п.п. и 10%.\n- Процесс очистки объяснён, а не спрятан в одной длинной цепочке.")
    week_readme(7, "01_storytelling_data_cleaning.ipynb", "- Написать краткий вывод с числом, знаменателем, ограничением и следующим действием.\n- Различать проценты и процентные пункты.\n- Очистить дубли, формат и категории с журналом причин.\n- Описать missingness, сохранить допустимые редкие наблюдения и проверить чувствительность к импутации.", "- Неделя 06: выбор графиков, корреляции и ограничения выводов.\n- Неделя 03: DataFrame, маски, группировки и типы.", "**Занятие 1, модуль 4:** разделы 1–3 и упражнение на записку: storytelling, проценты и знаменатели.\n\n**Занятие 2, модуль 5:** разделы 4–12: журнал очистки, пропуски, IQR и проверки. Часть кода запускается заранее, время практики посвящается причинам решений.", sources)


def build_week_08():
    folder = ROOT / PLAN[7]["folder"]
    rnd = random.Random(808)
    rows = []
    for i in range(400):
        city = rnd.choice(["Astana", "Atyrau", "Aktau"])
        district = rnd.choice(["center", "outskirts"])
        building = rnd.choice(["brick", "panel", "monolith"])
        area = rnd.uniform(28, 140)
        rooms = max(1, min(5, round(area / 28 + rnd.gauss(0, 0.35))))
        age = rnd.randint(0, 50)
        floor = rnd.randint(1, 16)
        balcony = rnd.choice(["yes", "no"])
        rent = round(max(60000, {"Astana": 80000, "Atyrau": 60000, "Aktau": 45000}[city]
                         + 1800 * area + 30000 * (district == "center") + 20000 * (building == "monolith")
                         + 6000 * (balcony == "yes") + 400 * floor - 900 * age + rnd.gauss(0, 18000)))
        rows.append({"listing_id": f"L{i+1:04d}", "city": city, "district": district, "building_type": building,
                     "area_m2": "" if i % 17 == 0 else round(area, 2), "rooms": rooms,
                     "age_years": "" if i % 23 == 0 else age, "floor": floor,
                     "balcony": "" if i % 19 == 0 else balcony, "rent_kzt": rent,
                     "next_month_payment_kzt": rent + rnd.randint(-700, 700)})
    save_csv(folder / "datasets" / "rental_listings.csv", rows)
    dataset_readme(8, """Seed: `808`. `rental_listings.csv`: **400 строк**, одна строка — независимое синтетическое объявление.

| Поле | Тип / единицы | Доступность при прогнозе |
|---|---|---|
| listing_id | string | ID; исключается из модельных признаков |
| city | category | Astana / Atyrau / Aktau; известно до прогноза |
| district | category | center / outskirts; известно |
| building_type | category | brick / panel / monolith; известно |
| area_m2 | float, м² / missing | Площадь; часть значений отсутствует |
| rooms | int, 1–5 | Количество комнат, положительное |
| age_years | int / missing | Возраст здания; часть значений отсутствует |
| floor | int, 1–16 | Этаж |
| balcony | yes / no / missing | Категориальный признак с пропусками |
| rent_kzt | positive int, KZT/месяц | Целевая величина: учебная месячная аренда |
| next_month_payment_kzt | int, KZT | **Утечка:** платёж после события, близкий к target; исключается |

Цена задаётся синтетической формулой с шумом; она не отражает реальный рынок недвижимости.
ID уникальны, повторяющихся объектов и временной структуры нет, поэтому в упражнении допустим
случайный split. Для реальных повторных объектов/временных объявлений нужен групповой или временной split.
Пропуски заданы детерминированно по номеру строки. Задача — обучение предобработке, не оценка стоимости жилья.""")
    sources = [("scikit-learn: предотвращение утечек", "https://scikit-learn.org/stable/common_pitfalls.html"),
               ("scikit-learn: ColumnTransformer со смешанными типами", "https://scikit-learn.org/stable/auto_examples/compose/plot_column_transformer_mixed_types.html"),
               ("scikit-learn: Pipeline", "https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html"),
               ("scikit-learn: OneHotEncoder", "https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html")]
    cells = [md("""# Неделя 08. Предобработка, новые признаки и Pipeline без утечек

        **Кейс:** подготовить смешанные признаки объявления и построить проверяемый конвейер.
        В таблицу специально добавлен признак из будущего, который нужно исключить.
        Данные полностью синтетические; рынок аренды по ним не оцениваем.

        **Главная идея:** разделяем данные до обучения преобразований; медианы, масштабы и категории
        изучаются только на train. Линейная модель Ridge здесь служит небольшим демонстрационным
        потребителем подготовленных признаков; её математика будет в неделе 09.
        """), setup(8, "from sklearn.base import clone\nfrom sklearn.compose import ColumnTransformer\nfrom sklearn.impute import SimpleImputer\nfrom sklearn.preprocessing import OneHotEncoder, StandardScaler, FunctionTransformer\nfrom sklearn.pipeline import Pipeline\nfrom sklearn.model_selection import train_test_split, KFold, cross_val_score\nfrom sklearn.linear_model import Ridge\nfrom sklearn.dummy import DummyRegressor\nfrom sklearn.metrics import mean_absolute_error, r2_score\nimport sklearn"),
        md("""## 1. Сначала доступность признаков и разбиение

        Прогноз строится при публикации объявления. `next_month_payment_kzt` появится позднее
        и тесно связан с целью: он запрещён независимо от того, насколько улучшает метрику.
        ID также исключаем. Случайный split подходит для данного независимого синтетического набора;
        реальные повторные объявления потребовали бы группового или временного разделения.
        """),
        code("""
        raw = pd.read_csv(DATA_DIR / "rental_listings.csv")
        assert raw["listing_id"].is_unique and len(raw) == 400
        allowed = ["city", "district", "building_type", "area_m2", "rooms", "age_years", "floor", "balcony"]
        X = raw[allowed].copy()
        y = raw["rent_kzt"].copy()
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=SEED)
        assert set(X_train.index).isdisjoint(X_test.index)
        assert "next_month_payment_kzt" not in X_train and "rent_kzt" not in X_train
        assert len(X_train) == 320 and len(X_test) == 80
        print("scikit-learn:", sklearn.__version__, "| train:", X_train.shape, "| test:", X_test.shape)
        """),
        md("""## 2. Исследуем train, а test оставляем для оценки

        Описательные таблицы и решения о преобразованиях ниже основаны на train.
        Test не подсказывает медиану заполнения, границы выбросов или выбор признаков.
        Пропуски в числовом и категориальном столбцах требуют разных операций.
        """),
        code("""
        train_profile = pd.DataFrame({"dtype": X_train.dtypes.astype(str),
                                      "missing_n": X_train.isna().sum(),
                                      "missing_share": X_train.isna().mean()})
        display(train_profile)
        display(X_train.select_dtypes(include="number").describe().round(2))
        display(y_train.describe().round(2).to_frame("train_rent_kzt"))
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        axes[0].hist(X_train["area_m2"].dropna(), bins=14, color="#277DA1", edgecolor="white")
        axes[0].set(xlabel="Площадь, м²", ylabel="Объявления", title="Train: наблюдаемая площадь")
        axes[1].hist(y_train / 1000, bins=14, color="#43AA8B", edgecolor="white")
        axes[1].set(xlabel="Аренда, тыс. KZT/месяц", ylabel="Объявления", title="Train: целевая величина")
        plt.tight_layout()
        plt.show()
        """),
        md(r"""## 3. Масштабирование и кодирование: короткий ручной пример

        StandardScaler вычисляет $z=(x-\mu_{train})/\sigma_{train}$.
        Стандартное отклонение используется с `ddof=0`. Для номинальной категории нельзя
        без основания вводить порядок `brick=1, panel=2, monolith=3`; one-hot создаёт отдельные индикаторы.
        Неизвестная категория на новых данных не должна рушить весь прогноз.
        """),
        code("""
        toy_train = pd.DataFrame({"area": [30.0, 50.0, 70.0], "type": ["brick", "panel", "brick"]})
        scaler_demo = StandardScaler().fit(toy_train[["area"]])
        encoded_demo = OneHotEncoder(handle_unknown="ignore", sparse_output=False).fit(toy_train[["type"]])
        display(pd.DataFrame(scaler_demo.transform(toy_train[["area"]]), columns=["scaled_area"]))
        display(pd.DataFrame(encoded_demo.transform(toy_train[["type"]]), columns=encoded_demo.get_feature_names_out()))
        unknown_demo = encoded_demo.transform(pd.DataFrame({"type": ["new_type"]}))
        assert np.allclose(unknown_demo, 0)
        assert np.isclose(scaler_demo.mean_[0], 50)
        """),
        md("""## 4. Новые признаки: функция без обучения на выборке

        `area_per_room` отражает площадь на комнату, `upper_floor` — этаж ≥10.
        Порог 10 задаётся заранее как учебное условие. Эти преобразования используют только
        признаки текущей строки: они не смотрят на target или статистику соседних наблюдений.
        Если площадь неизвестна, отношение тоже неизвестно — его обработает следующий шаг.
        """),
        code("""
        def make_features(frame):
            "Создать признаки в копии DataFrame, сохранив строки и исходные поля."
            result = frame.copy()
            if not result["rooms"].gt(0).all():
                raise ValueError("rooms должно быть положительным для area_per_room")
            result["area_per_room"] = result["area_m2"] / result["rooms"]
            result["upper_floor"] = (result["floor"] >= 10).astype(int)
            return result

        engineered_train = make_features(X_train)
        display(engineered_train[["area_m2", "rooms", "area_per_room", "floor", "upper_floor"]].head())
        assert "area_per_room" not in X_train
        assert engineered_train.index.equals(X_train.index)
        """),
        md("""## 5. Числовая и категориальная ветви

        Числа: median imputation → индикаторы пропусков → scaling.
        Категории: most-frequent imputation → one-hot.
        `handle_unknown='ignore'` кодирует новую категорию нулевым вектором в её блоке.
        Это технически позволяет прогноз, но не доказывает качество на новом городе.
        """),
        code("""
        numeric_columns = ["area_m2", "rooms", "age_years", "floor", "area_per_room", "upper_floor"]
        categorical_columns = ["city", "district", "building_type", "balcony"]
        numeric_pipe = Pipeline([
            ("imputer", SimpleImputer(strategy="median", add_indicator=True)),
            ("scaler", StandardScaler()),
        ])
        categorical_pipe = Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ])
        preprocessor = ColumnTransformer([
            ("num", numeric_pipe, numeric_columns),
            ("cat", categorical_pipe, categorical_columns),
        ], remainder="drop")
        print("Числовых исходных ветвей:", len(numeric_columns), "| Категориальных:", len(categorical_columns))
        """),
        md("""## 6. Полный Pipeline: от исходной строки до прогноза

        `fit` обучает преобразования и модель на train. `predict` выполняет те же
        преобразования с уже выученными параметрами. Нам не нужно вручную кодировать
        новые данные в отдельном блокноте и надеяться на совпадение столбцов.
        Ridge с фиксированным alpha=1 — демонстрационная линейная модель, настройки здесь не подбираем.
        """),
        code("""
        pipeline = Pipeline([
            ("features", FunctionTransformer(make_features, validate=False)),
            ("preprocess", preprocessor),
            ("model", Ridge(alpha=1.0)),
        ])
        # Определение pipeline ещё не обучает ни медианы, ни категории, ни модель.
        assert not hasattr(preprocessor, "transformers_")
        print(pipeline)
        """),
        md("""## 7. Короткий предварительный просмотр кросс-валидации

        Кросс-валидацию подробно изучим в неделе 15. Здесь важен один принцип:
        **внутрь CV передаётся весь Pipeline**, чтобы каждый fold учил свои медианы и масштабы.
        Только train делится на три части; внешний test до финальной оценки не используется.
        Отрицательное имя scoring означает соглашение sklearn «больше — лучше», поэтому меняем знак для MAE.
        """),
        code("""
        cv = KFold(n_splits=3, shuffle=True, random_state=SEED)
        cv_mae = -cross_val_score(pipeline, X_train, y_train, cv=cv,
                                  scoring="neg_mean_absolute_error", n_jobs=1)
        display(pd.DataFrame({"fold": [1, 2, 3], "validation_mae_kzt": cv_mae}).round(2))
        assert np.isfinite(cv_mae).all() and (cv_mae >= 0).all()
        pipeline.fit(X_train, y_train)
        """),
        md("""## 8. Проверяем, что imputer видел только train

        После fit достаём обученную числовую ветвь и независимо вычисляем медианы train.
        Эта проверка способна обнаружить fit на полном наборе или неправильный набор столбцов.
        Проверка формы и конечности подготовленной матрицы ловит пропуски, деление на ноль и несогласованные категории.
        """),
        code("""
        fitted_pre = pipeline.named_steps["preprocess"]
        fitted_num = fitted_pre.named_transformers_["num"]
        medians = fitted_num.named_steps["imputer"].statistics_.copy()
        expected_medians = engineered_train[numeric_columns].median().to_numpy()
        assert np.allclose(medians, expected_medians)
        train_matrix = fitted_pre.transform(engineered_train)
        feature_names = fitted_pre.get_feature_names_out()
        assert train_matrix.shape[0] == len(X_train)
        assert train_matrix.shape[1] == len(feature_names)
        assert np.isfinite(train_matrix).all()
        display(pd.DataFrame(train_matrix[:5], columns=feature_names).round(2))
        print("Матрица train:", train_matrix.shape, "| Все параметры импутации соответствуют train.")
        """),
        md("""## 9. Transform на test не должен менять параметры

        Test преобразуется выученными медианами и категориями. Его собственная средняя после
        scaling не обязана быть нулевой: это нормальный результат, а не повод снова вызвать fit.
        У train и test должно быть одинаковое число признаков в одном и том же порядке.
        """),
        code("""
        test_matrix = fitted_pre.transform(make_features(X_test))
        assert test_matrix.shape[1] == train_matrix.shape[1]
        assert np.isfinite(test_matrix).all()
        assert np.array_equal(medians, fitted_num.named_steps["imputer"].statistics_)
        test_predictions = pipeline.predict(X_test)
        assert test_predictions.shape == (len(X_test),) and np.isfinite(test_predictions).all()
        print("Test преобразован без повторного обучения; матрица:", test_matrix.shape)
        """),
        md(r"""## 10. Сравнение с baseline на отложенной части

        $MAE=\frac{1}{n}\sum_i|y_i-\hat y_i|$ измеряется в KZT/месяц.
        Baseline предсказывает медиану train для каждого объявления. Сравниваем оба метода
        на одних и тех же 80 test-строках; после просмотра test не меняем признаки или настройки.
        R² — дополнительная относительная мера, которая может быть отрицательной для плохого прогноза.
        """),
        code("""
        baseline = DummyRegressor(strategy="median").fit(X_train, y_train)
        baseline_predictions = baseline.predict(X_test)
        comparison = pd.DataFrame([
            {"method": "Train median baseline", "mae_kzt": mean_absolute_error(y_test, baseline_predictions),
             "r2": r2_score(y_test, baseline_predictions)},
            {"method": "Pipeline + Ridge", "mae_kzt": mean_absolute_error(y_test, test_predictions),
             "r2": r2_score(y_test, test_predictions)},
        ])
        display(comparison.round(3))
        manual_mae = np.mean(np.abs(y_test.to_numpy() - test_predictions))
        assert np.isclose(manual_mae, comparison.loc[1, "mae_kzt"])
        assert np.allclose(baseline_predictions, y_train.median())
        """),
        md("""## 11. Диагностика и новая категория

        Диагональ actual=predicted помогает увидеть систематические ошибки; распределение
        абсолютной ошибки показывает разброс. Эти картинки описывают один учебный test.
        Отдельная искусственная строка с новым городом проверяет устойчивость API, не качество модели в этом городе.
        """),
        code("""
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        axes[0].scatter(y_test / 1000, test_predictions / 1000, alpha=0.7)
        bounds = np.array([min(y_test.min(), test_predictions.min()), max(y_test.max(), test_predictions.max())]) / 1000
        axes[0].plot(bounds, bounds, "--", color="#F94144")
        axes[0].set(xlabel="Факт, тыс. KZT", ylabel="Прогноз, тыс. KZT", title="Отложенные синтетические объявления")
        axes[1].hist(np.abs(y_test - test_predictions) / 1000, bins=12, color="#43AA8B", edgecolor="white")
        axes[1].set(xlabel="Абсолютная ошибка, тыс. KZT", ylabel="Объявления", title="Ошибки Pipeline")
        plt.tight_layout()
        plt.show()
        new_listing = X_test.iloc[[0]].copy()
        new_listing["city"] = "NewCity"
        prediction_new = pipeline.predict(new_listing)
        assert prediction_new.shape == (1,) and np.isfinite(prediction_new).all()
        assert np.array_equal(medians, fitted_num.named_steps["imputer"].statistics_)
        print("Новая категория обработана; качество вне обучающих категорий отдельно не оценено.")
        """),
        md("""## 12. Миниатюрная демонстрация утечки статистики

        На трёх train-значениях среднее равно 2. Если незаметно добавить test=100 до fit,
        среднее станет 26,5. Даже без target предобработка начала использовать будущее.
        Ниже намеренно показан неправильный fit только на отдельном игрушечном массиве;
        основной pipeline выше такого шага не выполняет.
        """),
        code("""
        toy_history = np.array([[0.0], [2.0], [4.0]])
        toy_future = np.array([[100.0]])
        correct_scaler = StandardScaler().fit(toy_history)
        leaked_scaler = StandardScaler().fit(np.vstack([toy_history, toy_future]))  # Намеренный антипример.
        display(pd.DataFrame({"fit_data": ["train only", "train + future (incorrect)"],
                              "learned_mean": [correct_scaler.mean_[0], leaked_scaler.mean_[0]]}))
        assert correct_scaler.mean_[0] == 2 and leaked_scaler.mean_[0] == 26.5
        """),
        md("""## Перед домашней работой

        Объясните, где вызван каждый fit и какие строки он мог видеть. Назовите два различных
        вида утечки: будущий платёж как признак и статистика полного датасета до split.
        Pipeline помогает соблюдать границы, но сам не распознаёт недопустимые бизнес-признаки.
        Для промышленного применения ещё понадобятся схема входа, оценка новых групп и мониторинг.

        Домашняя работа: [Homework Week 08](../homework/Homework_Week_08.md).
        """), sources_cell(sources)]
    save_notebook(folder / "practice" / "01_leakage_safe_preprocessing.ipynb", cells, 8)
    tasks = [
        {"title": "Контракт и holdout", "points": 15, "description": "Опишите момент прогноза и допустимость каждого поля. Создайте свой фиксированный train/test split 75/25, исключив ID и будущий платёж. Зафиксируйте индексы, чтобы все последующие варианты использовали один и тот же holdout.", "starter": "# TODO: сначала список разрешённых признаков и split, затем EDA.\nX_train = X_test = y_train = y_test = None\nsplit_manifest = None"},
        {"title": "Новые признаки без target", "points": 20, "description": "Реализуйте функцию признаков, добавляющую log1p(area_m2) и индикатор нового здания age_years≤5. Для неизвестного возраста сохраните неизвестность, а не считайте здание старым. Проверьте отсутствие мутации исходника и сохранность индекса.", "starter": "def add_features(frame):\n    # TODO: работайте только с признаками текущей строки и корректно обработайте missing.\n    return None\n\n# TODO: проверки индекса, missing и неизменности исходных данных."},
        {"title": "Сравнение предобработки внутри CV", "points": 25, "description": "Постройте полный Pipeline с ColumnTransformer. Сравните median+StandardScaler и median+RobustScaler внутри 3-fold CV только на train, сохранив один и тот же Ridge(alpha=1). Выберите вариант по средней validation MAE до единственной test-оценки.", "starter": "# TODO: preprocessing и модель должны входить в один Pipeline на каждом fold.\ncandidate_pipelines = {}\ncv_results = None\nif cv_results is not None:\n    display(cv_results)"},
        {"title": "Проверки утечки и схемы", "points": 25, "description": "Проверьте выученные медианы против train, одинаковую размерность train/test, конечность матрицы, отсутствие будущего платежа и сохранение параметров после predict. Проверьте новый тип здания, а не новый город из лабораторной.", "starter": "# TODO: после обучения выбранного pipeline извлеките параметры transformer.\nvalidation_report = None\nif validation_report is not None:\n    display(validation_report)"},
        {"title": "Финальная оценка и вывод", "points": 15, "description": "Один раз оцените выбранный конвейер и median baseline на test. Покажите MAE в KZT, scatter факт/прогноз и три вывода с ограничениями. Не выбирайте лучший вариант по test. Объясните, почему техническая поддержка неизвестной категории не гарантирует качество.", "starter": "# TODO: заполните после завершения выбора модели по train-CV.\nfinal_metrics = None\nif final_metrics is not None:\n    display(final_metrics)"},
    ]
    make_homework(8, 'raw = pd.read_csv(DATA_DIR / "rental_listings.csv")\nprint("Строк:", len(raw))\nprint("Поля:", raw.columns.tolist())\n# TODO: не вычисляйте статистики полного набора для обучения преобразований.', tasks, "4–5", "- log1p не требует fit, но статистическая импутация требует.\n- Булево сравнение с NaN может дать False; явным mask сохраните неизвестный возраст.\n- `clone` позволяет создать независимые estimator для вариантов.\n- CV использует только train; выбранный вариант фиксируется до test.\n- Документация RobustScaler доступна в sklearn; стратегия должна быть обоснована, не просто заменена.", "- Файл next_month_payment_kzt нигде не используется в X.\n- Каждый fit видит только свою обучающую часть.\n- Заполнение, encoding и scaling находятся внутри Pipeline.\n- Test использован один раз после выбора варианта.\n- Starter без решения не выдаётся за готовый pipeline.")
    week_readme(8, "01_leakage_safe_preprocessing.ipynb", "- Определить доступность признака в момент прогноза.\n- Создать row-wise признаки без target и мутации исходника.\n- Объединить imputation, encoding и scaling в ColumnTransformer/Pipeline.\n- Проверить train-only параметры и неизвестные категории.\n- Сравнить демонстрационную модель с baseline на честном holdout.", "- Неделя 07: очистка, пропуски, правила и аудит.\n- Недели 02–06: массивы, pandas, статистики и графики.\n- Ridge и CV здесь даны как preview; подробные алгоритмы будут в неделях 09 и 15.", "**Занятие 1:** разделы 1–5: признаки, split, imputation, encoding, scaling.\n\n**Занятие 2:** разделы 6–12: полный Pipeline, preview CV, проверки утечек и финальная оценка. При нехватке времени CV-код запускается заранее, а в классе разбирается граница fit.", sources)


if __name__ == "__main__":
    for builder in [build_week_01, build_week_02, build_week_03, build_week_04,
                    build_week_05, build_week_06, build_week_07, build_week_08]:
        builder()
