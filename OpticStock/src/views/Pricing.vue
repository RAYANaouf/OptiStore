<template>
  <div class="pricing-app">
    <div class="app-nav">
      <button @click="$router.push('/dashboard')" class="back-btn">
        ← Back to Dashboard
      </button>
    </div>
    
    <div class="pricing-header">
      <h1>💰 Pricing App</h1>
      <p>Price Management System</p>
    </div>
    
    <div class="pricing-content">
      <div class="pricing-placeholder">
        <h2>Pricing Management - Coming Soon</h2>
        <p>This will be a comprehensive pricing management system including:</p>
        <ul>
          <li>Product pricing configuration</li>
          <li>Discount and promotion management</li>
          <li>Price history tracking</li>
          <li>Competitive pricing analysis</li>
          <li>Margin calculation tools</li>
          <li>Bulk price updates</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Pricing'
}
</script>

<style scoped>
.pricing-app {
  padding: 30px;
}

.app-nav {
  margin-bottom: 20px;
}

.back-btn {
  padding: 10px 20px;
  background-color: #27ae60;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

.back-btn:hover {
  background-color: #16a085;
}

.pricing-header {
  margin-bottom: 30px;
}

.pricing-header h1 {
  color: #2c3e50;
  margin: 0 0 10px;
  font-size: 2.5em;
}

.pricing-header p {
  color: #7f8c8d;
  margin: 0;
  font-size: 1.2em;
}

.pricing-content {
  background: white;
  border-radius: 12px;
  padding: 40px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.pricing-placeholder h2 {
  color: #2c3e50;
  margin: 0 0 20px;
}

.pricing-placeholder p {
  color: #7f8c8d;
  margin: 0 0 20px;
  font-size: 1.1em;
}

.pricing-placeholder ul {
  color: #34495e;
  line-height: 1.6;
}

.pricing-placeholder li {
  margin-bottom: 10px;
}
</style>
