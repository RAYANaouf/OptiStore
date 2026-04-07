<template>
  <div class="pos-app">
    
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
          <!-- Tabs for multiple clients -->
          <div class="client-tabs">
            <div class="tabs-container">
              <button 
                v-for="(client, index) in clients" 
                :key="index"
                @click="switchClient(index)"
                class="client-tab"
                :class="{ 'active-tab': activeClientIndex === index }"
              >
                <span class="tab-name">{{ client.name || 'Client ' + (index + 1) }}</span>
                <span v-if="clients.length > 1" 
                      @click.stop="removeClient(index)" 
                      class="tab-close">×</span>
              </button>
            </div>
            <button @click="addClient" class="add-tab-btn">+</button>
          </div>
          
          <div class="card-header">
            <div class="dropdowns-section">
              <select 
                v-model="selectedCustomer"
                class="dropdown-select"
              >
                <option value="">Walk-in Customer</option>
                <option v-for="customer in customers" :key="customer.name" :value="customer.name">
                  {{ customer.customer_name }}
                </option>
              </select>
              <select 
                v-model="selectedPriceList"
                class="dropdown-select"
              >
                <option value="">Standard Price</option>
                <option v-for="priceList in priceLists" :key="priceList.name" :value="priceList.name">
                  {{ priceList.price_list_name }}
                </option>
              </select>
            </div>
          </div>
          <div class="items-list">
            <div v-for="(item, index) in selectedItems" :key="index" 
                 class="selected-item" 
                 :class="{ 'active': selectedIndex === index }"
                 @click="selectedIndex = index">
              <span class="item-name">{{ item.name }}</span>
              <span class="item-qty">{{ item.quantity }}</span>
              <span class="item-price">{{ item.price.toFixed(0) }} DA</span>
            </div>
            <div v-if="selectedItems.length === 0" class="empty-cart">
              <p>No items selected</p>
            </div>
          </div>
          <div class="onscreen-keyboard">
            <div class="calculator-grid">
              <button @click="addNumber('1')" class="keyboard-btn num-btn">1</button>
              <button @click="addNumber('2')" class="keyboard-btn num-btn">2</button>
              <button @click="addNumber('3')" class="keyboard-btn num-btn">3</button>
              <button @click="setInputMode('qty')" 
                      class="keyboard-btn mode-btn" 
                      :class="{ 'active-mode': inputMode === 'qty' }">Qty</button>
              
              <button @click="addNumber('4')" class="keyboard-btn num-btn">4</button>
              <button @click="addNumber('5')" class="keyboard-btn num-btn">5</button>
              <button @click="addNumber('6')" class="keyboard-btn num-btn">6</button>
              <button @click="setInputMode('price')" 
                      class="keyboard-btn mode-btn" 
                      :class="{ 'active-mode': inputMode === 'price' }">Price</button>

              <button @click="addNumber('7')" class="keyboard-btn num-btn">7</button>
              <button @click="addNumber('8')" class="keyboard-btn num-btn">8</button>
              <button @click="addNumber('9')" class="keyboard-btn num-btn">9</button>
              <button  class="keyboard-btn ">-</button>

              <button class="keyboard-btn empty-btn">.</button>
              <button @click="addNumber('0')" class="keyboard-btn num-btn ">0</button>
              <button class="keyboard-btn empty-btn" @click="deleteLastNumber">Delete</button>
              <button class="keyboard-btn empty-btn" @click="removeSelectedItem">Remove</button>
              <button @click="checkout" class="keyboard-btn action-btn complete-btn">Complete</button>
              <button @click="printReceipt" class="keyboard-btn action-btn print-btn">Print</button>
            </div>
          </div>
        </div>

        <!-- Right Side - Navigation + Item Selector -->
        <div class="right-panel">
          <!-- Navigation Bar -->
          <div class="pos-nav">
            <div class="nav-left">
              <button @click="toggleTimeline" class="timeline-btn-fixed">
                →
              </button>
            </div>
            <div class="nav-right">
              <button @click="$router.push('/dashboard')" class="back-btn">
                Exit
              </button>
            </div>
          </div>
          
          <!-- Item Selector -->
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
                <div class="product-image">👓</div>
                <div class="product-info">
                  <h4>{{ product.name }}</h4>
                  <p class="product-price">{{ product.price.toFixed(0) }} DA</p>
                </div>
                <div class="product-stock">{{ product.stock }}</div>
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
      // Multiple clients support
      clients: [
        { name: '', items: [], selectedIndex: 0, selectedCustomer: '', selectedPriceList: '' }
      ],
      activeClientIndex: 0,
      // Current client getters (computed from active client)
      searchQuery: '',
      products: [],
      allProducts: [],
      loading: false,
      customers: [],
      priceLists: [],
      numberInput: '',
      inputMode: 'qty'
    }
  },
  computed: {
    // Current client data (computed from active client)
    selectedItems() {
      return this.clients[this.activeClientIndex]?.items || [];
    },
    selectedIndex: {
      get() {
        return this.clients[this.activeClientIndex]?.selectedIndex || 0;
      },
      set(value) {
        this.clients[this.activeClientIndex].selectedIndex = value;
      }
    },
    selectedCustomer: {
      get() {
        return this.clients[this.activeClientIndex]?.selectedCustomer || '';
      },
      set(value) {
        this.clients[this.activeClientIndex].selectedCustomer = value;
        this.clients[this.activeClientIndex].name = value || 'Client ' + (this.activeClientIndex + 1);
      }
    },
    selectedPriceList: {
      get() {
        return this.clients[this.activeClientIndex]?.selectedPriceList || '';
      },
      set(value) {
        this.clients[this.activeClientIndex].selectedPriceList = value;
      }
    },
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
    this.fetchPriceLists();
    // Add keyboard shortcut listener
    window.addEventListener('keydown', this.handleKeyboardShortcut);
  },
  beforeUnmount() {
    window.removeEventListener('keydown', this.handleKeyboardShortcut);
  },
  methods: {
    toggleTimeline() {
      this.isTimelineOpen = !this.isTimelineOpen;
    },
    setInputMode(mode) {
      this.inputMode = mode;
    },
    handleKeyboardShortcut(event) {
      // Ignore if typing in an input field
      if (event.target.tagName === 'INPUT' || event.target.tagName === 'TEXTAREA') {
        return;
      }
      
      const key = event.key.toLowerCase();
      if (key === 'q') {
        this.setInputMode('qty');
      } else if (key === 'p') {
        this.setInputMode('price');
      }
    },
    clearSearch() {
      this.searchQuery = '';
    },
    // On-screen keyboard methods
    navigateUp() {
      if (this.selectedItems.length > 0) {
        this.selectedIndex = Math.max(0, this.selectedIndex - 1);
      }
    },
    navigateDown() {
      if (this.selectedItems.length > 0) {
        this.selectedIndex = Math.min(this.selectedItems.length - 1, this.selectedIndex + 1);
      }
    },
    increaseSelectedQuantity() {
      if (this.selectedItems[this.selectedIndex]) {
        this.selectedItems[this.selectedIndex].quantity++;
      }
    },
    decreaseSelectedQuantity() {
      if (this.selectedItems[this.selectedIndex] && this.selectedItems[this.selectedIndex].quantity > 1) {
        this.selectedItems[this.selectedIndex].quantity--;
      }
    },
    removeSelectedItem() {
      if (this.selectedItems.length > 0) {
        this.selectedItems.splice(this.selectedIndex, 1);
        if (this.selectedIndex >= this.selectedItems.length && this.selectedIndex > 0) {
          this.selectedIndex--;
        }
      }
    },
    // Tab management methods
    addClient() {
      const newIndex = this.clients.length;
      this.clients.push({
        name: 'Client ' + (newIndex + 1),
        items: [],
        selectedIndex: 0,
        selectedCustomer: '',
        selectedPriceList: ''
      });
      this.activeClientIndex = newIndex;
    },
    removeClient(index) {
      if (this.clients.length <= 1) {
        return; // Keep at least one client
      }
      this.clients.splice(index, 1);
      if (this.activeClientIndex >= this.clients.length) {
        this.activeClientIndex = this.clients.length - 1;
      }
    },
    switchClient(index) {
      this.activeClientIndex = index;
    },
    clearCart() {
      this.clients[this.activeClientIndex].items = [];
      this.clients[this.activeClientIndex].selectedIndex = 0;
    },
    // Number input methods
    addNumber(num) {
      if (this.selectedItems.length === 0 || this.selectedIndex >= this.selectedItems.length) {
        return;
      }
      
      const item = this.selectedItems[this.selectedIndex];
      const currentValue = this.inputMode === 'qty' ? item.quantity.toString() : item.price.toString();
      const newValue = currentValue + num;
      
      if (this.inputMode === 'qty') {
        item.quantity = parseInt(newValue) || 1;
      } else {
        item.price = parseFloat(newValue) || 0;
      }
    },
    deleteLastNumber() {
      if (this.selectedItems.length === 0 || this.selectedIndex >= this.selectedItems.length) {
        return;
      }
      
      const item = this.selectedItems[this.selectedIndex];
      
      if (this.inputMode === 'qty') {
        const qtyStr = item.quantity.toString();
        item.quantity = qtyStr.length > 1 ? parseInt(qtyStr.slice(0, -1)) : 1;
      } else {
        const priceStr = item.price.toString();
        item.price = priceStr.length > 1 ? parseFloat(priceStr.slice(0, -1)) : 0;
      }
    },
    clearNumberInput() {
      this.numberInput = '';
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
    async fetchPriceLists() {
      try {
        const response = await this.$call('opti_stock.api.get_price_lists');
        if (response && response.data) {
          this.priceLists = response.data;
        }
      } catch (error) {
        console.error('Error fetching price lists:', error);
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
      const items = this.clients[this.activeClientIndex].items;
      const existingItem = items.find(item => item.id === product.id);
      if (existingItem) {
        existingItem.quantity++;
      } else {
        items.push({
          ...product,
          quantity: 1
        });
      }
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
        alert(`Checkout successful! Total: ${this.totalAmount.toFixed(0)} DA`);
        this.clearCart();
      }
    },
    printReceipt() {
      if (this.selectedItems.length === 0) {
        alert('No items to print');
        return;
      }
      
      // Generate receipt content
      const receiptContent = `
        <div style="font-family: monospace; padding: 20px; max-width: 300px;">
          <h2 style="text-align: center;">Receipt</h2>
          <hr>
          ${this.selectedItems.map(item => `
            <div style="display: flex; justify-content: space-between; margin: 10px 0;">
              <span>${item.name} x${item.quantity}</span>
              <span>${(item.price * item.quantity).toFixed(0)} DA</span>
            </div>
          `).join('')}
          <hr>
          <div style="display: flex; justify-content: space-between; font-weight: bold; margin-top: 10px;">
            <span>Total:</span>
            <span>${this.totalAmount.toFixed(0)} DA</span>
          </div>
          <p style="text-align: center; margin-top: 20px;">Thank you!</p>
        </div>
      `;
      
      // Open print window
      const printWindow = window.open('', '_blank');
      printWindow.document.write(`
        <html>
          <head><title>Receipt</title></head>
          <body>${receiptContent}</body>
        </html>
      `);
      printWindow.document.close();
      printWindow.print();
    }
  }
}
</script>

<style scoped>
.pos-app {
  padding: 30px;
  min-height: 100vh;
  background: 
    radial-gradient(circle at 20% 30%, rgba(39, 174, 96, 0.15) 0%, transparent 50%),
    radial-gradient(circle at 80% 70%, rgba(39, 174, 96, 0.1) 0%, transparent 40%),
    radial-gradient(circle at 50% 50%, rgba(39, 174, 96, 0.05) 0%, transparent 60%),
    radial-gradient(circle at 10% 80%, rgba(39, 174, 96, 0.08) 0%, transparent 35%),
    radial-gradient(circle at 90% 20%, rgba(39, 174, 96, 0.12) 0%, transparent 45%),
    linear-gradient(135deg, #f5f7fa 0%, #e4e7f1 100%);
  position: relative;
}

.pos-content{
  position: relative;
  z-index: 1;
}

.pos-nav{
  position: relative;
  z-index: 1;
}

.pos-app::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    /* Large flowing waves */
    radial-gradient(ellipse 80% 40% at 50% 100%, rgba(39, 174, 96, 0.4) 0%, transparent 70%),
    radial-gradient(ellipse 60% 30% at 20% 0%, rgba(39, 174, 96, 0.3) 0%, transparent 60%),
    radial-gradient(ellipse 70% 35% at 80% 50%, rgba(39, 174, 96, 0.25) 0%, transparent 65%),
    radial-gradient(ellipse 50% 25% at 30% 80%, rgba(39, 174, 96, 0.35) 0%, transparent 55%),
    /* Stars - many more added */
    radial-gradient(circle at 5% 10%, rgba(39, 174, 96, 1) 0%, rgba(39, 174, 96, 0.3) 3px, transparent 6px),
    radial-gradient(circle at 15% 5%, rgba(39, 174, 96, 1) 0%, rgba(39, 174, 96, 0.3) 4px, transparent 8px),
    radial-gradient(circle at 25% 15%, rgba(39, 174, 96, 1) 0%, rgba(39, 174, 96, 0.3) 3px, transparent 6px),
    radial-gradient(circle at 35% 8%, rgba(39, 174, 96, 1) 0%, rgba(39, 174, 96, 0.3) 5px, transparent 10px),
    radial-gradient(circle at 45% 20%, rgba(39, 174, 96, 1) 0%, rgba(39, 174, 96, 0.3) 3px, transparent 6px),
    radial-gradient(circle at 55% 5%, rgba(39, 174, 96, 1) 0%, rgba(39, 174, 96, 0.3) 4px, transparent 8px),
    radial-gradient(circle at 65% 18%, rgba(39, 174, 96, 1) 0%, rgba(39, 174, 96, 0.3) 3px, transparent 6px),
    radial-gradient(circle at 75% 12%, rgba(39, 174, 96, 1) 0%, rgba(39, 174, 96, 0.3) 5px, transparent 10px),
    radial-gradient(circle at 85% 25%, rgba(39, 174, 96, 1) 0%, rgba(39, 174, 96, 0.3) 3px, transparent 6px),
    radial-gradient(circle at 95% 8%, rgba(39, 174, 96, 1) 0%, rgba(39, 174, 96, 0.3) 4px, transparent 8px),
    radial-gradient(circle at 10% 30%, rgba(39, 174, 96, 1) 0%, rgba(39, 174, 96, 0.3) 4px, transparent 8px),
    radial-gradient(circle at 20% 45%, rgba(39, 174, 96, 1) 0%, rgba(39, 174, 96, 0.3) 3px, transparent 6px),
    radial-gradient(circle at 30% 35%, rgba(39, 174, 96, 1) 0%, rgba(39, 174, 96, 0.3) 5px, transparent 10px),
    radial-gradient(circle at 40% 50%, rgba(39, 174, 96, 1) 0%, rgba(39, 174, 96, 0.3) 3px, transparent 6px),
    radial-gradient(circle at 50% 40%, rgba(39, 174, 96, 1) 0%, rgba(39, 174, 96, 0.3) 4px, transparent 8px),
    radial-gradient(circle at 60% 55%, rgba(39, 174, 96, 1) 0%, rgba(39, 174, 96, 0.3) 3px, transparent 6px),
    radial-gradient(circle at 70% 45%, rgba(39, 174, 96, 1) 0%, rgba(39, 174, 96, 0.3) 5px, transparent 10px),
    radial-gradient(circle at 80% 60%, rgba(39, 174, 96, 1) 0%, rgba(39, 174, 96, 0.3) 3px, transparent 6px),
    radial-gradient(circle at 90% 50%, rgba(39, 174, 96, 1) 0%, rgba(39, 174, 96, 0.3) 4px, transparent 8px),
    radial-gradient(circle at 5% 70%, rgba(39, 174, 96, 1) 0%, rgba(39, 174, 96, 0.3) 5px, transparent 10px),
    radial-gradient(circle at 15% 85%, rgba(39, 174, 96, 1) 0%, rgba(39, 174, 96, 0.3) 3px, transparent 6px),
    radial-gradient(circle at 25% 75%, rgba(39, 174, 96, 1) 0%, rgba(39, 174, 96, 0.3) 4px, transparent 8px),
    radial-gradient(circle at 35% 90%, rgba(39, 174, 96, 1) 0%, rgba(39, 174, 96, 0.3) 3px, transparent 6px),
    radial-gradient(circle at 45% 80%, rgba(39, 174, 96, 1) 0%, rgba(39, 174, 96, 0.3) 5px, transparent 10px),
    radial-gradient(circle at 55% 95%, rgba(39, 174, 96, 1) 0%, rgba(39, 174, 96, 0.3) 3px, transparent 6px),
    radial-gradient(circle at 65% 85%, rgba(39, 174, 96, 1) 0%, rgba(39, 174, 96, 0.3) 4px, transparent 8px),
    radial-gradient(circle at 75% 95%, rgba(39, 174, 96, 1) 0%, rgba(39, 174, 96, 0.3) 3px, transparent 6px),
    radial-gradient(circle at 85% 75%, rgba(39, 174, 96, 1) 0%, rgba(39, 174, 96, 0.3) 5px, transparent 10px),
    radial-gradient(circle at 95% 90%, rgba(39, 174, 96, 1) 0%, rgba(39, 174, 96, 0.3) 3px, transparent 6px),
    radial-gradient(circle at 12% 55%, rgba(39, 174, 96, 1) 0%, rgba(39, 174, 96, 0.3) 4px, transparent 8px),
    radial-gradient(circle at 28% 65%, rgba(39, 174, 96, 1) 0%, rgba(39, 174, 96, 0.3) 3px, transparent 6px),
    radial-gradient(circle at 42% 70%, rgba(39, 174, 96, 1) 0%, rgba(39, 174, 96, 0.3) 5px, transparent 10px),
    radial-gradient(circle at 58% 75%, rgba(39, 174, 96, 1) 0%, rgba(39, 174, 96, 0.3) 3px, transparent 6px),
    radial-gradient(circle at 72% 30%, rgba(39, 174, 96, 1) 0%, rgba(39, 174, 96, 0.3) 4px, transparent 8px),
    radial-gradient(circle at 88% 40%, rgba(39, 174, 96, 1) 0%, rgba(39, 174, 96, 0.3) 3px, transparent 6px),
    radial-gradient(circle at 8% 95%, rgba(39, 174, 96, 1) 0%, rgba(39, 174, 96, 0.3) 5px, transparent 10px),
    radial-gradient(circle at 38% 25%, rgba(39, 174, 96, 1) 0%, rgba(39, 174, 96, 0.3) 3px, transparent 6px),
    radial-gradient(circle at 68% 78%, rgba(39, 174, 96, 1) 0%, rgba(39, 174, 96, 0.3) 4px, transparent 8px),
    radial-gradient(circle at 92% 65%, rgba(39, 174, 96, 1) 0%, rgba(39, 174, 96, 0.3) 3px, transparent 6px),
    radial-gradient(circle at 48% 92%, rgba(39, 174, 96, 1) 0%, rgba(39, 174, 96, 0.3) 5px, transparent 10px);
  pointer-events: none;
  z-index: 0;
  animation: galaxyPulse 4s ease-in-out infinite;
}

.pos-app::after {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    /* Additional wave layers for depth */
    radial-gradient(ellipse 100% 50% at 0% 50%, rgba(39, 174, 96, 0.15) 0%, transparent 50%),
    radial-gradient(ellipse 100% 50% at 100% 30%, rgba(39, 174, 96, 0.12) 0%, transparent 45%);
  pointer-events: none;
  z-index: 0;
  animation: waveFlow 10s ease-in-out infinite;
  filter: blur(20px);
}

@keyframes galaxyPulse {
  0%, 100% { 
    opacity: 1;
    transform: scale(1);
  }
  50% { 
    opacity: 0.85;
    transform: scale(1.02);
  }
}

@keyframes waveFlow {
  0%, 100% { 
    transform: translateX(-30px) scale(1);
    opacity: 0.6;
  }
  33% { 
    transform: translateX(20px) scale(1.1);
    opacity: 0.9;
  }
  66% { 
    transform: translateX(-10px) scale(0.95);
    opacity: 0.7;
  }
}

.pos-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-left {
  display: flex;
  gap: 8px;
  align-items: center;
}

.nav-right {
  display: flex;
  gap: 8px;
  align-items: center;
}

.timeline-btn-fixed {
  position: relative;
  top: 0;
  left: 0;
  width: 30px;
  height: 40px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 18px;
  z-index: 999;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  transition: background-color 0.3s;
}

.timeline-btn-fixed:hover {
  background: #2980b9;
}

.back-btn {
  padding: 15px 15px;
  background-color: white;
  color: #27ae60;
  border: 1px solid #27ae60;
  border-radius: 12px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

.back-btn:hover {
  background-color: #f0f0f0;
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
  height: calc(100vh - 40px);
  padding: 10px 20px 20px 20px;
  overflow: hidden;
}

/* Right Panel */
.right-panel {
  display: flex;
  flex-direction: column;
  gap: 15px;
  height: 100%;
  overflow: hidden;
}

/* Selected Items Card */
.selected-items-card {
  background: white;
  border-radius: 12px;
  border: 1px solid #e1e8ed;
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

/* Client Tabs */
.client-tabs {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 10px 15px 0;
  border-bottom: 1px solid #e1e8ed;
  background: #f8f9fa;
}

.tabs-container {
  display: flex;
  gap: 5px;
  flex: 1;
  overflow-x: auto;
}

.client-tab {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 15px;
  background: white;
  border: 1px solid #e1e8ed;
  border-bottom: none;
  border-radius: 8px 8px 0 0;
  cursor: pointer;
  font-size: 14px;
  white-space: nowrap;
  transition: all 0.2s;
}

.client-tab:hover {
  background: #f0f0f0;
}

.active-tab {
  background: white;
  border-color: #3498db;
  border-bottom: 2px solid #3498db;
  color: #3498db;
  font-weight: 600;
}

.tab-name {
  max-width: 100px;
  overflow: hidden;
  text-overflow: ellipsis;
}

.tab-close {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  font-size: 14px;
  color: #999;
  transition: all 0.2s;
}

.tab-close:hover {
  background: #e74c3c;
  color: white;
}

.add-tab-btn {
  width: 30px;
  height: 30px;
  background: #27ae60;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}

.add-tab-btn:hover {
  background: #229954;
}

.card-header {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 20px;
  padding: 20px 20px 15px 20px;
  border-bottom: 1px solid #e1e8ed;
}

.card-header h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.3em;
}

.dropdowns-section {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}

.dropdown-select {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #e1e8ed;
  border-radius: 6px;
  font-size: 14px;
  background-color: white;
  transition: border-color 0.3s;
}

.dropdown-select:focus {
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
}

.selected-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 15px;
  background: white;
  transition: all 0.3s ease;
  gap: 10px;
  cursor: pointer;
  border: 1px solid transparent;
}

.selected-item:hover {
  background: #f0f9f6;
  border-color: #27ae60;
}

.selected-item.active {
  border-color: #44A292;
  box-shadow: 0 0 0 2px rgba(68, 162, 146, 0.2);
}

.item-name {
  font-weight: 500;
  color: #2c3e50;
  flex: 1;
}

.item-qty {
  color: #7f8c8d;
  font-size: 0.9em;
  width: 50px;
  text-align: center;
}

.item-price {
  color: #2c3e50;
  font-weight: 600;
  font-size: 0.9em;
  width: 100px;
  text-align: right;
}

.selected-indicator {
  color: #44A292;
  font-weight: bold;
  font-size: 16px;
}

.onscreen-keyboard {
  background: #f8f9fa;
  border-radius: 0;
  border: 1px solid #e1e8ed;
}


.calculator-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0;
  width: 100%;
}

.keyboard-btn {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 0;
  padding: 15px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s;
  min-width: 60px;
  color: #2c3e50;
}

.keyboard-btn:hover {
  background: #f5f5f5;
}

.keyboard-btn:active {
  background: #e0e0e0;
}

.nav-btn {
  background: #3498db;
  color: white;
  border-color: #3498db;
}

.nav-btn:hover {
  background: #2980b9;
  border-color: #2980b9;
}


.remove-btn {
  background: #e74c3c;
  color: white;
  border-color: #e74c3c;
}

.remove-btn:hover {
  background: #c0392b;
  border-color: #c0392b;
}



.keyboard-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.keyboard-btn:disabled:hover {
  background: white;
  transform: none;
  box-shadow: none;
}

.num-btn {
  background: white;
  color: #2c3e50;
  border-color: #e5e7eb;
}

.num-btn:hover {
  background: #f5f5f5;
  border-color: #e5e7eb;
}

.clear-btn {
  background: white;
  color: #2c3e50;
  border-color: #e5e7eb;
}

.clear-btn:hover {
  background: #f5f5f5;
  border-color: #e5e7eb;
}

.apply-btn {
  background: white;
  color: #2c3e50;
  border-color: #e5e7eb;
}

.apply-btn:hover {
  background: #f5f5f5;
  border-color: #e5e7eb;
}

.empty-btn {
  background: white;
  border: 1px solid #e5e7eb;
  cursor: default;
}

.empty-btn:hover {
  background: white;
}

.mode-btn {
  background: white;
  color: #2c3e50;
  border-color: #e5e7eb;
  transition: all 0.2s;
}

.mode-btn:hover {
  background: #f5f5f5;
  border-color: #3498db;
}

.active-mode {
  background: #3498db !important;
  color: white !important;
  border-color: #3498db !important;
}

.action-btn {
  grid-column: span 2;
  font-weight: bold;
}

.complete-btn {
  background: #27ae60;
  color: white;
  border-color: #27ae60;
}

.complete-btn:hover {
  background: #229954;
  border-color: #229954;
}

.print-btn {
  background: #E1472B;
  color: white;
  border-color: #E1472B;
}

.print-btn:hover {
  background: #c73d24;
  border-color: #c73d24;
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





/* Item Selector */
.item-selector {
  background: white;
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
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 10px;
  overflow-y: auto;
  max-height: 100%;
  align-content: start;
}

.product-card {
  background: white;
  border-radius: 8px;
  padding: 12px;
  border: 1px solid #e1e8ed;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
  position: relative;
}

.product-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.product-image {
  font-size: 36px;
  text-align: center;
  margin-bottom: 8px;
}

.product-info h4 {
  margin: 0 0 8px;
  color: #2c3e50;
  font-size: 1em;
}

.product-price {
  margin: 0 0 5px;
  color: white;
  font-weight: bold;
  font-size: 0.9em;
  position: absolute;
  top: 0;
  right: 0;
  background: #44A292;
  padding: 2px 6px;
  border-bottom-left-radius: 8px;
  border-top-right-radius: 8px;
}

.product-stock {
  margin: 0;
  color: white;
  font-weight: bold;
  font-size: 0.9em;
  position: absolute;
  top: 0;
  left: 0;
  background: #3498db;
  padding: 2px 6px;
  border-top-left-radius: 8px;
  border-bottom-right-radius: 8px;
}
</style>
