# Дополнительные презентации — Week 14

**K-Means, DBSCAN, PCA и t-SNE** · 4 академических часа · 2 занятия по 90 минут.

Это дополнение к основной презентации преподавателя. Ниже задан короткий маршрут по полным оригиналам: номер страницы означает физическую страницу PDF с первой страницы, а не номер, напечатанный на слайде. В оригиналах встречаются последовательные кадры анимации.

Сначала посмотреть выбранные страницы, затем повторить вычисление или график в [практике](../practice/). Рекомендованные минуты — ориентир для чтения и объяснения; часть можно вынести в подготовку. Они входят в теоретическую часть занятия, если преподаватель использует эти материалы в классе.

| Порядок | Файл | Выбранные страницы PDF | Минуты |
|---|---|---|---:|
| 1 | [ISL Chapter 12: Unsupervised Learning](01_Stanford_ISL_Unsupervised_Learning.pdf) | 5–10, 13–24, 29–37 | 28 |
| 2 | [95-865: Manifold Learning (t-SNE)](02_CMU_95865_tSNE.pdf) | 5–10 | 14 |
| 3 | [95-865: Density-Based Clustering, TF-IDF and Topic Modeling](03_CMU_95865_DBSCAN.pdf) | 5–16 | 20 |

## 1. ISL Chapter 12: Unsupervised Learning

**ISL authors / Stanford-hosted** · Gareth James, Daniela Witten, Trevor Hastie, Robert Tibshirani; linked from ISL Python resources. Полный оригинал: **76 страниц**.

PCA как проекция на направления дисперсии, explained variance, влияние масштаба; затем цель k-means и шаги Lloyd. Много геометрических графиков, формулы связаны с визуализацией.

**Дополнительное чтение и границы:** Иерархическая кластеризация и matrix completion не обязательны; SVD выводится только на уровне формы матриц в практике.

[Страница курса/авторов](https://www.statlearning.com/resources-python) · [Прямой оригинал](https://web.stanford.edu/~hastie/ISLR2/Slides/Ch12_Unsupervised_Learning.pdf) · [Локальный PDF](01_Stanford_ISL_Unsupervised_Learning.pdf)

**Права источника:** All rights reserved; authors permit non-profit educational use/modification. No commercial-course reuse permission is inferred. Unaltered reference copy for instructor review.

## 2. 95-865: Manifold Learning (t-SNE)

**Carnegie Mellon University** · George H. Chen; original in-slide credits retained. Полный оригинал: **22 страниц**.

t-SNE: вероятности соседства в исходном и двумерном пространствах, Gaussian/Student-t, perplexity и ограничения интерпретации кластеров.

**Дополнительное чтение и границы:** 15–22: дополнительные примеры image embeddings. UMAP на 11–14 выходит за основной силлабус.

[Страница курса/авторов](https://www.andrew.cmu.edu/user/georgech/95-865/index_2026_spring_mini4.html) · [Прямой оригинал](https://www.andrew.cmu.edu/user/georgech/95-865/Lectures/UDA%20Lecture%206.pdf) · [Локальный PDF](02_CMU_95865_tSNE.pdf)

**Права источника:** No blanket redistribution license verified. Unaltered private instructor reference; original author notices retained.

## 3. 95-865: Density-Based Clustering, TF-IDF and Topic Modeling

**Carnegie Mellon University** · George H. Chen; original in-slide credits retained. Полный оригинал: **41 страниц**.

DBSCAN через ε-окрестность: min_samples, core/border/noise и последовательное расширение кластера. Несколько кадров показывают один алгоритм на точках.

**Дополнительное чтение и границы:** 18–20: чувствительность ε и HDBSCAN. Остаток лекции о текстовых данных и topic modeling не обязателен.

[Страница курса/авторов](https://www.andrew.cmu.edu/user/georgech/95-865/index_2026_spring_mini4.html) · [Прямой оригинал](https://www.andrew.cmu.edu/user/georgech/95-865/Lectures/UDA%20Lecture%209.pdf) · [Локальный PDF](03_CMU_95865_DBSCAN.pdf)

**Права источника:** No blanket redistribution license verified. Unaltered private instructor reference; original author notices retained.

## Связь с практикой и домашним заданием

На этой неделе используются следующие исполняемые материалы:

- [01_clustering_pca_tsne](../practice/01_clustering_pca_tsne.ipynb)

**Вопросы после чтения:** Почему PCA требует проверки масштаба? Что означает noise=-1 в DBSCAN? Какие расстояния нельзя уверенно читать по t-SNE-карте?

Задание, критерии и starter находятся в [homework](../homework/). Выполнение готового starter проверяет среду и исходные данные; ответы и эксперименты студент дополняет самостоятельно.

## Происхождение и использование

Оригиналы скачаны с университетских страниц или страниц авторов 18 октября 2026 года; credits и содержимое не изменялись. Это частная справочная подборка преподавателя. Разрешения на коммерческое распространение не предполагаются из факта открытого скачивания или приватности репозитория; индивидуальные условия сохранены выше и в [общих уведомлениях](../../THIRD_PARTY_NOTICES.md).

[К неделе](../README.md) · [Каталог всего курса](../../RESOURCE_CATALOG.md)
