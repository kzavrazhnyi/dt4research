// dt4research — Client-side logic for hybrid visualization approach

document.addEventListener('DOMContentLoaded', function() {
    
    // DOM elements
    const mainGraphDiv = document.getElementById('cy-graph-main');
    const controlsDiv = document.querySelector('.controls');
    const applyButton = document.getElementById('applyButton');
    const goalInput = document.getElementById('goalInput');
    const detailsContent = document.getElementById('detailsContent');
    
    // Cytoscape instances
    let cy_main = null;
    let selectedNodeData = null;
    
    // Initialize main graph
    cy_main = cytoscape({
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
    
    // Helper: render details panel
    function renderDetails(data) {
        if (!data) {
            detailsContent.innerHTML = '<p>Клікніть на вузол графу, щоб побачити деталі.</p>';
            return;
        }
        if (data.type === 'component') {
            detailsContent.innerHTML = `
                <div><strong>Компонент:</strong> ${data.name}</div>
            `;
        } else if (data.type === 'resource') {
            const v = Number(data.value).toFixed(1);
            const pct = Math.max(0, Math.min(100, Number(data.value)));
            detailsContent.innerHTML = `
                <div><strong>Ресурс:</strong> ${data.name}</div>
                <div class="mini-bar"><div class="mini-bar__fill" style="width: ${pct}%"></div></div>
                <span class="mini-bar__label">${v}</span>
            `;
        }
    }
    
    // Update main graph with current system state
    async function updateMainGraph() {
        try {
            const response = await fetch('/api/v1/system-state');
            const state = await response.json();
            
            // Clear existing elements
            cy_main.elements().remove();
            
            // Add components (including "Ресурси" as a regular node in flat graph)
            state.components.forEach(c => {
                cy_main.add({
                    data: {
                        id: c.id,
                        name: c.name,
                        type: 'component'
                    }
                });
            });
            
            // Add resources as separate nodes (flat graph approach)
            state.resources.forEach(r => {
                const size = 40 + (r.value * 0.4); // Size based on value
                const label = r.type; // Enum serialized as string on backend

                cy_main.add({
                    data: {
                        id: r.id,
                        name: label,
                        label: label,
                        type: 'resource',
                        size: size,
                        value: r.value
                    }
                });
                
                // Connect each resource to "Процеси" (Processes)
                cy_main.add({
                    data: {
                        id: `edge-${r.id}-processes`,
                        source: r.id,
                        target: 'comp-processes'
                    }
                });
            });
            
            // Add high-level component connections (model structure)
            cy_main.add({ data: { id: 'e1', source: 'comp-strategy', target: 'comp-structure' } });
            cy_main.add({ data: { id: 'e2', source: 'comp-strategy', target: 'comp-processes' } });
            cy_main.add({ data: { id: 'e3', source: 'comp-structure', target: 'comp-processes' } });
            cy_main.add({ data: { id: 'e4', source: 'comp-processes', target: 'comp-culture' } });
            cy_main.add({ data: { id: 'e5', source: 'comp-culture', target: 'comp-resources' } });
            
            // Apply layout
            cy_main.layout({
                name: 'dagre',
                nodeSep: 40,
                rankSep: 80,
                edgeSep: 20,
                rankDir: 'TB',
                animate: true,
                animationDuration: 300
            }).run();
            
            // No separate detail graph; details shown in sidebar
            
        } catch (error) {
            console.error('Error updating main graph:', error);
        }
    }
    
    // Event handlers

    // Click on any node to show details in the sidebar
    cy_main.on('tap', 'node', function(evt) {
        const data = evt.target.data();
        selectedNodeData = data;
        renderDetails(data);
    });

    // Tooltips on hover using popper + tippy
    cy_main.on('mouseover', 'node', function(e) {
        const target = e.target;
        const d = target.data();
        const content = d.type === 'resource'
            ? `${d.name}<br/>Значення: ${Number(d.value).toFixed(1)}`
            : d.name;

        const ref = target.popperRef();
        target.tippy = tippy(document.createElement('div'), {
            getReferenceClientRect: ref.getBoundingClientRect,
            content: content,
            allowHTML: true,
            placement: 'top',
            trigger: 'manual',
            theme: 'light-border'
        });
        target.tippy.show();
    });

    cy_main.on('mouseout', 'node', function(e) {
        if (e.target.tippy) {
            e.target.tippy.destroy();
            e.target.tippy = null;
        }
    });
    
    // Apply button
    applyButton.addEventListener('click', async function() {
        const goal = goalInput.value.trim();
        
        if (!goal) {
            alert('Будь ласка, введіть стратегічну ціль!');
            return;
        }
        
        try {
            // Disable button during request
            applyButton.disabled = true;
            applyButton.textContent = 'Аналізує...';
            
            const response = await fetch('/api/v1/apply-mechanism', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ target_goal: goal })
            });
            
            if (response.ok) {
                const newState = await response.json();
                console.log('Agent applied mechanism, new state:', newState);
                
                // Update visualizations
                await updateMainGraph();
                // Clear details to avoid stale data; user can click again
                selectedNodeData = null;
                renderDetails(null);
            } else {
                alert('Помилка при обробці запиту');
            }
            
        } catch (error) {
            console.error('Error applying mechanism:', error);
            alert('Помилка зв\'язку з сервером');
        } finally {
            applyButton.disabled = false;
            applyButton.textContent = 'Запустити Агента';
        }
    });
    
    // Initial load
    updateMainGraph();
    
});



