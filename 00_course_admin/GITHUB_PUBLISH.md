# Публикация в приватный GitHub-репозиторий

Предназначенный владелец: **AssylbekGizatov**. Название: **tech-orda-course-authored-by-gizatov-a-s**. Полное название курса в README: **Tech Orda course authored by Gizatov A. S.**

Этот документ описывает воспроизводимый способ загрузки подготовленного курса. Наличие файла или локального Git-коммита само по себе не означает, что удалённый репозиторий уже создан.

## Из локальной копии курса

Установите [Git](https://git-scm.com/downloads) и [GitHub CLI](https://cli.github.com/). Откройте терминал в корне курса и войдите в нужный аккаунт штатной командой GitHub CLI:

```bash
gh auth login --hostname github.com --git-protocol https --web
gh auth setup-git
gh api user --jq .login
```

Последняя команда должна показать `AssylbekGizatov`. Пароли и токены не записываются в notebook, `.env`, README или чат.

Задайте собственные `git user.name` и `git user.email`, если они ещё не настроены. Затем выполните проверку и публикацию:

```bash
python scripts/publish_private_repo.py
python scripts/publish_private_repo.py --publish
```

Первая команда только проверяет комплект. Вторая создаёт **новый PRIVATE** репозиторий, проверяет владельца и приватность, отправляет ветку `main`, затем сравнивает удалённый SHA с локальным и повторно проверяет `private=true`. Существующий репозиторий и другой `origin` скрипт не перезаписывает. Force-push не используется.

Если репозиторий уже создан через веб-интерфейс, не запускайте создание повторно. В его настройках проверьте **Private**, подключите именно этот URL как `origin` и отправьте `main` обычным `git push`; не применяйте `--force` для разрешения расхождений.

Оригинальные PDF хранятся полностью в соответствующих неделях. Одинаковые бинарные файлы в нескольких папках Git хранит как один объект. Рабочие виртуальные окружения, секреты и промежуточные runtime outputs исключены через `.gitignore`; готовые результаты внутри `.ipynb` сохранены.

## Первоисточники команд

- [GitHub CLI: gh repo create](https://cli.github.com/manual/gh_repo_create)
- [GitHub: создание нового репозитория](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository)

Проверены 18 октября 2026 года. Общая проверка курса и ноутбуков описана в [VALIDATION.md](VALIDATION.md).
