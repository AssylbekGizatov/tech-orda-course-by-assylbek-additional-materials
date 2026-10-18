# Дополнительные презентации — Week 13

**Gradient Boosting, XGBoost и LightGBM** · 4 академических часа · 2 занятия по 90 минут.

Это дополнение к основной презентации преподавателя. Ниже задан короткий маршрут по полным оригиналам: номер страницы означает физическую страницу PDF с первой страницы, а не номер, напечатанный на слайде. В оригиналах встречаются последовательные кадры анимации.

Сначала посмотреть выбранные страницы, затем повторить вычисление или график в [практике](../practice/). Рекомендованные минуты — ориентир для чтения и объяснения; часть можно вынести в подготовку. Они входят в теоретическую часть занятия, если преподаватель использует эти материалы в классе.

| Порядок | Файл | Выбранные страницы PDF | Минуты |
|---|---|---|---:|
| 1 | [ISL Chapter 8: Tree-Based Methods](01_Stanford_ISL_Tree_Methods.pdf) | 43–55 | 30 |
| 2 | [CS229: Ensemble Methods](02_Stanford_CS229_Ensemble_Methods.pdf) | 25–35 | 25 |

## 1. ISL Chapter 8: Tree-Based Methods

**ISL authors / Stanford-hosted** · Gareth James, Daniela Witten, Trevor Hastie, Robert Tibshirani; linked from ISL Python resources. Полный оригинал: **81 страниц**.

Пошаговое обучение на остатках, shrinkage/learning rate, глубина слабого дерева и число итераций. Псевдокод сопоставить с ручным residual boosting и реальным XGBoost/LightGBM.

**Дополнительное чтение и границы:** BART на страницах 56–81 — отдельный продвинутый метод, не входит в обязательное чтение.

[Страница курса/авторов](https://www.statlearning.com/resources-python) · [Прямой оригинал](https://web.stanford.edu/~hastie/ISLR2/Slides/Ch8_Tree_Based_Methods.pdf) · [Локальный PDF](01_Stanford_ISL_Tree_Methods.pdf)

**Права источника:** All rights reserved; authors permit non-profit educational use/modification. No commercial-course reuse permission is inferred. Unaltered reference copy for instructor review.

## 2. CS229: Ensemble Methods

**Stanford University** · Nandita Bhaskhar, 2022; original slide credits preserved. Полный оригинал: **35 страниц**.

Разница AdaBoost и gradient boosting, последовательная коррекция ошибок, градиент в пространстве функций и параметры обучения.

**Дополнительное чтение и границы:** Если функциональные градиенты пока сложны, ограничиться квадратичной ошибкой: отрицательный градиент равен остатку. API библиотек брать из notebook и официальных ссылок в нём.

[Страница курса/авторов](https://cs229.stanford.edu/syllabus-spring2022.html) · [Прямой оригинал](https://cs229.stanford.edu/lectures-spring2022/cs229-boosting_slides.pdf) · [Локальный PDF](02_Stanford_CS229_Ensemble_Methods.pdf)

**Права источника:** No blanket redistribution license verified on the linked course page. Attribution and original notices retained; private instructor reference, not relicensed.

## Связь с практикой и домашним заданием

На этой неделе используются следующие исполняемые материалы:

- [01_boosting_xgboost_lightgbm_midterm](../practice/01_boosting_xgboost_lightgbm_midterm.ipynb)

**Вопросы после чтения:** Чем последовательное исправление ошибок отличается от bagging? Как learning rate связан с числом итераций? Где завершается tuning и начинается итоговая оценка?

Задание, критерии и starter находятся в [homework](../homework/). Выполнение готового starter проверяет среду и исходные данные; ответы и эксперименты студент дополняет самостоятельно.

## Происхождение и использование

Оригиналы скачаны с университетских страниц или страниц авторов 18 октября 2026 года; credits и содержимое не изменялись. Это частная справочная подборка преподавателя. Разрешения на коммерческое распространение не предполагаются из факта открытого скачивания или приватности репозитория; индивидуальные условия сохранены выше и в [общих уведомлениях](../../THIRD_PARTY_NOTICES.md).

[К неделе](../README.md) · [Каталог всего курса](../../RESOURCE_CATALOG.md)
