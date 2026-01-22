// 1. Declare the chart variable at the very top (Global Scope)
let co2Chart = null;

// 2. Define the Graphing function independently
function updateGraph(slopes, region) {
    const canvas = document.getElementById('co2Chart');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    
    const labels = [0, 1000, 2000, 3000, 4000, 5000];
    
    const datasets = Object.keys(slopes).map((modelName, index) => {
        const colors = [
            'rgba(59, 130, 246, 1)', // Blue
            'rgba(16, 185, 129, 1)', // Green
            'rgba(239, 68, 68, 1)'   // Red
        ];
        
        return {
            label: modelName,
            data: labels.map(tokenCount => tokenCount * slopes[modelName]),
            borderColor: colors[index % colors.length],
            backgroundColor: colors[index % colors.length].replace('1)', '0.1)'),
            borderWidth: 2,
            tension: 0.1
        };
    });

    // If a chart already exists, destroy it before creating a new one
    if (co2Chart) {
        co2Chart.destroy();
    }

    co2Chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: `Carbon Emission Projection in ${region} (kg CO₂)`
                },
                legend: { position: 'bottom' }
            },
            scales: {
                x: { title: { display: true, text: 'Number of Tokens' } },
                y: { 
                    beginAtZero: true,
                    title: { display: true, text: 'kg CO₂' } 
                }
            }
        }
    });
}

// 3. The Main Form Listener
document.getElementById('carbon-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const payload = {
        prompt_text: document.getElementById('prompt_text').value,
        model: document.getElementById('model_select').value,
        region: document.getElementById('region_select').value
    };

    try {
        const response = await fetch('/api/calculate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        if (result.status === "success") {
            // Update UI Displays
            document.getElementById('co2_range_display').innerText = result.co2_range;
            document.getElementById('car_range_display').innerText = result.car_range;
            document.getElementById('token_count_display').innerText = "Tokens: " + result.tokens;

            // Update Projection Cards
            const periods = ['mo1', 'mo6', 'yr1', 'yr5'];
            periods.forEach(p => {
                const co2El = document.getElementById(p + '_co2');
                const carEl = document.getElementById(p + '_car');
                if(co2El) co2El.innerText = result.projections[p].co2 + " kg";
                if(carEl) carEl.innerText = result.projections[p].car;
            });

            // Trigger Graph Update
            updateGraph(result.slopes, payload.region);
        } else {
            alert("Error from server: " + result.message);
        }
    } catch (error) {
        console.error("Failed to fetch calculation:", error);
        alert("Check your Python terminal for errors.");
    }
});