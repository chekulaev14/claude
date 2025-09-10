# Claude Code Instructions

## MCP Servers Configuration


### Playwright - Browser Automation
Use Playwright MCP for browser testing and web scraping:
- **Navigate first**: Always use `mcp__playwright__browser_navigate` before other commands
- **Take snapshots**: Use `mcp__playwright__browser_snapshot` to understand page structure
- **Interact carefully**: Get element references from snapshots before clicking/typing
- Common commands:
  - `browser_navigate` - Open URLs
  - `browser_snapshot` - Get page structure
  - `browser_click` - Click elements
  - `browser_type` - Enter text
  - `browser_take_screenshot` - Capture visuals

### Task Master AI - Project Management
**Import Task Master's development workflow commands and guidelines, treat as if import is in the main CLAUDE.md file.**
@./.taskmaster/CLAUDE.md

### Sequential Thinking - Enhanced Problem Solving
Use Sequential Thinking MCP for complex tasks requiring structured reasoning:
- **Always use for complex problems**: Before starting any non-trivial task
- **Break down complex tasks**: Split large problems into logical steps
- **Document reasoning**: Keep track of decision-making process
- Available commands:
  - `mcp__sequential_thinking__start_thinking` - Begin structured analysis
  - `mcp__sequential_thinking__continue_thinking` - Add reasoning steps
  - `mcp__sequential_thinking__finalize_thinking` - Complete analysis and get solution
- **Best practices**:
  1. Start thinking session at beginning of complex tasks
  2. Use multiple thinking steps to explore options
  3. Always finalize before implementing solutions
  4. Document key insights from thinking process

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

### When working on this project:
1. **ALWAYS use Sequential Thinking** - для каждой сложной задачи начинай с `start_thinking`, анализируй проблему пошагово через `continue_thinking`, завершай через `finalize_thinking`
2. **ALWAYS use Task Master** - постоянно отслеживай задачи через `task-master list`, обновляй статусы, используй TodoWrite
3. **ALWAYS use Playwright** - постоянно проверяй через браузер, что верстка не разъехалась и изменения применились корректно после каждого изменения HTML/CSS
4. **ALWAYS update Documentation** - после любых значимых изменений обновляй соответствующие файлы в `/docs/`
5. **Enhanced Workflow**: Sequential Thinking для анализа → Task Master для планирования → Реализация → Playwright для проверки → Обновление документации → Task Master для обновления статуса

## Task Master AI Instructions
