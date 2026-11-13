# Победитель: панель проекта

Сайт с готовностью проектов «Победитель», «Победитель Junior», «Дворовый футбол» и «Рядом» к RuStore, Google Play и App Store. Светлая и тёмная тема, фильтры задач, графики активности.

- `index.html` — сайт (чистый HTML, без сборки). Данные читает из `data/*.json`.
- `data/tasks.json` — задачи по играм и магазинам (статус Готово, Сделать, Ждёт; исполнитель Вы или Claude).
- `data/commits.json` — журнал изменений игр (из репозитория winner-app).
- `data/schedule.json` — график работ (факт и оценка).
- `data/links.json` — ссылки на тест, git и документы.
- `tools/build_commits.py` — пересобирает журнал изменений из трёх репозиториев: `python3 tools/build_commits.py <winner-app> <football-cage> <path>`.
- `.github/workflows/refresh-commits.yml` — раз в день и вручную обновляет `data/commits.json` из GitHub-репозиториев `winner-app`, `football-cage` и `path`.
- `img/` — кадры и иконки игр, `vendor/d3.min.js` — библиотека графиков.

Журнал коммитов обновляется автоматически раз в день GitHub Actions; задачи, график и ссылки можно править в JSON вручную. История коммитов этого репозитория хранит всю динамику готовности.
