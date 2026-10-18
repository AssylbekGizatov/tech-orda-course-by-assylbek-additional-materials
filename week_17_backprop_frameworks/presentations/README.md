# Дополнительные презентации — Week 17

**Backpropagation, Keras/TensorFlow и PyTorch** · 4 академических часа · 2 занятия по 90 минут.

Это дополнение к основной презентации преподавателя. Ниже задан короткий маршрут по полным оригиналам: номер страницы означает физическую страницу PDF с первой страницы, а не номер, напечатанный на слайде. В оригиналах встречаются последовательные кадры анимации.

Сначала посмотреть выбранные страницы, затем повторить вычисление или график в [практике](../practice/). Рекомендованные минуты — ориентир для чтения и объяснения; часть можно вынести в подготовку. Они входят в теоретическую часть занятия, если преподаватель использует эти материалы в классе.

| Порядок | Файл | Выбранные страницы PDF | Минуты |
|---|---|---|---:|
| 1 | [CS231n: Neural Networks and Backpropagation](01_Stanford_CS231n_Backpropagation.pdf) | 22–34, 49–52, 57–78, 95–109 | 34 |
| 2 | [MIT 15.773: Training Deep Neural Networks](02_MIT_15773_Training_Neural_Networks.pdf) | 34, 40, 43–49, 57, 64, 67, 69, 73–75, 77, 85 | 16 |
| 3 | [MIT 15.773: Lightning Introduction to Keras/TF](03_MIT_15773_Keras_TensorFlow.pdf) | 3–20, 27–40 | 20 |

## 1. CS231n: Neural Networks and Backpropagation

**Stanford University** · Ehsan Adeli; see original acknowledgements, 2025. Полный оригинал: **147 страниц**.

Вычислительный граф, простой численный пример chain rule, upstream/local/downstream gradient и паттерны потока градиента. На занятии: 23, 30–34, 52, 59, 69–72, 78, 98–104; остальные кадры раскрывают шаги.

**Дополнительное чтение и границы:** 111–145: autograd, векторные/матричные производные для углубления. 12–20 и 53–55 о сложных моделях не нужны новичку.

[Страница курса/авторов](https://cs231n.stanford.edu/2025/schedule.html) · [Прямой оригинал](https://cs231n.stanford.edu/slides/2025/lecture_4.pdf) · [Локальный PDF](01_Stanford_CS231n_Backpropagation.pdf)

**Права источника:** No blanket redistribution license verified on the linked course page. Attribution and original notices retained; private instructor reference, not relicensed.

## 2. MIT 15.773: Training Deep Neural Networks

**MIT OpenCourseWare / Sloan** · Vivek Farias and Rama Ramakrishnan; MIT 15.773, Spring 2024. Полный оригинал: **95 страниц**.

Визуальная опора для MSE/binary cross-entropy, learning rate и gradient descent. Повторяющиеся кадры можно перелистывать; каждую формулу связать с одной строкой NumPy.

**Дополнительное чтение и границы:** 29–85 целиком — подробное объяснение для самостоятельного повторения. Code snippets исторического PDF не заменяют проверенную практику.

[Страница курса/авторов](https://ocw.mit.edu/courses/15-773-hands-on-deep-learning-spring-2024/resources/mit15_773_s24_lec02_pdf/) · [Прямой оригинал](https://ocw.mit.edu/courses/15-773-hands-on-deep-learning-spring-2024/mit15_773_s24_lec02.pdf) · [Локальный PDF](02_MIT_15773_Training_Neural_Networks.pdf)

**Права источника:** MIT OCW CC BY-NC-SA 4.0, subject to separately marked third-party material; preserve attribution; commercial teaching requires applicable permission.

## 3. MIT 15.773: Lightning Introduction to Keras/TF

**MIT OpenCourseWare / Sloan** · Vivek Farias and Rama Ramakrishnan; MIT 15.773, Spring 2024. Полный оригинал: **44 страниц**.

Batch/epoch, validation, overfitting, early stopping и Keras/TF API. В практике запускаются обе настоящие библиотеки: TensorFlow/Keras и PyTorch.

**Дополнительное чтение и границы:** Подробное сравнение DL learning curves продолжается на неделе 18. Keras shapes и современные API брать из исполняемого notebook.

[Страница курса/авторов](https://ocw.mit.edu/courses/15-773-hands-on-deep-learning-spring-2024/resources/mit15_773_s24_lec03a_pdf/) · [Прямой оригинал](https://ocw.mit.edu/courses/15-773-hands-on-deep-learning-spring-2024/mit15_773_s24_lec03a.pdf) · [Локальный PDF](03_MIT_15773_Keras_TensorFlow.pdf)

**Права источника:** MIT OCW CC BY-NC-SA 4.0, subject to separately marked third-party material; preserve attribution; commercial teaching requires applicable permission.

## Связь с практикой и домашним заданием

На этой неделе используются следующие исполняемые материалы:

- [01_backpropagation_numpy](../practice/01_backpropagation_numpy.ipynb)
- [02_pytorch_digits_training](../practice/02_pytorch_digits_training.ipynb)
- [03_tensorflow_keras_digits_training](../practice/03_tensorflow_keras_digits_training.ipynb)

**Вопросы после чтения:** Как произведение локальных производных даёт градиент? Для чего zero_grad/backward/step? Чем validation loss отличается от training loss?

Задание, критерии и starter находятся в [homework](../homework/). Выполнение готового starter проверяет среду и исходные данные; ответы и эксперименты студент дополняет самостоятельно.

## Происхождение и использование

Оригиналы скачаны с университетских страниц или страниц авторов 18 октября 2026 года; credits и содержимое не изменялись. Это частная справочная подборка преподавателя. Разрешения на коммерческое распространение не предполагаются из факта открытого скачивания или приватности репозитория; индивидуальные условия сохранены выше и в [общих уведомлениях](../../THIRD_PARTY_NOTICES.md).

[К неделе](../README.md) · [Каталог всего курса](../../RESOURCE_CATALOG.md)
