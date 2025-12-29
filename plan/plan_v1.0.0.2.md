# Project Plan — Version 1.0.0.2

## English Version

Release goal: improve readability and professionalism of the dashboard (UI/UX), make the backend reliable, testable, and prepare the system for state persistence.

## Stage 1: Immediate Visual Quality (Fixing the UI/UX)
Goal: Make the dashboard readable, interactive, and professional.

Corresponds to previous items: Visualization (1) and UI Panel (2).

### 1.1 Layout
- Switch from `breadthfirst` to `cytoscape-dagre` for clean top-down hierarchy with minimal crossings.
- Configure parameters: rankDir=TB, nodeSep, rankSep, edgeSep.

Include scripts in `app/templates/index.html` (in <head>):

```html
<script src="https://cdn.jsdelivr.net/npm/cytoscape@3.26.0/dist/cytoscape.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/dagre@0.8.5/dist/dagre.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/cytoscape-dagre@2.5.0/cytoscape-dagre.js"></script>
```

Replace layout in `app/static/app.js`:

```javascript
cy_main.layout({
  name: 'dagre',
  nodeSep: 40,
  rankSep: 80,
  edgeSep: 20,
  rankDir: 'TB', // top -> bottom
  animate: true,
  animationDuration: 300
}).run();
```

### 1.2 Interactivity (Tooltips)
- Add `cytoscape-popper` + `tippy.js` for tooltips.
- Short label in node (resource type), full name + current value in tooltip on hover.

Scripts in `index.html`:

```html
<script src="https://unpkg.com/@popperjs/core@2"></script>
<script src="https://unpkg.com/cytoscape-popper@2.0.0/cytoscape-popper.js"></script>
<link rel="stylesheet" href="https://unpkg.com/tippy.js@6/dist/tippy.css" />
<script src="https://unpkg.com/tippy.js@6"></script>
```

In `app.js` on initialization:

```javascript
cy_main.on('mouseover', 'node', (e) => {
  const d = e.target.data();
  const content = d.type === 'resource' ? `${d.name}<br/>Value: ${Number(d.value).toFixed(1)}` : d.name;
  const ref = e.target.popperRef();
  e.target.tippy = tippy(document.createElement('div'), {
    getReferenceClientRect: ref.getBoundingClientRect,
    content: content,
    allowHTML: true,
    placement: 'top',
    trigger: 'manual'
  });
  e.target.tippy.show();
});
cy_main.on('mouseout', 'node', (e) => e.target.tippy?.destroy());
```

### 1.3 Details Panel
- Shows: name, value, and mini-bar 0–100.
- Mini-bar implemented as simple div progress (CSS):

```html
<div class="mini-bar">
  <div class="mini-bar__fill" style="width: 65%"></div>
  <div class="mini-bar__ticks"></div>
  <span class="mini-bar__label">65</span>
  </div>
```

CSS in `style.css`:

```css
.mini-bar{position:relative;height:10px;background:#eee;border-radius:6px}
.mini-bar__fill{height:100%;background:#4CAF50;border-radius:6px}
.mini-bar__label{display:block;margin-top:6px;color:#444;font-size:12px}
```

### 1.4 Fonts
- Add Cyrillic Roboto or Inter:

```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap&subset=cyrillic" rel="stylesheet">
```

Update `body { font-family: 'Inter', 'Segoe UI', Roboto, Arial, sans-serif; }`.

### Stage 1 Success Criteria
- Hierarchical graph without chaos and crossings.
- Tooltips with full name and current value.
- Details panel with mini-bar 0–100.
- Unified web fonts with good Cyrillic support.

---

## Execution Roadmap (Stage 1)
1. Connect `cytoscape-dagre`, `popper`, `tippy`. Switch layout in `app.js`.
2. Add tooltips and mini-bar in details panel. Connect web font.

See further stages in files: `plan_v1.0.0.3.md` (Robust Backend) and `plan_v1.0.0.4.md` (Persistence).

## Notes
- Follow rules for running via scripts (`start_server.ps1` / `start_server.bat`) and UTF‑8 in PowerShell.
- Code comments — in English; responses and documentation — in Ukrainian.

---

## Українська версія

# План проєкту — версія 1.0.0.2

Мета релізу: підняти читабельність і професійність дашборду (UI/UX), зробити бекенд надійним, тестованим і підготувати систему до персистентності стану.

## Етап 1: Негайна Візуальна Якість (Fixing the UI/UX)
Мета: Зробити дашборд читабельним, інтерактивним та професійним.

Відповідає попереднім пунктам: Візуалізація (1) та Панель UI (2).

### 1.1 Layout (Макет)
- Перехід з `breadthfirst` на `cytoscape-dagre` для чистої ієрархії «згори-вниз» з мінімумом перетинів.
- Налаштування параметрів: rankDir=TB, nodeSep, rankSep, edgeSep.

Включення скриптів у `app/templates/index.html` (у <head>):

```html
<script src="https://cdn.jsdelivr.net/npm/cytoscape@3.26.0/dist/cytoscape.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/dagre@0.8.5/dist/dagre.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/cytoscape-dagre@2.5.0/cytoscape-dagre.js"></script>
```

Заміна layout у `app/static/app.js`:

```javascript
cy_main.layout({
  name: 'dagre',
  nodeSep: 40,
  rankSep: 80,
  edgeSep: 20,
  rankDir: 'TB', // top -> bottom
  animate: true,
  animationDuration: 300
}).run();
```

### 1.2 Інтерактивність (Підказки)
- Додаємо `cytoscape-popper` + `tippy.js` для тултіпів.
- Короткий лейбл у вузлі (тип ресурсу), повна назва + поточне значення у підказці при hover.

Скрипти у `index.html`:

```html
<script src="https://unpkg.com/@popperjs/core@2"></script>
<script src="https://unpkg.com/cytoscape-popper@2.0.0/cytoscape-popper.js"></script>
<link rel="stylesheet" href="https://unpkg.com/tippy.js@6/dist/tippy.css" />
<script src="https://unpkg.com/tippy.js@6"></script>
```

В `app.js` при ініціалізації:

```javascript
cy_main.on('mouseover', 'node', (e) => {
  const d = e.target.data();
  const content = d.type === 'resource' ? `${d.name}<br/>Value: ${Number(d.value).toFixed(1)}` : d.name;
  const ref = e.target.popperRef();
  e.target.tippy = tippy(document.createElement('div'), {
    getReferenceClientRect: ref.getBoundingClientRect,
    content: content,
    allowHTML: true,
    placement: 'top',
    trigger: 'manual'
  });
  e.target.tippy.show();
});
cy_main.on('mouseout', 'node', (e) => e.target.tippy?.destroy());
```

### 1.3 Панель деталей
- Показує: назву, значення та міні-бар 0–100.
- Міні-бар реалізується простим div-прогресом (CSS):

```html
<div class="mini-bar">
  <div class="mini-bar__fill" style="width: 65%"></div>
  <div class="mini-bar__ticks"></div>
  <span class="mini-bar__label">65</span>
  </div>
```

CSS у `style.css`:

```css
.mini-bar{position:relative;height:10px;background:#eee;border-radius:6px}
.mini-bar__fill{height:100%;background:#4CAF50;border-radius:6px}
.mini-bar__label{display:block;margin-top:6px;color:#444;font-size:12px}
```

### 1.4 Шрифти
- Додаємо кириличний Roboto або Inter:

```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap&subset=cyrillic" rel="stylesheet">
```

Оновити `body { font-family: 'Inter', 'Segoe UI', Roboto, Arial, sans-serif; }`.

### Критерії успіху Етапу 1
- Ієрархічний граф без хаосу та перетинів.
- Підказки з повною назвою і поточним значенням.
- Детальна панель з міні-баром 0–100.
- Єдині веб-шрифти з гарною кирилицею.

---

## Дорожня карта виконання (Етап 1)
1. Підключити `cytoscape-dagre`, `popper`, `tippy`. Перемкнути layout у `app.js`.
2. Додати тултіпи й міні-бар у панелі деталей. Підключити веб-шрифт.

Див. подальші етапи у файлах: `plan_v1.0.0.3.md` (Robust Backend) та `plan_v1.0.0.4.md` (Persistence).

## Примітки
- Дотримуватись правил запуску через скрипти (`start_server.ps1` / `start_server.bat`) і UTF‑8 у PowerShell.
- Коментарі в коді — англійською; відповіді та документація — українською.


