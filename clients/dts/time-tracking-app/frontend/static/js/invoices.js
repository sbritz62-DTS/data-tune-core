/**
 * Invoices Tab Module - Redesigned with Date Range Selection
 */

async function loadInvoicesTab(container) {
    app.showLoading();
    
    try {
        const response = await API.get('/invoices');
        const invoices = response.data || [];

        let html = `
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">Invoice Management</h2>
                    <button class="button button-primary" onclick="showCreateInvoiceForm()">+ Create Invoice</button>
                </div>
            </div>

            <div id="invoice-form-container"></div>

            <div class="card">
                <h3>Invoices (${invoices.length})</h3>
        `;

        if (invoices.length === 0) {
            html += '<p class="text-muted">No invoices yet. Create one to get started!</p>';
        } else {
            html += `
                <table>
                    <thead>
                        <tr>
                            <th>Invoice #</th>
                            <th>Client</th>
                            <th>Hours</th>
                            <th>Amount</th>
                            <th>Status</th>
                            <th>Date</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            invoices.forEach(invoice => {
                const statusClass = getStatusClass(invoice.Status);
                html += `
                    <tr>
                        <td><strong>${invoice.InvoiceNumber}</strong></td>
                        <td>${invoice.ClientName}</td>
                        <td>${invoice.TotalHours.toFixed(1)}</td>
                        <td>$${invoice.TotalAmount.toFixed(2)}</td>
                        <td><span class="${statusClass}">${invoice.Status}</span></td>
                        <td>${invoice.InvoiceDate}</td>
                        <td>
                            <button class="button button-secondary" onclick="showInvoiceDetails(${invoice.InvoiceID})">View</button>
                            <button class="button button-danger" onclick="deleteInvoice(${invoice.InvoiceID})">Delete</button>
                        </td>
                    </tr>
                `;
            });

            html += `
                    </tbody>
                </table>
            `;
        }

        html += '</div>';
        container.innerHTML = html;
    } catch (error) {
        container.innerHTML = `<div class="card"><p class="text-danger">Failed to load invoices</p></div>`;
    } finally {
        app.hideLoading();
    }
}

function getStatusClass(status) {
    const classes = {
        'Draft': 'text-muted',
        'Sent': 'text-secondary',
        'Paid': 'text-success',
        'Overdue': 'text-danger',
        'Cancelled': 'text-muted'
    };
    return classes[status] || 'text-muted';
}

function getLastFourBusinessWeeksDates() {
    /**
     * Calculate 4 complete business weeks back from today
     * Business weeks: Monday-Friday
     */
    const today = new Date();
    
    // Get current week's Monday
    const dayOfWeek = today.getDay();
    const diff = today.getDate() - dayOfWeek + (dayOfWeek === 0 ? -6 : 1);
    const currentMonday = new Date(today.setDate(diff));
    
    // Go back 4 weeks (28 days) from current Monday
    const endDate = new Date(currentMonday);
    endDate.setDate(endDate.getDate() - 1); // Friday of previous week
    
    const startDate = new Date(endDate);
    startDate.setDate(startDate.getDate() - 27); // 4 weeks back (20 business days, plus 2 days)
    
    // Format as YYYY-MM-DD
    const formatDate = (d) => d.toISOString().split('T')[0];
    
    return {
        start: formatDate(startDate),
        end: formatDate(endDate)
    };
}

async function showCreateInvoiceForm() {
    app.showLoading();
    
    try {
        // Get all clients
        const clientsResponse = await API.get('/clients');
        const clients = clientsResponse.data || [];

        // Get default date range
        const dateRange = getLastFourBusinessWeeksDates();

        const formContainer = document.getElementById('invoice-form-container');
        formContainer.innerHTML = `
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">Create Invoice</h3>
                </div>
                
                <form id="invoice-form" onsubmit="submitInvoiceForm(event)">
                    <!-- Step 1: Client Selection -->
                    <div class="form-group">
                        <label for="invoice-client">Client *</label>
                        <select id="invoice-client" name="client_id" required onchange="onClientSelect()">
                            <option value="">Select a client...</option>
                            ${clients.map(c => `<option value="${c.ClientID}">${c.ClientName}</option>`).join('')}
                        </select>
                    </div>

                    <!-- Step 2: Date Range (Hidden until client selected) -->
                    <div id="date-range-section" style="display: none;">
                        <div class="grid">
                            <div>
                                <div class="form-group">
                                    <label for="range-start">From Date *</label>
                                    <input type="date" id="range-start" value="${dateRange.start}" required>
                                </div>
                            </div>
                            <div>
                                <div class="form-group">
                                    <label for="range-end">To Date *</label>
                                    <input type="date" id="range-end" value="${dateRange.end}" required>
                                </div>
                            </div>
                        </div>
                        <button type="button" class="button button-primary" onclick="loadHoursByRange()">Load Hours</button>
                    </div>

                    <!-- Step 3: Hours Summary (Hidden until hours loaded) -->
                    <div id="hours-summary-section" style="display: none;">
                        <div class="card" style="background-color: var(--bg-light); padding: 15px; margin: 15px 0;">
                            <h4>Hours Summary</h4>
                            
                            <div class="grid">
                                <div>
                                    <p><strong>Total Hours:</strong></p>
                                    <p style="font-size: 1.5em; color: var(--accent);" id="total-hours-display">0.0</p>
                                </div>
                                <div>
                                    <p><strong>Total Amount:</strong></p>
                                    <p style="font-size: 1.5em; color: var(--accent);" id="total-amount-display">$0.00</p>
                                </div>
                            </div>

                            <button type="button" class="button button-secondary" style="margin-top: 10px;" onclick="toggleLineItems()">
                                📋 View Hour Details
                            </button>

                            <!-- Line Items (Hidden by default) -->
                            <div id="line-items-section" style="display: none; margin-top: 15px;">
                                <table>
                                    <thead>
                                        <tr>
                                            <th>Date</th>
                                            <th>Hours</th>
                                            <th>Rate</th>
                                            <th>Amount</th>
                                        </tr>
                                    </thead>
                                    <tbody id="line-items-tbody">
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>

                    <!-- Step 4: Invoice Details (Hidden until hours loaded) -->
                    <div id="invoice-details-section" style="display: none;">
                        <div class="form-group">
                            <label for="invoice-date">Invoice Date *</label>
                            <input type="date" id="invoice-date" name="invoice_date" required 
                                   value="${new Date().toISOString().split('T')[0]}">
                        </div>

                        <div class="form-group">
                            <label for="invoice-notes">Notes</label>
                            <textarea id="invoice-notes" name="notes" placeholder="Optional notes for this invoice"></textarea>
                        </div>

                        <div class="button-group">
                            <button type="submit" class="button button-primary">✅ Create Invoice</button>
                            <button type="button" class="button button-secondary" onclick="document.getElementById('invoice-form-container').innerHTML = ''">Cancel</button>
                        </div>
                    </div>
                </form>
            </div>
        `;

        // Store loaded hours data globally for form submission
        window.loadedHoursData = null;

    } catch (error) {
        app.showError('Failed to load clients');
    } finally {
        app.hideLoading();
    }
}

function onClientSelect() {
    const clientId = document.getElementById('invoice-client').value;
    const dateRangeSection = document.getElementById('date-range-section');
    const hoursSummarySection = document.getElementById('hours-summary-section');
    const invoiceDetailsSection = document.getElementById('invoice-details-section');

    if (clientId) {
        dateRangeSection.style.display = 'block';
        hoursSummarySection.style.display = 'none';
        invoiceDetailsSection.style.display = 'none';
        window.loadedHoursData = null;
    } else {
        dateRangeSection.style.display = 'none';
        hoursSummarySection.style.display = 'none';
        invoiceDetailsSection.style.display = 'none';
    }
}

async function loadHoursByRange() {
    const clientId = document.getElementById('invoice-client').value;
    const startDate = document.getElementById('range-start').value;
    const endDate = document.getElementById('range-end').value;

    if (!clientId || !startDate || !endDate) {
        app.showError('Please select client and date range');
        return;
    }

    if (startDate > endDate) {
        app.showError('Start date must be before or equal to end date');
        return;
    }

    app.showLoading();

    try {
        const response = await API.get(`/clients/${clientId}/hours-by-range?start_date=${startDate}&end_date=${endDate}`);
        const data = response;

        if (data.total_hours === 0) {
            app.showError('No unbilled hours found in this date range');
            window.loadedHoursData = null;
            return;
        }

        // Store hours data for form submission
        window.loadedHoursData = {
            total_hours: data.total_hours,
            total_amount: data.total_amount,
            entries: data.entries
        };

        // Update display
        document.getElementById('total-hours-display').textContent = data.total_hours.toFixed(1);
        document.getElementById('total-amount-display').textContent = `$${data.total_amount.toFixed(2)}`;

        // Populate line items
        const tbody = document.getElementById('line-items-tbody');
        tbody.innerHTML = data.entries.map(entry => `
            <tr>
                <td>${entry.Date}</td>
                <td>${entry.Hours.toFixed(1)}</td>
                <td>$${entry.Rate.toFixed(2)}</td>
                <td>$${entry.Amount.toFixed(2)}</td>
            </tr>
        `).join('');

        // Show summary and details sections
        document.getElementById('hours-summary-section').style.display = 'block';
        document.getElementById('invoice-details-section').style.display = 'block';
        document.getElementById('line-items-section').style.display = 'none'; // Keep hidden by default

        app.showSuccess('Hours loaded successfully');

    } catch (error) {
        app.showError('Failed to load hours - ' + (error.message || 'Unknown error'));
        window.loadedHoursData = null;
    } finally {
        app.hideLoading();
    }
}

function toggleLineItems() {
    const section = document.getElementById('line-items-section');
    section.style.display = section.style.display === 'none' ? 'block' : 'none';
}

async function submitInvoiceForm(event) {
    event.preventDefault();
    
    if (!window.loadedHoursData) {
        app.showError('No hours loaded. Please load hours first');
        return;
    }

    app.showLoading();

    try {
        const clientId = parseInt(document.getElementById('invoice-client').value);
        const invoiceDate = document.getElementById('invoice-date').value;
        const notes = document.getElementById('invoice-notes').value;

        // Build items array from loaded hours data
        const items = window.loadedHoursData.entries.map(entry => ({
            EntryID: entry.EntryID,
            Date: entry.Date,
            Description: 'Development Work',
            Hours: entry.Hours,
            Rate: entry.Rate,
            Amount: entry.Amount
        }));

        const payload = {
            client_id: clientId,
            invoice_date: invoiceDate,
            total_hours: window.loadedHoursData.total_hours,
            total_amount: window.loadedHoursData.total_amount,
            notes: notes,
            items: items
        };

        await API.post('/invoices', payload);
        app.showSuccess('Invoice created successfully!');
        
        // Clear form
        document.getElementById('invoice-form-container').innerHTML = '';
        
        // Reload invoices list
        loadInvoicesTab(document.getElementById('invoices'));
        
    } catch (error) {
        app.showError('Failed to create invoice - ' + (error.message || 'Unknown error'));
    } finally {
        app.hideLoading();
    }
}

async function showInvoiceDetails(invoiceId) {
    app.showLoading();
    
    try {
        const response = await API.get(`/invoices/${invoiceId}`);
        const invoice = response.data;
        const items = invoice.Items || [];

        const formContainer = document.getElementById('invoice-form-container');
        formContainer.innerHTML = `
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">${invoice.InvoiceNumber}</h3>
                </div>

                <div class="grid">
                    <div>
                        <p><strong>Client:</strong> ${invoice.ClientName}</p>
                        <p><strong>Date:</strong> ${invoice.InvoiceDate}</p>
                        <p><strong>Due:</strong> ${invoice.DueDate}</p>
                    </div>
                    <div>
                        <p><strong>Hours:</strong> ${invoice.TotalHours.toFixed(1)}</p>
                        <p><strong>Amount:</strong> $${invoice.TotalAmount.toFixed(2)}</p>
                        <p><strong>Status:</strong> 
                            <select id="status-select" onchange="updateInvoiceStatus(${invoiceId}, this.value)">
                                <option value="Draft" ${invoice.Status === 'Draft' ? 'selected' : ''}>Draft</option>
                                <option value="Sent" ${invoice.Status === 'Sent' ? 'selected' : ''}>Sent</option>
                                <option value="Paid" ${invoice.Status === 'Paid' ? 'selected' : ''}>Paid</option>
                                <option value="Overdue" ${invoice.Status === 'Overdue' ? 'selected' : ''}>Overdue</option>
                                <option value="Cancelled" ${invoice.Status === 'Cancelled' ? 'selected' : ''}>Cancelled</option>
                            </select>
                        </p>
                    </div>
                </div>

                ${invoice.Notes ? `<p><strong>Notes:</strong> ${invoice.Notes}</p>` : ''}

                <h4 style="margin-top: 20px;">Line Items</h4>
                ${items.length === 0 ? '<p class="text-muted">No line items</p>' : `
                    <table>
                        <thead><tr><th>Date</th><th>Hours</th><th>Rate</th><th>Amount</th></tr></thead>
                        <tbody>
                            ${items.map(item => `
                                <tr>
                                    <td>${item.Date}</td>
                                    <td>${item.Hours.toFixed(1)}</td>
                                    <td>$${item.Rate.toFixed(2)}</td>
                                    <td>$${item.Amount.toFixed(2)}</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                `}

                <div class="button-group" style="margin-top: 20px;">
                    <button class="button button-primary" onclick="generatePDF(${invoiceId})">📄 Generate PDF</button>
                    <button class="button button-danger" onclick="deleteInvoice(${invoiceId})">Delete</button>
                    <button class="button button-secondary" onclick="document.getElementById('invoice-form-container').innerHTML = ''">Close</button>
                </div>
            </div>
        `;
    } catch (error) {
        app.showError('Failed to load invoice');
    } finally {
        app.hideLoading();
    }
}

async function updateInvoiceStatus(invoiceId, status) {
    try {
        await API.put(`/invoices/${invoiceId}/status`, { status });
        app.showSuccess('Status updated!');
        loadInvoicesTab(document.getElementById('invoices'));
    } catch (error) {
        app.showError('Failed to update status');
    }
}

async function generatePDF(invoiceId) {
    app.showLoading();
    try {
        const response = await API.post(`/invoices/${invoiceId}/pdf`, {});
        app.showSuccess('PDF generated successfully!');
    } catch (error) {
        app.showError('Failed to generate PDF');
    } finally {
        app.hideLoading();
    }
}

async function deleteInvoice(invoiceId) {
    if (!confirm('Are you sure you want to delete this invoice?')) {
        return;
    }

    app.showLoading();
    try {
        await API.delete(`/invoices/${invoiceId}`);
        app.showSuccess('Invoice deleted successfully!');
        loadInvoicesTab(document.getElementById('invoices'));
    } catch (error) {
        app.showError('Failed to delete invoice');
    } finally {
        app.hideLoading();
    }
}
