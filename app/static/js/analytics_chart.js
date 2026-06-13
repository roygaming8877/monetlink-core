/**
 * MonetLink Analytics Engine
 * Initializes Chart.js with production gradients
 */
function initDashboardChart(canvasId, labels, dataViews, dataEarnings) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    // Gradients
    const viewGrad = ctx.createLinearGradient(0, 0, 0, 400);
    viewGrad.addColorStop(0, 'rgba(59, 130, 246, 0.3)');
    viewGrad.addColorStop(1, 'rgba(59, 130, 246, 0.0)');

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Views',
                data: dataViews,
                borderColor: '#3b82f6',
                backgroundColor: viewGrad,
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { labels: { color: '#cbd5e1' } } }
        }
    });
}
