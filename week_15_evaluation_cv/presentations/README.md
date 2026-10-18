# Дополнительные презентации — Week 15

**Метрики и кросс-валидация** · 4 академических часа · 2 занятия по 90 минут.

Это дополнение к основной презентации преподавателя. Ниже задан короткий маршрут по полным оригиналам: номер страницы означает физическую страницу PDF с первой страницы, а не номер, напечатанный на слайде. В оригиналах встречаются последовательные кадры анимации.

Сначала посмотреть выбранные страницы, затем повторить вычисление или график в [практике](../practice/). Рекомендованные минуты — ориентир для чтения и объяснения; часть можно вынести в подготовку. Они входят в теоретическую часть занятия, если преподаватель использует эти материалы в классе.

| Порядок | Файл | Выбранные страницы PDF | Минуты |
|---|---|---|---:|
| 1 | [CS229: Evaluation Metrics](01_Stanford_CS229_Evaluation_Metrics.pdf) | 5–8, 13, 15, 17, 19, 21–22, 24, 26–36, 38–43 | 36 |
| 2 | [ISL Chapter 5: Resampling Methods](02_Stanford_ISL_Resampling.pdf) | 4–15, 20–32 | 28 |

## 1. CS229: Evaluation Metrics

**Stanford University** · Nandita Bhaskhar, April 22, 2022; adapted from past CS229 teams. Полный оригинал: **45 страниц**.

Confusion matrix, precision/recall/F1, изменение порога, ROC/PR, log-loss/Brier, calibration и регрессионные метрики. Одна численная таблица связывает определения и бизнес-ошибки.

**Дополнительное чтение и границы:** Страницы с одним лишь указанием внешнего изображения можно пропустить. На первом проходе calibration считать проверкой качества вероятностей, а не отдельным алгоритмом.

[Страница курса/авторов](https://cs229.stanford.edu/notes2022fall/) · [Прямой оригинал](https://cs229.stanford.edu/notes2022fall/cs229-evaluation_metrics_slides.pdf) · [Локальный PDF](01_Stanford_CS229_Evaluation_Metrics.pdf)

**Права источника:** No blanket redistribution license verified on the linked course page. Attribution and original notices retained; private instructor reference, not relicensed.

## 2. ISL Chapter 5: Resampling Methods

**ISL authors / Stanford-hosted** · Gareth James, Daniela Witten, Trevor Hastie, Robert Tibshirani; linked from ISL Python resources. Полный оригинал: **66 страниц**.

Validation, LOOCV и k-fold CV с рисунками разбиений; особенно важен пример неправильного отбора признаков до CV. Связать с Pipeline и честным outer test.

**Дополнительное чтение и границы:** 33–50: bootstrap и неопределённость. Nested CV в notebook содержит готовую структурированную реализацию, вывод формул не требуется.

[Страница курса/авторов](https://www.statlearning.com/resources-python) · [Прямой оригинал](https://web.stanford.edu/~hastie/ISLR2/Slides/Ch5_Resampling_Methods.pdf) · [Локальный PDF](02_Stanford_ISL_Resampling.pdf)

**Права источника:** All rights reserved; authors permit non-profit educational use/modification. No commercial-course reuse permission is inferred. Unaltered reference copy for instructor review.

## Связь с практикой и домашним заданием

На этой неделе используются следующие исполняемые материалы:

- [01_metrics_cv_and_overfitting](../practice/01_metrics_cv_and_overfitting.ipynb)

**Вопросы после чтения:** Почему accuracy недостаточно при дисбалансе? Когда подходит PR-AUC? Какие действия должны выполняться внутри каждого CV-fold?

Задание, критерии и starter находятся в [homework](../homework/). Выполнение готового starter проверяет среду и исходные данные; ответы и эксперименты студент дополняет самостоятельно.

## Происхождение и использование

Оригиналы скачаны с университетских страниц или страниц авторов 18 октября 2026 года; credits и содержимое не изменялись. Это частная справочная подборка преподавателя. Разрешения на коммерческое распространение не предполагаются из факта открытого скачивания или приватности репозитория; индивидуальные условия сохранены выше и в [общих уведомлениях](../../THIRD_PARTY_NOTICES.md).

[К неделе](../README.md) · [Каталог всего курса](../../RESOURCE_CATALOG.md)
