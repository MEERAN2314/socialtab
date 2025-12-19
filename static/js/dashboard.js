// Dashboard functionality

let currentTab = 'owed';
let debtsData = null;
let notificationsData = null;
let historyData = null;

// Initialize dashboard
async function initDashboard() {
    const username = localStorage.getItem('username');
    if (username) {
        document.getElementById('userName').textContent = username;
    }
    
    await Promise.all([
        loadDebts(),
        loadNotifications(),
        loadStats(),
        loadHistory()
    ]);
}

// Load debts
async function loadDebts() {
    try {
        const response = await apiCall('/debts/my-debts');
        debtsData = await response.json();
        
        renderDebts();
        updateStats();
    } catch (error) {
        console.error('Error loading debts:', error);
        showToast('Failed to load debts', 'error');
    }
}

// Render debts
function renderDebts() {
    const owedList = document.getElementById('owedList');
    const owingList = document.getElementById('owingList');
    
    // Render owed to me
    if (debtsData.owed_to_me && debtsData.owed_to_me.length > 0) {
        owedList.innerHTML = debtsData.owed_to_me.map(debt => createDebtCard(debt, 'creditor')).join('');
    } else {
        owedList.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-inbox"></i>
                <h3>No debts owed to you</h3>
                <p>Create a new debt to get started</p>
            </div>
        `;
    }
    
    // Render I owe
    if (debtsData.i_owe && debtsData.i_owe.length > 0) {
        owingList.innerHTML = debtsData.i_owe.map(debt => createDebtCard(debt, 'debtor')).join('');
    } else {
        owingList.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-check-circle"></i>
                <h3>You're all clear!</h3>
                <p>No outstanding debts</p>
            </div>
        `;
    }
}

// Create debt card HTML
function createDebtCard(debt, role) {
    const statusClass = `status-${debt.status}`;
    const otherUser = role === 'creditor' ? debt.debtor_username : debt.creditor_username;
    
    let actions = '';
    if (role === 'debtor' && debt.status === 'pending') {
        actions = `
            <div class="debt-actions">
                <button class="btn btn-success btn-sm" onclick="acceptDebt('${debt.id}')">
                    <i class="fas fa-check"></i> Accept
                </button>
                <button class="btn btn-danger btn-sm" onclick="disputeDebt('${debt.id}')">
                    <i class="fas fa-times"></i> Dispute
                </button>
            </div>
        `;
    } else if (role === 'debtor' && debt.status === 'active') {
        actions = `
            <div class="debt-actions">
                <button class="btn btn-success btn-sm" onclick="markPaid('${debt.id}')">
                    <i class="fas fa-check-circle"></i> Mark as Paid
                </button>
            </div>
        `;
    } else if (role === 'creditor' && debt.status === 'pending') {
        actions = `
            <div class="debt-actions">
                <button class="btn btn-danger btn-sm" onclick="deleteDebt('${debt.id}')">
                    <i class="fas fa-trash"></i> Cancel
                </button>
            </div>
        `;
    }
    
    return `
        <div class="debt-card">
            <div class="debt-header">
                <div class="debt-amount">${formatCurrency(debt.amount)}</div>
                <div class="debt-status ${statusClass}">${debt.status}</div>
            </div>
            <div class="debt-description">
                <strong>${debt.description}</strong>
            </div>
            <div class="debt-meta">
                <span><i class="fas fa-user"></i> ${otherUser}</span>
                <span><i class="fas fa-clock"></i> ${formatDate(debt.created_at)}</span>
            </div>
            ${actions}
        </div>
    `;
}

// Load notifications
async function loadNotifications() {
    try {
        const response = await apiCall('/users/notifications');
        notificationsData = await response.json();
        
        renderNotifications();
        document.getElementById('notificationCount').textContent = notificationsData.unread_count;
    } catch (error) {
        console.error('Error loading notifications:', error);
    }
}

// Render notifications
function renderNotifications() {
    const notificationsList = document.getElementById('notificationsList');
    
    if (notificationsData.notifications && notificationsData.notifications.length > 0) {
        notificationsList.innerHTML = notificationsData.notifications.map(notif => `
            <div class="notification-card ${notif.read ? '' : 'unread'}" onclick="markNotificationRead('${notif.id}')">
                <div class="debt-header">
                    <strong>${notif.title}</strong>
                    ${!notif.read ? '<span class="debt-status status-pending">New</span>' : ''}
                </div>
                <p>${notif.message}</p>
                <div class="debt-meta">
                    <span><i class="fas fa-clock"></i> ${formatDate(notif.created_at)}</span>
                </div>
            </div>
        `).join('');
    } else {
        notificationsList.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-bell-slash"></i>
                <h3>No notifications</h3>
                <p>You're all caught up!</p>
            </div>
        `;
    }
}

// Load history
async function loadHistory() {
    try {
        const response = await apiCall('/debts/history');
        historyData = await response.json();
        
        renderHistory();
    } catch (error) {
        console.error('Error loading history:', error);
    }
}

// Render history
function renderHistory() {
    const historyList = document.getElementById('historyList');
    
    if (historyData.history && historyData.history.length > 0) {
        historyList.innerHTML = historyData.history.map(debt => {
            const role = debt.creditor_username === localStorage.getItem('username') ? 'creditor' : 'debtor';
            return createDebtCard(debt, role);
        }).join('');
    } else {
        historyList.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-history"></i>
                <h3>No history yet</h3>
                <p>Completed debts will appear here</p>
            </div>
        `;
    }
}

// Load stats
async function loadStats() {
    try {
        const response = await apiCall('/users/stats');
        const stats = await response.json();
        
        document.getElementById('totalOwedToMe').textContent = formatCurrency(stats.total_owed_to_me);
        document.getElementById('totalIOwe').textContent = formatCurrency(stats.total_i_owe);
        
        const netBalance = stats.net_balance;
        const netElement = document.getElementById('netBalance');
        netElement.textContent = formatCurrency(Math.abs(netBalance));
        
        // Update color based on balance
        const netCard = netElement.closest('.stat-card');
        if (netBalance > 0) {
            netCard.classList.remove('stat-negative');
            netCard.classList.add('stat-positive');
        } else if (netBalance < 0) {
            netCard.classList.remove('stat-positive');
            netCard.classList.add('stat-negative');
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Update stats from debts data
function updateStats() {
    if (debtsData) {
        document.getElementById('totalOwedToMe').textContent = formatCurrency(debtsData.total_owed_to_me);
        document.getElementById('totalIOwe').textContent = formatCurrency(debtsData.total_i_owe);
    }
}

// Switch tabs
function switchTab(tab) {
    currentTab = tab;
    
    // Update tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    // Update tab content
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
    
    if (tab === 'owed') {
        document.getElementById('owedTab').classList.add('active');
    } else if (tab === 'owing') {
        document.getElementById('owingTab').classList.add('active');
    } else if (tab === 'notifications') {
        document.getElementById('notificationsTab').classList.add('active');
    } else if (tab === 'history') {
        document.getElementById('historyTab').classList.add('active');
    }
}

// Show new debt modal
function showNewDebtModal() {
    document.getElementById('newDebtModal').classList.add('active');
}

// Close new debt modal
function closeNewDebtModal() {
    document.getElementById('newDebtModal').classList.remove('active');
    document.getElementById('newDebtForm').reset();
}

// Check if user exists
let userCheckTimeout;
document.getElementById('debtorUsername')?.addEventListener('input', (e) => {
    clearTimeout(userCheckTimeout);
    const username = e.target.value.trim();
    
    if (username.length < 3) {
        document.getElementById('userCheck').textContent = '';
        return;
    }
    
    userCheckTimeout = setTimeout(async () => {
        try {
            const response = await apiCall(`/users/search/${username}`);
            if (response.ok) {
                document.getElementById('userCheck').textContent = '✓ User found';
                document.getElementById('userCheck').style.color = 'var(--primary-green)';
            }
        } catch (error) {
            document.getElementById('userCheck').textContent = '✗ User not found';
            document.getElementById('userCheck').style.color = '#ef4444';
        }
    }, 500);
});

// Create new debt
document.getElementById('newDebtForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const btn = document.getElementById('createDebtBtn');
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Creating...';
    
    const formData = {
        debtor_username: document.getElementById('debtorUsername').value.trim(),
        amount: parseFloat(document.getElementById('amount').value),
        description: document.getElementById('description').value.trim(),
        debt_type: 'single'
    };
    
    try {
        const response = await apiCall('/debts/create', {
            method: 'POST',
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showToast('Debt created! Waiting for acceptance...', 'success');
            closeNewDebtModal();
            await loadDebts();
        } else {
            showToast(data.detail || 'Failed to create debt', 'error');
        }
    } catch (error) {
        showToast('Network error. Please try again.', 'error');
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-check"></i> Create Debt';
    }
});

// Accept debt
async function acceptDebt(debtId) {
    try {
        const response = await apiCall(`/debts/${debtId}/action`, {
            method: 'POST',
            body: JSON.stringify({ action: 'accept' })
        });
        
        if (response.ok) {
            showToast('Debt accepted', 'success');
            await loadDebts();
            await loadStats();
        } else {
            const data = await response.json();
            showToast(data.detail || 'Failed to accept debt', 'error');
        }
    } catch (error) {
        showToast('Network error', 'error');
    }
}

// Dispute debt
async function disputeDebt(debtId) {
    const reason = prompt('Why are you disputing this debt?');
    if (!reason) return;
    
    try {
        const response = await apiCall(`/debts/${debtId}/action`, {
            method: 'POST',
            body: JSON.stringify({ action: 'dispute', reason })
        });
        
        if (response.ok) {
            showToast('Debt disputed', 'success');
            await loadDebts();
        } else {
            const data = await response.json();
            showToast(data.detail || 'Failed to dispute debt', 'error');
        }
    } catch (error) {
        showToast('Network error', 'error');
    }
}

// Mark as paid
async function markPaid(debtId) {
    if (!confirm('Mark this debt as paid?')) return;
    
    try {
        const response = await apiCall(`/debts/${debtId}/action`, {
            method: 'POST',
            body: JSON.stringify({ action: 'mark_paid' })
        });
        
        if (response.ok) {
            showToast('Debt marked as paid!', 'success');
            await loadDebts();
            await loadStats();
        } else {
            const data = await response.json();
            showToast(data.detail || 'Failed to mark as paid', 'error');
        }
    } catch (error) {
        showToast('Network error', 'error');
    }
}

// Delete debt
async function deleteDebt(debtId) {
    if (!confirm('Cancel this debt request?')) return;
    
    try {
        const response = await apiCall(`/debts/${debtId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showToast('Debt cancelled', 'success');
            await loadDebts();
        } else {
            const data = await response.json();
            showToast(data.detail || 'Failed to delete debt', 'error');
        }
    } catch (error) {
        showToast('Network error', 'error');
    }
}

// Mark notification as read
async function markNotificationRead(notifId) {
    try {
        await apiCall(`/users/notifications/${notifId}/read`, {
            method: 'POST'
        });
        await loadNotifications();
    } catch (error) {
        console.error('Error marking notification as read:', error);
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    if (window.location.pathname === '/dashboard') {
        initDashboard();
    }
});

// Close modal when clicking outside
document.getElementById('newDebtModal')?.addEventListener('click', (e) => {
    if (e.target.id === 'newDebtModal') {
        closeNewDebtModal();
    }
});
