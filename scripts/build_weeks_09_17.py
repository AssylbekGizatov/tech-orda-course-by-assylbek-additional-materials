#!/usr/bin/env python3
"""Rebuild the original, offline teaching labs for weeks 09–17.

Run from the repository root. This script never downloads files and only writes
these nine week folders. Notebook execution is a separate validation step.
"""
from pathlib import Path
import hashlib
import json
import textwrap

import numpy as np
import pandas as pd
import sklearn
from sklearn.datasets import load_diabetes, load_digits, load_wine, make_classification, make_moons

ROOT = Path(__file__).resolve().parents[1]
PLAN = {p["week"]: p for p in json.loads((ROOT / "course_plan.json").read_text())}


def clean(s):
    return textwrap.dedent(s).strip() + "\n"


class Notebook:
    def __init__(self):
        self.cells = []

    def m(self, text):
        self.cells.append({"cell_type": "markdown", "metadata": {}, "source": clean(text)})
        return self

    def c(self, text):
        self.cells.append({"cell_type": "code", "metadata": {}, "source": clean(text),
                           "execution_count": None, "outputs": []})
        return self

    def save(self, week, filename, homework=False):
        folder = ROOT / PLAN[week]["folder"] / ("homework" if homework else "practice")
        folder.mkdir(exist_ok=True, parents=True)
        for i, cell in enumerate(self.cells):
            cell["id"] = hashlib.sha1((filename + str(i)).encode()).hexdigest()[:12]
        obj = {"cells": self.cells, "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.12"},
            "course": {"title": "Tech Orda course authored by Gizatov A. S.",
                       "week": week, "offline": True, "role": "starter" if homework else "worked_lab"}
        }, "nbformat": 4, "nbformat_minor": 5}
        path = folder / filename
        path.write_text(json.dumps(obj, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        return filename


def intro(n, week, title, goals, duration="108 минут практики (2 × 54 минуты)"):
    n.m(f"""
    # Неделя {week:02d}. {title}

    **Tech Orda · Gizatov A. S. · beginner ML/AI · Python 3**

    **Практика:** {duration}. На неделе также 72 минуты разбора теории: всего
    2 занятия × 90 минут = 4 академических часа. Домашнее задание выполняется отдельно.

    **Результат:** {goals}

    Ячейки идут от постановки задачи и описательной аналитики к алгоритму,
    проверке и интерпретации. Сначала предскажите результат ячейки, затем запускайте.
    Данные уже находятся в `../datasets`; интернет, GPU и API-ключи не нужны.
    Запуск: **Restart Kernel → Run All**. Зависимости устанавливаются заранее
    по инструкции в корне репозитория; из notebook ничего не устанавливается.
    """)


def setup(n, week, extra=""):
    n.c(f"""
    # Ограничиваем число потоков: небольшие учебные задачи запускаются на CPU.
    import os
    for variable in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
        os.environ.setdefault(variable, "1")
    from pathlib import Path
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from IPython.display import display
    from sklearn.model_selection import train_test_split

    SEED = 42
    rng = np.random.default_rng(SEED)
    # Поддерживается запуск из корня репозитория, practice/ и homework/.
    ROOT = next((p for p in [Path.cwd(), *Path.cwd().parents]
                 if (p / "course_plan.json").exists()), None)
    if ROOT is None:
        raise FileNotFoundError("Откройте notebook внутри клонированного репозитория")
    WEEK = ROOT / {PLAN[week]['folder']!r}
    DATA = WEEK / "datasets"
    plt.rcParams.update({{"figure.figsize": (8, 4), "axes.grid": True,
                          "grid.alpha": 0.2, "font.size": 10}})
    {extra}
    """)


def load_split(n, dataset, regression=False, binary=False):
    target = '(df["target"] == 0).astype(int)' if binary else 'df["target"]'
    strat = "" if regression else ", stratify=y"
    n.m("""
    ## Данные и граница между обучением и проверкой

    `sample_id` нужен для аудита разделения, **не для обучения**. `target` — ответ;
    его нельзя включать в признаки. Проверки схемы выполняем для всего CSV,
    а содержательный EDA — только для обучающей части. Test откроем после фиксации
    модели и правила принятия решений. Фиксированный seed делает опыт повторяемым,
    но не превращает одно разделение в доказательство универсальности результата.
    """)
    n.c(f"""
    df = pd.read_csv(DATA / {dataset!r}).set_index("sample_id")
    assert df.index.is_unique and df.notna().all().all()
    X = df.drop(columns="target")
    y = {target}
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=SEED{strat})
    assert set(X_train.index).isdisjoint(X_test.index)
    assert "target" not in X_train and "sample_id" not in X_train
    print({{"train": X_train.shape, "sealed_test": X_test.shape}})
    display(X_train.head(3))
    """)


def dataset_file(week, name, frame, desc, dictionary, urls, synthetic=False, extra=""):
    folder = ROOT / PLAN[week]["folder"] / "datasets"
    folder.mkdir(exist_ok=True, parents=True)
    data = frame.copy()
    data.insert(0, "sample_id", np.arange(len(data)))
    path = folder / name
    data.to_csv(path, index=False, float_format="%.10g")
    meta = {"file": name, "rows": len(data), "columns": list(data.columns),
            "source_type": "synthetic" if synthetic else "packaged_real_dataset",
            "exported_with_scikit_learn": sklearn.__version__, "seed": 42 if synthetic else None,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "source_urls": urls}
    (folder / (Path(name).stem + "_metadata.json")).write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n")
    readme = folder / "README.md"
    if not readme.exists():
        readme.write_text("# Данные недели\n\nВсе CSV хранятся локально и не требуют скачивания при запуске.\n", encoding="utf-8")
    block = f"\n## `{name}`\n\n{desc}\n\n" + ("**Синтетические данные.** Это учебная генерация, не наблюдения реальных людей или организаций.\n\n" if synthetic else "**Реальные учебные данные.** CSV — экспорт комплекта scikit-learn; преобразования указаны ниже.\n\n")
    block += f"Размер: **{len(data)} строк × {len(data.columns)} столбцов**; разделитель — запятая; UTF-8. Пропуски не добавлены. `sample_id` — добавленный локальный номер строки, не исходный идентификатор.\n\n"
    block += "| Столбец | Смысл и допустимые значения |\n|---|---|\n| `sample_id` | Уникальный целый индекс экспорта; исключить из модели. |\n"
    block += "".join(f"| `{key}` | {value} |\n" for key, value in dictionary.items())
    block += "\n" + extra + "\n\nИсточники и происхождение:\n\n" + "".join(f"- <{url}>\n" for url in urls)
    block += "\nSHA-256, версия экспортера и схема сохранены в соседнем `*_metadata.json`. Права исходных наборов остаются у их авторов; авторство курса не означает авторство данных.\n"
    with readme.open("a", encoding="utf-8") as f:
        f.write(block)


WINE_DICT = {
    "alcohol": "Содержание алкоголя, исходная числовая шкала UCI.",
    "malic_acid": "Яблочная кислота.", "ash": "Зольность.",
    "alcalinity_of_ash": "Щёлочность золы.", "magnesium": "Магний.",
    "total_phenols": "Общее содержание фенолов.", "flavanoids": "Флаваноиды.",
    "nonflavanoid_phenols": "Нефлаваноидные фенолы.", "proanthocyanins": "Проантоцианины.",
    "color_intensity": "Интенсивность окраски.", "hue": "Оттенок.",
    "od280/od315_of_diluted_wines": "Отношение оптических плотностей OD280/OD315.",
    "proline": "Пролин.", "target": "Класс культивара 0, 1 или 2; исходные UCI-коды 1–3 сдвинуты scikit-learn на −1."
}
DIAB_DICT = {
    "age": "Возраст в годах, raw-шкала.", "sex": "Исходный закодированный пол; не трактовать числовую разницу как меру.",
    "bmi": "Индекс массы тела.", "bp": "Среднее артериальное давление, исходная шкала.",
    "s1": "Общий холестерин сыворотки (tc).", "s2": "Липопротеины низкой плотности (ldl).",
    "s3": "Липопротеины высокой плотности (hdl).", "s4": "Отношение общего холестерина к HDL (tch).",
    "s5": "Показатель ltg; документация описывает его как возможно логарифм триглицеридов.",
    "s6": "Показатель сахара крови (glu).", "target": "Численная мера прогрессирования через год; непрерывная цель регрессии, не диагноз."
}


def export_datasets():
    for week in range(9, 18):
        folder = ROOT / PLAN[week]["folder"] / "datasets"
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "README.md").write_text("# Данные недели\n\nCSV хранятся локально. Для моделирования используйте только признаки, указанные ниже.\n", encoding="utf-8")
    wine = load_wine(as_frame=True).frame
    diabetes = load_diabetes(as_frame=True, scaled=False).frame
    for week in [9, 13, 16]:
        dataset_file(week, "diabetes_raw.csv", diabetes,
            "Набор Diabetes: 442 наблюдения, используемые в примере регрессии Efron, Hastie, Johnstone и Tibshirani (2004). Экспорт `load_diabetes(as_frame=True, scaled=False)`: глобальная нормализация scikit-learn отключена, scaler обучается внутри train/CV.",
            DIAB_DICT, ["https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_diabetes.html",
                        "https://www4.stat.ncsu.edu/~boos/var.select/diabetes.html",
                        "https://hastie.su.domains/Papers/LARS/LeastAngle_2002.pdf"],
            extra="Исходные единицы всех лабораторных показателей в карточке scikit-learn не уточнены; их не выдумываем. Набор используется только как компактный учебный benchmark; лабораторные модели не предназначены для решений о здоровье.")
    for week in [10, 11, 12, 14]:
        dataset_file(week, "wine.csv", wine,
            "Wine Recognition (UCI): результаты химического анализа 178 образцов трёх культиваров из одного региона Италии. Исходные владельцы: M. Forina et al., PARVUS. Экспорт `load_wine(as_frame=True)` без изменения признаков.",
            WINE_DICT, ["https://archive.ics.uci.edu/dataset/109/wine",
                        "https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_wine.html"],
            extra="Числовые признаки оставлены в исходных шкалах; единицы не дополняются догадками. Это задача распознавания культивара по химическим измерениям, не оценка качества напитка. В неделе 10 бинарная цель `target == 0` создаётся в notebook; исходный `target` затем исключается из X.")
    xm, ym = make_moons(n_samples=450, noise=0.075, random_state=42)
    moons = pd.DataFrame(xm, columns=["x1", "x2"])
    moons["target"] = ym
    dataset_file(14, "moons_synthetic.csv", moons,
        "Две вложенные дуги с шумом: `make_moons(n_samples=450, noise=0.075, random_state=42)`.",
        {"x1": "Первая безразмерная координата.", "x2": "Вторая безразмерная координата.",
         "target": "Исходная дуга 0/1; скрыть при кластеризации, использовать только для последующего внешнего аудита."},
        ["https://scikit-learn.org/stable/modules/generated/sklearn.datasets.make_moons.html"], synthetic=True)
    xc, yc = make_classification(n_samples=1000, n_features=8, n_informative=4,
        n_redundant=2, weights=[0.88, 0.12], class_sep=1.1, flip_y=0.02,
        shuffle=False, random_state=42)
    cls = pd.DataFrame(xc, columns=[f"x{i}" for i in range(8)])
    cls["target"] = yc
    dataset_file(15, "imbalanced_synthetic.csv", cls,
        "Синтетическая редкая положительная категория: `make_classification(n_samples=1000, n_features=8, n_informative=4, n_redundant=2, weights=[0.88,0.12], class_sep=1.1, flip_y=0.02, shuffle=False, random_state=42)`. Все параметры зафиксированы.",
        {**{f"x{i}": ("Информативная безразмерная координата." if i < 4 else "Линейная комбинация информативных координат." if i < 6 else "Случайная шумовая координата.") for i in range(8)},
         "target": "Синтетическая метка 0/1; 1 — редкий положительный класс."},
        ["https://scikit-learn.org/stable/modules/generated/sklearn.datasets.make_classification.html"], synthetic=True,
        extra="Доля класса 1 близка к 12%, но может отличаться из-за генерации и label noise. Стоимости FP/FN в лабораторной — учебные допущения, не реальные бизнес-данные.")
    digits = load_digits(as_frame=True).frame
    dataset_file(17, "digits_8x8.csv", digits,
        "Optical Recognition of Handwritten Digits, E. Alpaydin / C. Kaynak: scikit-learn включает 1797 изображений из тестовой части исходного UCI набора. Экспорт `load_digits(as_frame=True)`.",
        {"pixel_0_0 … pixel_7_7": "64 столбца: интенсивность пикселя в строке r и столбце c изображения 8×8, целые 0…16. Порядок — построчно (row-major).", "target": "Изображённая цифра, целое 0…9."},
        ["https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits",
         "https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html"],
        extra="Наша train/validation/test-разбивка выполняется внутри этих 1797 строк и не совпадает с исходным UCI benchmark. Идентификаторы автора почерка здесь отсутствуют: результаты случайной разбивки не доказывают качество на новых авторах. Деление пикселей на 16 опирается на известную схему данных и не обучается на test.")


def week09():
    n = Notebook()
    intro(n, 9, "Линейная регрессия: от формулы до проверяемого прогноза",
          "вывести градиент MSE, реализовать два решения least squares, сравнить их со scikit-learn и проверить, что регуляризация выбрана без test.")
    setup(n, 9)
    load_split(n, "diabetes_raw.csv", regression=True)
    n.m("""
    ## 1. Описательная аналитика обучающей выборки

    До модели выясним, что означает цель и в каких шкалах измерены признаки.
    Среднее и медиана описывают центр, стандартное отклонение — разброс;
    корреляция измеряет линейную связь, но не доказывает причинность.
    **Вопрос:** почему нельзя сравнивать величины raw-коэффициентов BMI и возраста
    без учёта единиц измерения?
    """)
    n.c("""
    display(X_train.describe().T.round(2))
    display(y_train.describe().to_frame("target"))
    fig, axes = plt.subplots(1, 3, figsize=(13, 3.5))
    y_train.hist(bins=18, ax=axes[0]); axes[0].set(title="Train: target", xlabel="Target", ylabel="Count")
    axes[1].scatter(X_train["bmi"], y_train, alpha=0.55)
    axes[1].set(title="Train: BMI and target", xlabel="BMI", ylabel="Target")
    corr = X_train.join(y_train).corr()["target"].drop("target").sort_values()
    corr.plot.barh(ax=axes[2]); axes[2].set(title="Train Pearson correlation", xlabel="r")
    plt.tight_layout(); plt.show()
    """)
    n.m(r"""
    ## 2. Модель, функция потерь и градиент

    Допишем к матрице столбец единиц: $A=[1,X]$. Тогда $\hat y=A\theta$,
    где $\theta_0$ — свободный член.

    $$J(\theta)=\frac1n\|A\theta-y\|_2^2,\qquad
    \nabla J(\theta)=\frac{2}{n}A^\top(A\theta-y).$$

    Обновление: $\theta\leftarrow\theta-\eta\nabla J$.
    Нормальные уравнения полезны для вывода, но явно обращать $A^TA$ численно
    невыгодно: `lstsq` использует более устойчивое разложение.
    Стандартизация обучается **только на train**, цель нормируем для наглядной шкалы loss.
    """)
    n.c("""
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler().fit(X_train)
    A = np.column_stack([np.ones(len(X_train)), scaler.transform(X_train)])
    target_mean, target_std = y_train.mean(), y_train.std(ddof=0)
    z = (y_train.to_numpy() - target_mean) / target_std
    theta_ls, _, rank, singular_values = np.linalg.lstsq(A, z, rcond=None)
    assert rank == A.shape[1]
    print("Матрица A:", A.shape, "; condition number:", round(np.linalg.cond(A), 2))
    """)
    n.m("""
    ## 3. Градиентный спуск с контролем сходимости

    Для квадратичной функции шаг можно связать с максимальным собственным числом
    гессиана. Возьмём консервативный шаг `0.9 / L`, где `L` — норма гессиана.
    Используем 6000 дешёвых векторных шагов: небольшой пример нужен для понимания,
    в рабочем pipeline обычно выбирают библиотечный оптимизатор.
    """)
    n.c("""
    theta_gd = np.zeros(A.shape[1])
    lipschitz = 2 * np.linalg.norm(A, ord=2) ** 2 / len(A)
    learning_rate = 0.9 / lipschitz
    loss_history = []
    for step in range(6000):
        residual = A @ theta_gd - z
        gradient = 2 * A.T @ residual / len(A)
        theta_gd -= learning_rate * gradient
        loss_history.append(np.mean((A @ theta_gd - z) ** 2))
    assert np.isfinite(loss_history).all()
    assert loss_history[-1] < loss_history[0]
    assert np.max(np.abs(A @ theta_gd - A @ theta_ls)) < 0.02
    print("MSE (normalized):", loss_history[-1], "; шаг:", learning_rate)
    """)
    n.c("""
    plt.plot(np.arange(1, len(loss_history)+1), loss_history, label="Gradient descent")
    plt.axhline(np.mean((A @ theta_ls - z) ** 2), color="crimson", ls="--", label="Least squares")
    plt.xscale("log"); plt.xlabel("Iteration (log axis)"); plt.ylabel("Normalized train MSE")
    plt.title("Convergence to the least-squares solution"); plt.legend(); plt.show()
    """)
    n.m("""
    ## 4. Проверка градиента через конечные разности

    Сравним формулу с изменением loss при небольшом сдвиге одного коэффициента.
    Такая проверка обнаруживает потерянный множитель 2, знак или неверный axis.
    Проверять градиент на точке оптимума неудобно: там обе величины почти нулевые.
    """)
    n.c("""
    probe = np.linspace(-0.2, 0.2, A.shape[1])
    analytic = 2 * A.T @ (A @ probe - z) / len(A)
    numeric = np.zeros_like(probe)
    eps = 1e-6
    for j in range(len(probe)):
        shift = np.zeros_like(probe); shift[j] = eps
        numeric[j] = (np.mean((A @ (probe + shift) - z) ** 2)
                      - np.mean((A @ (probe - shift) - z) ** 2)) / (2 * eps)
    assert np.allclose(analytic, numeric, atol=1e-7)
    print("Максимальная ошибка градиента:", np.max(np.abs(analytic - numeric)))
    """)
    n.m("""
    ## 5. Библиотечный baseline и CV внутри train

    `DummyRegressor` предсказывает среднее train. `Pipeline` заново обучает scaler
    в каждом fold. У `neg_root_mean_squared_error` знак отрицательный, потому что
    scoring API максимизирует оценку. Возвращаем знак, чтобы читать ошибку в единицах цели.
    """)
    n.c("""
    from sklearn.pipeline import make_pipeline
    from sklearn.linear_model import LinearRegression, Ridge
    from sklearn.dummy import DummyRegressor
    from sklearn.model_selection import KFold, cross_val_score, GridSearchCV
    cv = KFold(n_splits=5, shuffle=True, random_state=SEED)
    models = {"mean baseline": DummyRegressor(),
              "OLS": make_pipeline(StandardScaler(), LinearRegression())}
    rows = []
    for name, model in models.items():
        scores = -cross_val_score(model, X_train, y_train, cv=cv,
                                  scoring="neg_root_mean_squared_error", n_jobs=1)
        rows.append({"model": name, "CV RMSE mean": scores.mean(), "CV fold SD": scores.std()})
    display(pd.DataFrame(rows).round(2))
    """)
    n.m(r"""
    ## 6. Ridge: обмен небольшого смещения на устойчивость

    scikit-learn минимизирует $\|y-Xw\|_2^2+\alpha\|w\|_2^2$.
    Свободный член не штрафуется. Масштабировать признаки нужно до Ridge,
    иначе одинаковый штраф имеет разный смысл в разных единицах.
    Сетку `alpha` выбираем заранее; test в подборе не участвует.
    """)
    n.c("""
    ridge_search = GridSearchCV(
        make_pipeline(StandardScaler(), Ridge()),
        {"ridge__alpha": [0.01, 0.1, 1.0, 10.0, 100.0, 1000.0]},
        cv=cv, scoring="neg_root_mean_squared_error", n_jobs=1)
    ridge_search.fit(X_train, y_train)
    cv_table = pd.DataFrame(ridge_search.cv_results_)
    display(cv_table[["param_ridge__alpha", "mean_test_score", "std_test_score"]]
            .rename(columns={"mean_test_score": "negative_CV_RMSE"}))
    print("Зафиксировали alpha:", ridge_search.best_params_)
    """)
    n.c("""
    # Численная проверка своей least-squares реализации относительно sklearn на train.
    ols = make_pipeline(StandardScaler(), LinearRegression()).fit(X_train, y_train)
    scratch_train = (A @ theta_ls) * target_std + target_mean
    assert np.allclose(scratch_train, ols.predict(X_train), atol=1e-7)
    coefficients = pd.Series(ols[-1].coef_, index=X_train.columns).sort_values()
    coefficients.plot.barh(color="steelblue")
    plt.xlabel("Target units per +1 train standard deviation")
    plt.title("OLS coefficients: association, not causality"); plt.show()
    """)
    n.m("""
    ## 7. Открываем test один раз

    Список моделей, метрики и alpha уже зафиксированы. Теперь проверим baseline,
    OLS и выбранный Ridge на одном holdout. Это финальный отчёт, а не очередной
    раунд выбора. `R²` может быть отрицательным: модель может проиграть константе.
    """)
    n.c("""
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    final_models = {"mean baseline": DummyRegressor().fit(X_train, y_train),
                    "OLS": ols, "Ridge (CV choice)": ridge_search.best_estimator_}
    final_rows = []
    for name, model in final_models.items():
        pred = model.predict(X_test)
        final_rows.append({"model": name, "MAE": mean_absolute_error(y_test, pred),
                           "RMSE": np.sqrt(mean_squared_error(y_test, pred)),
                           "R2": r2_score(y_test, pred)})
    display(pd.DataFrame(final_rows).round(3))
    test_pred = ridge_search.predict(X_test)
    assert test_pred.shape == y_test.shape and np.isfinite(test_pred).all()
    """)
    n.m("""
    ## 8. Диагностика ошибок

    На графике остатков ищем кривизну, рост разброса и отдельные крупные ошибки.
    Test-диагностика помогает сформировать **гипотезу для следующего эксперимента**;
    если изменить модель после этого графика, текущий test уже не независимый финальный экзамен.
    """)
    n.c("""
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    axes[0].scatter(y_test, test_pred, alpha=0.7)
    low, high = min(y_test.min(), test_pred.min()), max(y_test.max(), test_pred.max())
    axes[0].plot([low, high], [low, high], "r--")
    axes[0].set(xlabel="Observed", ylabel="Predicted", title="Final holdout predictions")
    residuals = y_test.to_numpy() - test_pred
    axes[1].scatter(test_pred, residuals, alpha=0.7); axes[1].axhline(0, color="r", ls="--")
    axes[1].set(xlabel="Predicted", ylabel="Observed - predicted", title="Residual diagnostic")
    plt.tight_layout(); plt.show()
    """)
    n.m("""
    ## Обсуждение и перенос

    1. Почему равенство предсказаний двух решателей полезнее простого утверждения «код работает»?
    2. Объясните разницу между train MSE, средним CV RMSE и итоговым test RMSE.
    3. Какие признаки могут быть связаны друг с другом, и как это влияет на коэффициенты?
    4. Чем предсказание отличается от оценки причинного эффекта изменения BMI?

    **Проверка готовности:** есть baseline, корректный split, численно проверенный градиент,
    CV внутри train, единственный финальный holdout и ограничения интерпретации.

    Первоисточники: [Stanford CS229 notes](https://cs229.stanford.edu/main_notes.pdf),
    [scikit-learn linear models](https://scikit-learn.org/stable/modules/linear_model.html),
    [Ridge API](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html),
    [предотвращение утечки](https://scikit-learn.org/stable/common_pitfalls.html).
    Код и русский учебный разбор написаны для курса; это не скопированный университетский notebook.
    """)
    n.save(9, "01_linear_regression_from_scratch.ipynb")


def week10():
    n = Notebook()
    intro(n, 10, "Логистическая регрессия и kNN: вероятность, расстояние, решение",
          "построить бинарный классификатор культивара 0, сравнить логистическую модель и kNN, выбрать порог на validation и объяснить роль масштаба признаков.")
    setup(n, 10)
    load_split(n, "wine.csv", binary=True)
    n.m("""
    ## 1. Формулировка бинарной задачи и EDA

    Положительный класс — `target == 0`; остальные два культивара объединяем в 0.
    Это **учебное изменение исходной задачи**, а не новая метка в оригинальном наборе.
    Три исходных класса не превращаются в упорядоченную числовую величину.
    Внутри train выделим validation: он понадобится для выбора порога.
    """)
    n.c("""
    X_fit, X_val, y_fit, y_val = train_test_split(
        X_train, y_train, test_size=0.25, stratify=y_train, random_state=SEED + 1)
    assert set(X_fit.index).isdisjoint(X_val.index)
    display(X_fit.describe().T[["mean", "std", "min", "max"]].round(2))
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.5))
    y_fit.value_counts().sort_index().plot.bar(ax=axes[0], rot=0)
    axes[0].set(title="Fit split class counts", xlabel="Is cultivar 0?", ylabel="Count")
    for label in [0, 1]:
        axes[1].hist(X_fit.loc[y_fit == label, "alcohol"], alpha=0.5, bins=12, label=f"class {label}")
    axes[1].set(title="Alcohol distribution: fit split", xlabel="Alcohol", ylabel="Count")
    axes[1].legend(); plt.tight_layout(); plt.show()
    """)
    n.m(r"""
    ## 2. Почему логистическая регрессия — классификатор

    $$z=w^Tx+b,\quad p(y=1\mid x)=\sigma(z)=\frac{1}{1+e^{-z}}.$$
    $$L=-\frac1n\sum_i[y_i\log p_i+(1-y_i)\log(1-p_i)].$$

    Модель оценивает вероятность; отдельное правило `p >= threshold` выдаёт класс.
    Log loss штрафует уверенные ошибочные вероятности сильнее. Численно устойчивый
    binary log loss можно записать через `logaddexp`, без `log(0)`.
    """)
    n.c("""
    from scipy.special import expit
    z_grid = np.linspace(-8, 8, 250)
    def binary_loss_from_logits(y_true, logits):
        return np.mean(np.logaddexp(0.0, logits) - np.asarray(y_true) * logits)
    assert np.isfinite(binary_loss_from_logits(np.array([0, 1]), np.array([-1000., 1000.])))
    plt.plot(z_grid, expit(z_grid)); plt.axhline(0.5, ls="--", color="gray")
    plt.xlabel("Logit z"); plt.ylabel("P(class=1)"); plt.title("Sigmoid"); plt.show()
    """)
    n.m("""
    ## 3. Базовая логистическая модель

    Scaler находится внутри Pipeline. Коэффициенты регуляризуются; `C` — обратная
    сила регуляризации. Для первой модели фиксируем `C=1`, не подбирая его на test.
    Отдельно обучаем baseline, который всегда выбирает наиболее частый класс.
    """)
    n.c("""
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LogisticRegression
    from sklearn.dummy import DummyClassifier
    from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, log_loss
    logistic = make_pipeline(StandardScaler(), LogisticRegression(C=1.0, max_iter=1500, random_state=SEED))
    logistic.fit(X_fit, y_fit)
    baseline = DummyClassifier(strategy="most_frequent").fit(X_fit, y_fit)
    val_probability = logistic.predict_proba(X_val)[:, 1]
    assert np.all((val_probability >= 0) & (val_probability <= 1))
    assert np.allclose(logistic.predict_proba(X_val).sum(axis=1), 1)
    print("Baseline validation accuracy:", accuracy_score(y_val, baseline.predict(X_val)))
    print("Logistic validation log loss:", log_loss(y_val, val_probability))
    """)
    n.m("""
    ## 4. Порог — решение с ценой ошибок

    Для учебного сценария пропуск положительного образца (FN) стоит 3 условные
    единицы, ложный сигнал (FP) — 1. Это явное допущение, не свойство Wine.
    Выберем порог на validation по минимальной стоимости. Самые низкие значения
    на маленькой validation могут быть случайностью; используем заранее заданную сетку.
    """)
    n.c("""
    from sklearn.metrics import confusion_matrix
    thresholds = np.linspace(0.1, 0.9, 17)
    threshold_rows = []
    for threshold in thresholds:
        pred = (val_probability >= threshold).astype(int)
        tn, fp, fn, tp = confusion_matrix(y_val, pred, labels=[0, 1]).ravel()
        threshold_rows.append({"threshold": threshold, "FP": fp, "FN": fn,
                               "cost_per_sample": (fp + 3 * fn) / len(y_val)})
    threshold_table = pd.DataFrame(threshold_rows)
    # При равенстве стоимости выбираем порог ближе к 0.5: правило задано заранее.
    selected_threshold = threshold_table.assign(distance=(threshold_table.threshold - 0.5).abs())\
        .sort_values(["cost_per_sample", "distance"]).iloc[0]["threshold"]
    display(threshold_table)
    print("Зафиксированный порог:", selected_threshold)
    """)
    n.c("""
    plt.plot(threshold_table.threshold, threshold_table.cost_per_sample, marker="o")
    plt.axvline(selected_threshold, color="crimson", ls="--")
    plt.xlabel("Probability threshold"); plt.ylabel("Validation cost per sample")
    plt.title("A model score and a decision rule are separate"); plt.show()
    """)
    n.m(r"""
    ## 5. kNN: учимся читать расстояния

    $$d(x,x')=\sqrt{\sum_j(x_j-x'_j)^2},\qquad
    \hat p(y=1\mid x)=\frac1k\sum_{i\in N_k(x)}y_i.$$

    Если шкала `proline` на порядки крупнее `hue`, она может определять соседей.
    На одной validation сравним заранее заданные варианты: raw kNN и scaled kNN.
    Это объяснительный опыт; k выбирается дальше на CV, а не по test.
    """)
    n.c("""
    from sklearn.neighbors import KNeighborsClassifier
    raw_knn = KNeighborsClassifier(n_neighbors=5).fit(X_fit, y_fit)
    scaled_knn = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5)).fit(X_fit, y_fit)
    comparison = pd.DataFrame([
        {"model": "raw kNN, k=5", "validation balanced accuracy": balanced_accuracy_score(y_val, raw_knn.predict(X_val))},
        {"model": "scaled kNN, k=5", "validation balanced accuracy": balanced_accuracy_score(y_val, scaled_knn.predict(X_val))}])
    display(comparison)
    """)
    n.m("""
    ## 6. Один прогноз kNN вручную

    Найдём соседей первого **validation**, а не test, объекта. Средняя метка
    соседей должна совпасть с `predict_proba` при uniform weights. Расстояния
    вычисляются после scaler, который видел только fit.
    """)
    n.c("""
    scaled_fit = scaled_knn[0].transform(X_fit)
    query = scaled_knn[0].transform(X_val.iloc[[0]])[0]
    distances = np.linalg.norm(scaled_fit - query, axis=1)
    neighbor_positions = np.argsort(distances)[:5]
    manual_probability = y_fit.iloc[neighbor_positions].mean()
    library_probability = scaled_knn.predict_proba(X_val.iloc[[0]])[0, 1]
    assert np.isclose(manual_probability, library_probability)
    display(pd.DataFrame({"sample_id": X_fit.index[neighbor_positions],
                          "distance": distances[neighbor_positions],
                          "label": y_fit.iloc[neighbor_positions].to_numpy()}))
    print("P(class=1):", manual_probability)
    """)
    n.m("""
    ## 7. Подбор k на CV только внутри train

    На каждом fold scaler переобучается. Слишком маленькое k повышает чувствительность
    к шуму; большое k сглаживает границу. Сравниваем mean и разброс, а не только победителя.
    После CV kNN переобучится на всём train. Logistic сохраняем в виде `fit + threshold`:
    переобучение после подбора порога может изменить распределение вероятностей.
    """)
    n.c("""
    from sklearn.model_selection import StratifiedKFold, GridSearchCV
    cv = StratifiedKFold(n_splits=4, shuffle=True, random_state=SEED)
    search = GridSearchCV(make_pipeline(StandardScaler(), KNeighborsClassifier()),
                          {"kneighborsclassifier__n_neighbors": [3, 5, 9, 15, 25]},
                          cv=cv, scoring="balanced_accuracy", n_jobs=1)
    search.fit(X_train, y_train)
    results = pd.DataFrame(search.cv_results_)
    plt.errorbar(results["param_kneighborsclassifier__n_neighbors"].astype(int),
                 results.mean_test_score, yerr=results.std_test_score, marker="o", capsize=3)
    plt.xlabel("k"); plt.ylabel("CV balanced accuracy ± fold SD")
    plt.title("Choosing k inside the training partition"); plt.show()
    print(search.best_params_)
    """)
    n.m("""
    ## 8. Финальный holdout: фиксируем обе модели

    Мы не объявляем победителя по test и не меняем порог после просмотра.
    Logistic обучалась на fit; kNN после CV использует полный train: бюджеты
    обучения отличаются, это честно отмечаем. Test невелик, поэтому одна ошибка
    может заметно изменить итоговую оценку.
    """)
    n.c("""
    from sklearn.metrics import roc_auc_score, ConfusionMatrixDisplay, RocCurveDisplay
    p_logistic = logistic.predict_proba(X_test)[:, 1]
    p_knn = search.predict_proba(X_test)[:, 1]
    rows = []
    for name, probabilities, threshold in [
        ("Logistic + validation threshold", p_logistic, selected_threshold),
        ("Scaled kNN + CV", p_knn, 0.5)]:
        pred = (probabilities >= threshold).astype(int)
        rows.append({"model": name, "threshold": threshold,
                     "accuracy": accuracy_score(y_test, pred),
                     "balanced_accuracy": balanced_accuracy_score(y_test, pred),
                     "F1": f1_score(y_test, pred, zero_division=0),
                     "ROC AUC": roc_auc_score(y_test, probabilities),
                     "log_loss": log_loss(y_test, probabilities)})
    display(pd.DataFrame(rows).round(3))
    assert np.isfinite(pd.DataFrame(rows).select_dtypes("number")).all().all()
    """)
    n.c("""
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    ConfusionMatrixDisplay.from_predictions(y_test, (p_logistic >= selected_threshold).astype(int),
                                            display_labels=["other", "cultivar 0"], ax=axes[0], colorbar=False)
    axes[0].set_title("Logistic: fixed decision threshold")
    RocCurveDisplay.from_predictions(y_test, p_logistic, name="Logistic", ax=axes[1])
    RocCurveDisplay.from_predictions(y_test, p_knn, name="kNN", ax=axes[1])
    axes[1].plot([0, 1], [0, 1], "k--", alpha=0.4)
    plt.tight_layout(); plt.show()
    """)
    n.m("""
    ## Самопроверка

    - При изменении порога меняется ли ROC AUC для уже рассчитанных вероятностей? Почему?
    - Почему accuracy может скрывать пропуски редкого класса?
    - Что произойдёт с raw kNN, если измерять один признак в тысячных долях исходной единицы?
    - Объясните, почему `target` исходной трёхклассовой задачи нельзя оставить в X.

    Источники: [Stanford CS229 notes](https://cs229.stanford.edu/main_notes.pdf),
    [LogisticRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html),
    [nearest neighbors](https://scikit-learn.org/stable/modules/neighbors.html),
    [decision threshold](https://scikit-learn.org/stable/modules/classification_threshold.html).
    """)
    n.save(10, "01_logistic_regression_and_knn.ipynb")


def week11():
    n = Notebook()
    intro(n, 11, "Деревья решений и SVM: два способа построить границу",
          "посчитать уменьшение Gini, визуализировать дерево, понять margin и RBF-ядро, сравнить модели на одинаковых CV folds и открыть test после выбора.")
    setup(n, 11)
    load_split(n, "wine.csv")
    n.m("""
    ## 1. EDA: класс и масштабы признаков

    На этой неделе решаем исходную задачу из **трёх классов**. Частоты классов
    не одинаковы, поэтому основной критерий выбора — macro F1: каждый класс
    получает одинаковый вес. Tree делит шкалы порогами, SVM чувствителен к масштабу.
    """)
    n.c("""
    display(X_train.describe().T[["mean", "std", "min", "max"]].round(2))
    display(y_train.value_counts().sort_index().rename("train_count"))
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.5))
    for label in sorted(y_train.unique()):
        subset = X_train.loc[y_train == label]
        axes[0].scatter(subset.alcohol, subset.flavanoids, label=f"class {label}", alpha=0.7)
    axes[0].set(xlabel="Alcohol", ylabel="Flavanoids", title="Train class structure"); axes[0].legend()
    X_train.std().sort_values().plot.barh(ax=axes[1]); axes[1].set(xscale="log", title="Train feature SD", xlabel="SD (log axis)")
    plt.tight_layout(); plt.show()
    """)
    n.m(r"""
    ## 2. Как дерево выбирает разделение

    $$G(S)=1-\sum_{k=1}^{K}p_k^2,$$
    $$\Delta G=G(S)-\frac{|S_L|}{|S|}G(S_L)-\frac{|S_R|}{|S|}G(S_R).$$

    Проверим один признак и несколько порогов вручную. Более крупное уменьшение
    impurity лучше разделяет **текущие обучающие данные**. Это ещё не гарантия
    лучшего качества на новых данных.
    """)
    n.c("""
    def gini(labels):
        proportions = np.bincount(np.asarray(labels, dtype=int), minlength=3) / len(labels)
        return 1 - np.sum(proportions ** 2)
    parent_gini = gini(y_train)
    split_rows = []
    for threshold in np.quantile(X_train["flavanoids"], [0.2, 0.4, 0.6, 0.8]):
        left = X_train["flavanoids"] <= threshold
        weighted = left.mean() * gini(y_train[left]) + (~left).mean() * gini(y_train[~left])
        split_rows.append({"threshold": threshold, "left_n": left.sum(),
                           "right_n": (~left).sum(), "gini_gain": parent_gini - weighted})
    assert np.isclose(gini(np.array([0, 0, 0])), 0)
    assert np.isclose(gini(np.array([0, 1, 2])), 2/3)
    display(pd.DataFrame(split_rows).round(3))
    """)
    n.m("""
    ## 3. Читаем настоящее дерево

    Начнём с глубины 2: ограничение делает правила обозримыми. В узле написаны
    признак, порог, impurity и количества наблюдений. Лист выдаёт распределение
    классов обучающих объектов; даже 100% в маленьком листе не означает уверенности
    о всей популяции.
    """)
    n.c("""
    from sklearn.tree import DecisionTreeClassifier, plot_tree, export_text
    small_tree = DecisionTreeClassifier(max_depth=2, min_samples_leaf=5, random_state=SEED)
    small_tree.fit(X_train, y_train)
    plt.figure(figsize=(14, 6))
    plot_tree(small_tree, feature_names=list(X_train.columns), class_names=["0", "1", "2"],
              filled=True, rounded=True, proportion=False, fontsize=9)
    plt.title("A readable training tree"); plt.show()
    print(export_text(small_tree, feature_names=list(X_train.columns), max_depth=2))
    """)
    n.m("""
    ## 4. Глубина и переобучение

    Рассмотрим train score и CV score при увеличении глубины. CV folds фиксированы
    и одинаковы для всех вариантов. Значения std по folds показывают нестабильность,
    но это не строгий доверительный интервал среднего качества.
    """)
    n.c("""
    from sklearn.model_selection import StratifiedKFold, cross_validate
    cv = StratifiedKFold(n_splits=4, shuffle=True, random_state=SEED)
    depth_rows = []
    for depth in [1, 2, 3, 4, 6, 10]:
        score = cross_validate(DecisionTreeClassifier(max_depth=depth, random_state=SEED),
                               X_train, y_train, cv=cv, scoring="f1_macro", return_train_score=True)
        depth_rows.append({"depth": depth, "train": score["train_score"].mean(),
                           "cv": score["test_score"].mean(), "cv_sd": score["test_score"].std()})
    depth_table = pd.DataFrame(depth_rows)
    plt.plot(depth_table.depth, depth_table.train, "o-", label="Train")
    plt.errorbar(depth_table.depth, depth_table.cv, yerr=depth_table.cv_sd, fmt="o-", label="CV", capsize=3)
    plt.xlabel("Maximum tree depth"); plt.ylabel("Macro F1"); plt.legend(); plt.show()
    """)
    n.m(r"""
    ## 5. SVM: широкий margin и штраф за нарушения

    Для бинарного случая с $y_i\in\{-1,+1\}$ линейный soft-margin SVM решает
    $$\min_{w,b}\frac12\|w\|^2+C\sum_i\max(0,1-y_i(w^Tx_i+b)).$$

    Большое `C` сильнее штрафует ошибки на train. RBF-ядро
    $K(x,x')=\exp(-\gamma\|x-x'\|^2)$ позволяет нелинейную границу.
    Большое `gamma` делает влияние отдельного образца более локальным.
    Для трёх классов `SVC` использует несколько бинарных задач.
    """)
    n.c("""
    margin = np.linspace(-2, 3, 200)
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.5))
    axes[0].plot(margin, np.maximum(0, 1-margin))
    axes[0].set(title="Hinge loss", xlabel="Signed margin y*f(x)", ylabel="Loss")
    distance = np.linspace(0, 4, 200)
    for gamma in [0.1, 1, 5]:
        axes[1].plot(distance, np.exp(-gamma * distance**2), label=f"gamma={gamma}")
    axes[1].set(title="RBF similarity", xlabel="Scaled distance", ylabel="Kernel value")
    axes[1].legend(); plt.tight_layout(); plt.show()
    """)
    n.m("""
    ## 6. Единый план сравнения

    Tree не требует StandardScaler для выбора осевых порогов. SVM получает scaler
    **внутри** pipeline. Сетки небольшие: задача недели — понять влияние параметров,
    а не перебрать тысячи комбинаций на 133 train-наблюдениях.
    """)
    n.c("""
    from sklearn.svm import SVC
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import GridSearchCV
    tree_search = GridSearchCV(DecisionTreeClassifier(random_state=SEED),
        {"max_depth": [2, 3, 5, None], "min_samples_leaf": [1, 5, 10]},
        scoring="f1_macro", cv=cv, n_jobs=1)
    svm_search = GridSearchCV(make_pipeline(StandardScaler(), SVC()),
        [{"svc__kernel": ["linear"], "svc__C": [0.1, 1, 10]},
         {"svc__kernel": ["rbf"], "svc__C": [0.1, 1, 10], "svc__gamma": ["scale", 0.01, 0.1]}],
        scoring="f1_macro", cv=cv, n_jobs=1)
    tree_search.fit(X_train, y_train); svm_search.fit(X_train, y_train)
    display(pd.DataFrame([
        {"family": "Tree", "best_CV_macro_F1": tree_search.best_score_, "params": tree_search.best_params_},
        {"family": "SVM", "best_CV_macro_F1": svm_search.best_score_, "params": svm_search.best_params_}]))
    selected = svm_search if svm_search.best_score_ >= tree_search.best_score_ else tree_search
    print("Семейство финальной модели выбрано по CV:", type(selected.best_estimator_).__name__)
    """)
    n.m("""
    ## 7. Геометрия на двух признаках — отдельный объяснительный опыт

    Картинку нельзя строить как проекцию границы полной 13-мерной модели: это была бы
    другая задача. Ниже **две новые учебные модели** обучаются только на `alcohol`
    и `flavanoids` train. Эта иллюстрация не участвует в финальном выборе.
    """)
    n.c("""
    features_2d = ["alcohol", "flavanoids"]
    two_dimensional = X_train[features_2d]
    models_2d = {"Tree depth=3": DecisionTreeClassifier(max_depth=3, random_state=SEED),
                 "Scaled RBF SVM": make_pipeline(StandardScaler(), SVC(C=1, gamma="scale"))}
    x_axis = np.linspace(two_dimensional.iloc[:, 0].min()-0.4, two_dimensional.iloc[:, 0].max()+0.4, 160)
    y_axis = np.linspace(two_dimensional.iloc[:, 1].min()-0.4, two_dimensional.iloc[:, 1].max()+0.4, 160)
    xx, yy = np.meshgrid(x_axis, y_axis)
    grid = pd.DataFrame(np.c_[xx.ravel(), yy.ravel()], columns=features_2d)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    for ax, (name, model) in zip(axes, models_2d.items()):
        model.fit(two_dimensional, y_train)
        ax.contourf(xx, yy, model.predict(grid).reshape(xx.shape), alpha=0.2, cmap="viridis")
        ax.scatter(two_dimensional.iloc[:, 0], two_dimensional.iloc[:, 1], c=y_train, cmap="viridis", edgecolor="k", s=25)
        ax.set(title=name, xlabel=features_2d[0], ylabel=features_2d[1])
    plt.tight_layout(); plt.show()
    """)
    n.m("""
    ## 8. Финальная оценка выбранной модели

    Test использован впервые. Сравним итоговый macro F1 с baseline. Даже если
    в этом небольшом holdout ошибок нет, нельзя заключать «100% на любом вине»:
    новый регион, прибор или способ измерения могут изменить распределение.
    """)
    n.c("""
    from sklearn.metrics import classification_report, f1_score, ConfusionMatrixDisplay
    from sklearn.dummy import DummyClassifier
    prediction = selected.predict(X_test)
    baseline = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
    print("Baseline test macro F1:", f1_score(y_test, baseline.predict(X_test), average="macro"))
    print(classification_report(y_test, prediction, zero_division=0))
    assert prediction.shape == y_test.shape and set(prediction).issubset({0, 1, 2})
    ConfusionMatrixDisplay.from_predictions(y_test, prediction, colorbar=False)
    plt.title("Final holdout: CV-selected model"); plt.show()
    """)
    n.m("""
    ## 9. Проверяем путь одного образца через дерево

    Для интерпретации берём первый train-образец. Сумма листовых вероятностей должна
    быть 1; число посещённых узлов не больше глубины + 1. Эти проверки относятся
    к устройству алгоритма, а не к гарантии качества.
    """)
    n.c("""
    example = X_train.iloc[[0]]
    node_ids = small_tree.decision_path(example).indices
    leaf_id = small_tree.apply(example)[0]
    assert leaf_id in node_ids
    assert len(node_ids) <= small_tree.get_depth() + 1
    assert np.isclose(small_tree.predict_proba(example).sum(), 1)
    print("Узлы пути:", node_ids, "; лист:", leaf_id)
    print("Вероятности в листе:", small_tree.predict_proba(example).round(3))
    """)
    n.m("""
    ## Вопросы для объяснения вслух

    1. Почему глубокое дерево может улучшать train F1 и ухудшать CV F1?
    2. Что будет с геометрией SVM при смене единиц одного признака без scaler?
    3. Чем `C` отличается от `gamma`? Покажите на hinge loss и RBF-графиках.
    4. Почему двумерная граница — отдельная модель, а не полное объяснение 13 признаков?

    Источники: [MIT 6.036 materials](https://ocw.mit.edu/courses/6-036-introduction-to-machine-learning-fall-2020/),
    [Stanford CS229 notes](https://cs229.stanford.edu/main_notes.pdf),
    [Decision Trees](https://scikit-learn.org/stable/modules/tree.html),
    [Support Vector Machines](https://scikit-learn.org/stable/modules/svm.html).
    """)
    n.save(11, "01_decision_trees_and_svm.ipynb")


def week12():
    n = Notebook()
    intro(n, 12, "Bagging, Random Forest и OOB: зачем усреднять деревья",
          "увидеть bootstrap-выборку, собрать небольшой ансамбль вручную, сравнить bagging и случайный лес, понять границы OOB и оценить устойчивость.")
    setup(n, 12)
    load_split(n, "wine.csv")
    n.m("""
    ## 1. EDA и baseline

    Продолжаем Wine, но эксперимент выполняем с нуля и с тем же фиксированным
    train/test split. Размер мал: главным ограничением становится вариативность
    оценки, а не время обучения. Деревья не требуют стандартизации для этой задачи.
    """)
    n.c("""
    display(X_train.describe().T.round(2))
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.5))
    y_train.value_counts().sort_index().plot.bar(ax=axes[0], rot=0)
    axes[0].set(title="Train class counts", xlabel="Cultivar", ylabel="Count")
    for label in sorted(y_train.unique()):
        axes[1].hist(X_train.loc[y_train == label, "flavanoids"], bins=10, alpha=0.5, label=str(label))
    axes[1].set(title="Train flavanoids distribution", xlabel="Flavanoids", ylabel="Count")
    axes[1].legend(title="Class"); plt.tight_layout(); plt.show()
    """)
    n.m(r"""
    ## 2. Bootstrap и out-of-bag

    Bootstrap выбирает $n$ строк из $n$ **с возвращением**. Вероятность, что строка
    ни разу не попадёт в выборку: $(1-1/n)^n\approx e^{-1}\approx0.368$.
    Такие строки — OOB для конкретного дерева. OOB у каждого дерева свой.
    Это не означает, что 36.8% исходных данных образуют один общий test.
    """)
    n.c("""
    n_train = len(X_train)
    sampled_positions = rng.integers(0, n_train, size=n_train)
    counts = np.bincount(sampled_positions, minlength=n_train)
    oob_positions = np.flatnonzero(counts == 0)
    assert counts.sum() == n_train and len(oob_positions) > 0
    print("Строк в bootstrap:", len(sampled_positions), "; уникальных:", np.count_nonzero(counts))
    print("Доля OOB:", len(oob_positions)/n_train, "; теоретически:", (1-1/n_train)**n_train)
    plt.hist(counts, bins=np.arange(counts.max()+2)-0.5)
    plt.xlabel("Times a train sample is drawn"); plt.ylabel("Number of samples")
    plt.title("Bootstrap multiplicities (0 = OOB)"); plt.show()
    """)
    n.m("""
    ## 3. Bagging своими руками на внутреннем validation

    У каждого дерева собственная bootstrap-выборка. Для классификации усредняем
    вероятности и выбираем максимальную. Случайный лес добавляет случайный набор
    признаков при **каждом split**; наш ручной bagging использует все признаки.
    """)
    n.c("""
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.metrics import f1_score, accuracy_score
    X_fit, X_val, y_fit, y_val = train_test_split(X_train, y_train, test_size=0.25,
        stratify=y_train, random_state=SEED + 1)
    manual_trees, probabilities = [], []
    bootstrap_rng = np.random.default_rng(SEED)
    for tree_id in range(25):
        positions = bootstrap_rng.integers(0, len(X_fit), size=len(X_fit))
        tree = DecisionTreeClassifier(random_state=SEED + tree_id)
        tree.fit(X_fit.iloc[positions], y_fit.iloc[positions])
        # Выравниваем классы: bootstrap теоретически может пропустить редкий класс.
        aligned = np.zeros((len(X_val), 3))
        aligned[:, tree.classes_.astype(int)] = tree.predict_proba(X_val)
        manual_trees.append(tree); probabilities.append(aligned)
    ensemble_probability = np.mean(probabilities, axis=0)
    assert np.allclose(ensemble_probability.sum(axis=1), 1)
    print("Manual bagging validation macro F1:", f1_score(y_val, ensemble_probability.argmax(axis=1), average="macro"))
    """)
    n.m(r"""
    ## 4. Почему усреднение может помочь

    Если ошибки одинаково распределены с дисперсией $\sigma^2$ и попарной корреляцией
    $\rho$, то дисперсия среднего $B$ моделей равна
    $$\operatorname{Var}(\bar f)=\rho\sigma^2+\frac{1-\rho}{B}\sigma^2.$$

    Число деревьев уменьшает второе слагаемое, но не первое. Случайные признаки
    стремятся снизить корреляцию. Формула — иллюстрация при упрощающих предположениях,
    не оценка реальной дисперсии нашего леса.
    """)
    n.c("""
    trees_count = np.arange(1, 101)
    for rho in [0.0, 0.2, 0.8]:
        plt.plot(trees_count, rho + (1-rho)/trees_count, label=f"rho={rho}")
    plt.xlabel("Number of models B"); plt.ylabel("Variance / sigma squared")
    plt.title("Correlated errors limit the benefit of averaging"); plt.legend(); plt.show()
    """)
    n.m("""
    ## 5. Сравнение single tree, bagging и Random Forest на общих folds

    Выбираем заранее macro F1 и четыре stratified folds. `n_jobs=1` и фиксированные
    seeds делают вычисления удобными для обычного ноутбука. `max_features='sqrt'`
    в лесу ограничивает кандидатов на каждом разделении.
    """)
    n.c("""
    from sklearn.ensemble import BaggingClassifier, RandomForestClassifier
    from sklearn.dummy import DummyClassifier
    from sklearn.model_selection import StratifiedKFold, cross_val_score
    cv = StratifiedKFold(n_splits=4, shuffle=True, random_state=SEED)
    candidates = {
        "majority baseline": DummyClassifier(strategy="most_frequent"),
        "single tree": DecisionTreeClassifier(random_state=SEED),
        "bagging": BaggingClassifier(estimator=DecisionTreeClassifier(), n_estimators=80,
                                     bootstrap=True, random_state=SEED, n_jobs=1),
        "random forest": RandomForestClassifier(n_estimators=100, max_features="sqrt",
                                                random_state=SEED, n_jobs=1)}
    rows = []
    for name, model in candidates.items():
        scores = cross_val_score(model, X_train, y_train, scoring="f1_macro", cv=cv, n_jobs=1)
        rows.append({"model": name, "CV_macro_F1": scores.mean(), "fold_SD": scores.std()})
    display(pd.DataFrame(rows).round(3))
    """)
    n.m("""
    ## 6. OOB в библиотечном лесу

    Для каждого train-объекта предсказание собирается только из деревьев, где объект
    не встречался при обучении. `oob_score_` по умолчанию — **accuracy**, не macro F1.
    Рассчитаем macro F1 вручную по `oob_decision_function_`, явно проверив покрытие.
    """)
    n.c("""
    oob_forest = RandomForestClassifier(n_estimators=180, oob_score=True, bootstrap=True,
        max_features="sqrt", random_state=SEED, n_jobs=1).fit(X_train, y_train)
    oob_probability = oob_forest.oob_decision_function_
    covered = np.isfinite(oob_probability).all(axis=1) & (oob_probability.sum(axis=1) > 0)
    assert covered.all(), "Увеличьте количество деревьев: есть строки без OOB-прогнозов"
    oob_pred = oob_forest.classes_[oob_probability.argmax(axis=1)]
    print("OOB accuracy:", oob_forest.oob_score_)
    print("OOB macro F1:", f1_score(y_train, oob_pred, average="macro"))
    assert np.isclose(accuracy_score(y_train, oob_pred), oob_forest.oob_score_)
    """)
    n.m("""
    ## 7. Подбор параметров и честный смысл OOB

    Выбор `min_samples_leaf` и `max_features` выполняем на CV train. Если многократно
    выбирать параметры по OOB, он становится validation-критерием и также может
    переоценивать победителя. Внешний test всё равно остаётся закрытым.
    """)
    n.c("""
    from sklearn.model_selection import GridSearchCV
    search = GridSearchCV(RandomForestClassifier(n_estimators=120, random_state=SEED, n_jobs=1),
        {"max_features": ["sqrt", 0.7], "min_samples_leaf": [1, 3, 7]},
        scoring="f1_macro", cv=cv, n_jobs=1)
    search.fit(X_train, y_train)
    display(pd.DataFrame(search.cv_results_)[["param_max_features", "param_min_samples_leaf", "mean_test_score", "std_test_score"]])
    print("Зафиксированные параметры:", search.best_params_)
    """)
    n.m("""
    ## 8. Устойчивость к seed на внутреннем validation

    Устойчивость — отдельный вопрос. Меняем seed ансамбля, сохраняя данные и
    параметры. **Не выбираем лучший seed**: это спрятанный подбор модели.
    Здесь измеряется вариативность обучения на данном split, а не полная неопределённость.
    """)
    n.c("""
    stability = []
    for seed in [11, 22, 33, 44, 55]:
        fitted = RandomForestClassifier(n_estimators=100, random_state=seed, n_jobs=1,
                                        **search.best_params_).fit(X_fit, y_fit)
        stability.append({"seed": seed, "validation_macro_F1": f1_score(y_val, fitted.predict(X_val), average="macro")})
    stability_table = pd.DataFrame(stability)
    display(stability_table)
    print("Разброс (sample SD):", stability_table.validation_macro_F1.std())
    """)
    n.m("""
    ## 9. Важность признаков: измеряем на validation

    Impurity importance — внутренний счётчик дерева и может предпочитать признаки
    с большим числом возможных разделений. Permutation importance измеряет падение
    метрики при перемешивании столбца; связанные признаки могут замещать друг друга.
    Используем модель на fit и validation, чтобы не настраиваться по test.
    """)
    n.c("""
    from sklearn.inspection import permutation_importance
    explain_model = RandomForestClassifier(n_estimators=120, random_state=SEED, n_jobs=1,
        **search.best_params_).fit(X_fit, y_fit)
    permutation = permutation_importance(explain_model, X_val, y_val, n_repeats=8,
        random_state=SEED, scoring="f1_macro", n_jobs=1)
    importance = pd.Series(permutation.importances_mean, index=X_train.columns).sort_values()
    importance.plot.barh(xerr=pd.Series(permutation.importances_std, index=X_train.columns).loc[importance.index])
    plt.xlabel("Validation macro F1 decrease ± shuffle SD")
    plt.title("Permutation importance, not causal influence"); plt.show()
    """)
    n.m("""
    ## 10. Итоговый test

    Модель выбрана по CV и переобучена на полном train. OOB, validation и final test
    отвечают на разные вопросы; не выбираем из них наиболее красивое число.
    """)
    n.c("""
    from sklearn.metrics import classification_report, ConfusionMatrixDisplay
    final_prediction = search.predict(X_test)
    print(classification_report(y_test, final_prediction, zero_division=0))
    assert final_prediction.shape == y_test.shape
    ConfusionMatrixDisplay.from_predictions(y_test, final_prediction, colorbar=False)
    plt.title("Final holdout: tuned Random Forest"); plt.show()
    """)
    n.m("""
    ## Что объяснить в отчёте

    Как формируются bootstrap и OOB? Чем Random Forest отличается от bagging?
    Почему число деревьев не устраняет корреляцию ошибок? Почему OOB accuracy нельзя
    напрямую сравнивать с CV macro F1? Какие ограничения есть у permutation importance?

    Первоисточники: [Breiman, Random Forests (2001)](https://www.stat.berkeley.edu/~breiman/randomforest2001.pdf),
    [scikit-learn ensembles](https://scikit-learn.org/stable/modules/ensemble.html),
    [OOB example](https://scikit-learn.org/stable/auto_examples/ensemble/plot_ensemble_oob.html),
    [permutation importance](https://scikit-learn.org/stable/modules/permutation_importance.html).
    """)
    n.save(12, "01_bagging_random_forest_oob.ipynb")


def week13():
    n = Notebook()
    intro(n, 13, "Gradient Boosting, XGBoost и LightGBM: последовательное исправление ошибок",
          "реализовать первые шаги boosting, запустить три реальные библиотеки, выбрать параметры на общих folds и подготовить честный промежуточный проект.")
    setup(n, 13)
    load_split(n, "diabetes_raw.csv", regression=True)
    n.m("""
    ## 1. EDA и план эксперимента

    Цель непрерывная: используем RMSE как основной критерий, MAE как дополнение.
    Набор небольшой и учебный; сравнение библиотек здесь не является общим рейтингом
    скорости или качества. Зафиксируем одинаковые folds и малые сетки параметров.
    """)
    n.c("""
    display(X_train.describe().T.round(2))
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.5))
    y_train.hist(bins=18, ax=axes[0]); axes[0].set(title="Train target", xlabel="Target", ylabel="Count")
    axes[1].scatter(X_train.bmi, y_train, alpha=0.6)
    axes[1].set(title="Train BMI vs target", xlabel="BMI", ylabel="Target")
    plt.tight_layout(); plt.show()
    X_fit, X_val, y_fit, y_val = train_test_split(X_train, y_train, test_size=0.25, random_state=SEED + 1)
    assert set(X_fit.index).isdisjoint(X_val.index)
    """)
    n.m(r"""
    ## 2. Boosting для squared error

    Начинаем с константы $F_0(x)=\bar y$. Для функции $\frac12(y-F)^2$
    отрицательный градиент по $F$ — остаток $r=y-F$.
    $$h_m\leftarrow\mathrm{fit}(X,r_m),\qquad
    F_m(x)=F_{m-1}(x)+\eta h_m(x).$$

    В отличие от bagging, деревья обучаются **последовательно**, каждое исправляет
    текущие ошибки. Ниже обучаем короткий ансамбль вручную на fit и наблюдаем validation.
    """)
    n.c("""
    from sklearn.tree import DecisionTreeRegressor
    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
    base_value = y_fit.mean()
    train_prediction = np.full(len(X_fit), base_value)
    val_prediction = np.full(len(X_val), base_value)
    weak_trees, history = [], []
    learning_rate = 0.15
    for iteration in range(40):
        residual = y_fit.to_numpy() - train_prediction
        tree = DecisionTreeRegressor(max_depth=2, min_samples_leaf=8, random_state=SEED + iteration)
        tree.fit(X_fit, residual)
        train_prediction += learning_rate * tree.predict(X_fit)
        val_prediction += learning_rate * tree.predict(X_val)
        weak_trees.append(tree)
        history.append({"round": iteration+1,
                        "fit_RMSE": np.sqrt(mean_squared_error(y_fit, train_prediction)),
                        "validation_RMSE": np.sqrt(mean_squared_error(y_val, val_prediction))})
    manual_history = pd.DataFrame(history)
    assert manual_history.fit_RMSE.iloc[-1] < manual_history.fit_RMSE.iloc[0]
    display(manual_history.head())
    """)
    n.c("""
    manual_history.set_index("round").plot()
    plt.xlabel("Boosting round"); plt.ylabel("RMSE"); plt.title("Sequential residual fitting")
    plt.show()
    reconstructed = base_value + learning_rate * sum(tree.predict(X_val) for tree in weak_trees)
    assert np.allclose(reconstructed, val_prediction)
    print("Прогноз воспроизведён суммой деревьев; max error:", np.max(abs(reconstructed-val_prediction)))
    """)
    n.m("""
    ## 3. Три реальные реализации

    Импортируем именно `xgboost` и `lightgbm`; sklearn-модель не выдаётся за эти
    библиотеки. Отсутствующая зависимость — ошибка окружения, которую исправляют
    установкой requirements до запуска. Все варианты CPU, `n_jobs=1`.

    scikit-learn GradientBoosting — прозрачный классический baseline.
    XGBoost добавляет собственную систему оптимизации и регуляризации.
    LightGBM использует histogram-алгоритмы и leaf-wise рост; `num_leaves` и
    `min_child_samples` помогают ограничивать сложность.
    """)
    n.c("""
    import xgboost as xgb
    import lightgbm as lgb
    from sklearn.ensemble import GradientBoostingRegressor
    from sklearn.dummy import DummyRegressor
    from sklearn.model_selection import KFold, cross_val_score, GridSearchCV
    from time import perf_counter
    print("XGBoost", xgb.__version__, "| LightGBM", lgb.__version__)
    candidates = {
        "mean baseline": DummyRegressor(),
        "sklearn GB": GradientBoostingRegressor(n_estimators=80, learning_rate=0.05,
                                                 max_depth=2, random_state=SEED),
        "XGBoost": xgb.XGBRegressor(n_estimators=80, learning_rate=0.05, max_depth=2,
             objective="reg:squarederror", tree_method="hist", random_state=SEED, n_jobs=1),
        "LightGBM": lgb.LGBMRegressor(n_estimators=80, learning_rate=0.05, num_leaves=7,
             min_child_samples=12, verbosity=-1, force_col_wise=True, random_state=SEED, n_jobs=1)}
    cv = KFold(n_splits=3, shuffle=True, random_state=SEED)
    """)
    n.m("""
    ## 4. Одинаковые folds, одинаковая метрика

    Положительный RMSE получается сменой знака score. Измеряем фактическое время
    этого запуска, но не делаем вывод о скорости библиотеки в целом: overhead
    доминирует на таком небольшом наборе.
    """)
    n.c("""
    baseline_rows = []
    for name, estimator in candidates.items():
        started = perf_counter()
        scores = -cross_val_score(estimator, X_train, y_train, cv=cv,
                                  scoring="neg_root_mean_squared_error", n_jobs=1)
        baseline_rows.append({"model": name, "CV_RMSE": scores.mean(),
                              "fold_SD": scores.std(), "seconds": perf_counter()-started})
    display(pd.DataFrame(baseline_rows).round(3))
    """)
    n.m("""
    ## 5. Небольшой и объявленный заранее бюджет подбора

    У каждой библиотеки четыре комбинации: два значения learning rate × два уровня
    сложности. Число кандидатов одинаково, смысл параметров роста деревьев отличается.
    Не расширяем сетку после просмотра test. CV-оценка победителя оптимистична из-за
    выбора из нескольких вариантов; независимый test нужен для итогового отчёта.
    """)
    n.c("""
    grids = {
        "sklearn GB": {"learning_rate": [0.03, 0.1], "max_depth": [1, 2]},
        "XGBoost": {"learning_rate": [0.03, 0.1], "max_depth": [1, 2]},
        "LightGBM": {"learning_rate": [0.03, 0.1], "num_leaves": [3, 7]}}
    searches, tuning_rows = {}, []
    for name, params in grids.items():
        search = GridSearchCV(candidates[name], params, cv=cv,
                              scoring="neg_root_mean_squared_error", n_jobs=1)
        search.fit(X_train, y_train)
        searches[name] = search
        tuning_rows.append({"family": name, "best_CV_RMSE": -search.best_score_,
                            "parameters": search.best_params_})
    tuning_table = pd.DataFrame(tuning_rows).sort_values("best_CV_RMSE")
    display(tuning_table)
    chosen_name = tuning_table.iloc[0]["family"]
    final_model = searches[chosen_name].best_estimator_
    print("Зафиксирована модель по CV:", chosen_name)
    """)
    n.m("""
    ## 6. Early stopping: отдельный опыт на fit/validation

    Early stopping выбирает число boosting rounds по validation. **Нельзя передавать
    X_test в eval_set.** Демонстрация ниже не заменяет CV-план выше; её результаты
    помогают понять алгоритм. Для финального проекта можно заранее выбрать один
    протокол и описать, как после early stopping переобучается модель.
    """)
    n.c("""
    early_xgb = xgb.XGBRegressor(n_estimators=400, learning_rate=0.05, max_depth=2,
        early_stopping_rounds=20, objective="reg:squarederror", eval_metric="rmse",
        tree_method="hist", random_state=SEED, n_jobs=1)
    early_xgb.fit(X_fit, y_fit, eval_set=[(X_val, y_val)], verbose=False)
    early_lgb = lgb.LGBMRegressor(n_estimators=400, learning_rate=0.05, num_leaves=7,
        min_child_samples=12, verbosity=-1, force_col_wise=True, random_state=SEED, n_jobs=1)
    early_lgb.fit(X_fit, y_fit, eval_set=[(X_val, y_val)], eval_metric="rmse",
                  callbacks=[lgb.early_stopping(20, verbose=False)])
    print("XGBoost rounds selected:", early_xgb.best_iteration + 1)
    print("LightGBM rounds selected:", early_lgb.best_iteration_)
    assert 1 <= early_xgb.best_iteration + 1 <= 400
    assert 1 <= early_lgb.best_iteration_ <= 400
    """)
    n.c("""
    xgb_curve = early_xgb.evals_result()["validation_0"]["rmse"]
    lgb_curve = early_lgb.evals_result_["valid_0"]["rmse"]
    plt.plot(np.arange(1, len(xgb_curve)+1), xgb_curve, label="XGBoost validation")
    plt.plot(np.arange(1, len(lgb_curve)+1), lgb_curve, label="LightGBM validation")
    plt.xlabel("Boosting round"); plt.ylabel("Validation RMSE")
    plt.title("Validation guides stopping; test stays sealed"); plt.legend(); plt.show()
    """)
    n.m("""
    ## 7. Отчёт о финальном holdout

    До этой ячейки определены семейство, параметры и метрики. Проверяем только
    выбранную модель и заранее объявленный baseline. Test не используется для
    нового подбора после получения результата.
    """)
    n.c("""
    final_prediction = final_model.predict(X_test)
    mean_prediction = DummyRegressor().fit(X_train, y_train).predict(X_test)
    report = []
    for name, prediction in [("mean baseline", mean_prediction), (chosen_name, final_prediction)]:
        report.append({"model": name, "MAE": mean_absolute_error(y_test, prediction),
                       "RMSE": np.sqrt(mean_squared_error(y_test, prediction)),
                       "R2": r2_score(y_test, prediction)})
    display(pd.DataFrame(report).round(3))
    assert final_prediction.shape == y_test.shape and np.isfinite(final_prediction).all()
    """)
    n.c("""
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    axes[0].scatter(y_test, final_prediction, alpha=0.7)
    bounds = [min(y_test.min(), final_prediction.min()), max(y_test.max(), final_prediction.max())]
    axes[0].plot(bounds, bounds, "r--"); axes[0].set(xlabel="Observed", ylabel="Predicted", title=chosen_name)
    axes[1].scatter(final_prediction, y_test.to_numpy()-final_prediction, alpha=0.7)
    axes[1].axhline(0, color="r", ls="--"); axes[1].set(xlabel="Predicted", ylabel="Residual", title="Final holdout errors")
    plt.tight_layout(); plt.show()
    """)
    n.m("""
    ## 8. Промежуточный проект: таблица доказательств

    Создайте краткую карточку эксперимента. Она должна позволить другому студенту
    воспроизвести результат и понять пределы вывода. Различайте измеренные метрики
    и гипотезы о будущем применении. Репозиторий исходной библиотеки — источник кода,
    но он не заменяет описание вашего split и трансформаций.
    """)
    n.c("""
    experiment_card = {
        "task": "Educational diabetes regression, no clinical deployment",
        "target": "target", "excluded_columns": ["sample_id", "target"],
        "train_rows": len(X_train), "test_rows": len(X_test), "seed": SEED,
        "selection": "3-fold CV RMSE on training partition",
        "winner": chosen_name, "parameters": searches[chosen_name].best_params_,
        "limitation": "Small historic teaching dataset; no external/site/time validation"}
    display(pd.Series(experiment_card))
    assert experiment_card["train_rows"] + experiment_card["test_rows"] == len(df)
    """)
    n.m("""
    ## Контрольные вопросы

    Почему обучаемое на остатках дерево не является самостоятельным прогнозом цели?
    Почему learning rate и число деревьев связаны? В чём разница между OOB и early stopping?
    Почему маленький Wine/Diabetes не позволяет выбрать «лучшую библиотеку вообще»?

    Источники: [Friedman, Greedy Function Approximation](https://jerryfriedman.su.domains/ftp/trebst.pdf),
    [XGBoost paper](https://arxiv.org/abs/1603.02754),
    [XGBoost sklearn interface](https://xgboost.readthedocs.io/en/stable/python/sklearn_estimator.html),
    [LightGBM paper](https://proceedings.neurips.cc/paper/2017/hash/6449f44a102fde848669bdd9eb6b76fa-Abstract.html),
    [LightGBM Python introduction](https://lightgbm.readthedocs.io/en/stable/Python-Intro.html).
    """)
    n.save(13, "01_boosting_xgboost_lightgbm_midterm.ipynb")


def week14():
    n = Notebook()
    intro(n, 14, "K-Means, DBSCAN, PCA и t-SNE: структура без готовых ответов",
          "различать кластер и класс, подобрать K-Means по внутренней метрике, увидеть преимущества DBSCAN на дугах, интерпретировать PCA и осторожно читать t-SNE.")
    setup(n, 14)
    n.m("""
    ## 1. Контракт данных и unsupervised split

    Wine имеет известные классы, но **не передаём их алгоритму и не используем
    для выбора k**. Они понадобятся только для заключительного внешнего аудита.
    Выделим случайный holdout без стратификации по скрытому классу. Для K-Means/PCA
    можем обучить преобразование на train и применить его к новым строкам.
    """)
    n.c("""
    df = pd.read_csv(DATA / "wine.csv").set_index("sample_id")
    assert df.index.is_unique and df.notna().all().all()
    X = df.drop(columns="target")
    train_ids, test_ids = train_test_split(df.index, test_size=0.25, random_state=SEED)
    X_train, X_test = X.loc[train_ids], X.loc[test_ids]
    assert set(train_ids).isdisjoint(test_ids)
    display(X_train.describe().T.round(2))
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.5))
    X_train.alcohol.hist(ax=axes[0], bins=15); axes[0].set(title="Train alcohol", xlabel="Alcohol", ylabel="Count")
    axes[1].scatter(X_train.alcohol, X_train.flavanoids, alpha=0.65)
    axes[1].set(title="Unlabelled train observations", xlabel="Alcohol", ylabel="Flavanoids")
    plt.tight_layout(); plt.show()
    """)
    n.m(r"""
    ## 2. K-Means: цель и один ручной шаг

    $$J=\sum_i\|x_i-\mu_{c_i}\|^2.$$
    Чередуем назначение ближайшего центра и пересчёт центра как среднего кластера.
    Фиксируем центры из train, делаем один шаг и проверяем, что objective не вырос
    при неизменных назначениях. Стандартизация предотвращает доминирование крупных шкал.
    """)
    n.c("""
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler().fit(X_train)
    Z_train = scaler.transform(X_train)
    centers_before = Z_train[[0, 30, 60]].copy()
    assignments = ((Z_train[:, None, :] - centers_before[None, :, :])**2).sum(axis=2).argmin(axis=1)
    assert set(assignments) == {0, 1, 2}
    centers_after = np.vstack([Z_train[assignments == k].mean(axis=0) for k in range(3)])
    old_objective = np.sum((Z_train - centers_before[assignments])**2)
    new_objective = np.sum((Z_train - centers_after[assignments])**2)
    assert new_objective <= old_objective + 1e-9
    print({"objective_before": old_objective, "objective_after_center_update": new_objective})
    """)
    n.m(r"""
    ## 3. Внутренний выбор k

    Silhouette: $s=(b-a)/\max(a,b)$, где $a$ — среднее расстояние до своего
    кластера, $b$ — минимальное среднее расстояние до другого. Больше — компактнее
    и лучше разделены найденные группы. Это не доказательство полезных бизнес-сегментов
    и не способ гарантированно восстановить неизвестные реальные классы.
    """)
    n.c("""
    from sklearn.cluster import KMeans, DBSCAN
    from sklearn.metrics import silhouette_score, adjusted_rand_score
    candidates, results = {}, []
    for k in range(2, 7):
        model = KMeans(n_clusters=k, n_init=15, random_state=SEED).fit(Z_train)
        candidates[k] = model
        results.append({"k": k, "inertia": model.inertia_,
                        "train_silhouette": silhouette_score(Z_train, model.labels_)})
    selection = pd.DataFrame(results)
    chosen_k = int(selection.sort_values("train_silhouette", ascending=False).iloc[0]["k"])
    kmeans = candidates[chosen_k]
    display(selection.round(3)); print("Зафиксировано k:", chosen_k)
    """)
    n.c("""
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.5))
    axes[0].plot(selection.k, selection.inertia, "o-"); axes[0].set(xlabel="k", ylabel="Train inertia", title="Elbow heuristic")
    axes[1].plot(selection.k, selection.train_silhouette, "o-")
    axes[1].set(xlabel="k", ylabel="Train silhouette", title="Internal cluster separation")
    plt.tight_layout(); plt.show()
    """)
    n.m(r"""
    ## 4. PCA: линейная проекция с максимальной дисперсией

    После центрирования $Z=USV^T$. Главные направления — строки $V^T$;
    проекция на первые $q$ компонент: $T=ZV_q$.
    `explained_variance_ratio_` описывает долю дисперсии **train**, а не точность
    классификатора. Знак компоненты может измениться без изменения смысла геометрии.
    """)
    n.c("""
    from sklearn.decomposition import PCA
    pca = PCA(n_components=2, svd_solver="full").fit(Z_train)
    projected_train = pca.transform(Z_train)
    projected_test = pca.transform(scaler.transform(X_test))
    assert projected_train.shape == (len(X_train), 2)
    assert np.allclose(pca.components_ @ pca.components_.T, np.eye(2), atol=1e-10)
    print("Explained variance ratios:", pca.explained_variance_ratio_)
    print("Доля дисперсии двух компонент:", pca.explained_variance_ratio_.sum())
    plt.scatter(projected_train[:, 0], projected_train[:, 1], c=kmeans.labels_, cmap="tab10", alpha=0.7)
    plt.xlabel("PC1"); plt.ylabel("PC2"); plt.title("Train PCA projection coloured by K-Means cluster")
    plt.show()
    """)
    n.m("""
    ## 5. Вклад признаков и ошибка восстановления

    Нагрузки помогают понять линейное направление. Они не являются причинными
    эффектами и не равны feature importance supervised-модели. Восстановление
    через две компоненты неизбежно теряет часть информации.
    """)
    n.c("""
    loadings = pd.DataFrame(pca.components_.T, index=X_train.columns, columns=["PC1", "PC2"])
    display(loadings.round(3))
    restored = pca.inverse_transform(projected_train)
    reconstruction_mse = np.mean((Z_train-restored)**2)
    assert reconstruction_mse >= 0 and np.isfinite(reconstruction_mse)
    loadings.plot.bar(figsize=(12, 4)); plt.ylabel("PCA component coefficient")
    plt.title("Directions in standardised feature space"); plt.tight_layout(); plt.show()
    print("Train reconstruction MSE per coordinate:", reconstruction_mse)
    """)
    n.m("""
    ## 6. Проверка на новых строках и внешний аудит классов

    K-Means имеет `predict`, PCA — `transform`: используем **те же** train scaler,
    центры и компоненты. Теперь впервые раскрываем исходные классы для ARI и таблицы
    сопряжённости. Номер кластера произволен: cluster 0 не означает class 0.
    После аудита k не меняем.
    """)
    n.c("""
    Z_test = scaler.transform(X_test)
    test_clusters = kmeans.predict(Z_test)
    cluster_count = len(np.unique(test_clusters))
    test_silhouette = silhouette_score(Z_test, test_clusters) if 1 < cluster_count < len(X_test) else np.nan
    print("Holdout silhouette:", test_silhouette)
    print("External ARI:", adjusted_rand_score(df.loc[test_ids, "target"], test_clusters))
    display(pd.crosstab(df.loc[test_ids, "target"], test_clusters, rownames=["true cultivar"], colnames=["cluster"]))
    assert len(test_clusters) == len(X_test)
    """)
    n.m("""
    ## 7. DBSCAN и некруглые группы

    На синтетических дугах сравним геометрию K-Means и DBSCAN. `eps` задаёт радиус,
    `min_samples` — минимальную плотность. Метка `-1` обозначает шум.
    Это **трансдуктивное исследование всего набора**, а не test-оценка новых объектов:
    sklearn DBSCAN не имеет стандартного `predict` для новых точек.
    """)
    n.c("""
    moons = pd.read_csv(DATA / "moons_synthetic.csv")
    points = moons[["x1", "x2"]].to_numpy()
    from sklearn.neighbors import NearestNeighbors
    nearest = NearestNeighbors(n_neighbors=6).fit(points)
    neighbor_distances, _ = nearest.kneighbors(points)
    plt.plot(np.sort(neighbor_distances[:, -1]))
    plt.xlabel("Points sorted by sixth-neighbor distance"); plt.ylabel("Distance")
    plt.title("A diagnostic for candidate eps values"); plt.show()
    """)
    n.c("""
    db_rows = []
    for eps in [0.10, 0.16, 0.22, 0.32]:
        labels = DBSCAN(eps=eps, min_samples=6).fit_predict(points)
        non_noise = labels != -1
        n_clusters = len(set(labels) - {-1})
        # Silhouette определён только для 2..n-1 групп и не учитывает исключённый шум.
        score = silhouette_score(points[non_noise], labels[non_noise]) if 1 < n_clusters < non_noise.sum() else np.nan
        db_rows.append({"eps": eps, "clusters": n_clusters, "noise_fraction": 1-non_noise.mean(),
                        "silhouette_excluding_noise": score})
    display(pd.DataFrame(db_rows).round(3))
    """)
    n.m("""
    ## 8. Геометрия и метрика могут расходиться

    Зафиксируем `eps=0.16` как объяснительный вариант. На дугах силуэт может предпочесть
    компактные группы K-Means, хотя DBSCAN лучше повторяет форму генератора.
    Поэтому нельзя выбирать алгоритм по единственному числу без цели исследования.
    """)
    n.c("""
    km_moons = KMeans(n_clusters=2, n_init=15, random_state=SEED).fit_predict(points)
    db_moons = DBSCAN(eps=0.16, min_samples=6).fit_predict(points)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    for ax, labels, name in zip(axes, [km_moons, db_moons], ["K-Means, k=2", "DBSCAN, eps=0.16"]):
        ax.scatter(points[:, 0], points[:, 1], c=labels, cmap="tab10", s=15)
        ax.set(title=name, xlabel="x1", ylabel="x2", aspect="equal")
    plt.tight_layout(); plt.show()
    print("ARI after revealing synthetic generator labels:",
          {"K-Means": adjusted_rand_score(moons.target, km_moons),
           "DBSCAN": adjusted_rand_score(moons.target, db_moons)})
    """)
    n.m("""
    ## 9. t-SNE: локальные соседства, не карта физических расстояний

    Делаем **две визуализации train** при разных perplexity. Не обучаем на train+test,
    не выбираем модель по красоте картинки. t-SNE не сохраняет глобальные расстояния
    и размеры групп, а стандартный sklearn TSNE не имеет `transform` для новых строк.
    Random seed, perplexity и начальная проекция влияют на результат.
    """)
    n.c("""
    from sklearn.manifold import TSNE, trustworthiness
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    for ax, perplexity in zip(axes, [10, 30]):
        embedding = TSNE(n_components=2, perplexity=perplexity, init="pca",
                         learning_rate="auto", max_iter=600, random_state=SEED).fit_transform(Z_train)
        assert embedding.shape == (len(Z_train), 2) and np.isfinite(embedding).all()
        local_score = trustworthiness(Z_train, embedding, n_neighbors=5)
        ax.scatter(embedding[:, 0], embedding[:, 1], c=kmeans.labels_, cmap="tab10", s=25)
        ax.set(title=f"perplexity={perplexity}, trust={local_score:.3f}", xlabel="t-SNE 1", ylabel="t-SNE 2")
    plt.tight_layout(); plt.show()
    """)
    n.m("""
    ## Выводы, которые можно защищать

    Напишите отдельно: что обнаружено алгоритмом, как это измерено и что остаётся
    неизвестным. Кластер не обязан совпадать с классом. Высокая доля дисперсии PCA
    не гарантирует полезность для prediction. Красивые острова t-SNE не доказывают,
    что исходные данные имеют именно столько изолированных групп.

    Источники: [Stanford CS229 notes](https://cs229.stanford.edu/main_notes.pdf),
    [scikit-learn clustering](https://scikit-learn.org/stable/modules/clustering.html),
    [PCA](https://scikit-learn.org/stable/modules/decomposition.html#pca),
    [van der Maaten & Hinton, t-SNE](https://jmlr.org/papers/v9/vandermaaten08a.html),
    [TSNE API](https://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html).
    """)
    n.save(14, "01_clustering_pca_tsne.ipynb")


def week15():
    n = Notebook()
    intro(n, 15, "Метрики, кросс-валидация и переобучение: как не обмануть себя",
          "рассчитать метрики вручную, оценить редкий класс, выбрать threshold по out-of-fold predictions, увидеть overfitting и различить обычную, групповую и временную проверку.")
    setup(n, 15)
    load_split(n, "imbalanced_synthetic.csv")
    n.m("""
    ## 1. EDA: редкий положительный класс

    Это синтетические данные, а не банковские или медицинские наблюдения.
    Положительный класс встречается примерно в 12% строк; label noise немного
    меняет долю. Сначала фиксируем задачу: важен поиск редкого класса, основной
    критерий подбора — average precision (AP).
    """)
    n.c("""
    display(X_train.describe().T.round(3))
    class_table = y_train.value_counts().sort_index().to_frame("count")
    class_table["fraction"] = class_table["count"] / len(y_train)
    display(class_table)
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.5))
    class_table["count"].plot.bar(ax=axes[0], rot=0)
    axes[0].set(title="Train class imbalance", xlabel="Class", ylabel="Count")
    for label in [0, 1]:
        axes[1].hist(X_train.loc[y_train == label, "x0"], bins=18, density=True, alpha=0.5, label=str(label))
    axes[1].set(title="Train x0 distributions", xlabel="x0", ylabel="Density")
    axes[1].legend(); plt.tight_layout(); plt.show()
    """)
    n.m(r"""
    ## 2. Матрица ошибок и метрики вручную

    $$\mathrm{precision}=\frac{TP}{TP+FP},\quad
    \mathrm{recall}=\frac{TP}{TP+FN},\quad
    F_1=\frac{2TP}{2TP+FP+FN}.$$

    Precision отвечает «какая доля сигналов верна», recall — «какая доля настоящих
    положительных случаев найдена». Accuracy может быть высокой у модели,
    игнорирующей редкий класс. Определим поведение при нулевом знаменателе явно.
    """)
    n.c("""
    from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
    example_true = np.array([1, 1, 1, 0, 0, 0, 0, 0])
    example_pred = np.array([1, 0, 1, 1, 0, 0, 0, 0])
    tn, fp, fn, tp = confusion_matrix(example_true, example_pred, labels=[0, 1]).ravel()
    safe_divide = lambda numerator, denominator: numerator/denominator if denominator else 0.0
    manual_precision = safe_divide(tp, tp+fp)
    manual_recall = safe_divide(tp, tp+fn)
    manual_f1 = safe_divide(2*tp, 2*tp+fp+fn)
    assert np.isclose(manual_precision, precision_score(example_true, example_pred, zero_division=0))
    assert np.isclose(manual_recall, recall_score(example_true, example_pred, zero_division=0))
    assert np.isclose(manual_f1, f1_score(example_true, example_pred, zero_division=0))
    display(pd.Series({"TN": tn, "FP": fp, "FN": fn, "TP": tp,
                       "precision": manual_precision, "recall": manual_recall, "F1": manual_f1}))
    """)
    n.m(r"""
    ## 3. Регрессия: MAE, RMSE, R²

    $$\mathrm{MAE}=\frac1n\sum|y_i-\hat y_i|,\quad
    \mathrm{RMSE}=\sqrt{\frac1n\sum(y_i-\hat y_i)^2},\quad
    R^2=1-\frac{\sum(y_i-\hat y_i)^2}{\sum(y_i-\bar y)^2}.$$

    Квадрат сильнее штрафует крупные ошибки. Ниже маленький **придуманный** пример
    используется только для арифметики, не для оценки новой модели. MAPE неудобна,
    когда реальные значения близки к нулю; R² не является процентом правильных ответов.
    """)
    n.c("""
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    observed = np.array([10., 20., 30., 40., 50.])
    predicted = np.array([11., 19., 32., 39., 70.])
    residual = observed - predicted
    manual_mae = np.abs(residual).mean()
    manual_rmse = np.sqrt(np.mean(residual**2))
    manual_r2 = 1 - np.sum(residual**2) / np.sum((observed-observed.mean())**2)
    assert np.isclose(manual_mae, mean_absolute_error(observed, predicted))
    assert np.isclose(manual_rmse, np.sqrt(mean_squared_error(observed, predicted)))
    assert np.isclose(manual_r2, r2_score(observed, predicted))
    display(pd.Series({"MAE": manual_mae, "RMSE": manual_rmse, "R2": manual_r2}))
    """)
    n.m("""
    ## 4. Baseline и честная CV

    Сравним константу и логистическую модель на одинаковых folds.
    Accuracy, balanced accuracy, AP и log loss описывают разные свойства.
    AP суммирует precision с весами прироста recall; это не то же самое, что
    trapezoidal area под интерполированной PR-кривой.
    """)
    n.c("""
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LogisticRegression
    from sklearn.dummy import DummyClassifier
    from sklearn.model_selection import StratifiedKFold, cross_validate, GridSearchCV, cross_val_predict
    outer_cv = StratifiedKFold(n_splits=4, shuffle=True, random_state=SEED)
    pipe = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1500, random_state=SEED))
    scoring = {"accuracy": "accuracy", "balanced_accuracy": "balanced_accuracy",
               "AP": "average_precision", "negative_log_loss": "neg_log_loss"}
    comparison = []
    for name, model in [("prior baseline", DummyClassifier(strategy="prior")), ("logistic C=1", pipe)]:
        values = cross_validate(model, X_train, y_train, cv=outer_cv, scoring=scoring)
        comparison.append({"model": name, **{metric: values[f"test_{metric}"].mean() for metric in scoring}})
    display(pd.DataFrame(comparison).round(3))
    """)
    n.m("""
    ## 5. Переобучение видно по train/validation gap

    Строим validation curve дерева на тех же folds. Рост train score вместе
    с остановкой CV score — предупреждение о переобучении. Слабые обе оценки
    могут указывать на underfitting, но также на слабые признаки или шум меток.
    Test пока не участвует даже в графиках.
    """)
    n.c("""
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.model_selection import validation_curve, learning_curve
    depths = [1, 2, 3, 5, 8, 12]
    train_scores, valid_scores = validation_curve(
        DecisionTreeClassifier(random_state=SEED), X_train, y_train,
        param_name="max_depth", param_range=depths, scoring="average_precision", cv=outer_cv, n_jobs=1)
    plt.plot(depths, train_scores.mean(axis=1), "o-", label="Train AP")
    plt.errorbar(depths, valid_scores.mean(axis=1), yerr=valid_scores.std(axis=1), fmt="o-", capsize=3, label="CV AP")
    plt.xlabel("Tree depth"); plt.ylabel("Average precision"); plt.legend()
    plt.title("Increasing complexity can widen the generalisation gap"); plt.show()
    """)
    n.m("""
    ## 6. Learning curve: стоит ли собирать больше данных?

    Меняем только количество train-строк внутри folds. Это полезный диагноз, но
    не прогноз с гарантией: новые данные могут отличаться от текущих. Scaler каждый
    раз обучается на доступном обучающем подмножестве.
    """)
    n.c("""
    sizes, train_lc, valid_lc = learning_curve(pipe, X_train, y_train,
        train_sizes=[0.25, 0.5, 0.75, 1.0], cv=outer_cv, scoring="average_precision",
        shuffle=True, random_state=SEED, n_jobs=1)
    plt.plot(sizes, train_lc.mean(axis=1), "o-", label="Train")
    plt.errorbar(sizes, valid_lc.mean(axis=1), yerr=valid_lc.std(axis=1), fmt="o-", label="CV", capsize=3)
    plt.xlabel("Training examples per fold"); plt.ylabel("Average precision")
    plt.title("Learning curve"); plt.legend(); plt.show()
    """)
    n.m("""
    ## 7. OOF-прогнозы с подбором внутри каждого outer fold

    Для threshold нужны вероятности объектов, которых модель не видела.
    `cross_val_predict(GridSearchCV(...))` выполняет внутренний подбор C только
    на outer-train. Так ответ конкретного outer-validation объекта не участвует
    ни в fit, ни в выборе C для его прогноза. Это дороже простого CV, но здесь сетка мала.
    """)
    n.c("""
    inner_cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=SEED + 1)
    search = GridSearchCV(pipe, {"logisticregression__C": [0.1, 1.0, 10.0]},
                          scoring="average_precision", cv=inner_cv, n_jobs=1)
    oof_probability = cross_val_predict(search, X_train, y_train, cv=outer_cv,
                                         method="predict_proba", n_jobs=1)[:, 1]
    assert oof_probability.shape == y_train.shape
    assert np.isfinite(oof_probability).all()
    print("Каждый train-объект получил один прогноз вне собственного outer-fold обучения.")
    """)
    n.m("""
    ## 8. Выбор порога по явно заданной стоимости

    Допущение: FN стоит 5, FP — 1 условную единицу. Выберем порог на OOF train.
    Стоимость на тех же OOF после выбора порога уже является оценкой для настройки,
    а не независимым финальным результатом. После refit вероятности могут немного
    сместиться; поэтому threshold также проверяется на итоговом holdout.
    """)
    n.c("""
    threshold_rows = []
    for threshold in np.linspace(0.05, 0.95, 37):
        tn, fp, fn, tp = confusion_matrix(y_train, oof_probability >= threshold, labels=[0, 1]).ravel()
        threshold_rows.append({"threshold": threshold, "cost_per_sample": (fp+5*fn)/len(y_train), "FP": fp, "FN": fn})
    threshold_table = pd.DataFrame(threshold_rows)
    threshold = float(threshold_table.assign(distance=(threshold_table.threshold-0.5).abs())
                       .sort_values(["cost_per_sample", "distance"]).iloc[0].threshold)
    search.fit(X_train, y_train)
    print("Финальные C и threshold:", search.best_params_, threshold)
    plt.plot(threshold_table.threshold, threshold_table.cost_per_sample)
    plt.axvline(threshold, color="crimson", ls="--")
    plt.xlabel("Threshold"); plt.ylabel("OOF selection cost per sample"); plt.show()
    """)
    n.m("""
    ## 9. Test: метрики порога и метрики вероятностей

    ROC AUC и AP вычисляются по вероятностям и не зависят от уже выбранного порога.
    F1, recall и стоимость зависят от него. Оба правила (0.5 и OOF threshold)
    объявлены до test. После этой ячейки не подбираем новый порог.
    """)
    n.c("""
    from sklearn.metrics import accuracy_score, balanced_accuracy_score, roc_auc_score, average_precision_score, log_loss
    test_probability = search.predict_proba(X_test)[:, 1]
    final_rows = []
    for name, cut in [("default 0.5", 0.5), ("OOF cost threshold", threshold)]:
        predicted = test_probability >= cut
        tn, fp, fn, tp = confusion_matrix(y_test, predicted, labels=[0, 1]).ravel()
        final_rows.append({"rule": name, "precision": precision_score(y_test, predicted, zero_division=0),
            "recall": recall_score(y_test, predicted), "F1": f1_score(y_test, predicted),
            "accuracy": accuracy_score(y_test, predicted), "cost_per_sample": (fp+5*fn)/len(y_test)})
    display(pd.DataFrame(final_rows).round(3))
    print({"ROC_AUC": roc_auc_score(y_test, test_probability),
           "AP": average_precision_score(y_test, test_probability),
           "log_loss": log_loss(y_test, test_probability)})
    """)
    n.c("""
    from sklearn.metrics import RocCurveDisplay, PrecisionRecallDisplay, ConfusionMatrixDisplay
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    RocCurveDisplay.from_predictions(y_test, test_probability, ax=axes[0])
    axes[0].plot([0, 1], [0, 1], "k--", alpha=0.4)
    PrecisionRecallDisplay.from_predictions(y_test, test_probability, ax=axes[1])
    axes[1].axhline(y_test.mean(), color="gray", ls="--", label="Test prevalence")
    axes[1].legend()
    ConfusionMatrixDisplay.from_predictions(y_test, test_probability >= threshold, ax=axes[2], colorbar=False)
    axes[2].set_title("Fixed OOF threshold")
    plt.tight_layout(); plt.show()
    """)
    n.m("""
    ## 10. Не любой split допустим

    Если у одного пользователя несколько строк, random split может поместить его
    по обе стороны. `GroupKFold` держит группы раздельно. Для прогноза будущего
    обучение должно предшествовать проверке: `TimeSeriesSplit` сохраняет порядок.
    Следующие мини-данные синтетические; мы проверяем только индексы split.
    """)
    n.c("""
    from sklearn.model_selection import GroupKFold, TimeSeriesSplit
    row_index = np.arange(60)
    groups = np.repeat(np.arange(12), 5)
    group_cv = GroupKFold(n_splits=3)
    for fit_index, val_index in group_cv.split(row_index, groups=groups):
        assert set(groups[fit_index]).isdisjoint(groups[val_index])
    time_cv = TimeSeriesSplit(n_splits=3, gap=2)
    for fit_index, val_index in time_cv.split(row_index):
        assert fit_index.max() < val_index.min()
        assert val_index.min()-fit_index.max()-1 >= 2
        print("Time split:", (fit_index.min(), fit_index.max()), "→", (val_index.min(), val_index.max()))
    """)
    n.m("""
    ## Чек-лист для отчёта о качестве

    Назовите единицу наблюдения, момент предсказания, допустимые признаки, split,
    baseline, метрику подбора, бюджет поиска и независимый test. Не называйте fold SD
    доверительным интервалом. После многократного просмотра test выделите новый
    набор для следующего финального подтверждения.

    Источники: [scikit-learn model evaluation](https://scikit-learn.org/stable/modules/model_evaluation.html),
    [cross-validation](https://scikit-learn.org/stable/modules/cross_validation.html),
    [nested CV example](https://scikit-learn.org/stable/auto_examples/model_selection/plot_nested_cross_validation_iris.html),
    [common pitfalls](https://scikit-learn.org/stable/common_pitfalls.html).
    """)
    n.save(15, "01_metrics_cv_and_overfitting.ipynb")


def week16():
    n = Notebook()
    intro(n, 16, "SHAP, LIME и первый нейрон",
          "получить реальные SHAP и LIME объяснения, проверить аддитивность и локальную точность, отделить объяснение модели от причинности и сделать forward pass нейрона.")
    setup(n, 16)
    load_split(n, "diabetes_raw.csv", regression=True)
    n.m("""
    ## 1. Что и на каких данных объясняем

    Объяснять модель до проверки качества опасно: убедительное объяснение может
    сопровождать слабый прогноз. На небольшом наборе обучим ограниченный Random Forest.
    Для объяснений используем validation внутри train; фоновые данные — только fit.
    Test сохраняем для финальной оценки, без подбора по нему признаков.
    """)
    n.c("""
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.dummy import DummyRegressor
    from sklearn.metrics import mean_squared_error, mean_absolute_error
    X_fit, X_val, y_fit, y_val = train_test_split(X_train, y_train, test_size=0.25, random_state=SEED + 1)
    assert set(X_fit.index).isdisjoint(X_val.index)
    display(X_fit.describe().T.round(2))
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.5))
    y_fit.hist(bins=16, ax=axes[0]); axes[0].set(title="Fit target", xlabel="Target", ylabel="Count")
    axes[1].scatter(X_fit.bmi, y_fit, alpha=0.6); axes[1].set(title="Fit BMI and target", xlabel="BMI", ylabel="Target")
    plt.tight_layout(); plt.show()
    """)
    n.m("""
    ## 2. Фиксированная модель и baseline

    На этой неделе задача — интерпретация, поэтому параметры объявлены заранее,
    а не оптимизируются по результатам объяснений. Референсное распределение SHAP задаётся
    train-статистиками листьев в режиме tree_path_dependent. Отдельную фоновую
    выборку не передаём. Ограничиваем количество деревьев и объясняемых строк для CPU.
    """)
    n.c("""
    model = RandomForestRegressor(n_estimators=90, max_depth=5, min_samples_leaf=5,
                                   max_features=0.8, random_state=SEED, n_jobs=1)
    model.fit(X_fit, y_fit)
    baseline = DummyRegressor().fit(X_fit, y_fit)
    print("Validation RF RMSE:", np.sqrt(mean_squared_error(y_val, model.predict(X_val))))
    print("Validation baseline RMSE:", np.sqrt(mean_squared_error(y_val, baseline.predict(X_val))))
    explain_rows = X_val.iloc[:20].copy()
    """)
    n.m(r"""
    ## 3. SHAP: аддитивные вклады в прогноз

    $$f(x)=\phi_0+\sum_{j=1}^{p}\phi_j(x).$$

    SHAP распределяет отличие прогноза от фонового значения между признаками
    относительно выбранной игры/фонового распределения. Для регрессора объясняем
    выход в единицах target. `feature_perturbation='tree_path_dependent'` использует число train-наблюдений
    в путях/листьях обученных деревьев как референсное распределение. Это явный
    выбор способа объяснения, **не** доказательство причинного эффекта.
    """)
    n.c("""
    import shap
    print("SHAP", shap.__version__)
    shap_explainer = shap.TreeExplainer(model,
        feature_perturbation="tree_path_dependent", model_output="raw")
    explanation = shap_explainer(explain_rows, check_additivity=True)
    reconstructed_prediction = np.asarray(explanation.base_values) + explanation.values.sum(axis=1)
    actual_prediction = model.predict(explain_rows)
    assert explanation.values.shape == explain_rows.shape
    assert np.allclose(reconstructed_prediction, actual_prediction, atol=1e-4)
    print("Максимальная ошибка аддитивности:", np.max(np.abs(reconstructed_prediction-actual_prediction)))
    """)
    n.m("""
    ## 4. Локальная waterfall и глобальное среднее

    Waterfall объясняет **один** прогноз. Среднее абсолютных SHAP по 20 validation
    строкам описывает именно эту небольшую выборку. Оно не показывает направление
    эффекта и не является универсальной важностью признака для всех моделей.
    """)
    n.c("""
    shap.plots.waterfall(explanation[0], max_display=10, show=False)
    plt.title("SHAP: first validation observation"); plt.tight_layout(); plt.show()
    mean_abs_shap = pd.Series(np.abs(explanation.values).mean(axis=0), index=X_fit.columns).sort_values()
    mean_abs_shap.plot.barh()
    plt.xlabel("Mean absolute SHAP value (target units)")
    plt.title("20 validation rows: model-specific attribution"); plt.show()
    """)
    n.m("""
    ## 5. Значение признака и его вклад

    Посмотрим BMI и SHAP(BMI). Рассеяние может отражать взаимодействия и другие
    признаки. График нельзя читать как «если вмешаться и изменить BMI на столько,
    реальный исход изменится на столько».
    """)
    n.c("""
    feature_position = list(X_fit.columns).index("bmi")
    plt.scatter(explain_rows.bmi, explanation.values[:, feature_position], c=explain_rows.age, cmap="viridis")
    plt.axhline(0, color="gray", ls="--")
    plt.colorbar(label="Age"); plt.xlabel("BMI"); plt.ylabel("SHAP(BMI), target units")
    plt.title("Local contributions for this model and background"); plt.show()
    display(pd.DataFrame({"feature": X_fit.columns,
                          "value": explain_rows.iloc[0].to_numpy(),
                          "SHAP": explanation.values[0]}).sort_values("SHAP"))
    """)
    n.m(r"""
    ## 6. LIME: локальная приближённая модель

    LIME генерирует окрестность точки, запрашивает исходную модель и обучает
    простую взвешенную аппроксимацию:
    $$\arg\min_g\sum_z\pi_x(z)(f(z)-g(z))^2+\Omega(g).$$

    Используем настоящую библиотеку `lime`, режим regression и train-статистики.
    LIME не обязан воспроизводить прогноз точно: оценим локальный R² и ошибку
    аппроксимации в выбранной точке. Коэффициенты LIME не равны SHAP-вкладам.
    """)
    n.c("""
    from lime.lime_tabular import LimeTabularExplainer
    def predict_for_lime(array):
        # Сохраняем имена признаков и правильный порядок столбцов.
        return model.predict(pd.DataFrame(array, columns=X_fit.columns))
    lime_explainer = LimeTabularExplainer(X_fit.to_numpy(),
        feature_names=list(X_fit.columns), mode="regression", discretize_continuous=True,
        random_state=SEED)
    observation = X_val.iloc[0].to_numpy()
    lime_explanation = lime_explainer.explain_instance(observation, predict_for_lime,
                                                     num_features=7, num_samples=1500)
    actual = float(predict_for_lime(observation.reshape(1, -1))[0])
    local_prediction = float(np.asarray(lime_explanation.local_pred).reshape(-1)[0])
    display(pd.DataFrame(lime_explanation.as_list(), columns=["local condition", "LIME weight"]))
    print({"model_prediction": actual, "local_surrogate_prediction": local_prediction,
           "absolute_local_error": abs(actual-local_prediction), "weighted_local_R2": lime_explanation.score})
    assert np.isfinite([actual, local_prediction, lime_explanation.score]).all()
    """)
    n.c("""
    lime_explanation.as_pyplot_figure()
    plt.title("LIME: local regression surrogate"); plt.tight_layout(); plt.show()
    """)
    n.m("""
    ## 7. Проверка устойчивости LIME

    Повторим объяснение при двух seeds с неизменной моделью. Различия — сигнал,
    что локальная аппроксимация чувствительна к выборке соседей. На коррелированных
    признаках искусственные комбинации могут быть нетипичными для реальных данных.
    Не выбираем seed только ради удобной истории.
    """)
    n.c("""
    stability = []
    for seed in [42, 43, 44]:
        local = LimeTabularExplainer(X_fit.to_numpy(), feature_names=list(X_fit.columns),
            mode="regression", discretize_continuous=True, random_state=seed)
        result = local.explain_instance(observation, predict_for_lime, num_features=7, num_samples=1500)
        stability.append({"seed": seed, "local_R2": result.score,
            "local_error": abs(actual-float(np.asarray(result.local_pred).reshape(-1)[0])),
            "top_condition": max(result.as_list(), key=lambda pair: abs(pair[1]))[0]})
    display(pd.DataFrame(stability))
    """)
    n.m("""
    ## 8. Финальная оценка зафиксированной модели

    Модель оставляем обученной на fit, потому что именно её объясняли. Если
    переобучить её на всём train, объяснения потребуется вычислить заново.
    Test измеряет качество этой конкретной модели, а SHAP/LIME описывают её поведение.
    """)
    n.c("""
    final_prediction = model.predict(X_test)
    display(pd.DataFrame([
        {"model": "mean baseline", "RMSE": np.sqrt(mean_squared_error(y_test, baseline.predict(X_test)))},
        {"model": "explained RF", "RMSE": np.sqrt(mean_squared_error(y_test, final_prediction))}]))
    print("Final RF MAE:", mean_absolute_error(y_test, final_prediction))
    assert final_prediction.shape == y_test.shape
    """)
    n.m(r"""
    ## 9. Переход к нейронным сетям: нейрон как знакомая модель

    $$z=Xw+b,\qquad a=\sigma(z).$$

    С линейным выходом это регрессия; с sigmoid — знакомая логистическая модель.
    Несколько нейронов образуют слой. Без нелинейности несколько линейных слоёв
    сворачиваются в одно линейное преобразование. Ниже данные **синтетические**:
    они нужны для геометрии, а не для ещё одного клинического эксперимента.
    """)
    n.c("""
    z = np.linspace(-5, 5, 300)
    sigmoid = lambda values: 1/(1+np.exp(-np.clip(values, -50, 50)))
    plt.plot(z, sigmoid(z), label="sigmoid")
    plt.plot(z, np.maximum(0, z), label="ReLU")
    plt.plot(z, np.tanh(z), label="tanh")
    plt.xlabel("Pre-activation z"); plt.ylabel("Activation"); plt.title("Common nonlinear activations")
    plt.legend(); plt.show()
    """)
    n.m("""
    ## 10. Один forward pass и форма тензоров

    XOR — четыре точки, которые нельзя разделить одной прямой. Скрытый слой
    позволяет нелинейное преобразование. Сейчас веса выбраны вручную только
    для демонстрации форм и вычислений; **сеть ещё не обучена**. Backprop — следующая неделя.
    """)
    n.c("""
    xor_X = np.array([[0., 0.], [0., 1.], [1., 0.], [1., 1.]])
    xor_y = np.array([[0.], [1.], [1.], [0.]])
    W1 = np.array([[1.0, -1.0, 0.5], [-1.0, 1.0, 0.5]])
    b1 = np.array([0.0, 0.0, -0.3])
    W2 = np.array([[1.0], [1.0], [-1.0]])
    b2 = np.array([-0.1])
    hidden = np.maximum(0, xor_X @ W1 + b1)
    logits = hidden @ W2 + b2
    probability = sigmoid(logits)
    loss = np.mean(np.logaddexp(0, logits)-xor_y*logits)
    assert hidden.shape == (4, 3) and probability.shape == (4, 1)
    assert np.isfinite(loss) and np.all((probability >= 0) & (probability <= 1))
    display(pd.DataFrame({"x1": xor_X[:, 0], "x2": xor_X[:, 1],
                          "target": xor_y[:, 0], "untrained_probability": probability[:, 0]}))
    print("Loss до обучения:", loss)
    """)
    n.m("""
    ## Что перенести в отчёт

    Для объяснения укажите модель, версию библиотеки, фоновые данные, конкретную
    выборку и шкалу output. Проверьте additivity SHAP и surrogate fidelity LIME.
    Укажите, какие изменения модели потребуют новых объяснений. Для нейрона
    запишите размерности X, W1, hidden, W2 и объясните роль активации.

    Источники: [Lundberg & Lee, SHAP](https://arxiv.org/abs/1705.07874),
    [SHAP TreeExplainer](https://shap.readthedocs.io/en/latest/generated/shap.TreeExplainer.html),
    [Ribeiro et al., LIME](https://arxiv.org/abs/1602.04938),
    [официальный LIME repository](https://github.com/marcotcr/lime),
    [Stanford CS231n neural networks](https://cs231n.github.io/neural-networks-1/).
    """)
    n.save(16, "01_shap_lime_and_neuron.ipynb")


def digits_split(n):
    n.m("""
    ## Локальные digits 8×8 и единая разбивка

    Одна строка — 64 пикселя и цифра 0…9. Известный диапазон пикселя 0…16
    позволяет делить на 16 без оценки статистик по данным. Сначала 20% test,
    затем 25% оставшихся строк на validation: примерно **60/20/20**.
    `sample_id` и target исключены из X. Все три лабораторные недели используют
    одинаковые индексы; test не выбирает число эпох.
    """)
    n.c("""
    df = pd.read_csv(DATA / "digits_8x8.csv").set_index("sample_id")
    assert df.index.is_unique and df.notna().all().all()
    pixels = df.drop(columns="target")
    assert pixels.shape[1] == 64 and pixels.min().min() >= 0 and pixels.max().max() <= 16
    all_ids = df.index.to_numpy()
    trainval_ids, test_ids = train_test_split(all_ids, test_size=0.2,
        stratify=df.target, random_state=SEED)
    train_ids, val_ids = train_test_split(trainval_ids, test_size=0.25,
        stratify=df.loc[trainval_ids, "target"], random_state=SEED + 1)
    assert set(train_ids).isdisjoint(val_ids) and set(trainval_ids).isdisjoint(test_ids)
    def arrays(ids):
        return (pixels.loc[ids].to_numpy(dtype="float32") / 16.0,
                df.loc[ids, "target"].to_numpy(dtype="int64"))
    X_train, y_train = arrays(train_ids)
    X_val, y_val = arrays(val_ids)
    X_test, y_test = arrays(test_ids)
    print({"train": X_train.shape, "validation": X_val.shape, "sealed_test": X_test.shape})
    """)
    n.m("""
    ## EDA только train: баланс, распределение и изображения

    Изображения уже уменьшены до 8×8, поэтому детали потеряны. Нулевые края
    встречаются часто. В исходном экспорте нет ID автора почерка: random split
    не проверяет перенос на полностью новых авторов. Сравнение framework на одном
    seed — учебная иллюстрация, не рейтинг библиотек.
    """)
    n.c("""
    display(pd.Series(y_train).value_counts().sort_index().rename("train_count"))
    display(pd.DataFrame(X_train).describe().T[["mean", "std", "min", "max"]].head(12).round(3))
    fig, axes = plt.subplots(2, 6, figsize=(11, 4))
    for ax, image, label in zip(axes.ravel(), X_train[:12], y_train[:12]):
        ax.imshow(image.reshape(8, 8), cmap="gray_r", vmin=0, vmax=1)
        ax.set_title(f"label {label}"); ax.axis("off")
    plt.tight_layout(); plt.show()
    plt.hist(X_train.ravel(), bins=17)
    plt.xlabel("Pixel intensity / 16"); plt.ylabel("Pixel count"); plt.title("Train pixel distribution")
    plt.show()
    """)


def week17_numpy():
    n = Notebook()
    intro(n, 17, "Backpropagation в NumPy: каждую производную можно проверить",
          "реализовать softmax cross-entropy и двухслойную сеть, проверить градиенты конечными разностями, выбрать checkpoint по validation и оценить закрытый test.",
          duration="54 минуты; первая практическая часть недели")
    setup(n, 17)
    digits_split(n)
    n.m(r"""
    ## 1. Forward pass и функция потерь

    $$H=\tanh(XW_1+b_1),\quad Z=HW_2+b_2,$$
    $$p_{ik}=\frac{e^{Z_{ik}}}{\sum_j e^{Z_{ij}}},\quad
    L=-\frac1n\sum_i\log p_{i,y_i}.$$

    Вычитаем максимум из logits каждой строки, чтобы избежать переполнения exp.
    Вычитание одной константы не меняет softmax. Скрытый слой имеет 32 нейрона.
    """)
    n.c("""
    def softmax(logits):
        shifted = logits-logits.max(axis=1, keepdims=True)
        exponent = np.exp(shifted)
        return exponent/exponent.sum(axis=1, keepdims=True)
    probe_probability = softmax(np.array([[1000., 1001., 999.]]))
    assert np.allclose(probe_probability.sum(axis=1), 1) and np.isfinite(probe_probability).all()
    params = {
        "W1": rng.normal(0, np.sqrt(1/64), (64, 32)), "b1": np.zeros((1, 32)),
        "W2": rng.normal(0, np.sqrt(1/32), (32, 10)), "b2": np.zeros((1, 10))}
    def forward(parameters, X):
        hidden = np.tanh(X @ parameters["W1"] + parameters["b1"])
        logits = hidden @ parameters["W2"] + parameters["b2"]
        return hidden, logits, softmax(logits)
    print("Число обучаемых параметров:", sum(value.size for value in params.values()))
    """)
    n.m(r"""
    ## 2. Chain rule: от loss к каждому весу

    Для softmax + cross-entropy $dZ=(P-Y)/n$.
    $$dW_2=H^TdZ,\quad db_2=\sum_i dZ_i,$$
    $$dH=dZW_2^T,\quad dA_1=dH\odot(1-H^2),$$
    $$dW_1=X^TdA_1,\quad db_1=\sum_i dA_{1,i}.$$

    `keepdims=True` сохраняет форму bias. Деление на n уже выполнено в dZ:
    повторное деление сделало бы градиент слишком маленьким.
    """)
    n.c("""
    def loss_and_gradients(parameters, X, y):
        hidden, logits, probability = forward(parameters, X)
        shifted = logits-logits.max(axis=1, keepdims=True)
        log_probability = shifted-np.log(np.exp(shifted).sum(axis=1, keepdims=True))
        loss = -log_probability[np.arange(len(y)), y].mean()
        d_logits = probability.copy()
        d_logits[np.arange(len(y)), y] -= 1
        d_logits /= len(y)
        d_hidden_pre = (d_logits @ parameters["W2"].T) * (1-hidden**2)
        gradients = {"W2": hidden.T @ d_logits, "b2": d_logits.sum(axis=0, keepdims=True),
                     "W1": X.T @ d_hidden_pre, "b1": d_hidden_pre.sum(axis=0, keepdims=True)}
        return loss, gradients
    initial_loss, initial_gradients = loss_and_gradients(params, X_train[:32], y_train[:32])
    assert np.isfinite(initial_loss)
    for key in params:
        assert initial_gradients[key].shape == params[key].shape
    print("Initial batch loss:", initial_loss)
    """)
    n.m("""
    ## 3. Gradient check: проверяем производную, а не красивую accuracy

    Берём по четыре заранее воспроизводимые координаты каждого массива параметров.
    Центральная разность приближает производную. Делаем это на float64 и небольшом
    batch, до обучения. Если проверка не проходит, сначала исправляют backprop,
    а не увеличивают число эпох.
    """)
    n.c("""
    X_probe, y_probe = X_train[:8].astype("float64"), y_train[:8]
    _, analytical = loss_and_gradients(params, X_probe, y_probe)
    eps, checks = 1e-5, []
    check_rng = np.random.default_rng(SEED)
    for key, values in params.items():
        for flat_index in check_rng.choice(values.size, size=min(4, values.size), replace=False):
            index = np.unravel_index(flat_index, values.shape)
            original = values[index]
            values[index] = original+eps; plus, _ = loss_and_gradients(params, X_probe, y_probe)
            values[index] = original-eps; minus, _ = loss_and_gradients(params, X_probe, y_probe)
            values[index] = original
            numeric = (plus-minus)/(2*eps)
            exact = analytical[key][index]
            checks.append({"parameter": key, "index": str(index), "analytic": exact,
                           "numeric": numeric, "absolute_error": abs(exact-numeric)})
    gradient_check = pd.DataFrame(checks)
    display(gradient_check)
    assert gradient_check.absolute_error.max() < 1e-6
    """)
    n.m("""
    ## 4. Обучение и validation checkpoint

    Один epoch здесь — один full-batch шаг на всех train-строках. Минимизируем train loss,
    а лучшую копию весов сохраняем по validation loss. Test не влияет ни на шаг,
    ни на количество эпох. Число 180 и learning rate 0.5 заданы до запуска.
    """)
    n.c("""
    learning_rate, epochs = 0.5, 180
    history, best_val_loss, best_params, best_epoch = [], np.inf, None, None
    for epoch in range(1, epochs+1):
        train_loss, gradients = loss_and_gradients(params, X_train, y_train)
        for key in params:
            params[key] -= learning_rate * gradients[key]
        val_loss, _ = loss_and_gradients(params, X_val, y_val)
        val_probability = forward(params, X_val)[2]
        history.append({"epoch": epoch, "train_loss_before_update": train_loss,
                        "validation_loss_after_update": val_loss,
                        "validation_accuracy": (val_probability.argmax(axis=1)==y_val).mean()})
        if val_loss < best_val_loss:
            best_val_loss, best_epoch = val_loss, epoch
            best_params = {key: value.copy() for key, value in params.items()}
    history = pd.DataFrame(history)
    assert np.isfinite(history.select_dtypes("number")).all().all()
    assert history.train_loss_before_update.iloc[-1] < history.train_loss_before_update.iloc[0]
    print("Validation checkpoint epoch:", best_epoch)
    """)
    n.c("""
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.5))
    history.plot(x="epoch", y=["train_loss_before_update", "validation_loss_after_update"], ax=axes[0])
    axes[0].set(ylabel="Cross entropy", title="Training dynamics")
    history.plot(x="epoch", y="validation_accuracy", ax=axes[1], legend=False)
    axes[1].set(ylabel="Accuracy", title="Validation checkpoint selection")
    plt.tight_layout(); plt.show()
    """)
    n.m("""
    ## 5. Итоговый test и baseline

    Восстанавливаем **лучший validation checkpoint**, затем впервые считаем test.
    Для классификации десяти цифр baseline выбирает наиболее частую цифру train.
    Не подбираем сеть после просмотра матрицы ошибок.
    """)
    n.c("""
    from sklearn.metrics import accuracy_score, classification_report, ConfusionMatrixDisplay
    test_probability = forward(best_params, X_test)[2]
    prediction = test_probability.argmax(axis=1)
    baseline_prediction = np.full(len(y_test), np.bincount(y_train).argmax())
    print("Baseline test accuracy:", accuracy_score(y_test, baseline_prediction))
    print("NumPy MLP test accuracy:", accuracy_score(y_test, prediction))
    print(classification_report(y_test, prediction, zero_division=0))
    assert np.allclose(test_probability.sum(axis=1), 1) and prediction.shape == y_test.shape
    ConfusionMatrixDisplay.from_predictions(y_test, prediction, colorbar=False)
    plt.title("NumPy backprop: final holdout"); plt.show()
    """)
    n.m("""
    ## 6. Что именно проверено

    Softmax устойчив к большим logits; формы градиентов совпадают с параметрами;
    выбранные производные совпали с конечными разностями; train loss уменьшился;
    checkpoint выбран без test. Gradient check охватывает 16 координат, а не
    доказывает правильность любой возможной сети или любого batch.

    **Перед следующим lab:** объясните, что в PyTorch/TensorFlow заменит функцию
    `loss_and_gradients`, где хранится градиент и почему optimizer не должен видеть test.

    Источники: [Stanford CS231n backprop](https://cs231n.github.io/optimization-2/),
    [Stanford CS231n neural networks](https://cs231n.github.io/neural-networks-1/),
    [MIT Introduction to Deep Learning](https://introtodeeplearning.com/).
    """)
    n.save(17, "01_backpropagation_numpy.ipynb")


def week17_torch():
    n = Notebook()
    intro(n, 17, "PyTorch: тот же цикл обучения с autograd",
          "обучить настоящую torch.nn сеть на локальных digits, проверить градиенты, сохранить validation checkpoint и выполнить детерминированный inference.",
          duration="27 минут guided comparison; подробный повтор — вне занятий")
    setup(n, 17)
    digits_split(n)
    n.m("""
    ## 1. Tensor, module, loss, optimizer

    Тензор хранит данные; `nn.Module` хранит слои и параметры; autograd вычисляет
    производные; optimizer обновляет веса. Работаем строго на CPU.
    `CrossEntropyLoss` получает **logits**, поэтому softmax перед loss не добавляем.
    Целевые классы — целые числа dtype `long`.
    """)
    n.c("""
    import torch
    from torch import nn
    from torch.utils.data import DataLoader, TensorDataset
    torch.manual_seed(SEED)
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    device = torch.device("cpu")
    Xtr = torch.tensor(X_train, dtype=torch.float32, device=device)
    ytr = torch.tensor(y_train, dtype=torch.long, device=device)
    Xva = torch.tensor(X_val, dtype=torch.float32, device=device)
    yva = torch.tensor(y_val, dtype=torch.long, device=device)
    model = nn.Sequential(nn.Linear(64, 32), nn.ReLU(), nn.Dropout(0.1), nn.Linear(32, 10)).to(device)
    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.003)
    loader = DataLoader(TensorDataset(Xtr, ytr), batch_size=64, shuffle=True,
        num_workers=0, generator=torch.Generator().manual_seed(SEED))
    print("PyTorch", torch.__version__, "parameters:", sum(p.numel() for p in model.parameters()))
    print(model)
    """)
    n.m(r"""
    ## 2. Один backward pass

    `loss.backward()` вычисляет $\partial L/\partial\theta$ и накапливает его в
    `.grad`. Поэтому перед новым шагом вызываем `zero_grad`.
    Здесь только инспектируем градиенты: `optimizer.step()` пока не выполняется.
    """)
    n.c("""
    model.train()
    optimizer.zero_grad(set_to_none=True)
    logits = model(Xtr[:64])
    loss = loss_fn(logits, ytr[:64])
    loss.backward()
    gradient_rows = []
    for name, parameter in model.named_parameters():
        assert parameter.grad is not None and torch.isfinite(parameter.grad).all()
        gradient_rows.append({"parameter": name, "shape": str(tuple(parameter.shape)),
                              "gradient_norm": parameter.grad.norm().item()})
    display(pd.DataFrame(gradient_rows))
    assert logits.shape == (64, 10)
    optimizer.zero_grad(set_to_none=True)
    """)
    n.m("""
    ## 3. Train и eval — разные режимы

    `model.train()` включает Dropout, `model.eval()` выключает его.
    `torch.no_grad()` отключает построение графа градиентов при оценке.
    Эти механизмы дополняют друг друга. Обучаем 24 эпохи, checkpoint выбираем
    по validation loss, а не по последней эпохе и не по test accuracy.
    """)
    n.c("""
    history, best_loss, best_state, best_epoch = [], float("inf"), None, None
    for epoch in range(1, 25):
        model.train(); loss_sum = 0.0
        for xb, yb in loader:
            optimizer.zero_grad(set_to_none=True)
            logits = model(xb)
            batch_loss = loss_fn(logits, yb)
            batch_loss.backward()
            optimizer.step()
            loss_sum += batch_loss.item()*len(xb)
        model.eval()
        with torch.no_grad():
            validation_logits = model(Xva)
            validation_loss = loss_fn(validation_logits, yva).item()
            validation_accuracy = (validation_logits.argmax(dim=1)==yva).float().mean().item()
        history.append({"epoch": epoch, "train_loss": loss_sum/len(Xtr),
                        "validation_loss": validation_loss, "validation_accuracy": validation_accuracy})
        if validation_loss < best_loss:
            best_loss, best_epoch = validation_loss, epoch
            best_state = {key: value.detach().clone() for key, value in model.state_dict().items()}
    model.load_state_dict(best_state)
    history = pd.DataFrame(history)
    assert np.isfinite(history.select_dtypes("number")).all().all()
    assert history.train_loss.iloc[-1] < history.train_loss.iloc[0]
    print("Restored validation checkpoint epoch:", best_epoch)
    """)
    n.c("""
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.5))
    history.plot(x="epoch", y=["train_loss", "validation_loss"], ax=axes[0])
    axes[0].set(ylabel="Cross entropy", title="PyTorch learning curves")
    history.plot(x="epoch", y="validation_accuracy", ax=axes[1], legend=False)
    axes[1].set(ylabel="Accuracy", title="Validation accuracy")
    plt.tight_layout(); plt.show()
    """)
    n.m("""
    ## 4. Финальный inference

    Восстановленные веса заморожены для отчёта. Softmax теперь нужен для просмотра
    вероятностей, а не для обучения. Высокая softmax-вероятность сама по себе
    не доказывает хорошую калибровку на новом распределении.
    """)
    n.c("""
    from sklearn.metrics import accuracy_score, classification_report, ConfusionMatrixDisplay
    model.eval()
    Xte = torch.tensor(X_test, dtype=torch.float32, device=device)
    with torch.no_grad():
        test_logits = model(Xte)
        probability = torch.softmax(test_logits, dim=1).cpu().numpy()
        repeated_logits = model(Xte)
    assert torch.equal(test_logits, repeated_logits), "Eval inference должен быть детерминированным"
    assert np.allclose(probability.sum(axis=1), 1, atol=1e-6)
    prediction = probability.argmax(axis=1)
    print("Baseline test accuracy:", np.mean(y_test == np.bincount(y_train).argmax()))
    print("PyTorch test accuracy:", accuracy_score(y_test, prediction))
    print(classification_report(y_test, prediction, zero_division=0))
    ConfusionMatrixDisplay.from_predictions(y_test, prediction, colorbar=False)
    plt.title("PyTorch: final holdout"); plt.show()
    """)
    n.m("""
    ## 5. Анализ ошибок без перенастройки

    Посмотрим до шести ошибочных предсказаний. Если ошибок меньше, показываем
    только имеющиеся. Это материал для следующей гипотезы, а не повод продолжить
    выбор checkpoint по test.
    """)
    n.c("""
    errors = np.flatnonzero(prediction != y_test)[:6]
    if len(errors):
        fig, axes = plt.subplots(1, len(errors), figsize=(2.1*len(errors), 2.5), squeeze=False)
        for ax, index in zip(axes.ravel(), errors):
            ax.imshow(X_test[index].reshape(8, 8), cmap="gray_r", vmin=0, vmax=1)
            ax.set_title(f"true={y_test[index]}, pred={prediction[index]}"); ax.axis("off")
        plt.tight_layout(); plt.show()
    else:
        print("На этом holdout ошибок нет; это не гарантия качества на новых авторах почерка.")
    """)
    n.m("""
    ## Сопоставление с NumPy

    `forward` заменён слоями; ручной chain rule — autograd; обновление массивов —
    Adam. В этой сети ReLU и Dropout, в NumPy lab — tanh и full-batch SGD, поэтому
    значения метрик не должны совпадать. Чтобы сравнить реализации численно,
    нужно одинаково задать архитектуру, веса, batch order, optimizer и dtype.

    Источники: [PyTorch optimization tutorial](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html),
    [autograd basics](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html),
    [reproducibility](https://docs.pytorch.org/docs/stable/notes/randomness.html).
    """)
    n.save(17, "02_pytorch_digits_training.ipynb")


def week17_keras():
    n = Notebook()
    intro(n, 17, "TensorFlow/Keras: модель, compile и обучение по batch",
          "обучить настоящую tf.keras сеть на том же локальном наборе, понять from_logits и GradientTape, выбрать validation checkpoint и проверить прогнозы.",
          duration="27 минут guided comparison; подробный повтор — вне занятий")
    setup(n, 17)
    digits_split(n)
    n.m("""
    ## 1. Реальный TensorFlow backend

    Используем `tf.keras`, а не замену на scikit-learn. GPU отключён: пример
    рассчитан на обычный CPU. Seeds и число потоков заданы явно. Разные версии
    TensorFlow/BLAS всё же могут давать небольшие численные отличия.
    """)
    n.c("""
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
    os.environ.setdefault("TF_NUM_INTRAOP_THREADS", "1")
    os.environ.setdefault("TF_NUM_INTEROP_THREADS", "1")
    import tensorflow as tf
    tf.config.threading.set_intra_op_parallelism_threads(1)
    tf.config.threading.set_inter_op_parallelism_threads(1)
    tf.keras.utils.set_random_seed(SEED)
    tf.config.experimental.enable_op_determinism()
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(64,)), tf.keras.layers.Dense(32, activation="relu"),
        tf.keras.layers.Dropout(0.1), tf.keras.layers.Dense(10)])
    loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.003),
                  loss=loss_fn, metrics=[tf.keras.metrics.SparseCategoricalAccuracy(name="accuracy")],
                  jit_compile=False)
    print("TensorFlow", tf.__version__); model.summary()
    assert model.count_params() == (64*32+32)+(32*10+10)
    """)
    n.m(r"""
    ## 2. Проверяем autograd через GradientTape

    `GradientTape` записывает операции forward pass и возвращает градиенты loss
    по trainable variables. `from_logits=True` объединяет softmax и cross-entropy
    устойчивым образом. Добавлять ещё один softmax перед этим loss не нужно.
    """)
    n.c("""
    with tf.GradientTape() as tape:
        logits = model(X_train[:64], training=False)
        batch_loss = loss_fn(y_train[:64], logits)
    gradients = tape.gradient(batch_loss, model.trainable_variables)
    gradient_rows = []
    for variable, gradient in zip(model.trainable_variables, gradients):
        assert gradient is not None and bool(tf.reduce_all(tf.math.is_finite(gradient)))
        gradient_rows.append({"variable": variable.name, "shape": str(tuple(variable.shape)),
                              "gradient_norm": float(tf.linalg.global_norm([gradient]))})
    display(pd.DataFrame(gradient_rows))
    assert tuple(logits.shape) == (64, 10)
    """)
    n.m("""
    ## 3. Keras train_on_batch и checkpoint

    `train_on_batch` — полноценный Keras training API. Явный batch-цикл показывает,
    как устроена эпоха, и работает без дополнительных tf.data thread pools.
    `compile` уже задал optimizer/loss; Keras сам делает backward и update.
    Validation считаем с `training=False`, чтобы отключить Dropout.
    """)
    n.c("""
    history, best_loss, best_weights, best_epoch = [], float("inf"), None, None
    shuffle_rng = np.random.default_rng(SEED)
    for epoch in range(1, 25):
        order = shuffle_rng.permutation(len(X_train))
        model.reset_metrics()
        for start in range(0, len(order), 64):
            batch = order[start:start+64]
            batch_metrics = model.train_on_batch(X_train[batch], y_train[batch], return_dict=True)
        # Метрики Keras агрегируются со времени reset_metrics; validation считаем отдельно.
        val_logits = model(X_val, training=False)
        validation_loss = float(loss_fn(y_val, val_logits))
        validation_accuracy = np.mean(np.asarray(val_logits).argmax(axis=1)==y_val)
        history.append({"epoch": epoch, "train_loss": float(batch_metrics["loss"]),
                        "validation_loss": validation_loss, "validation_accuracy": validation_accuracy})
        if validation_loss < best_loss:
            best_loss, best_epoch = validation_loss, epoch
            best_weights = [weight.copy() for weight in model.get_weights()]
    model.set_weights(best_weights)
    history = pd.DataFrame(history)
    assert np.isfinite(history.select_dtypes("number")).all().all()
    assert history.train_loss.iloc[-1] < history.train_loss.iloc[0]
    print("Restored validation checkpoint epoch:", best_epoch)
    """)
    n.c("""
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.5))
    history.plot(x="epoch", y=["train_loss", "validation_loss"], ax=axes[0])
    axes[0].set(ylabel="Cross entropy", title="Keras learning curves")
    history.plot(x="epoch", y="validation_accuracy", ax=axes[1], legend=False)
    axes[1].set(ylabel="Accuracy", title="Validation accuracy")
    plt.tight_layout(); plt.show()
    """)
    n.m("""
    ## 4. Финальный test

    Выбор checkpoint завершён до test. Прямой вызов модели удобен для небольшого
    локального массива; `tf.nn.softmax` переводит logits в вероятности для отчёта.
    Повторный inference с выключенным Dropout должен совпасть.
    """)
    n.c("""
    from sklearn.metrics import accuracy_score, classification_report, ConfusionMatrixDisplay
    test_logits = model(X_test, training=False)
    repeated_logits = model(X_test, training=False)
    probability = tf.nn.softmax(test_logits, axis=1).numpy()
    prediction = probability.argmax(axis=1)
    assert np.allclose(test_logits.numpy(), repeated_logits.numpy(), atol=1e-7)
    assert np.allclose(probability.sum(axis=1), 1, atol=1e-6)
    assert prediction.shape == y_test.shape
    print("Baseline test accuracy:", np.mean(y_test == np.bincount(y_train).argmax()))
    print("Keras test accuracy:", accuracy_score(y_test, prediction))
    print(classification_report(y_test, prediction, zero_division=0))
    ConfusionMatrixDisplay.from_predictions(y_test, prediction, colorbar=False)
    plt.title("TensorFlow/Keras: final holdout"); plt.show()
    """)
    n.m("""
    ## 5. Читаем одно распределение вероятностей

    Самый вероятный класс — argmax. Разность первых двух вероятностей — простая
    характеристика неоднозначности этого прогноза, но не доверительный интервал
    и не оценка ошибки в новых условиях.
    """)
    n.c("""
    index = 0
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.5))
    axes[0].imshow(X_test[index].reshape(8, 8), cmap="gray_r", vmin=0, vmax=1)
    axes[0].set_title(f"True={y_test[index]}, prediction={prediction[index]}"); axes[0].axis("off")
    axes[1].bar(np.arange(10), probability[index]); axes[1].set_xticks(np.arange(10))
    axes[1].set(xlabel="Digit class", ylabel="Softmax probability", title="Fixed model output")
    plt.tight_layout(); plt.show()
    top_two = np.sort(probability[index])[-2:]
    print("Top-two probability gap:", top_two[1]-top_two[0])
    """)
    n.m("""
    ## Сравните три реализации

    NumPy требует явных производных; TensorFlow и PyTorch вычисляют их автоматически.
    Keras `compile/train_on_batch` содержит optimizer-step; в PyTorch он записан
    в цикле. Оба framework обучили настоящие сети на локальных данных. Разные
    инициализации и детали optimizer означают, что метрики не обязаны совпадать.

    **Контроль:** объясните `from_logits`, `training=False`, batch, epoch, validation
    checkpoint и запрет выбора числа эпох по test.

    Источники: [TensorFlow automatic differentiation](https://www.tensorflow.org/guide/autodiff),
    [Keras model training APIs](https://keras.io/api/models/model_training_apis/),
    [Keras Sequential guide](https://keras.io/guides/sequential_model/),
    [TensorFlow beginner tutorial](https://www.tensorflow.org/tutorials/quickstart/beginner).
    """)
    n.save(17, "03_tensorflow_keras_digits_training.ipynb")


WEEK_DETAILS = {
    9: {
        "prerequisites": "Недели 02–03 и 08: NumPy/pandas, матричные операции, train/test, StandardScaler и Pipeline.",
        "outcomes": ["Записать линейную модель, MSE и градиент с правильными размерностями.",
                     "Реализовать least squares и gradient descent, проверить производную конечной разностью.",
                     "Подобрать Ridge по CV и объяснить остатки без причинных утверждений."],
        "practice": ["Train EDA → матрица дизайна → least squares → градиентный спуск и проверка градиента.",
                     "Baseline/Pipeline → Ridge CV → финальный test → residual plot и ограничения."],
        "labs": ["01_linear_regression_from_scratch.ipynb"], "dataset": "diabetes_raw.csv", "minutes": 150,
        "tasks": [
            ("Аудит и train EDA", 15, "Разделите raw Diabetes с seed=109 и test_size=0.25. Исключите sample_id/target из X. На train посчитайте mean/median/std и пропуски; постройте распределение target и связь bmi–target. Напишите два наблюдения и одну проверяемую гипотезу. Сохраните идентификаторы split."),
            ("Собственный решатель", 25, "Реализуйте MSE gradient descent для bmi и bp с intercept. Scaler обучайте только на train. Покажите loss curve, проверьте не менее трёх координат градиента центральной разностью; сравните train-предсказания с np.linalg.lstsq. Объясните условие выбора шага и используемую численную погрешность."),
            ("Pipeline и регуляризация", 25, "На всех десяти признаках сравните DummyRegressor, OLS и Ridge. Для Ridge используйте 5-fold CV и заранее записанную сетку минимум четырёх alpha. Сохраните mean/std CV RMSE, правило выбора и итоговые параметры; preprocessing должен находиться внутри CV pipeline."),
            ("Финальная оценка", 20, "После фиксации модели один раз откройте test. Рассчитайте MAE, RMSE, R² и постройте predicted-vs-observed и residual plot. Добавьте проверки конечности прогнозов и непересечения ID. Не меняйте alpha после test."),
            ("Технический вывод", 15, "В 200–350 словах объясните результат относительно baseline, единицы коэффициентов, связь регуляризации с коррелированными признаками и ограничения маленького набора. Укажите, что потребуется для следующего независимого эксперимента.")],
        "hints": "Сначала отладьте loss и gradient на маленьком массиве. Не обращайте XᵀX явно. Отрицательный sklearn score для RMSE нужно умножить на −1. CV fold SD не равен доверительному интервалу."
    },
    10: {
        "prerequisites": "Неделя 09: train/validation/test, Pipeline, градиент; базовая вероятность и массивы NumPy.",
        "outcomes": ["Отделить вероятность sigmoid от правила выбора класса.", "Подобрать порог по validation и объяснить FP/FN.", "Проверить kNN вручную и показать влияние единиц измерения."],
        "practice": ["Бинарная постановка Wine → EDA → sigmoid/log loss → logistic fit → validation threshold.",
                     "Raw/scaled kNN → ручные соседи → CV по k → фиксированный test и ROC/матрица ошибок."],
        "labs": ["01_logistic_regression_and_knn.ipynb"], "dataset": "wine.csv", "minutes": 150,
        "tasks": [
            ("Постановка и EDA", 15, "Создайте бинарную цель target==0. С seed=110 выделите stratified test 25%, затем validation внутри train. Покажите баланс и распределения двух признаков на fit. Докажите проверкой, что исходный target не остался в X."),
            ("Logistic и стоимость решений", 25, "Обучите StandardScaler→LogisticRegression. На validation сравните пороги 0.2, 0.35, 0.5, 0.65 и 0.8 при цене FN=4 и FP=1. Выберите правило до test; покажите confusion counts и cost per sample для всей сетки. Объясните log loss отдельно от accuracy."),
            ("kNN и расстояния", 25, "Сравните raw и scaled kNN на одинаковых CV folds. Для scaled варианта подберите k из 3, 5, 9, 15. Для одного validation объекта вручную найдите соседей и воспроизведите вероятность uniform kNN. Исследуйте смену единиц proline на fit/validation; не используйте test для этого опыта."),
            ("Финальная проверка", 20, "На запечатанном test оцените заранее выбранные logistic и kNN: precision, recall, F1, balanced accuracy и ROC AUC. Для logistic примените выбранный порог. Покажите confusion matrix, объясните различие метрик порога и вероятностей."),
            ("Защита решения", 15, "Опишите split, правила выбора k/threshold, обучающие бюджеты моделей и ограничения малой validation. Объясните, почему изменение порога не меняет ROC AUC для тех же вероятностей и почему выбор лучшего test-порога недопустим.")],
        "hints": "Для бинарной вероятности выбирайте колонку класса 1. StandardScaler нельзя fit на validation/test. Для kNN сопоставляйте метки соседей по позициям, а не случайно перемешанным индексам."
    },
    11: {
        "prerequisites": "Недели 09–10: классификация, macro F1, CV, масштабирование; понимание векторов и расстояний.",
        "outcomes": ["Вычислить Gini gain и прочитать путь дерева.", "Объяснить trade-off глубины, margin, C и gamma.", "Сравнить tree/SVM на общих folds и отличить 2D-иллюстрацию от полной модели."],
        "practice": ["Train EDA → ручной Gini gain → дерево глубины 2 → depth validation curve.",
                     "Hinge/RBF → одинаковые CV folds для tree/SVM → 2D-границы → final holdout."],
        "labs": ["01_decision_trees_and_svm.ipynb"], "dataset": "wine.csv", "minutes": 150,
        "tasks": [
            ("Трёхклассовая задача", 15, "Используйте исходный Wine target 0/1/2. Сделайте stratified split seed=111, test_size=0.25. Обоснуйте macro F1, покажите таблицу class counts и EDA двух выбранных признаков на train."),
            ("Дерево и impurity", 25, "Для выбранного признака вручную рассчитайте Gini gain минимум пяти допустимых порогов. Обучите дерево глубины 2, визуализируйте его и распишите путь одного train-объекта. Убедитесь, что pure leaf имеет Gini=0; покажите train/CV кривую для глубин 1,2,3,5,8."),
            ("SVM и подбор", 25, "Соберите StandardScaler→SVC. На одних stratified folds сравните linear kernel и RBF с минимум тремя C и двумя gamma. Объявите сетку до запуска. Сопоставьте CV mean/std с ограниченным деревом и выберите финальную модель только по CV."),
            ("Геометрия и test", 20, "Постройте 2D decision boundaries отдельных tree/SVM, обученных на двух признаках train, и подпишите, что это отдельные иллюстрации. Затем один раз оцените выбранную полную модель на test: macro F1, per-class recall, confusion matrix и baseline."),
            ("Объяснение сложности", 15, "Объясните C, gamma и max_depth на языке ошибок и формы границы. Укажите, почему признаки масштабируются для SVM, почему высокий train score недостаточен и почему маленький test не даёт универсальной гарантии.")],
        "hints": "Gini делится по числу строк в дочерних узлах. Для multiclass F1 укажите average='macro'. В 2D-grid передавайте те же два имени столбцов, что при fit."
    },
    12: {
        "prerequisites": "Неделя 11: деревья, impurity, CV; среднее, дисперсия и выборка с возвращением.",
        "outcomes": ["Собрать bootstrap и интерпретировать OOB-покрытие.", "Различать bagging и Random Forest, объяснять роль корреляции ошибок.", "Подбирать параметры без test и корректно читать permutation importance."],
        "practice": ["Train EDA → bootstrap/OOB → ручной bagging → single tree/bagging/RF на общих folds.",
                     "OOB accuracy и macro F1 → CV grid → seed stability → permutation importance → test."],
        "labs": ["01_bagging_random_forest_oob.ipynb"], "dataset": "wine.csv", "minutes": 165,
        "tasks": [
            ("Bootstrap эксперимент", 15, "С seed=112 выделите stratified test 25%. На train сгенерируйте 200 bootstrap-выборок и посчитайте среднюю/SD долю OOB. Сопоставьте с (1−1/n)^n. Покажите histogram и проверку размера каждой выборки."),
            ("Сравнение ансамблей", 25, "На одинаковых 4-fold CV сравните single tree, BaggingClassifier и RandomForestClassifier с объявленными заранее параметрами. В ручном ансамбле минимум пяти деревьев усредните вероятности и проверьте их сумму. Укажите разницу случайности строк и признаков."),
            ("OOB и tuning", 25, "Для леса с bootstrap=True вычислите oob_score_ и собственный OOB macro F1 с проверкой покрытия всех строк. Подберите max_features/min_samples_leaf на CV train; покажите полную маленькую таблицу параметров. Не называйте выбранный OOB независимым test."),
            ("Устойчивость и финальный отчёт", 20, "На внутреннем validation измерьте вариативность качества для пяти seeds, не выбирая лучший. Постройте permutation importance с повторениями на validation. После фиксации параметров оцените test macro F1 и confusion matrix; не переобучайте после просмотра ошибок."),
            ("Критический разбор", 15, "Объясните предел пользы большого числа деревьев, различие OOB accuracy и macro F1, ограничения importance при коррелированных признаках и почему вариативность seed не равна полной неопределённости модели.")],
        "hints": "OOB определяется отдельно для каждого дерева. Учитывайте порядок classes_ при усреднении вероятностей. OOB требует bootstrap=True; при слишком малом числе деревьев некоторые строки могут не иметь OOB-прогноза."
    },
    13: {
        "prerequisites": "Недели 09, 11–12: регрессия, деревья, CV, градиент и ансамбли. Дополнительные зависимости: xgboost, lightgbm.",
        "outcomes": ["Собрать additive model на остатках.", "Запустить sklearn GB, XGBoost и LightGBM и описать различия параметров.", "Подготовить промежуточный проект с закрытым test и воспроизводимой карточкой эксперимента."],
        "practice": ["Train EDA → ручной boosting → реальные библиотеки → общий CV baseline.",
                     "Равный небольшой search budget → early stopping на validation → final test → карточка midterm."],
        "labs": ["01_boosting_xgboost_lightgbm_midterm.ipynb"], "dataset": "diabetes_raw.csv", "minutes": 210,
        "tasks": [
            ("Паспорт промежуточного проекта", 15, "Сформулируйте задачу raw Diabetes, target, недопустимые признаки, метрику и ограничения. Зафиксируйте split seed=113, test 25%, список train IDs и hash CSV. Выполните train EDA и задайте DummyRegressor baseline."),
            ("Механика boosting", 20, "Реализуйте минимум 20 итераций residual boosting с shallow trees. Покажите уменьшение train loss, validation curve и восстановление прогноза как суммы деревьев. Объясните различие градиента по прогнозу и по параметрам дерева."),
            ("Три настоящие библиотеки", 30, "Реально обучите sklearn GradientBoosting, XGBoost и LightGBM. Используйте общие 3-fold CV, одинаковое число кандидатов (не менее четырёх на семейство), CPU и фиксированные seeds. Приведите параметры и версии; замена XGBoost/LightGBM на sklearn не засчитывается."),
            ("Early stopping и test", 20, "Покажите early stopping одной библиотеки на fit/validation внутри train. Отдельно зафиксируйте итоговый протокол выбора модели и числа деревьев. После выбора откройте test один раз, посчитайте MAE/RMSE/R² и baseline. Нарисуйте residual plot."),
            ("Midterm memo", 15, "Сдайте notebook и memo на 400–600 слов: постановка, provenance, split, search budget, CV-таблица, final test, ограничения и следующий эксперимент. Различайте измеренное время на малом наборе и общий рейтинг библиотек. Приложите команду воспроизведения.")],
        "hints": "eval_set не должен содержать test. XGBoost best_iteration имеет нумерацию с нуля; LightGBM best_iteration_ — количество итераций. Сохраняйте параметры, которые действительно участвовали в финальном fit."
    },
    14: {
        "prerequisites": "Недели 08–12: масштабирование, расстояния, матрицы; различие supervised/unsupervised. PCA не требует знания нейросетей.",
        "outcomes": ["Рассчитать шаг K-Means и корректно выбрать внутренний критерий.", "Объяснить DBSCAN noise и отсутствие стандартного predict.", "Различать PCA transform и transductive t-SNE; не приписывать проекции лишний смысл."],
        "practice": ["Unlabelled Wine → scaling → ручной Lloyd-step → k и silhouette → DBSCAN moons.",
                     "PCA/SVD/loadings → holdout transform и внешний ARI-аудит → два t-SNE и ограничения."],
        "labs": ["01_clustering_pca_tsne.ipynb"], "dataset": "wine.csv", "minutes": 165,
        "tasks": [
            ("Unsupervised protocol", 15, "Разделите Wine случайно с seed=114 и test_size=0.25 без stratify по target. Уберите target из алгоритмов. На train покажите EDA и обучите scaler. Запишите, когда разрешено раскрыть классы для внешнего аудита."),
            ("K-Means", 25, "Реализуйте один Lloyd-step и проверьте невозрастание objective при пересчёте центров. На train сравните k=2…6 по inertia/silhouette и зафиксируйте выбор. На holdout примените прежний scaler/центры, затем раскройте target для ARI и contingency table."),
            ("DBSCAN", 25, "На локальном moons_synthetic.csv исследуйте не менее четырёх eps при фиксированном min_samples. Покажите число кластеров, noise fraction и silhouette только там, где он определён. Сравните геометрию с K-Means и явно назовите опыт трансдуктивным."),
            ("PCA и t-SNE", 20, "PCA обучите на Wine train; покажите explained variance, loadings и реконструкционную ошибку. Примените transform к test без refit. Для train постройте t-SNE при двух perplexity и двух seeds; не используйте красивые острова как доказательство количества классов."),
            ("Интерпретация", 15, "Для каждого алгоритма напишите: цель, что означает метрика, есть ли штатный predict/transform для новых строк, какие выводы допустимы. Объясните произвольность cluster IDs, проблему глобальных расстояний t-SNE и отличие кластера от класса.")],
        "hints": "Silhouette не определён при одном кластере или если каждый объект — свой кластер. DBSCAN label=-1 означает noise. PCA signs произвольны; важны направления/подпространство. В t-SNE perplexity должно быть меньше числа строк."
    },
    15: {
        "prerequisites": "Недели 09–14: метрики базового уровня, классификация/регрессия, CV, Pipeline и train/test discipline.",
        "outcomes": ["Рассчитать и объяснить classification/regression metrics.", "Построить validation/learning curves и nested-OOF threshold.", "Выбрать GroupKFold или TimeSeriesSplit по единице наблюдения и моменту прогноза."],
        "practice": ["Imbalance EDA → ручные метрики → baseline multi-metric CV → overfitting curves.",
                     "Nested OOF → cost threshold → final test/ROC/PR → group/time split assertions."],
        "labs": ["01_metrics_cv_and_overfitting.ipynb"], "dataset": "imbalanced_synthetic.csv", "minutes": 180,
        "tasks": [
            ("Аудит редкого класса", 15, "Используйте synthetic dataset и split seed=115, test_size=0.25, stratify=target. Покажите train prevalence, EDA и majority/prior baseline. Объясните, почему accuracy не является достаточным основным критерием."),
            ("Арифметика метрик", 25, "Напишите собственные precision/recall/F1 из TP/FP/FN и MAE/RMSE/R² для небольших придуманных массивов. Сверьте со sklearn, включая отсутствие predicted positives. Объясните разницу AP и ROC AUC, macro и micro, probability metric и threshold metric."),
            ("CV, overfit и threshold", 25, "Постройте train/CV curve для глубины дерева. Получите OOF probabilities logistic модели; если подбираете C, делайте это внутри каждого outer fold. По OOF выберите threshold при FN=6, FP=1; покажите таблицу стоимости. Test запрещён в этом шаге."),
            ("Финальная оценка", 20, "После refit на train один раз оцените test: AP, ROC AUC, log loss, precision, recall, F1 и cost per sample. Сравните заранее объявленные пороги 0.5 и OOF. Постройте PR/ROC и confusion matrix; покажите, какие числа не изменились при смене порога."),
            ("Выбор схемы проверки", 15, "Для трёх сценариев (новый клиент, новые визиты известных клиентов, прогноз следующего месяца) предложите и обоснуйте split. На синтетических ID покажите GroupKFold без пересечения групп и TimeSeriesSplit с проверкой порядка. Объясните, почему fold SD не является готовым 95% CI.")],
        "hints": "Нельзя сначала подобрать C по всем train labels, а затем называть ordinary OOF для этого выбранного C полностью независимым от подбора. Для более простой версии объявите C заранее; для подбора используйте nested CV."
    },
    16: {
        "prerequisites": "Недели 09–15: регрессия/лес, validation, метрики и train/test; функции активации вводятся с нуля. Зависимости: shap, lime.",
        "outcomes": ["Получить настоящие SHAP/LIME explanations и проверить их свойства.", "Описать background, output scale, fidelity и ограничения причинных выводов.", "Вычислить forward pass нейрона/слоя и подготовиться к backprop."],
        "practice": ["Train/validation RF → SHAP additivity/waterfall → LIME fidelity/stability → fixed test.",
                     "Нейрон как регрессия/logistic → activation plots → XOR forward pass → формы тензоров."],
        "labs": ["01_shap_lime_and_neuron.ipynb"], "dataset": "diabetes_raw.csv", "minutes": 180,
        "tasks": [
            ("Модель для объяснения", 15, "С seed=116 выделите test 25% и validation внутри train. Проведите fit EDA, обучите ограниченный RandomForestRegressor и baseline; зафиксируйте параметры. Объяснять разрешено validation, фоновые данные брать только из fit."),
            ("Реальный SHAP", 25, "Вызовите shap.TreeExplainer для 15–25 validation объектов с feature_perturbation='tree_path_dependent'. Опишите референсное распределение: train-статистики листьев обученной модели; отдельная фоновая выборка не передаётся. Проверьте base_value+sum(SHAP)=predict в согласованных единицах. Постройте waterfall одного объекта и mean absolute SHAP; опишите, к какой выборке относится глобальный график."),
            ("Реальный LIME", 25, "Получите LimeTabularExplainer regression explanation того же объекта. Покажите исходный прогноз, surrogate prediction, абсолютную ошибку и local R². Повторите с тремя seeds и сравните top conditions. Сопоставьте с SHAP, не называя коэффициенты одинаковыми величинами."),
            ("Нейрон и tensor shapes", 20, "На синтетических XOR-точках реализуйте два слоя с tanh или ReLU и sigmoid-выходом. Выпишите формы X/W/b/hidden/logits, посчитайте stable binary cross-entropy и нарисуйте три функции активации. Явно отметьте, что forward pass с заданными весами ещё не является обучением."),
            ("Отчёт и финальная проверка", 15, "Один раз оцените test той модели, которую объясняли. В отчёте отделите качество предсказаний, локальную fidelity и причинность. Опишите влияние background, коррелированных признаков и переобучения модели на действительность прежних объяснений.")],
        "hints": "Регрессионный RF позволяет объяснять SHAP в единицах target. LIME ожидает callable, возвращающий прогнозы для 2D массива; восстановите имена и порядок столбцов. Высокий local R² не означает глобальную или причинную верность."
    },
    17: {
        "prerequisites": "Неделя 16: нейрон, loss и активации; NumPy и chain rule на уровне формул; локально установлены torch и tensorflow.",
        "outcomes": ["Реализовать backward двухслойной сети и проверить градиенты.", "Реально обучить сети в PyTorch и tf.keras на одинаковых локальных данных.", "Использовать validation checkpoint, режим inference и корректный logits loss."],
        "practice": ["Digits EDA → NumPy softmax/CE → chain rule → finite differences → обучение/checkpoint (54 мин).",
                     "PyTorch: forward/backward/optimizer (27 мин); TensorFlow/Keras: GradientTape/train_on_batch (27 мин)."],
        "labs": ["01_backpropagation_numpy.ipynb", "02_pytorch_digits_training.ipynb", "03_tensorflow_keras_digits_training.ipynb"],
        "dataset": "digits_8x8.csv", "minutes": 210,
        "tasks": [
            ("Данные и единый протокол", 15, "На локальном digits сделайте примерно 60/20/20 train/validation/test с seeds 117 и 118. Нормируйте пиксели известной константой 16, исключите ID/target. Сохраните одни и те же индексы для всех реализаций и покажите train class counts, pixel histogram и 12 изображений."),
            ("NumPy backprop", 25, "Реализуйте сеть 64→16→10 с tanh и stable softmax CE. Выведите формы градиентов, проверьте конечными разностями не менее 12 ненулевых координат разных параметров. Обучите сеть; checkpoint выбирайте по validation loss, а не test accuracy."),
            ("Два настоящих framework", 25, "Обучите PyTorch и TensorFlow/Keras сети на тех же split IDs. Используйте реальные библиотеки, integer class targets и loss from logits. Покажите ненулевые конечные градиенты, learning curves и restore best validation weights. Хотя бы один framework реализуйте с явным batch loop."),
            ("Воспроизводимая оценка", 20, "Зафиксируйте seeds, число потоков, версии, архитектуры, optimizer, learning rate и число эпох. После выбора checkpoint оцените каждую модель один раз на общем test: accuracy/macro F1, baseline и confusion matrix. Проверьте сумму вероятностей и повторяемость eval inference."),
            ("Сравнение и ограничения", 15, "Объясните различия autograd и ручного chain rule, train/eval и training=False, batch/epoch и роли zero_grad. В 250–400 словах сравните наблюдения, не делая рейтинга framework по одному split; отметьте отсутствие writer IDs в локальном наборе.")],
        "hints": "PyTorch CrossEntropyLoss и Keras SparseCategoricalCrossentropy(from_logits=True) ожидают logits. Softmax применяют после обучения для отчёта. В NumPy проверяйте gradient на float64 и ненулевых координатах; в framework обновлениями управляет optimizer."
    },
}


def make_readme_and_homework(week):
    details, plan = WEEK_DETAILS[week], PLAN[week]
    folder = ROOT / plan["folder"]
    table_rows = []
    for index, (session, practice) in enumerate(zip(plan["sessions"], details["practice"]), start=1):
        table_rows.append(f"| {index} · модуль {session['module']} | {session['topic']} | {practice} | 90 мин |")
    content = f"# Неделя {week:02d} — {plan['title']}\n\n"
    content += "**Tech Orda course authored by Gizatov A. S.**\n\n"
    content += "## Место в расписании\n\n**2 занятия × 90 минут = 180 астрономических минут = 4 академических часа по 45 минут.** На каждом занятии 36 минут теории и 54 минуты практики: 72/108 минут за неделю, то есть 40%/60%. Домашняя работа ниже — самостоятельная нагрузка сверх этих часов.\n\n"
    content += "| Занятие | Теория: 36 минут | Практика: 54 минуты | Всего |\n|---|---|---|---|\n" + "\n".join(table_rows) + "\n\n"
    if week == 16:
        content += "Неделя пересекает границу модулей: занятие 1 завершает модуль 9 (интерпретация), занятие 2 начинает модуль 10 (нейросети).\n\n"
    content += "## Результаты обучения\n\n" + "".join(f"- {item}\n" for item in details["outcomes"])
    content += f"\n**Предварительные знания:** {details['prerequisites']}\n\n"
    content += "## Материалы недели\n\n"
    content += "- [presentations/](presentations/): дополнительные материалы университетов. Читайте карточку источника/маршрут в этой папке; углублённые разделы не обязательны для первого прохождения.\n"
    for filename in details["labs"]:
        content += f"- [practice/{filename}](practice/{filename}): авторская практика с русскими пояснениями, формулами, кодом, графиками и проверками.\n"
    content += "- [datasets/README.md](datasets/README.md): происхождение, преобразования, словарь данных; CSV и SHA-256 metadata рядом.\n"
    content += f"- [Homework Week {week}](homework/Homework_Week_{week:02d}.md): задания, время, критерии на 100 баллов и формат сдачи.\n"
    content += f"- [Homework_Week_{week:02d}_starter.ipynb](homework/Homework_Week_{week:02d}_starter.ipynb): незаполненный запускаемый стартер. TODO отмечены явно; запуск не означает выполнение домашней работы.\n\n"
    content += "## Как провести занятие\n\nПеред исполнением ячейки студент формулирует ожидаемый результат. После графика — одно наблюдение и одно ограничение. Преподаватель разбирает источник данных и границу train/validation/test до сравнения моделей. Практические notebooks содержат полный маршрут; часть обсуждения переносится в самостоятельное чтение при более медленном темпе группы.\n\n"
    content += "В Jupyter откройте notebook внутри клонированного репозитория и выберите **Restart Kernel → Run All**. Поддерживается рабочая директория корня, `practice/` или `homework/`. Установите зависимости по корневому README заранее. Во время исполнения не нужны интернет, API-ключи и GPU.\n\n"
    if week in [13, 16, 17]:
        deps = {13: "xgboost и lightgbm", 16: "shap и lime", 17: "torch и tensorflow"}[week]
        content += f"**Дополнительные реальные библиотеки:** {deps}. Отсутствующий пакет должен быть установлен; подмена библиотек на sklearn не считается выполнением темы.\n\n"
    content += "## Критерий завершения недели\n\nСтудент может объяснить каждую существенную ячейку, происхождение данных, смысл метрик и границы вывода. Корректность включает схемы/размерности, численные sanity checks, отсутствие target leakage и честный протокол проверки. Наличие высокой accuracy само по себе не является критерием правильности.\n\n"
    content += "Университетские материалы и datasets сохраняют авторство исходных авторов. Название курса относится к авторской организации программы, русским практикам и домашним заданиям.\n"
    (folder / "README.md").write_text(content, encoding="utf-8")

    hw = f"# Homework Week {week} — {plan['title']}\n\n"
    hw += f"**Время:** ориентировочно {details['minutes']} минут самостоятельной работы; не входит в 4 академических часа недели. **Уровень:** beginner с опорой на практику. **Максимум:** 100 баллов.\n\n"
    hw += "## Цель\n\nСамостоятельно воспроизвести ход эксперимента, проверить код и обосновать выводы. Можно опираться на lab, но изменённые условия и результаты нужно объяснить собственными словами.\n\n"
    hw += "## Задания\n\n"
    for index, (title, points, task) in enumerate(details["tasks"], start=1):
        hw += f"### {index}. {title} — {points} баллов\n\n{task}\n\n"
    hw += "## Рубрика\n\n| Критерий | Баллы | Что проверяется |\n|---|---:|---|\n"
    for title, points, task in details["tasks"]:
        hw += f"| {title} | {points} | Все результаты и проверки соответствующего задания представлены; объяснение согласуется с кодом и наблюдениями. |\n"
    hw += "| **Итого** | **100** | Корректность, воспроизводимость и содержательная интерпретация. |\n\n"
    hw += "Ориентир оценки внутри каждого задания: 60% баллов — корректные вычисления/протокол; 25% — объяснение и графики; 15% — воспроизводимость и проверки. Пустой TODO или текст без требуемых вычислений не получает баллы за реализацию. Утечка target/test лишает баллов за соответствующий этап оценки; ошибка должна быть исправлена, а результат пересчитан.\n\n"
    hw += "## Что сдать\n\n"
    hw += f"- `Surname_Week_{week:02d}.ipynb` на основе [стартера](Homework_Week_{week:02d}_starter.ipynb), выполненный сверху вниз, с сохранёнными outputs и именем студента.\n"
    hw += "- Итоговый вывод в Markdown внутри notebook; таблицы, формулы, подписи осей и единицы там, где они известны.\n"
    if week == 13:
        hw += "- `Midterm_Memo.md` с кратким отчётом и командой воспроизведения.\n"
    hw += "- Версии использованных библиотек, random seeds и описание split. Используйте относительные пути; исходные CSV не изменяйте.\n\n"
    hw += "Перед сдачей перезапустите kernel и выполните Run All. Не полагайтесь на переменные из предыдущего запуска. Секреты/API-ключи для заданий не требуются.\n\n"
    hw += f"## Подсказки без готового решения\n\n{details['hints']}\n\n"
    hw += "При ошибке сначала проверьте shape, dtype, индексы и наличие target в X. Если результат слишком хорош, проверьте split и доступность признаков в момент предсказания. Сравнение по test завершает эксперимент; для новой настройки нужен новый независимый план оценки.\n"
    (folder / "homework" / f"Homework_Week_{week:02d}.md").write_text(hw, encoding="utf-8")

    n = Notebook()
    n.m(f"""
    # Homework Week {week} — стартер

    **{plan['title']} · Tech Orda · Gizatov A. S.**

    Это **не решение**: TODO-ячеек достаточно для технического Run All, но они
    не выполняют задания. Полные требования и рубрика — в соседнем
    `Homework_Week_{week:02d}.md`. Заполните код, сохраните графики и напишите выводы.
    Не меняйте исходный CSV; используйте seed и split из задания.
    """)
    setup(n, week)
    n.c(f"""
    student_name = "TODO: имя и фамилия"
    dataset = pd.read_csv(DATA / {details['dataset']!r})
    assert "sample_id" in dataset and "target" in dataset
    assert dataset.sample_id.is_unique
    print("Локальный файл загружен:", dataset.shape)
    # Эти поля заполняются вашими содержательными результатами, а не флагами True.
    answers = {{"task_1": None, "task_2": None, "task_3": None, "task_4": None, "task_5": None}}
    """)
    for index, (title, points, task) in enumerate(details["tasks"], start=1):
        n.m(f"## Задание {index}. {title} ({points} баллов)\n\n{task}\n\n**Ваше объяснение:** TODO — постановка, результат, ограничения.")
        n.c(f"""
        # TODO {index}: реализуйте задание выше. Добавляйте code/Markdown ячейки по необходимости.
        # answers["task_{index}"] должен содержать ваши результаты/пояснения после выполнения.
        # Данные для fit/validation/test и выбор параметров организуйте по требованиям задания.
        answers["task_{index}"] = None
        """)
    n.m("""
    ## Самопроверка перед сдачей

    Таблица ниже проверяет только наличие заполненных полей. Она **не оценивает
    содержательную правильность** и не заменяет rubric. Проверьте отсутствие утечек,
    сохранённые outputs, независимый Run All и собственное объяснение каждого результата.
    """)
    n.c("""
    completion = pd.Series({key: value is not None for key, value in answers.items()}, name="field_filled")
    display(completion)
    print(f"Заполнено полей: {int(completion.sum())}/{len(completion)}. Это не автоматическая оценка домашней работы.")
    if not completion.all():
        print("TODO остаются незаполненными — продолжите самостоятельное решение.")
    """)
    n.save(week, f"Homework_Week_{week:02d}_starter.ipynb", homework=True)


if __name__ == "__main__":
    export_datasets()
    week09(); week10(); week11(); week12(); week13(); week14(); week15(); week16()
    week17_numpy(); week17_torch(); week17_keras()
    for week in range(9, 18):
        make_readme_and_homework(week)
