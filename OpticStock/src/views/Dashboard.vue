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
      </div>
      
      <div class="dashboard-card" @click="$router.push('/stock')">
        <div class="card-icon">📦</div>
        <h3>Stock Level</h3>
      </div>
      
      <div class="dashboard-card" @click="$router.push('/pricing')">
        <div class="card-icon">💰</div>
        <h3>Pricing App</h3>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: 'Admin'
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
  grid-template-columns: repeat(3, 1fr);
  max-width: 70%;
  margin: 0 auto 40px auto;
  gap: 20px;
}

.dashboard-card {
  background: white;
  border-radius: 12px;
  padding: 30px 20px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
  text-align: center;
  min-height: 160px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.dashboard-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 20px rgba(0,0,0,0.15);
}

.card-icon {
  font-size: 48px;
  margin-bottom: 15px;
}

.dashboard-card h3 {
  color: #2c3e50;
  margin: 0;
  font-size: 1.2em;
  font-weight: 600;
}
</style>
