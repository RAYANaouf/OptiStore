<template>
  <div class="app-container">
    <!-- Header with logout - Only show when logged in and not on POS page -->
    <header v-if="$auth.isLoggedIn && $route.name !== 'POS'" class="app-header">
      <div class="header-content">
        <h1 class="app-title">OpticStock</h1>
        <button @click="$auth.logout()" class="logout-btn">
          Logout
        </button>
      </div>
    </header>
    
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
  flex-direction: column;
  height: 100vh;
  font-family: Arial, sans-serif;
  overflow: hidden;
}

.app-header {
  background-color: #2c3e50;
  color: white;
  padding: 15px 30px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 100%;
}

.app-title {
  margin: 0;
  color: #3498db;
  font-size: 1.8em;
  font-weight: 600;
}

.logout-btn {
  padding: 8px 16px;
  background-color: #e74c3c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
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
