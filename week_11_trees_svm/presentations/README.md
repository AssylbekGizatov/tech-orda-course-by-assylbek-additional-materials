# Дополнительные презентации — Week 11

**Деревья решений и SVM** · 4 академических часа · 2 занятия по 90 минут.

Это дополнение к основной презентации преподавателя. Ниже задан короткий маршрут по полным оригиналам: номер страницы означает физическую страницу PDF с первой страницы, а не номер, напечатанный на слайде. В оригиналах встречаются последовательные кадры анимации.

Сначала посмотреть выбранные страницы, затем повторить вычисление или график в [практике](../practice/). Рекомендованные минуты — ориентир для чтения и объяснения; часть можно вынести в подготовку. Они входят в теоретическую часть занятия, если преподаватель использует эти материалы в классе.

| Порядок | Файл | Выбранные страницы PDF | Минуты |
|---|---|---|---:|
| 1 | [ISL Chapter 8: Tree-Based Methods](01_Stanford_ISL_Tree_Methods.pdf) | 1–16, 25–32 | 28 |
| 2 | [ISL Chapter 9: Support Vector Machines](02_Stanford_ISL_SVM.pdf) | 1–12, 17–26 | 30 |
| 3 | [CPSC470: Learning from Observations](03_Yale_CPSC470_Learning_from_Observations.pdf) | 11–17, 19–21 | 15 (доп.) |

## 1. ISL Chapter 8: Tree-Based Methods

**ISL authors / Stanford-hosted** · Gareth James, Daniela Witten, Trevor Hastie, Robert Tibshirani; linked from ISL Python resources. Полный оригинал: **81 страниц**.

Разбиение пространства, узлы и листья, регрессионные и классификационные деревья, Gini и преимущества/ограничения. Есть дерево, области признаков и численные критерии.

**Дополнительное чтение и границы:** 17–24: pruning и подбор размера дерева. Bagging и boosting далее на неделях 12–13.

[Страница курса/авторов](https://www.statlearning.com/resources-python) · [Прямой оригинал](https://web.stanford.edu/~hastie/ISLR2/Slides/Ch8_Tree_Based_Methods.pdf) · [Локальный PDF](01_Stanford_ISL_Tree_Methods.pdf)

**Права источника:** All rights reserved; authors permit non-profit educational use/modification. No commercial-course reuse permission is inferred. Unaltered reference copy for instructor review.

## 2. ISL Chapter 9: Support Vector Machines

**ISL authors / Stanford-hosted** · Gareth James, Daniela Witten, Trevor Hastie, Robert Tibshirani; linked from ISL Python resources. Полный оригинал: **34 страниц**.

Геометрия margin, опорные векторы, soft margin, kernel и нелинейная граница. Полную оптимизационную задачу читать как описание ограничений; вывод двойственной задачи не требуется.

**Дополнительное чтение и границы:** 27–34: расширенные сравнения и дополнительные иллюстрации.

[Страница курса/авторов](https://www.statlearning.com/resources-python) · [Прямой оригинал](https://web.stanford.edu/~hastie/ISLR2/Slides/Ch9_Support_Vector_Machines.pdf) · [Локальный PDF](02_Stanford_ISL_SVM.pdf)

**Права источника:** All rights reserved; authors permit non-profit educational use/modification. No commercial-course reuse permission is inferred. Unaltered reference copy for instructor review.

## 3. CPSC470: Learning from Observations

**Yale University course archive** · Brian Scassellati; Yale CPSC 470, Spring 2019. Полный оригинал: **23 страниц**.

Дополнительный разбор дерева на примере решения о посещении ресторана: таблица наблюдений, энтропия, information gain и переобучение.

**Дополнительное чтение и границы:** Это альтернативное объяснение для повторения после занятия; вводный обзор AI и организационные страницы 1–10, 22–23 пропустить.

[Страница курса/авторов](https://zoo.cs.yale.edu/classes/cs470/lectures/s2019/) · [Прямой оригинал](https://zoo.cs.yale.edu/classes/cs470/lectures/s2019/15-Learning-from-Observations.pdf) · [Локальный PDF](03_Yale_CPSC470_Learning_from_Observations.pdf)

**Права источника:** No blanket redistribution license verified on the linked course page. Attribution and original notices retained; private instructor reference, not relicensed.

## Связь с практикой и домашним заданием

На этой неделе используются следующие исполняемые материалы:

- [01_decision_trees_and_svm](../practice/01_decision_trees_and_svm.ipynb)

**Вопросы после чтения:** Как один split уменьшает impurity? Почему глубокое дерево переобучается? Как C и gamma меняют SVM?

Задание, критерии и starter находятся в [homework](../homework/). Выполнение готового starter проверяет среду и исходные данные; ответы и эксперименты студент дополняет самостоятельно.

## Происхождение и использование

Оригиналы скачаны с университетских страниц или страниц авторов 18 октября 2026 года; credits и содержимое не изменялись. Это частная справочная подборка преподавателя. Разрешения на коммерческое распространение не предполагаются из факта открытого скачивания или приватности репозитория; индивидуальные условия сохранены выше и в [общих уведомлениях](../../THIRD_PARTY_NOTICES.md).

[К неделе](../README.md) · [Каталог всего курса](../../RESOURCE_CATALOG.md)
