/**
 * Timesheet Tab Module
 */

async function loadTimesheetTab(container) {
    app.showLoading();
    
    try {
        const response = await API.get('/timesheet/current');
        const timesheetData = response.data || {};
        const weekStartStr = response.week_start;
        
        // Use backend's week_start directly - don't recalculate
        let weekStart = new Date(weekStartStr + 'T00:00:00');

        // Calculate dates for each day (Monday to Sunday)
        const dayDates = [];
        const dayNames = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
        for (let day = 0; day < 7; day++) {
            const d = new Date(weekStart);
            d.setDate(d.getDate() + day);
            dayDates.push({
                name: dayNames[day],
                date: d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
            });
        }

        // Format the week start date for display
        const weekStartDisplay = weekStart.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });

        let html = `
            <div class="card">
                <div class="card-header">
                    <div>
                        <h2 class="card-title">Weekly Timesheet</h2>
                        <p class="text-muted" style="margin-top: 5px;">Week of ${weekStartDisplay}</p>
                    </div>
                    <div class="button-group">
                        <button class="button button-primary" onclick="saveAllTimesheet()">💾 Save All</button>
                        <button class="button button-secondary" onclick="reloadTimesheet()">🔄 Refresh</button>
                    </div>
                </div>
            </div>
        `;

        if (Object.keys(timesheetData).length === 0) {
            html += '<div class="card"><p class="text-muted">No clients available. Add clients first!</p></div>';
        } else {
            html += '<div class="timesheet-grid"><table>';
            html += `
                <thead>
                    <tr>
                        <th>Client</th>
            `;
            
            dayDates.forEach(day => {
                html += `<th>${day.name}<br><small>${day.date}</small></th>`;
            });
            
            html += `
                        <th>Weekly Total</th>
                    </tr>
                </thead>
                <tbody>
            `;

            // Sort clients by name
            const sortedClients = Object.entries(timesheetData).sort((a, b) => 
                a[1].ClientName.localeCompare(b[1].ClientName)
            );

            const dailyTotals = [0, 0, 0, 0, 0, 0, 0];

            sortedClients.forEach(([clientId, client]) => {
                let weeklyTotal = 0;
                let row = `<tr><td><strong>${client.ClientName}</strong></td>`;

                for (let day = 1; day <= 7; day++) {
                    const dayData = client.days[day] || {};
                    const hours = dayData.hours || 0;
                    weeklyTotal += hours;
                    dailyTotals[day - 1] += hours;
                    
                    row += `
                        <td>
                            <input type="number" 
                                class="timesheet-input" 
                                data-client="${clientId}" 
                                data-day="${day}" 
                                value="${hours > 0 ? hours : ''}" 
                                step="0.5" 
                                min="0" 
                                max="24"
                                placeholder="0">
                        </td>
                    `;
                }

                row += `<td><strong>${weeklyTotal.toFixed(1)}</strong></td></tr>`;
                html += row;
            });

            // Add daily totals row
            html += `<tr class="totals-row"><td><strong>Daily Total</strong></td>`;
            let grandTotal = 0;
            dailyTotals.forEach(total => {
                grandTotal += total;
                html += `<td><strong>${total.toFixed(1)}</strong></td>`;
            });
            html += `<td><strong>${grandTotal.toFixed(1)}</strong></td></tr>`;

            html += `
                </tbody>
            </table></div>
            `;
        }

        html += '</div>';
        container.innerHTML = html;

        // Add event listeners
        document.querySelectorAll('.timesheet-input').forEach(input => {
            input.addEventListener('blur', () => saveTimeEntry(input));
            input.addEventListener('keydown', (e) => handleTimesheetKeydown(e, input));
            input.addEventListener('wheel', (e) => e.preventDefault());
        });
    } catch (error) {
        container.innerHTML = `<div class="card"><p class="text-danger">Failed to load timesheet</p></div>`;
    } finally {
        app.hideLoading();
    }
}

function handleTimesheetKeydown(event, input) {
    const currentDay = parseInt(input.dataset.day);
    const currentClient = parseInt(input.dataset.client);
    
    // Arrow keys for navigation
    if (event.key === 'ArrowDown') {
        event.preventDefault();
        const dayInputs = Array.from(document.querySelectorAll(
            `.timesheet-input[data-day="${currentDay}"]`
        ));
        const currentIndex = dayInputs.findIndex(inp => 
            parseInt(inp.dataset.client) === currentClient
        );
        if (currentIndex < dayInputs.length - 1) {
            dayInputs[currentIndex + 1].focus();
            dayInputs[currentIndex + 1].select();
        }
    } else if (event.key === 'ArrowUp') {
        event.preventDefault();
        const dayInputs = Array.from(document.querySelectorAll(
            `.timesheet-input[data-day="${currentDay}"]`
        ));
        const currentIndex = dayInputs.findIndex(inp => 
            parseInt(inp.dataset.client) === currentClient
        );
        if (currentIndex > 0) {
            dayInputs[currentIndex - 1].focus();
            dayInputs[currentIndex - 1].select();
        }
    } else if (event.key === 'ArrowRight') {
        event.preventDefault();
        if (currentDay < 7) {
            const nextInput = document.querySelector(
                `.timesheet-input[data-client="${currentClient}"][data-day="${currentDay + 1}"]`
            );
            if (nextInput) {
                nextInput.focus();
                nextInput.select();
            }
        }
    } else if (event.key === 'ArrowLeft') {
        event.preventDefault();
        if (currentDay > 1) {
            const prevInput = document.querySelector(
                `.timesheet-input[data-client="${currentClient}"][data-day="${currentDay - 1}"]`
            );
            if (prevInput) {
                prevInput.focus();
                prevInput.select();
            }
        }
    } else if (event.key === 'Enter') {
        event.preventDefault();
        
        // Get all inputs for this day, sorted by client ID
        const dayInputs = Array.from(document.querySelectorAll(
            `.timesheet-input[data-day="${currentDay}"]`
        ));
        
        // Find current input index
        const currentIndex = dayInputs.findIndex(inp => 
            parseInt(inp.dataset.client) === currentClient
        );
        
        // Move to next client's input for same day
        if (currentIndex < dayInputs.length - 1) {
            const nextInput = dayInputs[currentIndex + 1];
            nextInput.focus();
            nextInput.select();
        } else {
            // At last client for this day
            input.blur();
        }
    }
}

async function saveTimeEntry(input) {
    const clientId = input.dataset.client;
    const day = input.dataset.day;
    const hours = parseFloat(input.value) || 0;

    if (hours < 0 || hours > 24) {
        app.showError('Hours must be between 0 and 24');
        input.value = '';
        return;
    }

    try {
        // Get week start date (for now, send today's date - API will handle it)
        const today = new Date();
        const weekStart = new Date(today);
        weekStart.setDate(today.getDate() - today.getDay() + (today.getDay() === 0 ? -6 : 1));
        
        const payload = {
            client_id: parseInt(clientId),
            week_start_date: weekStart.toISOString().split('T')[0],
            day_of_week: parseInt(day),
            hours_worked: hours,
            rate_used: 100 // Default rate, should be client's rate
        };

        await API.post('/timesheet', payload);
        updateTotals();
    } catch (error) {
        app.showError('Failed to save time entry');
        input.value = ''; // Clear on error
    }
}

function updateTotals() {
    // Update weekly totals for each client row
    const allInputs = document.querySelectorAll('.timesheet-input');
    const clientRows = {};

    // Group inputs by client
    allInputs.forEach(input => {
        const clientId = input.dataset.client;
        if (!clientRows[clientId]) {
            clientRows[clientId] = [];
        }
        clientRows[clientId].push(input);
    });

    // Calculate totals for each client and each day
    const dayTotals = [0, 0, 0, 0, 0, 0, 0];

    Object.entries(clientRows).forEach(([clientId, inputs]) => {
        let weeklyTotal = 0;
        
        inputs.forEach(input => {
            const hours = parseFloat(input.value) || 0;
            const day = parseInt(input.dataset.day) - 1;
            weeklyTotal += hours;
            dayTotals[day] += hours;
        });

        // Find and update the weekly total cell for this client
        const clientRow = inputs[0].closest('tr');
        if (clientRow) {
            const totalCell = clientRow.querySelector('td:last-child');
            if (totalCell) {
                totalCell.textContent = weeklyTotal.toFixed(1);
            }
        }
    });

    // Update the totals row
    const totalsRow = document.querySelector('tr.totals-row');
    if (totalsRow) {
        const cells = totalsRow.querySelectorAll('td');
        let grandTotal = 0;
        dayTotals.forEach((total, index) => {
            if (cells[index + 1]) {
                cells[index + 1].textContent = total.toFixed(1);
                grandTotal += total;
            }
        });
        if (cells[cells.length - 1]) {
            cells[cells.length - 1].textContent = grandTotal.toFixed(1);
        }
    }
}

async function saveAllTimesheet() {
    app.showLoading();
    try {
        const entries = [];
        const today = new Date();
        const weekStart = new Date(today);
        weekStart.setDate(today.getDate() - today.getDay() + (today.getDay() === 0 ? -6 : 1));

        document.querySelectorAll('.timesheet-input').forEach(input => {
            const hours = parseFloat(input.value) || 0;
            if (hours > 0) {
                entries.push({
                    client_id: parseInt(input.dataset.client),
                    week_start_date: weekStart.toISOString().split('T')[0],
                    day_of_week: parseInt(input.dataset.day),
                    hours_worked: hours,
                    rate_used: 100
                });
            }
        });

        if (entries.length === 0) {
            app.showError('No hours to save');
            return;
        }

        await API.post('/timesheet/save-all', entries);
        app.showSuccess('Timesheet saved successfully!');
        updateTotals();
    } catch (error) {
        app.showError('Failed to save timesheet');
    } finally {
        app.hideLoading();
    }
}

function reloadTimesheet() {
    loadTimesheetTab(document.getElementById('timesheet'));
}
