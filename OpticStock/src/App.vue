<template>
  <div class="app-container">
    <!-- Sidebar Navigation - Only show when logged in -->
    <div v-if="$auth.isLoggedIn" class="sidebar">
      <div class="logo">
        <h2>OpticStock</h2>
      </div>
      <nav class="nav-menu">
        <router-link to="/dashboard" class="nav-item">
          <span class="nav-icon">📊</span>
          Dashboard
        </router-link>
        <router-link to="/pos" class="nav-item">
          <span class="nav-icon">💳</span>
          POS App
        </router-link>
        <router-link to="/stock" class="nav-item">
          <span class="nav-icon">📦</span>
          Stock Level
        </router-link>
        <router-link to="/pricing" class="nav-item">
          <span class="nav-icon">💰</span>
          Pricing App
        </router-link>
      </nav>
      <div class="logout-section">
        <button @click="$auth.logout()" class="logout-btn">
          Logout
        </button>
      </div>
    </div>
    
    <!-- Main Content Area -->
    <div class="main-content">
      <router-view />
    </div>
  </div>
</template>

<script>
export default {
	inject: ['$auth']
};
</script>

<style scoped>
.app-container {
  display: flex;
  height: 100vh;
  font-family: Arial, sans-serif;
}

.sidebar {
  width: 250px;
  background-color: #2c3e50;
  color: white;
  display: flex;
  flex-direction: column;
  padding: 20px 0;
}

.logo {
  padding: 0 20px 30px;
  border-bottom: 1px solid #34495e;
  margin-bottom: 20px;
}

.logo h2 {
  margin: 0;
  color: #3498db;
}

.nav-menu {
  flex: 1;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 15px 20px;
  color: white;
  text-decoration: none;
  transition: background-color 0.3s;
}

.nav-item:hover {
  background-color: #34495e;
}

.nav-item.router-link-active {
  background-color: #3498db;
}

.nav-icon {
  margin-right: 10px;
  font-size: 18px;
}

.logout-section {
  padding: 20px;
  border-top: 1px solid #34495e;
}

.logout-btn {
  width: 100%;
  padding: 10px;
  background-color: #e74c3c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.logout-btn:hover {
  background-color: #c0392b;
}

.main-content {
  flex: 1;
  background-color: #f5f5f5;
  overflow-y: auto;
}
</style>
