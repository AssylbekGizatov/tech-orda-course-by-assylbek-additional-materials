# Публикация в приватный GitHub-репозиторий

Предназначенный владелец: **AssylbekGizatov**. Название: **tech-orda-course-authored-by-gizatov-a-s**. Полное название курса в README: **Tech Orda course authored by Gizatov A. S.**

## Действующий репозиторий

Курс загружен 18 октября 2026 года: [AssylbekGizatov/tech-orda-course-authored-by-gizatov-a-s](https://github.com/AssylbekGizatov/tech-orda-course-authored-by-gizatov-a-s).

При заключительной проверке подтверждены статус **Private**, ветка **main**, все **351 файл** и **26 папок недель**. Контрольные суммы всех удалённых Git-объектов файлов совпали с локальным комплектом. Первоначальная загрузка: [коммит 42b5361](https://github.com/AssylbekGizatov/tech-orda-course-by-assylbek-additional-materials/commit/42b53612fca29b8f0da24315a4909d2ddacc5934).

Для получения рабочей копии после входа в GitHub:

```bash
gh repo clone AssylbekGizatov/tech-orda-course-authored-by-gizatov-a-s
cd tech-orda-course-authored-by-gizatov-a-s
```

Для последующих обновлений используйте обычные Git-коммиты и `git push origin main`. Скрипт первоначальной публикации повторно запускать не требуется: он намеренно отказывается создавать уже существующий репозиторий.

## Первоначальная загрузка — уже выполнена

Ниже сохранена воспроизводимая процедура первоначального создания репозитория.

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

Перед последующими отправками проверьте правильность `origin` и сохранение статуса **Private**. Не применяйте `--force` для разрешения расхождений.

Оригинальные PDF хранятся полностью в соответствующих неделях. Одинаковые бинарные файлы в нескольких папках Git хранит как один объект. Рабочие виртуальные окружения, секреты и промежуточные runtime outputs исключены через `.gitignore`; готовые результаты внутри `.ipynb` сохранены.

## Первоисточники команд

- [GitHub CLI: gh repo create](https://cli.github.com/manual/gh_repo_create)
- [GitHub: создание нового репозитория](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository)

Проверены 18 октября 2026 года. Общая проверка курса и ноутбуков описана в [VALIDATION.md](VALIDATION.md).
