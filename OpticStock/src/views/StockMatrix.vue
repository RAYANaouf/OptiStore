<template>
  <div class="stock-matrix-page">
    <div class="matrix-header">
      <div class="header-left">
        <button @click="$router.push('/dashboard')" class="header-btn back-btn">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M19 12H5M12 19l-7-7 7-7"/>
          </svg>
          Back
        </button>
        <h1>Lens Stock Matrix</h1>
      </div>
      <div class="matrix-legend">
        <span class="legend-item">
          <span class="legend-color in-stock"></span> In Stock
        </span>
        <span class="legend-item">
          <span class="legend-color low-stock"></span> Low Stock
        </span>
        <span class="legend-item">
          <span class="legend-color out-stock"></span> Out of Stock
        </span>
      </div>
    </div>

    <!-- Filters Section -->
    <div class="filters-section">
      <div class="filter-group">
        <label>Item Group</label>
        <select v-model="selectedItemGroup" class="filter-select" :disabled="loadingFilters">
          <option value="">{{ loadingFilters ? 'Loading...' : 'All Groups' }}</option>
          <option v-for="group in itemGroups" :key="group" :value="group">
            {{ group }}
          </option>
        </select>
      </div>
      <div class="filter-group">
        <label>Brand</label>
        <select v-model="selectedBrand" class="filter-select" :disabled="loadingFilters">
          <option value="">{{ loadingFilters ? 'Loading...' : 'All Brands' }}</option>
          <option v-for="brand in brands" :key="brand" :value="brand">
            {{ brand }}
          </option>
        </select>
      </div>
      <div class="filter-group">
        <label>Company</label>
        <select v-model="selectedCompany" class="filter-select" :disabled="loadingFilters">
          <option value="">{{ loadingFilters ? 'Loading...' : 'All Companies' }}</option>
          <option v-for="company in companies" :key="company" :value="company">
            {{ company }}
          </option>
        </select>
      </div>
      <div class="filter-group">
        <label>Warehouse</label>
        <select v-model="selectedWarehouse" class="filter-select" :disabled="loadingFilters || !selectedCompany">
          <option value="">{{ loadingFilters ? 'Loading...' : (selectedCompany ? 'All Warehouses' : 'Select Company First') }}</option>
          <option v-for="warehouse in warehouses" :key="warehouse" :value="warehouse">
            {{ warehouse }}
          </option>
        </select>
      </div>
      <div class="filter-group">
        <label>Stock Status</label>
        <select v-model="stockStatusFilter" class="filter-select">
          <option value="all">All Status</option>
          <option value="in">In Stock</option>
          <option value="low">Low Stock</option>
          <option value="out">Out of Stock</option>
        </select>
      </div>
      <button @click="resetFilters" class="reset-btn">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 12"/>
          <path d="M3 3v9h9"/>
        </svg>
        Reset
      </button>
    </div>

    <div class="matrix-container">
      <!-- Matrix Tabs -->
      <div class="matrix-tabs">
        <button
          v-for="tab in ['--', '-+', '++']"
          :key="tab"
          class="matrix-tab"
          :class="{ active: selectedTab === tab }"
          @click="selectedTab = tab"
        >
          <span class="tab-cly">{{ tab[0] }}</span>
          <span class="tab-divider">/</span>
          <span class="tab-sph">{{ tab[1] }}</span>
        </button>
      </div>
      
      <div v-if="loadingItems" class="matrix-loading">
        <div class="loading-spinner"></div>
        <span>Loading items...</span>
      </div>
      <div class="matrix-table-wrapper">
        <table class="matrix-table">
          <thead>
            <tr>
              <th class="corner-cell">
                <div class="corner-label">
                  <span>SPH \ CLY</span>
                </div>
              </th>
              <th v-for="cly in filteredClyValues" :key="cly" class="cly-header">
                {{ formatPowerAbsolute(cly) }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="sph in filteredSphValues" :key="sph">
              <th class="sph-header">{{ formatPowerAbsolute(sph) }}</th>
              <td 
                v-for="cly in filteredClyValues" 
                :key="`${sph}-${cly}`"
                class="stock-cell"
                :class="getStockClass(sph, cly)"
                @click="openStockEditor(sph, cly)"
              >
                {{ getStockQuantity(sph, cly) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Stock Editor Modal -->
    <div v-if="showEditor" class="modal-overlay" @click="closeEditor">
      <div class="modal-container editor-modal" @click.stop>
        <div class="modal-header">
          <h3>Edit Stock</h3>
          <button class="modal-close" @click="closeEditor">&times;</button>
        </div>
        <div class="modal-body">
          <div class="power-display">
            <div class="power-item">
              <label>SPH (Sphere)</label>
              <span class="power-value">{{ formatPower(selectedSph) }}</span>
            </div>
            <div class="power-item">
              <label>CLY (Cylinder)</label>
              <span class="power-value">{{ formatPower(selectedCly) }}</span>
            </div>
          </div>
          <div class="form-group">
            <label>Current Quantity</label>
            <input 
              v-model.number="editQuantity" 
              type="number" 
              class="form-input large"
              min="0"
              autofocus
            />
          </div>
          <div class="quick-actions">
            <button @click="adjustQuantity(-1)" class="quick-btn minus">-1</button>
            <button @click="adjustQuantity(1)" class="quick-btn plus">+1</button>
            <button @click="adjustQuantity(-5)" class="quick-btn minus">-5</button>
            <button @click="adjustQuantity(5)" class="quick-btn plus">+5</button>
            <button @click="adjustQuantity(-10)" class="quick-btn minus">-10</button>
            <button @click="adjustQuantity(10)" class="quick-btn plus">+10</button>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="closeEditor">Cancel</button>
          <button class="btn btn-primary" @click="saveStock">Save</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StockMatrix',
  inject: ['$call'],
  data() {
    return {
      // Generate SPH values: 0.00 to 20.00 in 0.50 steps (reduced for performance)
      sphValues: this.generatePowerValues(0, 20, 0.50),
      // Generate CLY values: 0.00 to 20.00 in 0.50 steps (reduced for performance)
      clyValues: this.generatePowerValues(0, 20, 0.50),
      // Mock stock data - in real app, this comes from backend
      stockData: {},
      // Cache stock data by tab for fast switching
      stockDataByTab: {
        '--': {},
        '-+': {},
        '++': {}
      },
      // Editor modal state
      showEditor: false,
      selectedSph: 0,
      selectedCly: 0,
      editQuantity: 0,
      // Filter states
      selectedItemGroup: '',
      selectedBrand: '',
      selectedCompany: '',
      selectedWarehouse: '',
      stockStatusFilter: 'all',
      // Filter options - loaded from ERPNext
      itemGroups: [],
      brands: [],
      companies: [],
      warehouses: [],
      loadingFilters: false,
      loadingItems: false,
      filteredItems: [],
      // Tab selection for matrix pagination by sign
      selectedTab: '--' // --, -+, ++
    }
  },
  computed: {
    // Pre-cached negative values
    negativeSphValues() {
      return this.generatePowerValues(-0.50, -20, -0.50)
    },
    negativeClyValues() {
      return this.generatePowerValues(-0.50, -20, -0.50)
    },
    // Filtered SPH values based on selected tab
    filteredSphValues() {
      if (this.selectedTab === '++' || this.selectedTab === '+-') {
        // Positive SPH
        return this.sphValues.filter(v => v >= 0)
      } else {
        // Negative SPH (-- and -+)
        return this.sphValues.filter(v => v <= 0).concat(this.negativeSphValues)
      }
    },
    // Filtered CLY values based on selected tab
    filteredClyValues() {
      if (this.selectedTab === '++' || this.selectedTab === '-+') {
        // Positive CLY (includes 0.00)
        return this.clyValues.filter(v => v >= 0)
      } else {
        // Negative CLY (-- and +-) - include 0.00 to get -0.00
        return this.clyValues.filter(v => v >= 0).map(v => -v).concat(this.negativeClyValues)
      }
    }
  },
  watch: {
    // Watch for filter changes and fetch items
    selectedItemGroup(newVal) {
      this.fetchItemsByFilters()
    },
    selectedBrand(newVal) {
      this.fetchItemsByFilters()
    },
    // Watch for company changes - fetch warehouses and refresh items
    selectedCompany(newVal) {
      this.fetchWarehouses()
      this.fetchItemsByFilters()
    },
    // Watch for warehouse changes - refresh items
    selectedWarehouse(newVal) {
      this.fetchItemsByFilters()
    },
    // Watch for tab changes and refresh matrix
    selectedTab(newVal) {
      // Defer to prevent freeze
      requestAnimationFrame(() => {
        this.stockData = this.stockDataByTab[newVal] || {}
      })
    }
  },
  created() {
    // Initialize with some mock data
    this.initializeMockData()
    // Fetch filter options from ERPNext
    this.fetchFilterOptions()
  },
  methods: {
    generatePowerValues(start, end, step) {
      const values = []
      // Handle both positive and negative steps
      if (step > 0) {
        for (let i = start; i <= end; i += step) {
          values.push(Math.round(i * 100) / 100)
        }
      } else {
        for (let i = start; i >= end; i += step) {
          values.push(Math.round(i * 100) / 100)
        }
      }
      return values
    },
    formatPower(value) {
      // Format to 2 decimal places, removing trailing zeros
      const formatted = value.toFixed(2)
      return formatted
    },
    formatPowerAbsolute(value) {
      // Format without sign - show absolute value
      const absValue = Math.abs(value)
      return absValue.toFixed(2)
    },
    initializeMockData() {
      // Create some random stock data for demonstration
      for (let sph of this.sphValues) {
        for (let cly of this.clyValues) {
          const key = `${sph}-${cly}`
          // Random stock between 0 and 50
          const randomStock = Math.floor(Math.random() * 50)
          this.stockData[key] = randomStock
        }
      }
    },
    getStockQuantity(sph, cly) {
      // Use absolute values for key lookup (matrix displays absolute values)
      const absSph = Math.abs(sph).toFixed(2)
      const absCly = Math.abs(cly).toFixed(2)
      const key = `${absSph}-${absCly}`
      return this.stockData[key] || 0
    },
    getStockClass(sph, cly) {
      const quantity = this.getStockQuantity(sph, cly)
      if (quantity === 0) return 'out-stock'
      if (quantity <= 5) return 'low-stock'
      return 'in-stock'
    },
    openStockEditor(sph, cly) {
      this.selectedSph = sph
      this.selectedCly = cly
      this.editQuantity = this.getStockQuantity(sph, cly)
      this.showEditor = true
    },
    closeEditor() {
      this.showEditor = false
    },
    adjustQuantity(delta) {
      this.editQuantity = Math.max(0, this.editQuantity + delta)
    },
    saveStock() {
      // Use absolute values for key (consistent with display)
      const absSph = Math.abs(this.selectedSph).toFixed(2)
      const absCly = Math.abs(this.selectedCly).toFixed(2)
      const key = `${absSph}-${absCly}`
      this.stockData[key] = this.editQuantity
      this.closeEditor()
    },
    resetFilters() {
      this.selectedItemGroup = ''
      this.selectedBrand = ''
      this.selectedCompany = ''
      this.selectedWarehouse = ''
      this.stockStatusFilter = 'all'
      this.filteredItems = []
    },
    async fetchItemsByFilters() {
      // Only fetch if at least one filter is selected
      if (!this.selectedItemGroup && !this.selectedBrand) {
        this.filteredItems = []
        return
      }
      
      this.loadingItems = true
      try {
        const response = await this.$call('opti_stock.api.get_items_by_filters', {
          item_group: this.selectedItemGroup || null,
          brand: this.selectedBrand || null,
          warehouse: this.selectedWarehouse || null,
          company: this.selectedCompany || null
        })

        console.log("fetched items : " , response)
        
        if (response && response.status === 'success') {
          this.filteredItems = response.data || []
          // Update stock data based on fetched items
          this.updateStockFromItems(this.filteredItems)
        }
      } catch (error) {
        console.error('Error fetching items:', error)
      } finally {
        this.loadingItems = false
      }
    },
    parsePowerValues(itemName) {
      // Extract power values from item name
      // Example: "1.56 HMC -2.00 +0.25" -> CLY: -2.00, SPH: +0.25
      // Example: "1.56 HMC +1.50 -0.75" -> SPH: +1.50, CLY: -0.75
      
      if (!itemName) return { sph: null, cly: null }
      
      // Find all signed numbers (with + or -)
      const pattern = /([+-]?\d+\.\d+)/g
      const matches = itemName.match(pattern)
      
      if (!matches || matches.length < 2) return { sph: null, cly: null }
      
      // Get the last two values from the end
      // CLY is usually the first power value, SPH is the second
      const lastTwo = matches.slice(-2)
      
      // Parse and round to nearest 0.25 to handle floating point precision
      const rawCly = lastTwo[0]
      const rawSph = lastTwo[1]
      
      
      return { sph: rawSph, cly: rawCly }
    },
    updateStockFromItems(items) {
      // Reset cache for all tabs
      this.stockDataByTab = {
        '--': {},
        '-+': {},
        '++': {}
      }

      // Process all items once and categorize by tab
      items.forEach(item => {
        const { sph, cly } = this.parsePowerValues(item.item_name)

        if (sph !== null && cly !== null) {
          // Determine signs of SPH and CLY
          const sphSign = sph.includes('+') ? '+' : '-'
          const clySign = cly.includes('+') ? '+' : '-'
          const itemTab = `${clySign}${sphSign}`

          // Only process items for our 3 supported tabs
          if (this.stockDataByTab[itemTab]) {
            // Build key with absolute values (no signs)
            const absSph = sph.replace('+', '').replace('-', '')
            const absCly = cly.replace('+', '').replace('-', '')
            const key = `${absSph}-${absCly}`

            // Add stock quantity to the appropriate tab cache
            this.stockDataByTab[itemTab][key] = (this.stockDataByTab[itemTab][key] || 0) + (item.stock_qty || 0)
          }
        }
      })

      // Set current stockData from cache based on selected tab
      this.stockData = this.stockDataByTab[this.selectedTab] || {}
    },
    getTabLabel(tab) {
      const labels = {
        '++': '+/+',
        '--': '-/-',
        '-+': '-/+',
        '+-': '+/-'
      }
      return labels[tab] || tab
    },
    async fetchFilterOptions() {
      this.loadingFilters = true
      try {
        // Fetch Item Groups
        const groupsResponse = await this.$call('opti_stock.api.get_item_groups')
        console.log('Item Groups Response:', groupsResponse)
        if (groupsResponse && groupsResponse.status === 'success') {
          this.itemGroups = groupsResponse.data || []
        }
        
        // Fetch Brands
        const brandsResponse = await this.$call('opti_stock.api.get_brands')
        if (brandsResponse && brandsResponse.status === 'success') {
          this.brands = brandsResponse.data || []
        }
        
        // Fetch Companies
        const companiesResponse = await this.$call('opti_stock.api.get_companies')
        if (companiesResponse && companiesResponse.status === 'success') {
          this.companies = companiesResponse.data || []
        }
      } catch (error) {
        console.error('Error fetching filter options:', error)
        // Fallback to empty arrays - dropdowns will show "All Groups" / "All Brands" only
      } finally {
        this.loadingFilters = false
      }
    },
    async fetchWarehouses() {
      // Fetch warehouses for selected company
      if (!this.selectedCompany) {
        this.warehouses = []
        this.selectedWarehouse = ''
        return
      }
      
      try {
        const response = await this.$call('opti_stock.api.get_warehouses', {
          company: this.selectedCompany
        })
        if (response && response.status === 'success') {
          this.warehouses = response.data || []
        }
      } catch (error) {
        console.error('Error fetching warehouses:', error)
        this.warehouses = []
      }
    }
  }
}
</script>

<style scoped>
.stock-matrix-page {
  padding: 20px;
  height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e7f1 100%);
  display: flex;
  flex-direction: column;
  gap: 20px;
  box-sizing: border-box;
  overflow: hidden;
}

.matrix-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.matrix-header h1 {
  font-size: 1.8em;
  color: #2c3e50;
  margin: 0;
}

.header-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border: none;
  border-radius: 10px;
  font-size: 0.9em;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.header-btn svg {
  width: 18px;
  height: 18px;
}

.back-btn {
  background: white;
  color: #2c3e50;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.back-btn:hover {
  background: #f8f9fa;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.logout-btn {
  background: #e74c3c;
  color: white;
}

.logout-btn:hover {
  background: #c0392b;
}

.matrix-legend {
  display: flex;
  gap: 20px;
}

/* Filters Section */
.filters-section {
  display: flex;
  gap: 16px;
  align-items: flex-end;
  padding: 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  overflow-x: auto;
  flex-wrap: nowrap;
  flex-shrink: 0;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex: 1;
}

.filter-group label {
  font-size: 0.8em;
  font-weight: 600;
  color: #7f8c8d;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.filter-select,
.filter-input {
  padding: 10px 14px;
  border: 2px solid #e1e8ed;
  border-radius: 8px;
  font-size: 0.95em;
  background: white;
  transition: border-color 0.2s;
}

.filter-select:focus,
.filter-input:focus {
  outline: none;
  border-color: #3498db;
}

.filter-select {
  cursor: pointer;
  min-width: 150px;
}

.filter-select:disabled {
  background: #f8f9fa;
  color: #95a5a6;
  cursor: not-allowed;
}

.filter-input {
  min-width: 200px;
}

.reset-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  background: #ecf0f1;
  color: #2c3e50;
  border: none;
  border-radius: 8px;
  font-size: 0.9em;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  height: fit-content;
}

.reset-btn:hover {
  background: #dfe6e9;
}

.reset-btn svg {
  width: 16px;
  height: 16px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.85em;
  color: #7f8c8d;
}

.legend-color {
  width: 16px;
  height: 16px;
  border-radius: 4px;
}

.legend-color.in-stock {
  background: #27ae60;
}

.legend-color.low-stock {
  background: #f39c12;
}

.legend-color.out-stock {
  background: #e74c3c;
}

/* Matrix Tabs - Small & Square */
.matrix-tabs {
  display: flex;
  gap: 4px;
  padding: 8px 12px;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-bottom: 1px solid #dee2e6;
  justify-content: center;
}

.matrix-tab {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 2px;
  width: 48px;
  height: 32px;
  padding: 0;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  background: white;
  cursor: pointer;
  transition: all 0.15s ease;
  font-size: 0.8em;
  font-weight: 600;
}

.matrix-tab:hover {
  background: #f1f3f5;
}

.matrix-tab.active {
  background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
  color: white;
  border-color: #2980b9;
}

.tab-cly,
.tab-sph {
  font-weight: 600;
  font-size: 0.9em;
}

.tab-divider {
  color: #adb5bd;
  font-size: 0.7em;
}

.matrix-tab.active .tab-divider {
  color: rgba(255, 255, 255, 0.6);
}

.tab-label {
  margin-left: 6px;
  font-size: 0.75em;
  opacity: 0.8;
}

.matrix-container {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  position: relative;
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.matrix-loading {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.95);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  z-index: 100;
}

.matrix-loading span {
  color: #7f8c8d;
  font-size: 0.9em;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e1e8ed;
  border-top-color: #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.matrix-table-wrapper {
  flex: 1;
  overflow: auto;
  min-height: 0;
}

.matrix-table {
  width: 100%;
  min-width: 1200px;
  border-collapse: separate;
  border-spacing: 0;
  font-size: 0.75em;
}

.corner-cell {
  position: sticky;
  top: 0;
  left: 0;
  z-index: 10;
  background: #2c3e50;
  color: white;
  padding: 12px 8px;
  font-size: 0.85em;
  min-width: 70px;
}

.corner-label {
  display: flex;
  flex-direction: column;
  align-items: center;
  line-height: 1.2;
}

.cly-header {
  position: sticky;
  top: 0;
  z-index: 5;
  background: #34495e;
  color: white;
  padding: 10px 4px;
  font-weight: 600;
  min-width: 45px;
  text-align: center;
  font-size: 0.9em;
}

.sph-header {
  position: sticky;
  left: 0;
  z-index: 5;
  background: #34495e;
  color: white;
  padding: 8px 12px;
  font-weight: 600;
  text-align: center;
  min-width: 70px;
}

.stock-cell {
  padding: 8px 4px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid #ecf0f1;
  font-weight: 600;
  min-width: 45px;
}

.stock-cell:hover {
  transform: scale(1.1);
  z-index: 1;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  border-radius: 4px;
}

.stock-cell.in-stock {
  background: #d5f4e6;
  color: #27ae60;
}

.stock-cell.low-stock {
  background: #fef3cd;
  color: #f39c12;
}

.stock-cell.out-stock {
  background: #f8d7da;
  color: #e74c3c;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-container {
  background: white;
  border-radius: 16px;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: modalSlideIn 0.3s ease;
}

.editor-modal {
  max-width: 350px;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #e1e8ed;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.3em;
  color: #2c3e50;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.8em;
  color: #7f8c8d;
  cursor: pointer;
  line-height: 1;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  transition: all 0.2s;
}

.modal-close:hover {
  background: #f0f0f0;
  color: #e74c3c;
}

.modal-body {
  padding: 24px;
}

.modal-footer {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  padding: 16px 24px;
  border-top: 1px solid #e1e8ed;
}

.power-display {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
  padding: 16px;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 12px;
}

.power-item {
  flex: 1;
  text-align: center;
}

.power-item label {
  display: block;
  font-size: 0.75em;
  color: #7f8c8d;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 6px;
}

.power-value {
  font-size: 1.4em;
  font-weight: 700;
  color: #2c3e50;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #2c3e50;
  font-size: 0.9em;
}

.form-input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e1e8ed;
  border-radius: 10px;
  font-size: 1em;
  transition: border-color 0.2s;
  text-align: center;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  border-color: #3498db;
}

.form-input.large {
  font-size: 2em;
  font-weight: 700;
  padding: 16px;
}

.quick-actions {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}

.quick-btn {
  padding: 12px;
  border: none;
  border-radius: 8px;
  font-size: 1em;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.quick-btn.minus {
  background: #ffebee;
  color: #e74c3c;
}

.quick-btn.minus:hover {
  background: #ffcdd2;
}

.quick-btn.plus {
  background: #e8f5e9;
  color: #27ae60;
}

.quick-btn.plus:hover {
  background: #c8e6c9;
}

.btn {
  padding: 12px 24px;
  border-radius: 10px;
  font-size: 0.95em;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.btn-primary {
  background: #3498db;
  color: white;
}

.btn-primary:hover {
  background: #2980b9;
}

.btn-secondary {
  background: #ecf0f1;
  color: #2c3e50;
}

.btn-secondary:hover {
  background: #dfe6e9;
}
</style>
