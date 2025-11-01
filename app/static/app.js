// dt4research — Client-side logic for hybrid visualization approach

document.addEventListener('DOMContentLoaded', function() {
    // DOM elements (English label first, Ukrainian in parentheses)
    const mainGraphDiv = document.getElementById('cy-graph-main');
    const applyButton = document.getElementById('applyButton');
    const goalInput = document.getElementById('goalInput');
    const goalLabel = document.getElementById('goalLabel');
    const detailsTitle = document.getElementById('detailsTitle');
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
                const newState = await response.json();
                console.log(locale.consoleApplied, newState);
                logUI('Apply response received', newState);
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

    (async () => {
        updateStaticText();
        await updateMainGraph();
        applyTranslationsToGraph();
        logUI('Interface ready');
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



