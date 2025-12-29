# Creating Research Structure with Pandoc (v1.3.0)

## English Version

## Goal

Organize a structure for writing research in Markdown with automatic compilation via Pandoc to DOCX for version v1.3.0, with Zotero integration for bibliography and citations.

## File Structure

### 1. Creating Folders

- `research/` - root folder for research v1.3.0 (local, not synced with GitHub)
- `research/00_setup/` - templates and configuration
- `research/01_sections/` - individual research sections

### 2. Files in `research/00_setup/`

- `reference.docx` - template with styles (if available, otherwise create basic one)
- `bibliography.bib` - bibliography file, exported from Zotero in BibTeX format
- `citation-style.csl` - citation style (e.g., APA, Chicago, IEEE, etc.)
- `README.md` - instructions for using v1.3.0 structure and Zotero integration

### 3. Files in `research/01_sections/`

Create basic .md files with headers:

- `00_Introduction.md`
- `01_Chapter1.md`
- `02_Chapter2.md`
- `03_Chapter3.md`
- `04_Chapter4.md`
- `05_Chapter5.md`
- `06_Conclusions.md`
- `07_References.md`
- `08_Appendices.md`

### 4. PowerShell Script `research/build_thesis.ps1`

- Check for Pandoc installation
- Automatic compilation of all *.md files from `01_sections/` in correct alphabetical order (thanks to prefixes 00_, 01_...)
- Generate DOCX with automatic table of contents (TOC)
- Use reference.docx for styles (if exists)
- Zotero integration:
- Use `bibliography.bib` for bibliography (if file exists, add `--bibliography=00_setup/bibliography.bib`)
- Use `citation-style.csl` for citation style (if file exists, add `--csl=00_setup/citation-style.csl`)
- Output result to `research/research_result_as_of_YYYY-MM-DD.docx` (date generated automatically)

## Technical Details

### build_thesis.ps1 Script

- UTF-8 encoding for Ukrainian character support (`[Console]::OutputEncoding = [System.Text.Encoding]::UTF8`)
- Check Pandoc installation via `Get-Command pandoc`
- Error handling with Ukrainian messages
- Support for optional reference.docx (if file exists, use `--reference-doc`)
- Automatic table of contents via `--toc`
- Automatic file sorting alphabetically (numeric prefixes 00_, 01_... ensure correct order)
- Generate output filename with current date in format `research_result_as_of_YYYY-MM-DD.docx` (e.g., `research_result_as_of_2025-11-08.docx`)
- Zotero integration:
- Check for `bibliography.bib` and add parameter `--bibliography=00_setup/bibliography.bib`
- Check for `citation-style.csl` and add parameter `--csl=00_setup/citation-style.csl`
- Automatic generation of bibliography list at end of document

### Basic .md File Structure

Each file contains:

- Level 1 header (#) with section name
- Empty template for content
- Examples of Pandoc citation usage (e.g., `[@author2024]` for citations from bibliography.bib)

### Zotero Integration

1. Export from Zotero: export bibliography in BibTeX format to file `research/00_setup/bibliography.bib`
2. Citation style: download needed .csl file from https://www.zotero.org/styles or create custom one, save as `research/00_setup/citation-style.csl`
3. Usage in Markdown: use Pandoc citation syntax, e.g., `[@smith2024]` or `[@smith2024, p. 23]`

## Dependencies

- Pandoc must be installed and available in PATH
- If Pandoc is not installed, script will output instructions with link
- Zotero (optional) for bibliography export

## Git Configuration

- Folder `research/` added to `.gitignore` for local use (not synced with GitHub)

## Versioning

All files and structure marked as v1.3.0 for tracking research version.

## Result

After executing the plan, a complete structure for writing research v1.3.0 with Zotero integration will be created, where each section is a separate .md file, and compilation to DOCX is done with one command with automatic bibliography list generation. Resulting file will be named `research_result_as_of_YYYY-MM-DD.docx` with automatically generated date. Folder `research/` remains local and is not pushed to GitHub. This is the most professional and flexible way to conduct research work in parallel with code development.

---

## Українська версія

# Створення структури для дослідження з Pandoc (v1.3.0)

## Мета

Організувати структуру для написання дослідження в Markdown з автоматичною збіркою через Pandoc у DOCX для версії v1.3.0, з інтеграцією Zotero для бібліографії та цитувань.

## Структура файлів

### 1. Створення папок

- `research/` - коренева папка для дослідження v1.3.0 (локальна, не синхронізується з GitHub)
- `research/00_setup/` - шаблони та конфігурація
- `research/01_sections/` - окремі розділи дослідження

### 2. Файли в `research/00_setup/`

- `reference.docx` - шаблон зі стилями (якщо є, інакше створити базовий)
- `bibliography.bib` - файл бібліографії, експортований з Zotero у форматі BibTeX
- `citation-style.csl` - стиль цитування (наприклад, APA, Chicago, IEEE тощо)
- `README.md` - інструкції з використання структури v1.3.0 та інтеграції з Zotero

### 3. Файли в `research/01_sections/`

Створити базові .md файли з заголовками:

- `00_Introduction.md`
- `01_Chapter1.md`
- `02_Chapter2.md`
- `03_Chapter3.md`
- `04_Chapter4.md`
- `05_Chapter5.md`
- `06_Conclusions.md`
- `07_References.md`
- `08_Appendices.md`

### 4. PowerShell скрипт `research/build_thesis.ps1`

- Перевірка наявності Pandoc
- Автоматична збірка всіх *.md файлів з `01_sections/` у правильному алфавітному порядку (завдяки префіксам 00_, 01_...)
- Генерація DOCX з автоматичним змістом (TOC)
- Використання reference.docx для стилів (якщо існує)
- Інтеграція з Zotero:
- Використання `bibliography.bib` для бібліографії (якщо файл існує, додати `--bibliography=00_setup/bibliography.bib`)
- Використання `citation-style.csl` для стилю цитування (якщо файл існує, додати `--csl=00_setup/citation-style.csl`)
- Вивід результату в `research/research_result_as_of_YYYY-MM-DD.docx` (дата генерується автоматично)

## Технічні деталі

### Скрипт build_thesis.ps1

- UTF-8 encoding для підтримки українських символів (`[Console]::OutputEncoding = [System.Text.Encoding]::UTF8`)
- Перевірка встановлення Pandoc через `Get-Command pandoc`
- Обробка помилок з повідомленнями українською
- Підтримка опційного reference.docx (якщо файл існує, використовувати `--reference-doc`)
- Автоматичний зміст через `--toc`
- Автоматичне сортування файлів за алфавітом (цифрові префікси 00_, 01_... забезпечують правильний порядок)
- Генерація назви вихідного файлу з поточною датою у форматі `research_result_as_of_YYYY-MM-DD.docx` (наприклад, `research_result_as_of_2025-11-08.docx`)
- Інтеграція Zotero:
- Перевірка наявності `bibliography.bib` та додавання параметра `--bibliography=00_setup/bibliography.bib`
- Перевірка наявності `citation-style.csl` та додавання параметра `--csl=00_setup/citation-style.csl`
- Автоматична генерація списку літератури в кінці документа

### Структура базових .md файлів

Кожен файл містить:

- Заголовок рівня 1 (#) з назвою розділу
- Порожній шаблон для наповнення
- Приклади використання цитувань у форматі Pandoc (наприклад, `[@author2024]` для цитування з bibliography.bib)

### Інтеграція з Zotero

1. Експорт з Zotero: експортувати бібліографію у форматі BibTeX у файл `research/00_setup/bibliography.bib`
2. Стиль цитування: завантажити потрібний .csl файл з https://www.zotero.org/styles або створити власний, зберегти як `research/00_setup/citation-style.csl`
3. Використання в Markdown: використовувати синтаксис Pandoc для цитувань, наприклад `[@smith2024]` або `[@smith2024, p. 23]`

## Залежності

- Pandoc повинен бути встановлений та доступний у PATH
- Якщо Pandoc не встановлений, скрипт виведе інструкції з посиланням
- Zotero (опційно) для експорту бібліографії

## Git конфігурація

- Папка `research/` додається до `.gitignore` для локального використання (не синхронізується з GitHub)

## Версійність

Всі файли та структура помічені як v1.3.0 для відстеження версії дослідження.

## Результат

Після виконання плану буде створена повна структура для написання дослідження v1.3.0 з інтеграцією Zotero, де кожен розділ - окремий .md файл, а збірка в DOCX виконується однією командою з автоматичним формуванням списку літератури. Результуючий файл буде названий `research_result_as_of_YYYY-MM-DD.docx` з автоматично згенерованою датою. Папка `research/` залишається локальною і не передається в GitHub. Це найбільш професійний і гнучкий спосіб ведення наукової роботи паралельно з розробкою коду.