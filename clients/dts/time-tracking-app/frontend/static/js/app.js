/**
 * Time Tracking App - Main Application Controller
 */

class App {
    constructor() {
        this.currentTab = 'clients';
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadTab('clients');
    }

    setupEventListeners() {
        // Tab buttons
        document.querySelectorAll('.tab-button').forEach(button => {
            button.addEventListener('click', (e) => {
                const tab = e.target.dataset.tab;
                this.switchTab(tab);
            });
        });
    }

    switchTab(tabName) {
        // Update active button
        document.querySelectorAll('.tab-button').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

        // Update active content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(tabName).classList.add('active');

        // Load tab content
        this.loadTab(tabName);
        this.currentTab = tabName;
    }

    loadTab(tabName) {
        const container = document.getElementById(tabName);
        
        if (tabName === 'clients') {
            loadClientsTab(container);
        } else if (tabName === 'timesheet') {
            loadTimesheetTab(container);
        } else if (tabName === 'invoices') {
            loadInvoicesTab(container);
        }
    }

    showLoading() {
        document.getElementById('loading').classList.remove('hidden');
    }

    hideLoading() {
        document.getElementById('loading').classList.add('hidden');
    }

    showError(message) {
        const errorDiv = document.getElementById('error');
        errorDiv.textContent = message;
        errorDiv.classList.remove('hidden');
        setTimeout(() => {
            errorDiv.classList.add('hidden');
        }, 5000);
    }

    showSuccess(message) {
        const msg = document.createElement('div');
        msg.className = 'success-message';
        msg.textContent = message;
        document.body.appendChild(msg);
        setTimeout(() => {
            msg.remove();
        }, 3000);
    }
}

// API Helper
class API {
    static baseURL = '/api';

    static async get(endpoint) {
        try {
            const response = await fetch(`${this.baseURL}${endpoint}`);
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error('GET error:', error);
            app.showError(`Error fetching ${endpoint}: ${error.message}`);
            throw error;
        }
    }

    static async post(endpoint, data) {
        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error('POST error:', error);
            app.showError(`Error posting to ${endpoint}: ${error.message}`);
            throw error;
        }
    }

    static async put(endpoint, data) {
        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error('PUT error:', error);
            app.showError(`Error updating ${endpoint}: ${error.message}`);
            throw error;
        }
    }

    static async delete(endpoint) {
        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, {
                method: 'DELETE'
            });
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error('DELETE error:', error);
            app.showError(`Error deleting ${endpoint}: ${error.message}`);
            throw error;
        }
    }
}

// Initialize app when DOM is ready
let app;
document.addEventListener('DOMContentLoaded', () => {
    app = new App();
});
