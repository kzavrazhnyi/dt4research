// Settings page script (Скрипт сторінки налаштувань)

function renderJson(targetEl, obj) {
    try {
        targetEl.textContent = JSON.stringify(obj, null, 2);
    } catch (e) {
        targetEl.textContent = String(obj);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const btnCheckDb = document.getElementById('btnCheckDb');
    const btnCheckRabbit = document.getElementById('btnCheckRabbit');
    const dbResult = document.getElementById('dbResult');
    const rabbitResult = document.getElementById('rabbitResult');
    const settingsTitle = document.getElementById('settingsTitle');
    const btnBack = document.getElementById('btnBack');
    const dbSectionTitle = document.getElementById('dbSectionTitle');
    const dbSectionDesc = document.getElementById('dbSectionDesc');
    const rabbitSectionTitle = document.getElementById('rabbitSectionTitle');
    const rabbitSectionDesc = document.getElementById('rabbitSectionDesc');
    const langSelect = document.getElementById('settingsLangSelect');

    const locales = {
        en: {
            settingsTitle: 'Settings',
            back: '← Back',
            dbTitle: 'Database Health',
            dbDesc: 'Connection to Postgres (Neon/Supabase) via DATABASE_URL',
            checkDb: 'Check DB',
            rabbitTitle: 'RabbitMQ Health',
            rabbitDesc: 'Connection to CloudAMQP via RABBITMQ_URL',
            checkRabbit: 'Check RabbitMQ'
        },
        uk: {
            settingsTitle: 'Налаштування',
            back: '← Назад',
            dbTitle: 'Перевірка БД',
            dbDesc: 'Підключення до Postgres (Neon/Supabase) через DATABASE_URL',
            checkDb: 'Перевірити БД',
            rabbitTitle: 'Перевірка RabbitMQ',
            rabbitDesc: 'Підключення до CloudAMQP через RABBITMQ_URL',
            checkRabbit: 'Перевірити RabbitMQ'
        }
    };

    function getLanguage() {
        const qs = new URLSearchParams(window.location.search);
        const qlang = qs.get('lang');
        if (qlang && ['en','uk'].includes(qlang)) return qlang;
        const ls = localStorage.getItem('dt4researchLanguage');
        return ['en','uk'].includes(ls) ? ls : 'uk';
    }

    function setLanguage(lang) {
        const L = locales[lang] || locales.uk;
        if (settingsTitle) settingsTitle.textContent = L.settingsTitle;
        if (btnBack) btnBack.textContent = L.back;
        if (dbSectionTitle) dbSectionTitle.textContent = L.dbTitle;
        if (dbSectionDesc) dbSectionDesc.textContent = L.dbDesc;
        if (btnCheckDb) btnCheckDb.textContent = L.checkDb;
        if (rabbitSectionTitle) rabbitSectionTitle.textContent = L.rabbitTitle;
        if (rabbitSectionDesc) rabbitSectionDesc.textContent = L.rabbitDesc;
        if (btnCheckRabbit) btnCheckRabbit.textContent = L.checkRabbit;
        if (langSelect) langSelect.value = lang;
    }

    const currentLang = getLanguage();
    setLanguage(currentLang);

    if (langSelect) {
        langSelect.addEventListener('change', (e) => {
            const lang = e.target.value;
            if (!['en','uk'].includes(lang)) return;
            localStorage.setItem('dt4researchLanguage', lang);
            setLanguage(lang);
        });
    }

    if (btnCheckDb) {
        btnCheckDb.addEventListener('click', async () => {
            dbResult.textContent = '...';
            try {
                const resp = await fetch('/api/v1/health/db');
                if (resp.status === 404) {
                    const alt = await fetch('/api/v1/system-state');
                    if (alt.ok) {
                        renderJson(dbResult, { ok: true, via: 'system-state' });
                        return;
                    }
                }
                const data = await resp.json();
                renderJson(dbResult, data);
            } catch (e) {
                renderJson(dbResult, { ok: false, error: String(e) });
            }
        });
    }

    if (btnCheckRabbit) {
        btnCheckRabbit.addEventListener('click', async () => {
            rabbitResult.textContent = '...';
            try {
                const resp = await fetch('/api/v1/health/rabbit');
                const data = await resp.json();
                renderJson(rabbitResult, data);
            } catch (e) {
                renderJson(rabbitResult, { ok: false, error: String(e) });
            }
        });
    }
});
