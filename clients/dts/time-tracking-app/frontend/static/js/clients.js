/**
 * Clients Tab Module
 */

async function loadClientsTab(container) {
    app.showLoading();
    
    try {
        const response = await API.get('/clients');
        const clients = response.data || [];

        let html = `
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">Client Management</h2>
                    <button class="button button-primary" onclick="showAddClientForm()">+ Add Client</button>
                </div>
            </div>

            <div id="client-form-container"></div>

            <div class="card">
                <h3>Active Clients (${clients.length})</h3>
        `;

        if (clients.length === 0) {
            html += '<p class="text-muted">No clients yet. Create one to get started!</p>';
        } else {
            html += `
                <table>
                    <thead>
                        <tr>
                            <th>Client Name</th>
                            <th>Hourly Rate</th>
                            <th>Contact</th>
                            <th>Email</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            clients.forEach(client => {
                html += `
                    <tr>
                        <td><strong>${client.ClientName}</strong></td>
                        <td>$${client.DefaultRate.toFixed(2)}/hr</td>
                        <td>${client.ContactName || '—'}</td>
                        <td>${client.ContactEmail || '—'}</td>
                        <td>
                            <button class="button button-secondary" onclick="showEditClientForm(${JSON.stringify(client).replace(/"/g, '&quot;')})">Edit</button>
                            <button class="button button-danger" onclick="deleteClient(${client.ClientID})">Delete</button>
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
        container.innerHTML = `<div class="card"><p class="text-danger">Failed to load clients</p></div>`;
    } finally {
        app.hideLoading();
    }
}

function showAddClientForm() {
    const formContainer = document.getElementById('client-form-container');
    formContainer.innerHTML = `
        <div class="card">
            <div class="card-header">
                <h3 class="card-title">Add New Client</h3>
            </div>
            
            <form id="client-form" onsubmit="submitClientForm(event)">
                <div class="grid">
                    <div>
                        <div class="form-group">
                            <label for="client-name">Client Name *</label>
                            <input type="text" id="client-name" name="name" required>
                        </div>
                        <div class="form-group">
                            <label for="client-rate">Hourly Rate ($) *</label>
                            <input type="number" id="client-rate" name="rate" step="0.01" min="0" required>
                        </div>
                        <div class="form-group">
                            <label for="client-terms">Payment Terms (days)</label>
                            <input type="number" id="client-terms" name="terms" value="30" min="0">
                        </div>
                    </div>

                    <div>
                        <div class="form-group">
                            <label for="client-contact">Contact Person</label>
                            <input type="text" id="client-contact" name="contact_name">
                        </div>
                        <div class="form-group">
                            <label for="client-email">Email</label>
                            <input type="email" id="client-email" name="contact_email">
                        </div>
                        <div class="form-group">
                            <label for="client-phone">Phone</label>
                            <input type="text" id="client-phone" name="contact_phone">
                        </div>
                    </div>
                </div>

                <div class="form-group">
                    <label for="client-address">Billing Address</label>
                    <textarea id="client-address" name="billing_address"></textarea>
                </div>

                <div class="button-group">
                    <button type="submit" class="button button-primary">Save Client</button>
                    <button type="button" class="button button-secondary" onclick="document.getElementById('client-form-container').innerHTML = ''">Cancel</button>
                </div>
            </form>
        </div>
    `;
    document.getElementById('client-name').focus();
}

function showEditClientForm(client) {
    const formContainer = document.getElementById('client-form-container');
    formContainer.innerHTML = `
        <div class="card">
            <div class="card-header">
                <h3 class="card-title">Edit Client</h3>
            </div>
            
            <form id="client-form" onsubmit="submitClientForm(event, ${client.ClientID})">
                <div class="grid">
                    <div>
                        <div class="form-group">
                            <label for="client-name">Client Name *</label>
                            <input type="text" id="client-name" name="name" value="${client.ClientName}" required>
                        </div>
                        <div class="form-group">
                            <label for="client-rate">Hourly Rate ($) *</label>
                            <input type="number" id="client-rate" name="rate" value="${client.DefaultRate}" step="0.01" min="0" required>
                        </div>
                        <div class="form-group">
                            <label for="client-terms">Payment Terms (days)</label>
                            <input type="number" id="client-terms" name="terms" value="${client.PaymentTerms}" min="0">
                        </div>
                    </div>

                    <div>
                        <div class="form-group">
                            <label for="client-contact">Contact Person</label>
                            <input type="text" id="client-contact" name="contact_name" value="${client.ContactName || ''}">
                        </div>
                        <div class="form-group">
                            <label for="client-email">Email</label>
                            <input type="email" id="client-email" name="contact_email" value="${client.ContactEmail || ''}">
                        </div>
                        <div class="form-group">
                            <label for="client-phone">Phone</label>
                            <input type="text" id="client-phone" name="contact_phone" value="${client.ContactPhone || ''}">
                        </div>
                    </div>
                </div>

                <div class="form-group">
                    <label for="client-address">Billing Address</label>
                    <textarea id="client-address" name="billing_address">${client.BillingAddress || ''}</textarea>
                </div>

                <div class="button-group">
                    <button type="submit" class="button button-primary">Update Client</button>
                    <button type="button" class="button button-secondary" onclick="document.getElementById('client-form-container').innerHTML = ''">Cancel</button>
                </div>
            </form>
        </div>
    `;
    document.getElementById('client-name').focus();
}

async function submitClientForm(event, clientId = null) {
    event.preventDefault();
    app.showLoading();

    const form = document.getElementById('client-form');
    const data = new FormData(form);
    const payload = Object.fromEntries(data);

    try {
        if (clientId) {
            // Update existing client
            await API.put(`/clients/${clientId}`, payload);
            app.showSuccess('Client updated successfully!');
        } else {
            // Create new client
            await API.post('/clients', payload);
            app.showSuccess('Client created successfully!');
        }
        
        // Reload clients tab
        loadClientsTab(document.getElementById('clients'));
    } catch (error) {
        app.showError('Failed to save client');
    } finally {
        app.hideLoading();
    }
}

async function deleteClient(clientId) {
    if (!confirm('Are you sure you want to delete this client?')) {
        return;
    }

    app.showLoading();
    try {
        await API.delete(`/clients/${clientId}`);
        app.showSuccess('Client deleted successfully!');
        loadClientsTab(document.getElementById('clients'));
    } catch (error) {
        app.showError('Failed to delete client');
    } finally {
        app.hideLoading();
    }
}
