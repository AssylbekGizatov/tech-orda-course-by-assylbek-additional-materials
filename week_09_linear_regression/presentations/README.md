# Дополнительные презентации — Week 09

**Линейная регрессия** · 4 академических часа · 2 занятия по 90 минут.

Это дополнение к основной презентации преподавателя. Ниже задан короткий маршрут по полным оригиналам: номер страницы означает физическую страницу PDF с первой страницы, а не номер, напечатанный на слайде. В оригиналах встречаются последовательные кадры анимации.

Сначала посмотреть выбранные страницы, затем повторить вычисление или график в [практике](../practice/). Рекомендованные минуты — ориентир для чтения и объяснения; часть можно вынести в подготовку. Они входят в теоретическую часть занятия, если преподаватель использует эти материалы в классе.

| Порядок | Файл | Выбранные страницы PDF | Минуты |
|---|---|---|---:|
| 1 | [ISL Chapter 3: Linear Regression](01_Stanford_ISL_Linear_Regression.pdf) | 1–10, 19–24, 30–32 | 38 |
| 2 | [ISL Chapter 6: Linear Model Selection and Regularization](02_Stanford_ISL_Regularization.pdf) | 27–33 | 20 |

## 1. ISL Chapter 3: Linear Regression

**ISL authors / Stanford-hosted** · Gareth James, Daniela Witten, Trevor Hastie, Robert Tibshirani; linked from ISL Python resources. Полный оригинал: **64 страниц**.

Модель y = β₀ + β₁x + ε, остатки, RSS/MSE, R² и многомерная регрессия. Формулы сопровождаются геометрией прямой, остатками и реальным примером.

**Дополнительное чтение и границы:** 11–18: стандартные ошибки и доверительные интервалы; 43–62: категориальные признаки и взаимодействия. Это дополнительные темы, не обязательные вычисления этой недели.

[Страница курса/авторов](https://www.statlearning.com/resources-python) · [Прямой оригинал](https://web.stanford.edu/~hastie/ISLR2/Slides/Ch3_Linear_Regression.pdf) · [Локальный PDF](01_Stanford_ISL_Linear_Regression.pdf)

**Права источника:** All rights reserved; authors permit non-profit educational use/modification. No commercial-course reuse permission is inferred. Unaltered reference copy for instructor review.

## 2. ISL Chapter 6: Linear Model Selection and Regularization

**ISL authors / Stanford-hosted** · Gareth James, Daniela Witten, Trevor Hastie, Robert Tibshirani; linked from ISL Python resources. Полный оригинал: **59 страниц**.

Ridge: штраф на размер коэффициентов, изменение решения с λ, масштабирование и компромисс bias/variance. Связать график путей коэффициентов с собственной таблицей Ridge в notebook.

**Дополнительное чтение и границы:** 34–45: Lasso и выбор λ через CV; остальные главы о subset selection оставить для самостоятельного чтения.

[Страница курса/авторов](https://www.statlearning.com/resources-python) · [Прямой оригинал](https://web.stanford.edu/~hastie/ISLR2/Slides/Ch6_Model_Selection.pdf) · [Локальный PDF](02_Stanford_ISL_Regularization.pdf)

**Права источника:** All rights reserved; authors permit non-profit educational use/modification. No commercial-course reuse permission is inferred. Unaltered reference copy for instructor review.

## Связь с практикой и домашним заданием

На этой неделе используются следующие исполняемые материалы:

- [01_linear_regression_from_scratch](../practice/01_linear_regression_from_scratch.ipynb)

**Вопросы после чтения:** Как меняется RSS при сдвиге коэффициента? Чем λ влияет на bias/variance? Почему scaling должен обучаться только на train?

Задание, критерии и starter находятся в [homework](../homework/). Выполнение готового starter проверяет среду и исходные данные; ответы и эксперименты студент дополняет самостоятельно.

## Происхождение и использование

Оригиналы скачаны с университетских страниц или страниц авторов 18 октября 2026 года; credits и содержимое не изменялись. Это частная справочная подборка преподавателя. Разрешения на коммерческое распространение не предполагаются из факта открытого скачивания или приватности репозитория; индивидуальные условия сохранены выше и в [общих уведомлениях](../../THIRD_PARTY_NOTICES.md).

[К неделе](../README.md) · [Каталог всего курса](../../RESOURCE_CATALOG.md)
