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
    const btnVideos = document.getElementById('btnVideos');
    const btnSettings = document.getElementById('btnSettings');

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
            videosBtn: 'Videos',
            settingsBtn: 'Settings',
            historyTitle: 'Run History',
            analyticsTitle: 'Key Indices',
            resetButton: 'Reset State',
            confirmReset: 'Are you sure you want to reset the simulation?',
            toastResetDone: 'State reset to initial',
            analyticsLabels: {
                adaptiveness: 'Adaptiveness Index (A)',
                sustainability: 'Sustainability Index (S)'
            },
            controlPanelTitle: 'Strategic Management',
            indicesTitle: 'Key Indices',
            operationalView: '🕹️ Operational Management',
            simulationView: '🔬 Scientific Simulation',
            simulationSettingsTitle: 'Experiment Settings',
            simDaysLabel: 'Duration (days):',
            simIntensityLabel: 'Intensity:',
            simTMarketLabel: 'T_market (days):',
            simUseAgentText: 'Activate AI Agent (Experimental Group)',
            runSimulationBtn: 'Run Simulation',
            exportCsvBtn: 'Export CSV',
            metricsTitle: 'Metrics Dynamics (S, C, A)',
            summaryTitle: 'Results (Before vs After)',
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
            videosBtn: 'Відео',
            settingsBtn: 'Налаштування',
            historyTitle: 'Історія запусків',
            analyticsTitle: 'Ключові індекси',
            resetButton: 'Скинути стан',
            confirmReset: 'Ви впевнені, що хочете скинути симуляцію?',
            toastResetDone: 'Стан скинуто до початкового',
            analyticsLabels: {
                adaptiveness: 'Індекс Адаптивності (A)',
                sustainability: 'Індекс Сталості (S)'
            },
            controlPanelTitle: 'Стратегічне управління',
            indicesTitle: 'Ключові Індекси',
            operationalView: '🕹️ Операційне управління',
            simulationView: '🔬 Наукова симуляція',
            simulationSettingsTitle: 'Налаштування експерименту',
            simDaysLabel: 'Тривалість (днів):',
            simIntensityLabel: 'Інтенсивність:',
            simTMarketLabel: 'T_market (днів):',
            simUseAgentText: 'Активувати AI Агента (Експериментальна група)',
            runSimulationBtn: 'Запустити симуляцію',
            exportCsvBtn: 'Експорт CSV',
            metricsTitle: 'Динаміка показників (S, C, A)',
            summaryTitle: 'Результати (Before vs After)',
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
        if (btnVideos) btnVideos.textContent = locale.videosBtn;
        if (btnSettings) btnSettings.textContent = locale.settingsBtn;

        // Update new elements (Оновити нові елементи)
        const controlPanelTitle = document.getElementById('controlPanelTitle');
        const indicesTitleEl = document.getElementById('indicesTitle');
        if (controlPanelTitle) controlPanelTitle.textContent = locale.controlPanelTitle;
        if (indicesTitleEl) indicesTitleEl.textContent = locale.indicesTitle;

        // Update simulation form elements (Оновити елементи форми симуляції)
        const simulationSettingsTitle = document.getElementById('simulationSettingsTitle');
        const simDaysLabelText = document.getElementById('simDaysLabelText');
        const simIntensityLabelText = document.getElementById('simIntensityLabelText');
        const simTMarketLabelText = document.getElementById('simTMarketLabelText');
        const simUseAgentText = document.getElementById('simUseAgentText');
        const runSimulationBtn = document.getElementById('runSimulationBtn');
        const exportCsvBtn = document.getElementById('exportCsvBtn');
        const metricsTitle = document.getElementById('metricsTitle');
        const summaryTitle = document.getElementById('summaryTitle');
        
        if (simulationSettingsTitle) simulationSettingsTitle.textContent = locale.simulationSettingsTitle;
        if (simDaysLabelText) simDaysLabelText.textContent = locale.simDaysLabel;
        if (simIntensityLabelText) simIntensityLabelText.textContent = locale.simIntensityLabel;
        if (simTMarketLabelText) simTMarketLabelText.textContent = locale.simTMarketLabel;
        if (simUseAgentText) simUseAgentText.textContent = locale.simUseAgentText;
        if (runSimulationBtn) runSimulationBtn.textContent = locale.runSimulationBtn;
        if (exportCsvBtn) exportCsvBtn.textContent = locale.exportCsvBtn;
        if (metricsTitle) metricsTitle.textContent = locale.metricsTitle;
        if (summaryTitle) summaryTitle.textContent = locale.summaryTitle;

        // Update navigation tabs (Оновити навігаційні вкладки)
        navTabs.forEach((tab, index) => {
            if (index === 0) {
                tab.textContent = locale.operationalView;
            } else if (index === 1) {
                tab.textContent = locale.simulationView;
            }
        });

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
            
            // Update live indices after state update (Оновити live індекси після оновлення стану)
            await updateLiveIndices();

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
                await updateLiveIndices(); // Update indices after agent action (Оновити індекси після дії агента)
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

    // --- TAB SWITCHING LOGIC (Логіка перемикання вкладок) ---
    const navTabs = document.querySelectorAll('.nav-tab');
    const views = document.querySelectorAll('.view-section');

    navTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Remove active from all tabs (Зняти active з усіх вкладок)
            navTabs.forEach(t => t.classList.remove('active'));
            // Hide all views (Приховати всі view)
            views.forEach(v => v.classList.remove('active'));

            // Activate clicked tab (Активувати натиснуту вкладку)
            tab.classList.add('active');
            const targetId = tab.getAttribute('data-target');
            const targetView = document.getElementById(targetId);
            if (targetView) {
                targetView.classList.add('active');
            }

            // Specific actions for views (Специфічні дії для view)
            if (targetId === 'view-operational' && cy_main) {
                // Critical for Cytoscape: recalculate dimensions (Критично для Cytoscape: перерахувати розміри)
                setTimeout(() => {
                    cy_main.resize();
                    cy_main.fit();
                }, 50);
            }
        });
    });

    // --- UPDATE LIVE INDICES (Оновлення live індексів) ---
    async function updateLiveIndices() {
        try {
            const response = await fetch('/api/v1/simulation/metrics/current');
            if (response.ok) {
                const metrics = await response.json();
                const sIndexEl = document.getElementById('liveSIndex');
                const cIndexEl = document.getElementById('liveCIndex');
                const aIndexEl = document.getElementById('liveAIndex');
                
                if (sIndexEl && metrics.s_index !== undefined) {
                    sIndexEl.textContent = metrics.s_index.toFixed(3);
                }
                if (cIndexEl && metrics.c_index !== undefined) {
                    cIndexEl.textContent = metrics.c_index.toFixed(3);
                }
                if (aIndexEl && metrics.a_index !== undefined) {
                    aIndexEl.textContent = metrics.a_index.toFixed(3);
                }
            }
        } catch (error) {
            console.error('Failed to update live indices:', error);
            // Set fallback values (Встановити резервні значення)
            const sIndexEl = document.getElementById('liveSIndex');
            const cIndexEl = document.getElementById('liveCIndex');
            const aIndexEl = document.getElementById('liveAIndex');
            if (sIndexEl) sIndexEl.textContent = 'Calc...';
            if (cIndexEl) cIndexEl.textContent = 'Calc...';
            if (aIndexEl) aIndexEl.textContent = 'Calc...';
        }
    }

    (async () => {
        updateStaticText();
        await updateMainGraph();
        applyTranslationsToGraph();
        await updateLiveIndices(); // Update live indices on load (Оновити live індекси при завантаженні)
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
    if (btnVideos) {
        btnVideos.addEventListener('click', () => {
            const path = currentLanguage === 'uk'
                ? '/docs/videos.uk.html'
                : '/docs/videos.en.html';
            window.open(path, '_blank');
        });
    }

    // Scientific Analytics (Наукова аналітика)
    let metricsChart = null;
    const scientificAnalytics = document.getElementById('scientificAnalytics');
    // Get tabs from simulation view (Отримати вкладки з view симуляції)
    const simChartsPanel = document.querySelector('.sim-charts');
    const tabButtons = simChartsPanel ? simChartsPanel.querySelectorAll('.tab-btn') : [];
    const tabContents = simChartsPanel ? simChartsPanel.querySelectorAll('.tab-content') : [];
    const runSimulationBtn = document.getElementById('runSimulationBtn');
    const simulationStatus = document.getElementById('simulationStatus');
    const metricsChartCanvas = document.getElementById('metricsChart');

    // Tab switching (Перемикання вкладок)
    if (tabButtons.length > 0) {
        tabButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                const targetTab = btn.dataset.tab;
                tabButtons.forEach(b => b.classList.remove('active'));
                tabContents.forEach(c => c.classList.remove('active'));
                btn.classList.add('active');
                const targetContent = document.getElementById(`tab${targetTab.charAt(0).toUpperCase() + targetTab.slice(1)}`);
                if (targetContent) {
                    targetContent.classList.add('active');
                }
                if (targetTab === 'metrics') {
                    loadMetricsData();
                } else if (targetTab === 'logs') {
                    loadAgentLogs();
                }
            });
        });
    }

    // Load and display agent logs (Завантажити та відобразити логи агента)
    async function loadAgentLogs() {
        try {
            const response = await fetch('/api/v1/simulation/agent-logs');
            if (response.ok) {
                const data = await response.json();
                const logsContent = document.getElementById('agentLogsContent');
                if (logsContent) {
                    if (data.logs && data.logs.length > 0) {
                        logsContent.textContent = data.logs.join('\n');
                    } else {
                        logsContent.textContent = 'No agent logs available. Run a simulation with agent enabled to see logs.';
                    }
                }
            }
        } catch (error) {
            console.error('Failed to load agent logs:', error);
            const logsContent = document.getElementById('agentLogsContent');
            if (logsContent) {
                logsContent.textContent = 'Error loading agent logs: ' + error.message;
            }
        }
    }

    // Save logs to file (Зберегти логи у файл)
    const saveLogsBtn = document.getElementById('saveLogsBtn');
    if (saveLogsBtn) {
        saveLogsBtn.addEventListener('click', () => {
            const logsContent = document.getElementById('agentLogsContent');
            if (!logsContent) {
                return;
            }

            const logText = logsContent.textContent || logsContent.innerText;

            const trimmedText = (logText || '').trim();
            const placeholderText = 'No agent logs available. Run a simulation with agent enabled to see logs.';
            
            if (!trimmedText || trimmedText === placeholderText) {
                alert('No logs to save. Run a simulation first.');
                return;
            }

            // Create blob and download (Створити blob та завантажити)
            const blob = new Blob([logText], { type: 'text/plain;charset=utf-8' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            
            // Generate filename with timestamp (Згенерувати ім'я файлу з часовою міткою)
            const timestamp = new Date().toISOString().slice(0, 19).replace(/:/g, '-');
            a.download = `simulation_logs_${timestamp}.txt`;
            
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
            
            // Show feedback (Показати зворотний зв'язок)
            if (simulationStatus) {
                const originalText = simulationStatus.textContent;
                simulationStatus.textContent = 'Logs saved successfully';
                simulationStatus.style.color = '#4CAF50';
                setTimeout(() => {
                    simulationStatus.textContent = originalText;
                    simulationStatus.style.color = '';
                }, 2000);
            }
        });
    }

    // Run simulation (Запустити симуляцію)
    if (runSimulationBtn) {
        runSimulationBtn.addEventListener('click', async () => {
            const days = parseInt(document.getElementById('simDays')?.value || '30');
            const intensity = document.getElementById('simIntensity')?.value || 'high';
            const tMarket = parseFloat(document.getElementById('simTMarket')?.value || '30.0');
            const useAgent = document.getElementById('simUseAgent')?.checked ?? true;
            const useStreaming = true; // Always use streaming for real-time logs (Завжди використовувати потокову передачу для логів в реальному часі)

            if (simulationStatus) {
                simulationStatus.textContent = 'Running simulation...';
                simulationStatus.style.color = '#4CAF50';
            }

            // Clear logs container (Очистити контейнер логів)
            const logsContent = document.getElementById('agentLogsContent');
            if (logsContent) {
                logsContent.textContent = '';
            }

            try {
                runSimulationBtn.disabled = true;
                
                if (useStreaming) {
                    // Use streaming endpoint for real-time logs (Використати потоковий ендпоінт для логів в реальному часі)
                    await runSimulationWithStreaming(days, intensity, tMarket, useAgent);
                } else {
                    // Use regular endpoint (Використати звичайний ендпоінт)
                    const response = await fetch('/api/v1/simulation/run', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ days, intensity, t_market: tMarket, use_agent: useAgent })
                    });

                    if (response.ok) {
                        const metrics = await response.json();
                        if (simulationStatus) {
                            simulationStatus.textContent = `Simulation completed: ${metrics.length} data points (${useAgent ? 'with' : 'without'} agent)`;
                        }
                        // Load agent logs if agent was used (Завантажити логи агента, якщо агент використовувався)
                        if (useAgent) {
                            await loadAgentLogs();
                        }
                        // Switch to metrics tab and load data (Перемкнути на вкладку метрик та завантажити дані)
                        if (tabButtons.length > 1) {
                            tabButtons[1].click();
                        }
                        await loadMetricsData();
                    } else {
                        if (simulationStatus) {
                            simulationStatus.textContent = 'Simulation failed';
                            simulationStatus.style.color = '#f44336';
                        }
                    }
                }
            } catch (error) {
                console.error('Simulation error:', error);
                if (simulationStatus) {
                    simulationStatus.textContent = 'Error: ' + error.message;
                    simulationStatus.style.color = '#f44336';
                }
            } finally {
                runSimulationBtn.disabled = false;
            }
        });
    }

    // Run simulation with real-time streaming (Запустити симуляцію з потоковою передачею в реальному часі)
    async function runSimulationWithStreaming(days, intensity, tMarket, useAgent) {
        // Switch to logs tab to see real-time output (Перемкнути на вкладку логів для перегляду в реальному часі)
        if (tabButtons.length > 2) {
            tabButtons[2].click();
        }
        
        const logsContent = document.getElementById('agentLogsContent');
        if (!logsContent) {
            return;
        }

        try {
            const response = await fetch('/api/v1/simulation/run-stream', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ days, intensity, t_market: tMarket, use_agent: useAgent })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value);
                const lines = chunk.split('\n');

                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        try {
                            const data = JSON.parse(line.slice(6));
                            if (data.type === 'log') {
                                // Append log message (Додати повідомлення логу)
                                logsContent.textContent += data.message + '\n';
                                // Auto-scroll to bottom (Автоматично прокрутити вниз)
                                logsContent.scrollTop = logsContent.scrollHeight;
                            } else if (data.type === 'complete') {
                                // Simulation completed (Симуляція завершена)
                                if (simulationStatus) {
                                    simulationStatus.textContent = `Simulation completed: ${data.metrics_count} data points (${useAgent ? 'with' : 'without'} agent)`;
                                }
                                // Load metrics data (Завантажити дані метрик)
                                await loadMetricsData();
                                // Optionally switch to metrics tab (Опціонально перемкнути на вкладку метрик)
                                // if (tabButtons.length > 1) {
                                //     tabButtons[1].click();
                                // }
                            }
                        } catch (e) {
                            console.error('Error parsing SSE data:', e);
                        }
                    }
                }
            }
        } catch (error) {
            console.error('Streaming error:', error);
            if (logsContent) {
                logsContent.textContent += '\n\nError: ' + error.message;
            }
            if (simulationStatus) {
                simulationStatus.textContent = 'Error: ' + error.message;
                simulationStatus.style.color = '#f44336';
            }
        }
    }

    // Export CSV (Експортувати CSV)
    const exportCsvBtn = document.getElementById('exportCsvBtn');
    if (exportCsvBtn) {
        exportCsvBtn.addEventListener('click', async () => {
            try {
                const response = await fetch('/api/v1/simulation/export/csv');
                if (response.ok) {
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `simulation_results_${new Date().toISOString().slice(0, 10)}.csv`;
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                    window.URL.revokeObjectURL(url);
                    if (simulationStatus) {
                        simulationStatus.textContent = 'CSV exported successfully';
                        simulationStatus.style.color = '#4CAF50';
                    }
                } else {
                    if (simulationStatus) {
                        simulationStatus.textContent = 'Export failed';
                        simulationStatus.style.color = '#f44336';
                    }
                }
            } catch (error) {
                console.error('Export error:', error);
                if (simulationStatus) {
                    simulationStatus.textContent = 'Export error: ' + error.message;
                    simulationStatus.style.color = '#f44336';
                }
            }
        });
    }

    // Load and display metrics (Завантажити та відобразити метрики)
    async function loadMetricsData() {
        try {
            const [historyResponse, summaryResponse] = await Promise.all([
                fetch('/api/v1/simulation/metrics/history'),
                fetch('/api/v1/simulation/summary')
            ]);

            if (historyResponse.ok && summaryResponse.ok) {
                const metrics = await historyResponse.json();
                const summary = await summaryResponse.json();

                // Render chart (Відобразити графік)
                renderMetricsChart(metrics);

                // Render summary table (Відобразити таблицю зведення)
                renderSummaryTable(summary);
            }
        } catch (error) {
            console.error('Failed to load metrics:', error);
        }
    }

    // Render metrics chart (Відобразити графік метрик)
    function renderMetricsChart(metrics) {
        if (!metricsChartCanvas || !metrics || metrics.length === 0) {
            return;
        }

        const ctx = metricsChartCanvas.getContext('2d');
        const labels = metrics.map((m, i) => `Day ${i + 1}`);
        const sData = metrics.map(m => m.s_index);
        const cData = metrics.map(m => m.c_index);
        const aData = metrics.map(m => m.a_index);

        // Destroy existing chart if exists (Знищити існуючий графік, якщо він є)
        if (metricsChart) {
            metricsChart.destroy();
        }

        metricsChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'S Index (Sustainability)',
                        data: sData,
                        borderColor: 'rgb(75, 192, 192)',
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        tension: 0.1
                    },
                    {
                        label: 'C Index (Control)',
                        data: cData,
                        borderColor: 'rgb(255, 99, 132)',
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        tension: 0.1
                    },
                    {
                        label: 'A Index (Adaptability)',
                        data: aData,
                        borderColor: 'rgb(54, 162, 235)',
                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                        tension: 0.1
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 1.0
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    title: {
                        display: true,
                        text: 'Scientific Metrics Over Time'
                    }
                }
            }
        });
    }

    // Render summary table (Відобразити таблицю зведення)
    function renderSummaryTable(summary) {
        const tableBody = document.querySelector('#summaryTableContent tbody');
        if (!tableBody || !summary) {
            return;
        }

        tableBody.innerHTML = '';

        const metrics = [
            { key: 's_index', label: 'S Index (Sustainability)' },
            { key: 'c_index', label: 'C Index (Control)' },
            { key: 'a_index', label: 'A Index (Adaptability)' }
        ];

        metrics.forEach(metric => {
            const row = document.createElement('tr');
            const before = summary.before?.[metric.key] || 0;
            const after = summary.after?.[metric.key] || 0;
            const change = summary.improvements?.[metric.key] || 0;
            const changeClass = change >= 0 ? 'positive' : 'negative';

            row.innerHTML = `
                <td>${metric.label}</td>
                <td>${before.toFixed(3)}</td>
                <td>${after.toFixed(3)}</td>
                <td class="${changeClass}">${change >= 0 ? '+' : ''}${change.toFixed(3)}</td>
            `;
            tableBody.appendChild(row);
        });
    }
});



