<template>
  <div class="pos-app">
    <div class="app-nav">
      <button @click="$router.push('/dashboard')" class="back-btn">
        ← Back to Dashboard
      </button>
    </div>
    
    <div class="pos-header">
      <h1>💳 POS App</h1>
      <p>Point of Sale System</p>
    </div>
    
    <div class="pos-content">
      <div class="pos-placeholder">
        <h2>POS System - Coming Soon</h2>
        <p>This will be a fully functional Point of Sale system including:</p>
        <ul>
          <li>Product catalog and search</li>
          <li>Shopping cart functionality</li>
          <li>Payment processing</li>
          <li>Receipt generation</li>
          <li>Order history</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'POS'
}
</script>

<style scoped>
.pos-app {
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

.pos-header {
  margin-bottom: 30px;
}

.pos-header h1 {
  color: #2c3e50;
  margin: 0 0 10px;
  font-size: 2.5em;
}

.pos-header p {
  color: #7f8c8d;
  margin: 0;
  font-size: 1.2em;
}

.pos-content {
  background: white;
  border-radius: 12px;
  padding: 40px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.pos-placeholder h2 {
  color: #2c3e50;
  margin: 0 0 20px;
}

.pos-placeholder p {
  color: #7f8c8d;
  margin: 0 0 20px;
  font-size: 1.1em;
}

.pos-placeholder ul {
  color: #34495e;
  line-height: 1.6;
}

.pos-placeholder li {
  margin-bottom: 10px;
}
</style>
