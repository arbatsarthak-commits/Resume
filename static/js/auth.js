/**
 * ResumeIQ AI - Authentication Helper
 * Handles token management, user state, and auth-dependent UI
 */

const AUTH_TOKEN_KEY = "resumeiq_token";
const AUTH_USER_KEY = "resumeiq_user";

function getAuthToken() {
  return localStorage.getItem(AUTH_TOKEN_KEY);
}

function getCurrentUser() {
  try {
    const raw = localStorage.getItem(AUTH_USER_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

function isAuthenticated() {
  return !!getAuthToken();
}

function setAuthData(token, user) {
  localStorage.setItem(AUTH_TOKEN_KEY, token);
  localStorage.setItem(AUTH_USER_KEY, JSON.stringify(user));
}

function clearAuthData() {
  localStorage.removeItem(AUTH_TOKEN_KEY);
  localStorage.removeItem(AUTH_USER_KEY);
}

function logout() {
  clearAuthData();
  window.location.href = "/";
}

/**
 * Fetch wrapper that automatically attaches JWT token.
 */
async function authFetch(url, options = {}) {
  const token = getAuthToken();
  const headers = options.headers || {};

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  if (!(options.body instanceof FormData)) {
    headers["Content-Type"] = headers["Content-Type"] || "application/json";
  }

  const response = await fetch(url, {
    ...options,
    headers
  });

  // If 401, clear auth and redirect to login
  if (response.status === 401) {
    const data = await response.json().catch(() => ({}));
    if (!data.success) {
      clearAuthData();
      const currentPath = window.location.pathname;
      if (currentPath !== "/login" && currentPath !== "/register") {
        window.location.href = "/login";
      }
    }
  }

  return response;
}

/**
 * Update navigation based on auth state.
 * Call this on page load.
 */
function updateAuthUI() {
  const user = getCurrentUser();
  const navMenu = document.getElementById("nav-menu");

  if (!navMenu) return;

  // Remove existing auth links
  const existingLogin = document.getElementById("nav-login-link");
  const existingLogout = document.getElementById("nav-logout-link");
  const existingProfile = document.getElementById("nav-profile-link");
  if (existingLogin) existingLogin.remove();
  if (existingLogout) existingLogout.remove();
  if (existingProfile) existingProfile.remove();

  if (user) {
    // User is logged in - show profile and logout
    const profileLink = document.createElement("a");
    profileLink.id = "nav-profile-link";
    profileLink.href = "/profile";
    profileLink.innerHTML = `<i class="fa-solid fa-user"></i> ${user.full_name || "Profile"}`;
    navMenu.appendChild(profileLink);

    const logoutLink = document.createElement("a");
    logoutLink.id = "nav-logout-link";
    logoutLink.href = "#";
    logoutLink.innerHTML = '<i class="fa-solid fa-sign-out-alt"></i> Logout';
    logoutLink.addEventListener("click", (e) => {
      e.preventDefault();
      logout();
    });
    navMenu.appendChild(logoutLink);
  } else {
    // User is not logged in - show login and register
    const loginLink = document.createElement("a");
    loginLink.id = "nav-login-link";
    loginLink.href = "/login";
    loginLink.innerHTML = '<i class="fa-solid fa-right-to-bracket"></i> Sign In';
    navMenu.appendChild(loginLink);
  }
}

// Auto-initialize auth UI on DOMContentLoaded
document.addEventListener("DOMContentLoaded", updateAuthUI);

