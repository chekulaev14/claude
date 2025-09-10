# Claude Code Instructions

## MCP Servers Configuration

**Import Task Master's development workflow commands and guidelines:**
@./.taskmaster/CLAUDE.md

## Documentation Rules - ОБЯЗАТЕЛЬНО

### ВСЕГДА обновлять документацию после:
- **Изменения структуры проекта** → обновить `docs/site-structure.md`
- **Добавления/изменения компонентов** → обновить `docs/components-guide.md`
- **Изменения контента или стилей** → обновить `docs/content-rules.md`
- **Технических изменений** → обновить `docs/development-notes.md`
- **Создания/изменения страниц** → обновить `docs/pages-info.md`

### Обязательные вопросы после каждого изменения:
1. "Нужно ли обновить документацию?"
2. "Изменилась ли структура проекта?"
3. "Появились ли новые компоненты или CSS классы?"

## Project-Specific Instructions

### ВСЕГДА используй эти MCP серверы:

1. **Sequential Thinking** - анализ сложных задач (`start_thinking` → `continue_thinking` → `finalize_thinking`)
2. **Task Master** - управление задачами (`task-master list`, `TodoWrite`, обновление статусов)
3. **Playwright** - проверка верстки после каждого изменения HTML/CSS

### Обязательный workflow:
Sequential Thinking → Task Master → Реализация → Playwright → Документация → Task Master статус

## Task Master AI Instructions
