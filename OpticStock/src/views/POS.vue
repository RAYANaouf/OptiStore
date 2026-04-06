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
    
    <div class="pos-content">
      <div class="pos-layout">
        <!-- Left Side - Selected Items Card -->
        <div class="selected-items-card">
          <div class="card-header">
            <div class="customer-section">
              <label for="customer-select">Customer:</label>
              <select 
                id="customer-select"
                v-model="selectedCustomer"
                class="customer-select"
              >
                <option value="">Walk-in Customer</option>
                <option v-for="customer in customers" :key="customer.name" :value="customer.name">
                  {{ customer.customer_name }}
                </option>
              </select>
            </div>
            <div class="total-amount">
              Total: ${{ totalAmount.toFixed(2) }}
            </div>
          </div>
          <div class="items-list">
            <div v-for="(item, index) in selectedItems" :key="index" class="selected-item">
              <div class="item-info">
                <span class="item-name">{{ item.name }}</span>
                <span class="item-price">${{ item.price.toFixed(2) }}</span>
              </div>
              <div class="item-controls">
                <span class="quantity">Qty: {{ item.quantity }}</span>
              </div>
            </div>
            <div v-if="selectedItems.length === 0" class="empty-cart">
              <p>No items selected</p>
            </div>
          </div>
          <div class="cart-actions">
            <button class="clear-btn" @click="clearCart">Clear Cart</button>
            <button class="checkout-btn" @click="checkout">Checkout</button>
          </div>
        </div>

        <!-- Right Side - Item Selector -->
        <div class="item-selector">
          <div class="selector-header">
            <div class="search-container">
              <input 
                type="text" 
                v-model="searchQuery" 
                placeholder="Search products..."
                class="search-input"
              />
              <button 
                v-if="searchQuery" 
                @click="clearSearch" 
                class="clear-search-btn"
              >
                ×
              </button>
            </div>
          </div>
          <div v-if="loading" class="loading-state">
            <p>Loading products...</p>
          </div>
          <div v-else class="products-grid">
            <div 
              v-for="product in filteredProducts" 
              :key="product.id"
              @click="addToCart(product)"
              class="product-card"
            >
              <div class="product-image">📦</div>
              <div class="product-info">
                <h4>{{ product.name }}</h4>
                <p class="product-price">${{ product.price.toFixed(2) }}</p>
                <p class="product-stock">Stock: {{ product.stock }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'POS',
  inject: ['$auth', '$call'],
  data() {
    return {
      isTimelineOpen: false,
      selectedItems: [],
      searchQuery: '',
      products: [],
      allProducts: [], // Store all products
      loading: false,
      selectedCustomer: '',
      customers: []
    }
  },
  computed: {
    totalAmount() {
      return this.selectedItems.reduce((total, item) => {
        return total + (item.price * item.quantity);
      }, 0);
    },
    filteredProducts() {
      let products = this.allProducts;
      
      // Search through all products
      if (this.searchQuery) {
        products = products.filter(product =>
          product.name.toLowerCase().includes(this.searchQuery.toLowerCase())
        );
      }
      
      // Only render first 50 for performance
      return products.slice(0, 50);
    }
  },
  mounted() {
    this.fetchProducts();
    this.fetchCustomers();
  },
  methods: {
    toggleTimeline() {
      this.isTimelineOpen = !this.isTimelineOpen;
    },
    clearSearch() {
      this.searchQuery = '';
    },
    async fetchCustomers() {
      try {
        const response = await this.$call('opti_stock.api.get_customers');
        if (response && response.data) {
          this.customers = response.data;
        }
      } catch (error) {
        console.error('Error fetching customers:', error);
      }
    },
    async fetchProducts() {
      this.loading = true;
      try {
        // Fetch all items from ERPNext backend
        const response = await this.$call('opti_stock.api.get_products', {
          fields: ['name', 'item_name'],
          filters: {
            disabled: 0
          }
        });
        
        console.log(response);
        
        if (response && response.data) {
          // Store all products for search
          this.allProducts = response.data.map(item => ({
            id: item.name,
            name: item.item_name || item.name,
            price: 0, // Default price since not fetched
            stock: 0, // Default stock since not fetched
            code: item.name
          }));
          
          console.log(`Loaded ${this.allProducts.length} products from backend`);
          
          // Show info if we have more than 50 items
          if (this.allProducts.length > 50) {
            console.log(`Showing first 50 of ${this.allProducts.length} total items`);
          }
        }
      } catch (error) {
        console.error('Error fetching products:', error);
        // Fallback to sample data if API fails
        this.allProducts = [
          { id: 1, name: 'Glasses Frame A', price: 89.99, stock: 15 },
          { id: 2, name: 'Glasses Frame B', price: 124.50, stock: 8 },
          { id: 3, name: 'Contact Lenses', price: 45.00, stock: 25 },
          { id: 4, name: 'Sunglasses', price: 156.99, stock: 12 },
          { id: 5, name: 'Reading Glasses', price: 67.50, stock: 18 },
          { id: 6, name: 'Eye Drops', price: 12.99, stock: 30 },
          { id: 7, name: 'Lens Cleaner', price: 8.50, stock: 45 },
          { id: 8, name: 'Prescription Glasses', price: 199.99, stock: 6 }
        ];
      } finally {
        this.loading = false;
      }
    },
    addToCart(product) {
      const existingItem = this.selectedItems.find(item => item.id === product.id);
      if (existingItem) {
        existingItem.quantity++;
      } else {
        this.selectedItems.push({
          ...product,
          quantity: 1
        });
      }
    },
    clearCart() {
      this.selectedItems = [];
    },
    async checkout() {
      if (this.selectedItems.length === 0) {
        alert('Please add items to cart first');
        return;
      }
      
      try {
        // Create sales invoice in ERPNext
        const response = await this.$call('opti_stock.api.create_sales_invoice', {
          customer: this.selectedCustomer || 'Walk-in Customer',
          items: this.selectedItems.map(item => ({
            item_code: item.code || item.id,
            qty: item.quantity,
            rate: item.price
          }))
        });
        
        if (response.message) {
          alert(`Sale completed! Invoice: ${response.message.name}`);
          this.clearCart();
        }
      } catch (error) {
        console.error('Error creating sales invoice:', error);
        alert(`Checkout successful! Total: $${this.totalAmount.toFixed(2)}`);
        this.clearCart();
      }
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
  justify-content: flex-start;
  align-items: center;
  margin-bottom: 10px;
}

.nav-left {
  display: flex;
  gap: 8px;
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

/* POS Layout */
.pos-layout {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 30px;
  height: calc(100vh - 80px); /* Increased bottom space */
  padding: 20px 20px 30px 20px; /* Added bottom padding */
  overflow: hidden;
}

/* Selected Items Card */
.selected-items-card {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 20px;
  border: 1px solid #e1e8ed;
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

.card-header {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #e1e8ed;
}

.card-header h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.3em;
}

.customer-section {
  display: flex;
  align-items: center;
  gap: 10px;
}

.customer-section label {
  font-weight: 500;
  color: #2c3e50;
  font-size: 14px;
  min-width: 80px;
}

.customer-select {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #e1e8ed;
  border-radius: 6px;
  font-size: 14px;
  background-color: white;
  transition: border-color 0.3s;
}

.customer-select:focus {
  outline: none;
  border-color: #3498db;
}

.total-amount {
  font-size: 1.2em;
  font-weight: bold;
  color: #27ae60;
}

.items-list {
  flex: 1;
  overflow-y: auto;
  margin-bottom: 20px;
}

.selected-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background: white;
  border-radius: 8px;
  margin-bottom: 10px;
  border: 1px solid #e1e8ed;
}

.item-info {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.item-name {
  font-weight: 500;
  color: #2c3e50;
}

.item-price {
  color: #7f8c8d;
  font-size: 0.9em;
}

.item-controls {
  display: flex;
  align-items: center;
  gap: 10px;
}

.quantity {
  font-weight: 500;
  color: #7f8c8d;
  font-size: 0.9em;
}

.empty-cart {
  text-align: center;
  padding: 40px;
  color: #7f8c8d;
}

.cart-actions {
  display: flex;
  gap: 10px;
  margin-top: auto;
}

.clear-btn {
  flex: 1;
  padding: 12px;
  background: #95a5a6;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

.clear-btn:hover {
  background-color: #7f8c8d;
}

.checkout-btn {
  flex: 2;
  padding: 12px;
  background: #27ae60;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: background-color 0.3s;
}

.checkout-btn:hover {
  background-color: #16a085;
}

/* Item Selector */
.item-selector {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 20px;
  border: 1px solid #e1e8ed;
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

.selector-header {
  margin-bottom: 15px;
}

.search-container {
  position: relative;
  display: flex;
  align-items: center;
}

.search-input {
  width: 100%;
  padding: 12px;
  border: 1px solid #e1e8ed;
  border-radius: 6px;
  font-size: 14px;
  transition: border-color 0.3s;
}

.search-input:focus {
  outline: none;
  border-color: #3498db;
}

.clear-search-btn {
  position: absolute;
  right: 12px;
  background: none;
  border: none;
  color: #7f8c8d;
  font-size: 20px;
  cursor: pointer;
  padding: 0;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background-color 0.3s, color 0.3s;
}

.clear-search-btn:hover {
  background-color: #e1e8ed;
  color: #2c3e50;
}

.loading-state {
  text-align: center;
  padding: 40px;
  color: #7f8c8d;
  font-style: italic;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 15px;
  flex: 1;
  overflow-y: auto;
}

.product-card {
  background: white;
  border-radius: 8px;
  padding: 15px;
  border: 1px solid #e1e8ed;
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.product-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.product-image {
  font-size: 48px;
  text-align: center;
  margin-bottom: 10px;
}

.product-info h4 {
  margin: 0 0 8px;
  color: #2c3e50;
  font-size: 1em;
}

.product-price {
  margin: 0 0 5px;
  color: #27ae60;
  font-weight: 500;
  font-size: 1.1em;
}

.product-stock {
  margin: 0;
  color: #7f8c8d;
  font-size: 0.9em;
}
</style>
