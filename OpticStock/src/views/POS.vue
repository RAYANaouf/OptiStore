<template>
  <div class="pos-app">
    <div class="pos-nav">
      <div class="nav-left">
        <button @click="toggleTimeline" class="timeline-btn">
          <span class="timeline-icon">📅</span>
          Timeline
        </button>
        <button @click="$router.push('/dashboard')" class="back-btn">
          ← Back to Dashboard
        </button>
      </div>
      <button @click="$auth.logout()" class="logout-btn-pos">
        Logout
      </button>
    </div>
    
    <!-- Timeline Sidebar -->
    <div class="timeline-sidebar" :class="{ 'timeline-open': isTimelineOpen }">
      <div class="timeline-header">
        <h3>Timeline</h3>
        <button @click="toggleTimeline" class="close-timeline">×</button>
      </div>
      <div class="timeline-content">
        <div class="timeline-item">
          <div class="timeline-time">10:30 AM</div>
          <div class="timeline-event">Sale #1234 - $125.50</div>
        </div>
        <div class="timeline-item">
          <div class="timeline-time">10:15 AM</div>
          <div class="timeline-event">Sale #1233 - $89.99</div>
        </div>
        <div class="timeline-item">
          <div class="timeline-time">09:45 AM</div>
          <div class="timeline-event">Sale #1232 - $45.00</div>
        </div>
        <div class="timeline-item">
          <div class="timeline-time">09:30 AM</div>
          <div class="timeline-event">Day Started</div>
        </div>
      </div>
    </div>
    
    <div class="pos-header">
      <h1>💳 POS App</h1>
      <p>Point of Sale System</p>
    </div>
    
    <div class="pos-content">
      <!-- POS functionality will be implemented here -->
    </div>
  </div>
</template>

<script>
export default {
  name: 'POS',
  inject: ['$auth'],
  data() {
    return {
      isTimelineOpen: false
    }
  },
  methods: {
    toggleTimeline() {
      this.isTimelineOpen = !this.isTimelineOpen;
    }
  }
}
</script>

<style scoped>
.pos-app {
  padding: 30px;
  min-height: 100vh;
}

.pos-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.nav-left {
  display: flex;
  gap: 10px;
  align-items: center;
}

.timeline-btn {
  padding: 10px 16px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.timeline-btn:hover {
  background-color: #2980b9;
}

.timeline-icon {
  font-size: 16px;
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

.logout-btn-pos {
  padding: 10px 20px;
  background-color: #e74c3c;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

.logout-btn-pos:hover {
  background-color: #c0392b;
}

/* Timeline Sidebar */
.timeline-sidebar {
  position: fixed;
  top: 0;
  left: -350px;
  width: 350px;
  height: 100vh;
  background: white;
  box-shadow: 2px 0 10px rgba(0,0,0,0.1);
  transition: left 0.3s ease-in-out;
  z-index: 1000;
  overflow-y: auto;
}

.timeline-sidebar.timeline-open {
  left: 0;
}

.timeline-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #e1e8ed;
  background: #f8f9fa;
}

.timeline-header h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.2em;
}

.close-timeline {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #7f8c8d;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background-color 0.3s;
}

.close-timeline:hover {
  background-color: #e1e8ed;
}

.timeline-content {
  padding: 20px;
}

.timeline-item {
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e1e8ed;
}

.timeline-item:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.timeline-time {
  color: #7f8c8d;
  font-size: 0.9em;
  margin-bottom: 5px;
}

.timeline-event {
  color: #2c3e50;
  font-weight: 500;
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
  min-height: 400px;
}
</style>
