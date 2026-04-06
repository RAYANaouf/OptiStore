<template>
  <div class="dashboard">
    <header class="dashboard-header">
      <h1>OpticStock Dashboard</h1>
      <p>Welcome back, {{ username }}</p>
    </header>
    
    <div class="dashboard-grid">
      <div class="dashboard-card" @click="$router.push('/pos')">
        <div class="card-icon">💳</div>
        <h3>POS App</h3>
        <p>Point of Sale system for transactions</p>
        <div class="card-stats">
          <span>Today: {{ todaySales }} sales</span>
        </div>
      </div>
      
      <div class="dashboard-card" @click="$router.push('/stock')">
        <div class="card-icon">📦</div>
        <h3>Stock Level</h3>
        <p>Monitor and manage inventory levels</p>
        <div class="card-stats">
          <span>Low stock: {{ lowStockItems }} items</span>
        </div>
      </div>
      
      <div class="dashboard-card" @click="$router.push('/pricing')">
        <div class="card-icon">💰</div>
        <h3>Pricing App</h3>
        <p>Manage product pricing and discounts</p>
        <div class="card-stats">
          <span>Products: {{ totalProducts }} items</span>
        </div>
      </div>
    </div>
    
    <div class="dashboard-summary">
      <h2>Quick Overview</h2>
      <div class="summary-grid">
        <div class="summary-item">
          <h4>Total Revenue Today</h4>
          <p class="summary-value">${{ revenueToday }}</p>
        </div>
        <div class="summary-item">
          <h4>Total Orders</h4>
          <p class="summary-value">{{ totalOrders }}</p>
        </div>
        <div class="summary-item">
          <h4>Items in Stock</h4>
          <p class="summary-value">{{ totalStockItems }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: 'Admin',
      todaySales: 45,
      lowStockItems: 8,
      totalProducts: 156,
      revenueToday: 2450.50,
      totalOrders: 45,
      totalStockItems: 1234
    }
  }
}
</script>

<style scoped>
.dashboard {
  padding: 30px;
}

.dashboard-header {
  margin-bottom: 30px;
}

.dashboard-header h1 {
  color: #2c3e50;
  margin: 0 0 10px;
}

.dashboard-header p {
  color: #7f8c8d;
  margin: 0;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 25px;
  margin-bottom: 40px;
}

.dashboard-card {
  background: white;
  border-radius: 12px;
  padding: 25px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.dashboard-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 20px rgba(0,0,0,0.15);
}

.card-icon {
  font-size: 48px;
  margin-bottom: 15px;
}

.dashboard-card h3 {
  color: #2c3e50;
  margin: 0 0 10px;
}

.dashboard-card p {
  color: #7f8c8d;
  margin: 0 0 15px;
}

.card-stats {
  color: #3498db;
  font-weight: bold;
}

.dashboard-summary {
  background: white;
  border-radius: 12px;
  padding: 25px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.dashboard-summary h2 {
  color: #2c3e50;
  margin: 0 0 20px;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.summary-item h4 {
  color: #7f8c8d;
  margin: 0 0 5px;
  font-weight: normal;
}

.summary-value {
  color: #2c3e50;
  font-size: 24px;
  font-weight: bold;
  margin: 0;
}
</style>
