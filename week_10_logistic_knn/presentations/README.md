# Дополнительные презентации — Week 10

**Логистическая регрессия и kNN** · 4 академических часа · 2 занятия по 90 минут.

Это дополнение к основной презентации преподавателя. Ниже задан короткий маршрут по полным оригиналам: номер страницы означает физическую страницу PDF с первой страницы, а не номер, напечатанный на слайде. В оригиналах встречаются последовательные кадры анимации.

Сначала посмотреть выбранные страницы, затем повторить вычисление или график в [практике](../practice/). Рекомендованные минуты — ориентир для чтения и объяснения; часть можно вынести в подготовку. Они входят в теоретическую часть занятия, если преподаватель использует эти материалы в классе.

| Порядок | Файл | Выбранные страницы PDF | Минуты |
|---|---|---|---:|
| 1 | [ISL Chapter 4: Classification](01_Stanford_ISL_Classification.pdf) | 1–20 | 36 |
| 2 | [MIT 6.0002: Classification](02_MIT_60002_Classification_kNN.pdf) | 3–11, 19–20 | 25 |

## 1. ISL Chapter 4: Classification

**ISL authors / Stanford-hosted** · Gareth James, Daniela Witten, Trevor Hastie, Robert Tibshirani; linked from ISL Python resources. Полный оригинал: **101 страниц**.

Почему линейная регрессия не даёт корректных вероятностей класса; sigmoid, log-odds, likelihood и конкретный расчёт вероятности. На графиках видна связь признака, вероятности и ошибки.

**Дополнительное чтение и границы:** 56–59: порог и ROC, повторение на неделе 15; LDA/QDA пока не обязательны.

[Страница курса/авторов](https://www.statlearning.com/resources-python) · [Прямой оригинал](https://web.stanford.edu/~hastie/ISLR2/Slides/Ch4_Classification.pdf) · [Локальный PDF](01_Stanford_ISL_Classification.pdf)

**Права источника:** All rights reserved; authors permit non-profit educational use/modification. No commercial-course reuse permission is inferred. Unaltered reference copy for instructor review.

## 2. MIT 6.0002: Classification

**MIT OpenCourseWare** · Eric Grimson, John Guttag, Ana Bell (course team); original credits preserved. Полный оригинал: **34 страниц**.

Матрица расстояний, ближайшие соседи, выбор k и границы применимости. Иллюстрации рукописных цифр и соседей дают понятный мост к собственному kNN на NumPy.

**Дополнительное чтение и границы:** 21–24: дополнительное сравнение с логистической регрессией. Исторический синтаксис кода из лекции 2016 года сверять с современным исполняемым notebook.

[Страница курса/авторов](https://ocw.mit.edu/courses/6-0002-introduction-to-computational-thinking-and-data-science-fall-2016/resources/mit6_0002f16_lec13/) · [Прямой оригинал](https://ocw.mit.edu/courses/6-0002-introduction-to-computational-thinking-and-data-science-fall-2016/19a63b4aaa3fd9c75cd1b8e940654f53_MIT6_0002F16_lec13.pdf) · [Локальный PDF](02_MIT_60002_Classification_kNN.pdf)

**Права источника:** MIT OCW CC BY-NC-SA 4.0, subject to separate third-party notices; commercial teaching requires applicable permission.

## Связь с практикой и домашним заданием

На этой неделе используются следующие исполняемые материалы:

- [01_logistic_regression_and_knn](../practice/01_logistic_regression_and_knn.ipynb)

**Вопросы после чтения:** Чем вероятность отличается от класса? Что меняется при увеличении k? Почему выбор порога требует validation?

Задание, критерии и starter находятся в [homework](../homework/). Выполнение готового starter проверяет среду и исходные данные; ответы и эксперименты студент дополняет самостоятельно.

## Происхождение и использование

Оригиналы скачаны с университетских страниц или страниц авторов 18 октября 2026 года; credits и содержимое не изменялись. Это частная справочная подборка преподавателя. Разрешения на коммерческое распространение не предполагаются из факта открытого скачивания или приватности репозитория; индивидуальные условия сохранены выше и в [общих уведомлениях](../../THIRD_PARTY_NOTICES.md).

[К неделе](../README.md) · [Каталог всего курса](../../RESOURCE_CATALOG.md)
