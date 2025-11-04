// dt4research — Client-side logic for hybrid visualization approach

document.addEventListener('DOMContentLoaded', function() {
    // DOM elements (English label first, Ukrainian in parentheses)
    const mainGraphDiv = document.getElementById('cy-graph-main');
    const applyButton = document.getElementById('applyButton');
    const resetButton = document.getElementById('resetButton');
    const goalInput = document.getElementById('goalInput');
    const goalLabel = document.getElementById('goalLabel');
    const detailsTitle = document.getElementById('detailsTitle');
    const historyTitle = document.getElementById('historyTitle');
    const analyticsTitle = document.getElementById('analyticsTitle');
    const detailsContent = document.getElementById('detailsContent');
    const headerTitle = document.getElementById('headerTitle');
    const languageLabel = document.getElementById('languageLabel');
    const languageSelect = document.getElementById('languageSelect');
    const btnTechPlan = document.getElementById('btnTechPlan');
    const btnApiRef = document.getElementById('btnApiRef');

    const logUI = (...args) => console.log('[UI]', ...args);

    const locales = {
        en: {
            headerTitle: 'dt4research — Cybernetic Model of Digital Transformation',
            languageLabel: 'Language:',
            goalLabel: 'Strategic goal:',
            goalPlaceholder: 'Enter strategic goal (e.g., "Increase ecological efficiency")',
            detailsTitle: 'Details Panel',
            detailsPlaceholder: 'Click a graph node to see details.',
            detailsComponent: 'Component:',
            detailsResource: 'Resource:',
            tooltipValue: 'Value:',
            applyButtonIdle: 'Run Agent',
            applyButtonLoading: 'Analyzing...',
            techPlanBtn: 'Tech Plan',
            apiBtn: 'API',
            historyTitle: 'Run History',
            analyticsTitle: 'Key Indices',
            resetButton: 'Reset State',
            confirmReset: 'Are you sure you want to reset the simulation?',
            toastResetDone: 'State reset to initial',
            analyticsLabels: {
                adaptiveness: 'Adaptiveness Index (A)',
                sustainability: 'Sustainability Index (S)'
            },
            alertEmptyGoal: 'Please enter a strategic goal!',
            alertRequestError: 'Error processing request',
            alertNetworkError: 'Server communication error',
            consoleApplied: 'Agent applied mechanism, new state:',
            components: {
                'comp-strategy': 'Strategy',
                'comp-structure': 'Structure',
                'comp-processes': 'Processes',
                'comp-culture': 'Culture',
                'comp-resources': 'Resources'
        },
        statuses: {
            Active: 'Active',
            Stable: 'Stable',
            'In Progress': 'In Progress',
            Healthy: 'Healthy',
            Available: 'Available'
        },
            resources: {
                'res-comm': 'Communication Channels',
                'res-edu': 'Learning Programs',
                'res-fin': 'Capital and Investments',
                'res-info': 'Information Systems',
                'res-oper': 'Operational Processes',
                'res-org': 'Organizational Structure',
                'res-risk': 'Risk Management',
                'res-strat': 'Strategic Planning',
                'res-tech': 'Technology Solutions'
            }
        },
        uk: {
            headerTitle: 'dt4research — Кібернетична модель цифрової трансформації',
            languageLabel: 'Мова:',
            goalLabel: 'Стратегічна ціль:',
            goalPlaceholder: 'Введіть стратегічну ціль (напр., "Збільшити екологічну ефективність")',
            detailsTitle: 'Панель деталей',
            detailsPlaceholder: 'Клікніть на вузол графу, щоб побачити деталі.',
            detailsComponent: 'Компонент:',
            detailsResource: 'Ресурс:',
            tooltipValue: 'Значення:',
            applyButtonIdle: 'Запустити агента',
            applyButtonLoading: 'Аналізує...',
            techPlanBtn: 'Технічний план',
            apiBtn: 'API',
            historyTitle: 'Історія запусків',
            analyticsTitle: 'Ключові індекси',
            resetButton: 'Скинути стан',
            confirmReset: 'Ви впевнені, що хочете скинути симуляцію?',
            toastResetDone: 'Стан скинуто до початкового',
            analyticsLabels: {
                adaptiveness: 'Індекс Адаптивності (A)',
                sustainability: 'Індекс Сталості (S)'
            },
            alertEmptyGoal: 'Будь ласка, введіть стратегічну ціль!',
            alertRequestError: 'Помилка при обробці запиту',
            alertNetworkError: 'Помилка зв\'язку з сервером',
            consoleApplied: 'Агент застосував механізм, новий стан:',
            components: {
                'comp-strategy': 'Стратегія',
                'comp-structure': 'Структура',
                'comp-processes': 'Процеси',
                'comp-culture': 'Культура',
                'comp-resources': 'Ресурси'
        },
        statuses: {
            Active: 'Активна',
            Stable: 'Стабільна',
            'In Progress': 'У процесі',
            Healthy: 'Належний стан',
            Available: 'Доступні'
        },
            resources: {
                'res-comm': 'Канали комунікації',
                'res-edu': 'Програми навчання',
                'res-fin': 'Капітал та інвестиції',
                'res-info': 'Інформаційні системи',
                'res-oper': 'Операційні процеси',
                'res-org': 'Організаційна структура',
                'res-risk': 'Управління ризиками',
                'res-strat': 'Стратегічне планування',
                'res-tech': 'Технологічні рішення'
            }
        }
    };

    let currentLanguage = localStorage.getItem('dt4researchLanguage');
    if (!['en', 'uk'].includes(currentLanguage)) {
        currentLanguage = 'en';
    }
    logUI('Initialized language', currentLanguage);

    let cy_main = cytoscape({
        container: mainGraphDiv,
        style: [
            {
                selector: 'node[type="component"]',
                style: {
                    'background-color': '#4A90E2',
                    'label': 'data(name)',
                    'color': '#fff',
                    'text-valign': 'center',
                    'text-halign': 'center',
                    'shape': 'square',
                    'width': 100,
                    'height': 100,
                    'border-width': 2,
                    'border-color': '#2E5C8A'
                }
            },
            {
                selector: 'node[type="resource"]',
                style: {
                    'background-color': '#4CAF50',
                    'label': 'data(name)',
                    'color': '#333',
                    'text-valign': 'bottom',
                    'text-halign': 'center',
                    'text-margin-y': 8,
                    'font-size': 14,
                    'shape': 'ellipse',
                    'width': 'data(size)',
                    'height': 'data(size)'
                }
            },
            {
                selector: 'edge',
                style: {
                    'width': 2,
                    'line-color': '#ccc',
                    'target-arrow-color': '#999',
                    'target-arrow-shape': 'triangle',
                    'curve-style': 'bezier',
                    'opacity': 0.7
                }
            }
        ],
        layout: {
            name: 'dagre',
            nodeSep: 40,
            rankSep: 80,
            edgeSep: 20,
            rankDir: 'TB',
            animate: false
        }
    });

    let selectedNodeId = null;

    // Render agent run history (Відобразити історію запусків агента)
    async function loadAgentHistory() {
        try {
            const response = await fetch('/api/v1/agent-runs?limit=10');
            const payload = await response.json();
            const list = document.getElementById('historyList');
            if (!list) {
                return;
            }
            list.innerHTML = '';

            const formatExplanation = (exp) => {
                // Format explanation object or string (Форматування пояснення об'єкта або рядка)
                if (exp && typeof exp === 'object') {
                    const parts = [];
                    for (const [k, v] of Object.entries(exp)) {
                        parts.push(`${k}: ${v > 0 ? '+' : ''}${Number(v).toFixed(1)}`);
                    }
                    return parts.join('; ');
                }
                if (typeof exp === 'string') {
                    return exp;
                }
                return '';
            };

            const escapeHtml = (str) => {
                // Basic HTML escape (Базове екранування HTML)
                return String(str)
                    .replace(/&/g, '&amp;')
                    .replace(/</g, '&lt;')
                    .replace(/>/g, '&gt;')
                    .replace(/"/g, '&quot;')
                    .replace(/'/g, '&#039;');
            };

            (payload.items || []).forEach((item) => {
                const li = document.createElement('li');
                const ts = new Date(item.timestamp);
                const tsStr = isNaN(ts.getTime()) ? item.timestamp : ts.toLocaleString();
                li.innerHTML = `
                    <div><strong>${tsStr}</strong></div>
                    <div>${escapeHtml(item.input_goal || '')}</div>
                    <div>${escapeHtml(formatExplanation(item.applied_rules_explanation))}</div>
                `;
                list.appendChild(li);
            });
        } catch (e) {
            console.error('Failed to load agent history', e); // Log error (Журнал помилки)
        }
    }

    const getLocale = () => locales[currentLanguage];

    const translateComponent = (componentId, fallback) => {
        const locale = getLocale();
        return locale.components[componentId] || fallback || componentId;
    };

    const translateResource = (resourceId, fallback) => {
        const locale = getLocale();
        return locale.resources[resourceId] || fallback || resourceId;
    };

    const translateStatus = (status) => {
        const locale = getLocale();
        return locale.statuses[status] || status;
    };

    const getSelectedNodeData = () => {
        if (!selectedNodeId) {
            return null;
        }
        const node = cy_main.getElementById(selectedNodeId);
        if (!node || node.empty()) {
            return null;
        }
        return node.data();
    };

    function renderDetails(nodeData) {
        const locale = getLocale();
        if (!nodeData) {
            detailsContent.innerHTML = `<p id="detailsPlaceholder">${locale.detailsPlaceholder}</p>`;
            logUI('Cleared details panel');
            return;
        }

        if (nodeData.type === 'component') {
            const name = translateComponent(nodeData.componentId || nodeData.id, nodeData.name);
            detailsContent.innerHTML = `
                <div><strong>${locale.detailsComponent}</strong> ${name}</div>
                <div><strong>Status:</strong> ${translateStatus(nodeData.status)}</div>
            `;
            logUI('Rendered component details', nodeData.id, name);
        } else if (nodeData.type === 'resource') {
            const name = translateResource(nodeData.resourceId || nodeData.id, nodeData.name);
            const value = Number(nodeData.value).toFixed(1);
            const pct = Math.max(0, Math.min(100, Number(nodeData.value)));
            detailsContent.innerHTML = `
                <div><strong>${locale.detailsResource}</strong> ${name}</div>
                <div class="mini-bar"><div class="mini-bar__fill" style="width: ${pct}%"></div></div>
                <span class="mini-bar__label">${value}</span>
            `;
            logUI('Rendered resource details', nodeData.id, name, value);
        }
    }

    function updateStaticText() {
        const locale = getLocale();
        headerTitle.textContent = locale.headerTitle;
        languageLabel.textContent = locale.languageLabel;
        goalLabel.textContent = locale.goalLabel;
        goalInput.placeholder = locale.goalPlaceholder;
        detailsTitle.textContent = locale.detailsTitle;
        if (historyTitle) historyTitle.textContent = locale.historyTitle;
        if (analyticsTitle) analyticsTitle.textContent = locale.analyticsTitle;
        if (resetButton) resetButton.textContent = locale.resetButton;
        languageSelect.value = currentLanguage;
        if (btnTechPlan) btnTechPlan.textContent = locale.techPlanBtn;
        if (btnApiRef) btnApiRef.textContent = locale.apiBtn;

        const selectedData = getSelectedNodeData();
        if (!selectedData) {
            renderDetails(null);
        } else {
            renderDetails(selectedData);
        }

        if (!applyButton.disabled) {
            applyButton.textContent = locale.applyButtonIdle;
        }
        logUI('Updated static text', currentLanguage);
    }

    function applyTranslationsToGraph() {
        const locale = getLocale();
        cy_main.nodes().forEach((node) => {
            const data = node.data();
            if (data.type === 'component') {
                const translated = translateComponent(data.componentId || data.id, data.rawName || data.name);
                node.data('name', translated);
            } else if (data.type === 'resource') {
                const translated = translateResource(data.resourceId || data.id, data.rawName || data.name);
                node.data('name', translated);
            }
        });
        logUI('Applied translations to graph nodes', { language: currentLanguage });
    }

    async function updateMainGraph() {
        try {
            logUI('Fetching system state', { language: currentLanguage });
            const response = await fetch('/api/v1/system-state');
            const state = await response.json();
            logUI('Fetched system state', state);

            cy_main.elements().remove();

            state.components.forEach((component) => {
                cy_main.add({
                    data: {
                        id: component.id,
                        name: translateComponent(component.id, component.name),
                        type: 'component',
                        componentId: component.id,
                        rawName: component.name,
                        status: component.status
                    }
                });
            });

            state.resources.forEach((resource) => {
                const size = 40 + (resource.value * 0.4);
                cy_main.add({
                    data: {
                        id: resource.id,
                        name: translateResource(resource.id, resource.name),
                        type: 'resource',
                        size: size,
                        value: resource.value,
                        resourceId: resource.id,
                        resourceType: resource.type,
                        rawName: resource.name
                    }
                });

                cy_main.add({
                    data: {
                        id: `edge-${resource.id}-processes`,
                        source: resource.id,
                        target: 'comp-processes'
                    }
                });
            });

            cy_main.add({ data: { id: 'e1', source: 'comp-strategy', target: 'comp-structure' } });
            cy_main.add({ data: { id: 'e2', source: 'comp-strategy', target: 'comp-processes' } });
            cy_main.add({ data: { id: 'e3', source: 'comp-structure', target: 'comp-processes' } });
            cy_main.add({ data: { id: 'e4', source: 'comp-processes', target: 'comp-culture' } });
            cy_main.add({ data: { id: 'e5', source: 'comp-culture', target: 'comp-resources' } });

            cy_main.layout({
                name: 'dagre',
                nodeSep: 40,
                rankSep: 80,
                edgeSep: 20,
                rankDir: 'TB',
                animate: true,
                animationDuration: 300
            }).run();

            const selectedData = getSelectedNodeData();
            renderDetails(selectedData);
            applyTranslationsToGraph();
            logUI('Graph updated', { nodes: cy_main.nodes().length, edges: cy_main.edges().length });

            // Compute basic analytics indices (Обчислити базові індекси аналітики)
            const byType = {};
            (state.resources || []).forEach((r) => { byType[r.type] = Number(r.value) || 0; });
            const val = (t) => Math.max(0, Math.min(100, byType[t] ?? 0));
            const A = (val('Technological') + val('Strategic') + val('Informational')) / 3;
            const S = (val('Technological') + val('Educational') + val('Risk')) / 3;

            const analytics = document.getElementById('analyticsContent');
            if (analytics) {
                const labels = getLocale().analyticsLabels;
                analytics.innerHTML = `
                    <div><strong>${labels.adaptiveness}</strong>: ${A.toFixed(1)}
                        <div class="mini-bar"><div class="mini-bar__fill" style="width: ${A}%"></div></div>
                    </div>
                    <div style=\"margin-top:10px;\"><strong>${labels.sustainability}</strong>: ${S.toFixed(1)}
                        <div class="mini-bar"><div class="mini-bar__fill" style="width: ${S}%"></div></div>
                    </div>
                `;
            }
        } catch (error) {
            console.error('Error updating main graph:', error);
            logUI('Failed to update main graph', error);
        }
    }

    cy_main.on('tap', 'node', (evt) => {
        const nodeData = evt.target.data();
        selectedNodeId = nodeData.id;
        renderDetails(nodeData);
        logUI('Node tapped', nodeData.id, nodeData.type);
    });

    cy_main.on('mouseover', 'node', (event) => {
        const target = event.target;
        const nodeData = target.data();
        const locale = getLocale();

        const label = nodeData.type === 'resource'
            ? translateResource(nodeData.resourceId || nodeData.id, nodeData.name)
            : translateComponent(nodeData.componentId || nodeData.id, nodeData.name);

        const content = nodeData.type === 'resource'
            ? `${label}<br/>${locale.tooltipValue} ${Number(nodeData.value).toFixed(1)}`
            : label;

        const reference = target.popperRef();
        target.tippy = tippy(document.createElement('div'), {
            getReferenceClientRect: reference.getBoundingClientRect,
            content,
            allowHTML: true,
            placement: 'top',
            trigger: 'manual',
            theme: 'light-border'
        });
        target.tippy.show();
        logUI('Tooltip shown', nodeData.id);
    });

    cy_main.on('mouseout', 'node', (event) => {
        if (event.target.tippy) {
            event.target.tippy.destroy();
            event.target.tippy = null;
            logUI('Tooltip hidden', event.target.id());
        }
    });

    // Lightweight toast notification (Легке сповіщення-тост)
    function showToast(message) {
        const existing = document.getElementById('dt4r-toast');
        if (existing) existing.remove();
        const div = document.createElement('div');
        div.id = 'dt4r-toast';
        div.textContent = String(message || '');
        // Inline style for portability (Інлайн-стиль для портативності)
        div.style.position = 'fixed';
        div.style.right = '20px';
        div.style.bottom = '20px';
        div.style.maxWidth = '380px';
        div.style.padding = '12px 14px';
        div.style.background = 'rgba(50, 50, 50, 0.92)';
        div.style.color = '#fff';
        div.style.borderRadius = '8px';
        div.style.boxShadow = '0 4px 12px rgba(0,0,0,0.25)';
        div.style.zIndex = '9999';
        div.style.fontSize = '14px';
        div.style.opacity = '0';
        div.style.transition = 'opacity 200ms ease';
        document.body.appendChild(div);
        requestAnimationFrame(() => { div.style.opacity = '1'; });
        setTimeout(() => {
            div.style.opacity = '0';
            setTimeout(() => div.remove(), 250);
        }, 3500);
    }

    applyButton.addEventListener('click', async () => {
        const locale = getLocale();
        const goal = goalInput.value.trim();

        if (!goal) {
            alert(locale.alertEmptyGoal);
            logUI('Goal validation failed');
            return;
        }

        try {
            applyButton.disabled = true;
            applyButton.textContent = locale.applyButtonLoading;
            logUI('Sending apply request', goal);

            const response = await fetch('/api/v1/apply-mechanism', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ target_goal: goal })
            });

            if (response.ok) {
                const data = await response.json();
                console.log(locale.consoleApplied, data);
                logUI('Apply response received', data);
                // Immediate feedback with explanation (Негайний зворотний зв'язок із поясненням)
                if (data && data.explanation) {
                    showToast(data.explanation);
                }
                // Refresh history list right away (Оновити історію негайно)
                await loadAgentHistory();
                await updateMainGraph();
                selectedNodeId = null;
                renderDetails(null);
            } else {
                alert(locale.alertRequestError);
                logUI('Apply request failed', response.status);
            }
        } catch (error) {
            console.error('Error applying mechanism:', error);
            alert(locale.alertNetworkError);
            logUI('Apply request error', error);
        } finally {
            applyButton.disabled = false;
            applyButton.textContent = getLocale().applyButtonIdle;
            logUI('Apply request finished');
        }
    });

    languageSelect.addEventListener('change', async (event) => {
        const newLanguage = event.target.value;
        if (!['en', 'uk'].includes(newLanguage) || newLanguage === currentLanguage) {
            languageSelect.value = currentLanguage;
            return;
        }
        currentLanguage = newLanguage;
        localStorage.setItem('dt4researchLanguage', currentLanguage);
        logUI('Language changed', currentLanguage);
        updateStaticText();
        applyTranslationsToGraph();
        await updateMainGraph();
    });

    if (resetButton) {
        resetButton.addEventListener('click', async () => {
            const confirmed = confirm(getLocale().confirmReset);
            if (!confirmed) {
                return;
            }
            try {
                resetButton.disabled = true;
                const resp = await fetch('/api/v1/system-reset', { method: 'POST' });
                if (resp.ok) {
                    await updateMainGraph();
                    await loadAgentHistory();
                    selectedNodeId = null;
                    renderDetails(null);
                    showToast(getLocale().toastResetDone);
                } else {
                    alert(getLocale().alertRequestError);
                }
            } catch (e) {
                alert(getLocale().alertNetworkError);
            } finally {
                resetButton.disabled = false;
            }
        });
    }

    (async () => {
        updateStaticText();
        await updateMainGraph();
        applyTranslationsToGraph();
        logUI('Interface ready');
        await loadAgentHistory();
    })();

    // Doc links
    if (btnTechPlan) {
        btnTechPlan.addEventListener('click', () => {
            const path = currentLanguage === 'uk'
                ? '/docs/plan.uk.html'
                : '/docs/plan.en.html';
            window.open(path, '_blank');
        });
    }
    if (btnApiRef) {
        btnApiRef.addEventListener('click', () => {
            const path = currentLanguage === 'uk'
                ? '/docs/api.uk.html'
                : '/docs/api.en.html';
            window.open(path, '_blank');
        });
    }
});



