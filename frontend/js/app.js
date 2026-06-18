// ============================================================
// PowerGuard IoT — Dashboard JavaScript
// ============================================================
// Handles navigation, API calls, chart rendering, and real-time
// updates for the energy monitoring dashboard.
// ============================================================

// ----------------------
// Configuration
// ----------------------

const CONFIG = {
    apiUrl: localStorage.getItem('apiUrl') || 'http://localhost:8000',
    refreshInterval: 2000,  // 2 seconds for real-time data
    tariffRate: parseFloat(localStorage.getItem('tariffRate')) || 6.50,
};

// ----------------------
// State
// ----------------------

let currentPage = 'realtime';
let refreshTimer = null;
let charts = {};
let realtimeHistory = {
    labels: [],
    main: [],
    channel1: [],
    channel2: [],
    maxPoints: 60,  // Keep last 60 readings (~2 min at 2s interval)
};

// ----------------------
// Initialization
// ----------------------

document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initRangeButtons();
    initSettings();
    initMobileMenu();
    startRealtimeUpdates();
    loadSettings();
});

// ----------------------
// Navigation
// ----------------------

function initNavigation() {
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const page = item.dataset.page;
            if (page) navigateTo(page);
        });
    });
}

function navigateTo(page) {
    // Update nav active state
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.toggle('active', item.dataset.page === page);
    });

    // Show correct page
    document.querySelectorAll('.page').forEach(p => {
        p.classList.toggle('active', p.id === `page-${page}`);
    });

    // Update title
    const titles = {
        realtime: 'Real-time Monitor',
        history: 'Historical Data',
        usage: 'Usage & Cost',
        peak: 'Peak Hours Analysis',
        anomalies: 'Anomaly Log',
        settings: 'Settings',
    };
    document.getElementById('page-title').textContent = titles[page] || page;

    currentPage = page;

    // Load page-specific data
    loadPageData(page);

    // Close mobile menu
    document.getElementById('sidebar').classList.remove('open');
}

function loadPageData(page) {
    switch (page) {
        case 'history': loadHistory(); break;
        case 'usage': loadUsageData(); break;
        case 'peak': loadPeakHours(); break;
        case 'anomalies': loadAnomalies(); break;
    }
}

// ----------------------
// Mobile Menu
// ----------------------

function initMobileMenu() {
    const toggle = document.getElementById('menu-toggle');
    const sidebar = document.getElementById('sidebar');
    toggle.addEventListener('click', () => {
        sidebar.classList.toggle('open');
    });
}

// ----------------------
// API Helpers
// ----------------------

async function apiGet(endpoint) {
    try {
        const response = await fetch(`${CONFIG.apiUrl}${endpoint}`);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error(`API Error (${endpoint}):`, error);
        updateConnectionStatus(false);
        return null;
    }
}

function updateConnectionStatus(connected) {
    const dot = document.querySelector('.pulse-dot');
    const statusEl = document.getElementById('device-status');

    if (connected) {
        dot.classList.remove('disconnected');
    } else {
        dot.classList.add('disconnected');
    }
}

// ----------------------
// Real-time Updates
// ----------------------

function startRealtimeUpdates() {
    updateRealtime();
    refreshTimer = setInterval(updateRealtime, CONFIG.refreshInterval);
}

async function updateRealtime() {
    const data = await apiGet('/api/realtime');
    if (!data) return;

    updateConnectionStatus(true);

    const now = new Date().toLocaleTimeString();
    document.getElementById('last-updated').textContent = `Last updated: ${now}`;

    if (data.status === 'no_data' || !data.channels || Object.keys(data.channels).length === 0) {
        document.getElementById('rt-voltage').textContent = '--';
        document.getElementById('rt-current').textContent = '--';
        document.getElementById('rt-power').textContent = '--';
        document.getElementById('rt-energy').textContent = '--';
        document.getElementById('rt-pf').textContent = '--';

        // Update device status
        updateDeviceStatus('offline');
        return;
    }

    // Get main reading (or first available)
    const channels = data.channels;
    const mainKey = Object.keys(channels).find(k => k.includes('main')) || Object.keys(channels)[0];
    const main = channels[mainKey];

    if (main) {
        // Animate value updates
        animateValue('rt-voltage', parseFloat(main.voltage_rms).toFixed(1));
        animateValue('rt-current', parseFloat(main.current_rms).toFixed(2));
        animateValue('rt-power', parseFloat(main.power_watts).toFixed(0));
        animateValue('rt-energy', parseFloat(main.energy_kwh).toFixed(4));

        // Power factor
        const pf = parseFloat(main.power_factor);
        document.getElementById('rt-pf').textContent = pf.toFixed(2);
        updatePowerFactorLabel(pf);

        // Cost estimate
        const energyKwh = parseFloat(main.energy_kwh);
        const cost = (energyKwh * CONFIG.tariffRate).toFixed(2);
        document.getElementById('rt-cost').textContent = `₹ ${cost}`;
        document.getElementById('rt-monthly-cost').textContent = `₹ ${(cost * 30).toFixed(2)}`;

        // Update device status
        updateDeviceStatus('online');
    }

    // Update realtime chart
    updateRealtimeChart(channels);
}

function animateValue(elementId, newValue) {
    const el = document.getElementById(elementId);
    if (el.textContent !== String(newValue)) {
        el.textContent = newValue;
    }
}

function updatePowerFactorLabel(pf) {
    const label = document.getElementById('pf-label');
    if (pf >= 0.95) {
        label.textContent = 'Excellent';
    } else if (pf >= 0.85) {
        label.textContent = 'Good';
    } else if (pf >= 0.7) {
        label.textContent = 'Fair';
    } else {
        label.textContent = 'Poor';
    }
}

function updateDeviceStatus(status) {
    const statusEl = document.getElementById('device-status');
    const dot = statusEl.querySelector('.status-dot');

    if (status === 'online') {
        dot.className = 'status-dot online';
        statusEl.querySelector('span:last-child').textContent = 'Device: Online';
    } else {
        dot.className = 'status-dot offline';
        statusEl.querySelector('span:last-child').textContent = 'Device: Disconnected';
    }
}

// ----------------------
// Real-time Chart
// ----------------------

function updateRealtimeChart(channels) {
    const now = new Date().toLocaleTimeString();

    // Push new data
    realtimeHistory.labels.push(now);

    // Extract power values per channel
    for (const key of Object.keys(channels)) {
        const channel = key.split('/').pop();
        if (!realtimeHistory[channel]) {
            realtimeHistory[channel] = [];
        }
        realtimeHistory[channel].push(channels[key].power_watts || 0);
    }

    // Also push to known channels if missing
    ['main', 'channel1', 'channel2'].forEach(ch => {
        if (!realtimeHistory[ch]) realtimeHistory[ch] = [];
        const key = Object.keys(channels).find(k => k.includes(ch));
        if (!key && realtimeHistory[ch].length < realtimeHistory.labels.length) {
            realtimeHistory[ch].push(0);
        }
    });

    // Trim to maxPoints
    if (realtimeHistory.labels.length > realtimeHistory.maxPoints) {
        realtimeHistory.labels.shift();
        ['main', 'channel1', 'channel2'].forEach(ch => {
            if (realtimeHistory[ch] && realtimeHistory[ch].length > realtimeHistory.maxPoints) {
                realtimeHistory[ch].shift();
            }
        });
    }

    // Render or update chart
    const ctx = document.getElementById('realtime-chart');
    if (!ctx) return;

    if (charts.realtime) {
        charts.realtime.data.labels = realtimeHistory.labels;
        charts.realtime.data.datasets[0].data = realtimeHistory.main || [];
        charts.realtime.data.datasets[1].data = realtimeHistory.channel1 || [];
        charts.realtime.data.datasets[2].data = realtimeHistory.channel2 || [];
        charts.realtime.update('none');  // No animation for smooth updates
    } else {
        charts.realtime = new Chart(ctx, {
            type: 'line',
            data: {
                labels: realtimeHistory.labels,
                datasets: [
                    {
                        label: 'Main Line',
                        data: realtimeHistory.main || [],
                        borderColor: '#0f172a',
                        backgroundColor: 'rgba(15, 23, 42, 0.05)',
                        fill: true,
                        tension: 0,
                        borderWidth: 2,
                        pointRadius: 0,
                    },
                    {
                        label: 'Channel 1',
                        data: realtimeHistory.channel1 || [],
                        borderColor: '#64748b',
                        backgroundColor: 'rgba(100, 116, 139, 0.05)',
                        fill: true,
                        tension: 0,
                        borderWidth: 2,
                        pointRadius: 0,
                    },
                    {
                        label: 'Channel 2',
                        data: realtimeHistory.channel2 || [],
                        borderColor: '#94a3b8',
                        backgroundColor: 'rgba(148, 163, 184, 0.05)',
                        fill: true,
                        tension: 0,
                        borderWidth: 2,
                        pointRadius: 0,
                    },
                ],
            },
            options: getChartOptions('Power (Watts)', true),
        });
    }
}

// ----------------------
// History Chart
// ----------------------

function initRangeButtons() {
    document.querySelectorAll('.range-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.range-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            loadHistory();
        });
    });

    // Channel select change
    const histChannel = document.getElementById('hist-channel');
    if (histChannel) histChannel.addEventListener('change', loadHistory);
}

async function loadHistory() {
    const channel = document.getElementById('hist-channel')?.value || 'main';
    const range = document.querySelector('.range-btn.active')?.dataset.range || '-24h';

    const data = await apiGet(`/api/history?channel=${channel}&range=${range}`);
    if (!data || !data.readings) return;

    const labels = data.readings.map(r => {
        const d = new Date(r.timestamp);
        return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    });
    const power = data.readings.map(r => r.power || 0);
    const voltage = data.readings.map(r => r.voltage || 0);

    // Power chart
    renderChart('history-chart', 'history', {
        labels,
        datasets: [{
            label: `Power — ${channel}`,
            data: power,
            borderColor: '#0f172a',
            backgroundColor: 'rgba(15, 23, 42, 0.05)',
            fill: true,
            tension: 0,
            borderWidth: 2,
            pointRadius: power.length > 100 ? 0 : 2,
        }],
    }, 'Power (Watts)');

    // Voltage chart
    renderChart('voltage-history-chart', 'voltageHistory', {
        labels,
        datasets: [{
            label: `Voltage — ${channel}`,
            data: voltage,
            borderColor: '#64748b',
            backgroundColor: 'rgba(100, 116, 139, 0.05)',
            fill: true,
            tension: 0,
            borderWidth: 2,
            pointRadius: voltage.length > 100 ? 0 : 2,
        }],
    }, 'Voltage (V)');
}

// ----------------------
// Usage Data
// ----------------------

async function loadUsageData() {
    const channel = document.getElementById('usage-channel')?.value || 'main';

    // Load daily usage
    const dailyData = await apiGet(`/api/usage/daily?channel=${channel}&days=30`);
    if (!dailyData) return;

    // Update summary cards
    const daily = dailyData.daily_breakdown || [];
    const today = daily.length > 0 ? daily[daily.length - 1] : null;

    document.getElementById('usage-today-kwh').textContent = today ? today.total_kwh.toFixed(2) : '--';
    document.getElementById('usage-today-cost').textContent = today ? `₹ ${today.cost_inr.toFixed(2)}` : '₹ --';
    document.getElementById('usage-month-kwh').textContent = dailyData.total_kwh?.toFixed(2) || '--';
    document.getElementById('usage-month-cost').textContent = `₹ ${dailyData.total_cost_inr?.toFixed(2) || '--'}`;

    const avgKwh = daily.length > 0 ? dailyData.total_kwh / daily.length : 0;
    document.getElementById('usage-avg-kwh').textContent = avgKwh.toFixed(2);
    document.getElementById('usage-avg-cost').textContent = `₹ ${(avgKwh * CONFIG.tariffRate).toFixed(2)}`;

    // Daily bar chart
    const labels = daily.map(d => d.date.slice(5));  // MM-DD format
    const kwh = daily.map(d => d.total_kwh);

    renderChart('daily-usage-chart', 'dailyUsage', {
        labels,
        datasets: [{
            label: 'Daily kWh',
            data: kwh,
            backgroundColor: kwh.map(v => v > avgKwh * 1.5 ? '#ef4444' : '#0f172a'),
            borderColor: '#ffffff',
            borderWidth: 1,
            borderRadius: 2,
        }],
    }, 'Energy (kWh)', 'bar');

    // Listen for channel change
    const usageChannel = document.getElementById('usage-channel');
    usageChannel.removeEventListener('change', loadUsageData);
    usageChannel.addEventListener('change', loadUsageData);
}

// ----------------------
// Peak Hours
// ----------------------

async function loadPeakHours() {
    const channel = document.getElementById('peak-channel')?.value || 'main';

    const data = await apiGet(`/api/analytics/peak-hours?channel=${channel}`);
    if (!data) return;

    const hourly = data.hourly_breakdown || [];
    const labels = hourly.map(h => `${h.hour}:00`);
    const power = hourly.map(h => h.avg_power_watts);

    // Color bars by intensity (using slate for normal, red for high)
    const maxPower = Math.max(...power, 1);
    const colors = power.map(p => {
        const ratio = p / maxPower;
        if (ratio > 0.8) return '#ef4444';
        if (ratio > 0.5) return '#64748b';
        return '#cbd5e1';
    });

    renderChart('peak-hours-chart', 'peakHours', {
        labels,
        datasets: [{
            label: 'Avg Power (W)',
            data: power,
            backgroundColor: colors,
            borderColor: '#ffffff',
            borderWidth: 1,
            borderRadius: 2,
        }],
    }, 'Average Power (Watts)', 'bar');

    // Update peak/off-peak lists
    updatePeakList('peak-hours-list', data.peak_hours || []);
    updatePeakList('offpeak-hours-list', data.off_peak_hours || []);

    // Listen for channel change
    const peakChannel = document.getElementById('peak-channel');
    peakChannel.removeEventListener('change', loadPeakHours);
    peakChannel.addEventListener('change', loadPeakHours);
}

function updatePeakList(elementId, hours) {
    const el = document.getElementById(elementId);
    if (!hours.length) {
        el.innerHTML = '<p class="no-data">No data available</p>';
        return;
    }

    el.innerHTML = hours.map(h => `
        <div class="peak-item">
            <span class="hour">${h.hour}:00 - ${h.hour + 1}:00</span>
            <span class="power">${h.avg_power_watts.toFixed(0)} W</span>
        </div>
    `).join('');
}

// ----------------------
// Anomalies
// ----------------------

async function loadAnomalies() {
    const hours = document.getElementById('anomaly-hours')?.value || 24;

    const data = await apiGet(`/api/anomalies?hours=${hours}`);
    if (!data) return;

    const tbody = document.getElementById('anomaly-tbody');
    const anomalies = data.anomalies || [];

    // Update badge
    const badge = document.getElementById('anomaly-badge');
    if (anomalies.length > 0) {
        badge.style.display = 'inline';
        badge.textContent = anomalies.length;
    } else {
        badge.style.display = 'none';
    }

    if (anomalies.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="no-data">No anomalies detected ✅</td></tr>';
        return;
    }

    tbody.innerHTML = anomalies.map(a => {
        const time = new Date(a.timestamp).toLocaleString();
        return `
            <tr>
                <td>${time}</td>
                <td>${a.channel}</td>
                <td>${a.type}</td>
                <td><span class="severity-badge ${a.severity}">${a.severity}</span></td>
                <td>${a.description}</td>
                <td>${a.power_at_detection?.toFixed(1) || '--'}</td>
                <td>${a.anomaly_score?.toFixed(2) || '--'}</td>
            </tr>
        `;
    }).join('');

    // Listen for filter change
    const anomalyHours = document.getElementById('anomaly-hours');
    anomalyHours.removeEventListener('change', loadAnomalies);
    anomalyHours.addEventListener('change', loadAnomalies);
}

// ----------------------
// Chart Helper
// ----------------------

function renderChart(canvasId, chartKey, chartData, yLabel, type = 'line') {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    if (charts[chartKey]) {
        charts[chartKey].destroy();
    }

    charts[chartKey] = new Chart(ctx, {
        type,
        data: chartData,
        options: getChartOptions(yLabel),
    });
}

function getChartOptions(yLabel, animate = false) {
    return {
        responsive: true,
        maintainAspectRatio: false,
        animation: animate ? { duration: 0 } : { duration: 400 },
        interaction: {
            intersect: false,
            mode: 'index',
        },
        plugins: {
            legend: {
                display: true,
                labels: {
                    color: '#475569',
                    font: { family: 'Inter', size: 12 },
                    usePointStyle: true,
                    pointStyle: 'rect',
                    padding: 16,
                },
            },
            tooltip: {
                backgroundColor: '#0f172a',
                titleColor: '#ffffff',
                bodyColor: '#e2e8f0',
                borderColor: '#e2e8f0',
                borderWidth: 0,
                padding: 12,
                cornerRadius: 4,
                titleFont: { family: 'Inter', weight: '600' },
                bodyFont: { family: 'Inter' },
            },
        },
        scales: {
            x: {
                ticks: {
                    color: '#94a3b8',
                    font: { family: 'Inter', size: 11 },
                    maxRotation: 0,
                    maxTicksLimit: 12,
                },
                grid: {
                    color: '#f1f5f9',
                },
            },
            y: {
                title: {
                    display: true,
                    text: yLabel,
                    color: '#475569',
                    font: { family: 'Inter', size: 12, weight: '500' },
                },
                ticks: {
                    color: '#94a3b8',
                    font: { family: 'Inter', size: 11 },
                },
                grid: {
                    color: '#f1f5f9',
                },
            },
        },
    };
}

// ----------------------
// Settings
// ----------------------

function initSettings() {
    document.getElementById('save-settings')?.addEventListener('click', saveSettings);
    document.getElementById('reset-settings')?.addEventListener('click', resetSettings);
}

function loadSettings() {
    const apiUrl = localStorage.getItem('apiUrl') || 'http://localhost:8000';
    const tariff = localStorage.getItem('tariffRate') || '6.50';

    document.getElementById('set-api-url').value = apiUrl;
    document.getElementById('set-tariff').value = tariff;

    CONFIG.apiUrl = apiUrl;
    CONFIG.tariffRate = parseFloat(tariff);
}

async function saveSettings() {
    const apiUrl = document.getElementById('set-api-url').value;
    const tariff = document.getElementById('set-tariff').value;
    const threshold = document.getElementById('set-power-threshold').value;
    const leftOn = document.getElementById('set-left-on').value;

    // Save to localStorage
    localStorage.setItem('apiUrl', apiUrl);
    localStorage.setItem('tariffRate', tariff);

    CONFIG.apiUrl = apiUrl;
    CONFIG.tariffRate = parseFloat(tariff);

    // Update backend thresholds
    await fetch(`${CONFIG.apiUrl}/api/settings/thresholds?power_threshold_watts=${threshold}&left_on_seconds=${leftOn}&tariff_rate_inr=${tariff}`, {
        method: 'POST',
    });

    // Visual feedback
    const btn = document.getElementById('save-settings');
    btn.textContent = 'Saved';
    setTimeout(() => {
        btn.textContent = 'Save Configuration';
    }, 2000);
}

function resetSettings() {
    document.getElementById('set-api-url').value = 'http://localhost:8000';
    document.getElementById('set-tariff').value = '6.50';
    document.getElementById('set-power-threshold').value = '2000';
    document.getElementById('set-left-on').value = '7200';
}
