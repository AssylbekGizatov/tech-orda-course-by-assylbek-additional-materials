# Дополнительные презентации — Week 16

**Интерпретация моделей и введение в нейросети** · 4 академических часа · 2 занятия по 90 минут.

Это дополнение к основной презентации преподавателя. Ниже задан короткий маршрут по полным оригиналам: номер страницы означает физическую страницу PDF с первой страницы, а не номер, напечатанный на слайде. В оригиналах встречаются последовательные кадры анимации.

Сначала посмотреть выбранные страницы, затем повторить вычисление или график в [практике](../practice/). Рекомендованные минуты — ориентир для чтения и объяснения; часть можно вынести в подготовку. Они входят в теоретическую часть занятия, если преподаватель использует эти материалы в классе.

| Порядок | Файл | Выбранные страницы PDF | Минуты |
|---|---|---|---:|
| 1 | [CS224U: Introduction to Model Interpretability](01_Stanford_CS224U_Explainability_LIME_SHAP.pdf) | 16, 20, 25, 30, 33–39, 42–46, 47–58 | 32 |
| 2 | [MIT 15.773: Introduction to Neural Networks and Deep Learning](02_MIT_15773_Introduction_Neural_Networks.pdf) | 55–64, 78–85, 88–94, 97–104 | 32 |

## 1. CS224U: Introduction to Model Interpretability

**Stanford University** · Jonathan Mak, May 27, 2020. Полный оригинал: **60 страниц**.

Что объясняет модель: локальные аппроксимации LIME, Shapley/SHAP, вклад признака и пределы причинных выводов. Формула аддитивного объяснения и картинки сопоставляются с настоящими SHAP/LIME outputs.

**Дополнительное чтение и границы:** Одинаковые последовательные кадры — этапы анимации, достаточно последнего полного кадра. Обоснование всех аксиом Shapley не требуется; в notebook явно описан tree_path_dependent.

[Страница курса/авторов](https://web.stanford.edu/class/cs224u/2020/materials/cs224u-2020-model-explainability.pdf) · [Прямой оригинал](https://web.stanford.edu/class/cs224u/2020/materials/cs224u-2020-model-explainability.pdf) · [Локальный PDF](01_Stanford_CS224U_Explainability_LIME_SHAP.pdf)

**Права источника:** No blanket redistribution license verified on the linked course page. Attribution and original notices retained; private instructor reference, not relicensed.

## 2. MIT 15.773: Introduction to Neural Networks and Deep Learning

**MIT OpenCourseWare / Sloan** · Vivek Farias and Rama Ramakrishnan; MIT 15.773, Spring 2024. Полный оригинал: **110 страниц**.

Переход от логистической регрессии к слою нейронов; веса, bias, activation, hidden/output layer и пошаговый forward pass с числами. Выбрана вводная часть практического курса MIT.

**Дополнительное чтение и границы:** 1–54: широкий контекст DL, не обязательный повтор; 69–77, 95–96, 105–109: дополнительные кадры вычислений. Полный курс MIT имеет graduate-статус, выбранные здесь объяснения начальные.

[Страница курса/авторов](https://ocw.mit.edu/courses/15-773-hands-on-deep-learning-spring-2024/resources/mit15_773_s24_lec01_pdf/) · [Прямой оригинал](https://ocw.mit.edu/courses/15-773-hands-on-deep-learning-spring-2024/mit15_773_s24_lec01.pdf) · [Локальный PDF](02_MIT_15773_Introduction_Neural_Networks.pdf)

**Права источника:** MIT OCW CC BY-NC-SA 4.0, subject to separately marked third-party material; preserve attribution; commercial teaching requires applicable permission.

## Связь с практикой и домашним заданием

На этой неделе используются следующие исполняемые материалы:

- [01_shap_lime_and_neuron](../practice/01_shap_lime_and_neuron.ipynb)

**Вопросы после чтения:** Что является базовым прогнозом в SHAP? Является ли важность признака причинным эффектом? Как из входа, веса и bias получить activation?

Задание, критерии и starter находятся в [homework](../homework/). Выполнение готового starter проверяет среду и исходные данные; ответы и эксперименты студент дополняет самостоятельно.

## Происхождение и использование

Оригиналы скачаны с университетских страниц или страниц авторов 18 октября 2026 года; credits и содержимое не изменялись. Это частная справочная подборка преподавателя. Разрешения на коммерческое распространение не предполагаются из факта открытого скачивания или приватности репозитория; индивидуальные условия сохранены выше и в [общих уведомлениях](../../THIRD_PARTY_NOTICES.md).

[К неделе](../README.md) · [Каталог всего курса](../../RESOURCE_CATALOG.md)
