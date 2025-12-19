// Global utility functions

function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast show ${type}`;
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

function toggleNav() {
    const navLinks = document.getElementById('navLinks');
    navLinks.style.display = navLinks.style.display === 'flex' ? 'none' : 'flex';
}

async function logout() {
    try {
        await fetch('/auth/logout', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        
        localStorage.removeItem('token');
        localStorage.removeItem('username');
        showToast('Logged out successfully', 'success');
        
        setTimeout(() => {
            window.location.href = '/';
        }, 1000);
    } catch (error) {
        console.error('Logout error:', error);
        localStorage.removeItem('token');
        localStorage.removeItem('username');
        window.location.href = '/';
    }
}

// Check authentication
function checkAuth() {
    const token = localStorage.getItem('token');
    const currentPath = window.location.pathname;
    
    if (!token && currentPath === '/dashboard') {
        window.location.href = '/login';
        return false;
    }
    
    if (token && (currentPath === '/login' || currentPath === '/signup')) {
        window.location.href = '/dashboard';
        return false;
    }
    
    return true;
}

// API helper
async function apiCall(endpoint, options = {}) {
    const token = localStorage.getItem('token');
    
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            ...(token && { 'Authorization': `Bearer ${token}` })
        }
    };
    
    const response = await fetch(endpoint, { ...defaultOptions, ...options });
    
    if (response.status === 401) {
        localStorage.removeItem('token');
        localStorage.removeItem('username');
        window.location.href = '/login';
        throw new Error('Unauthorized');
    }
    
    return response;
}

// Format currency
function formatCurrency(amount) {
    return `$${parseFloat(amount).toFixed(2)}`;
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diff = now - date;
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    
    if (days === 0) return 'Today';
    if (days === 1) return 'Yesterday';
    if (days < 7) return `${days} days ago`;
    if (days < 30) return `${Math.floor(days / 7)} weeks ago`;
    if (days < 365) return `${Math.floor(days / 30)} months ago`;
    return date.toLocaleDateString();
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
});
