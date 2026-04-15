<template>
  <div class="stock-matrix-page">
    <aside class="sidebar">
      <div class="sidebar-header">
        <div class="header-title-row">
          <button @click="$router.push('/dashboard')" class="sidebar-back-btn">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M19 12H5M12 19l-7-7 7-7"/>
            </svg>
            Back
          </button>
          <h2>OptiStock</h2>
        </div>
      </div>
      <div class="companies-filter">
        <div class="filter-header" @click="toggleCompanies">
          <div class="header-content">
            <h3>Filter by Companies</h3>
            <div class="selection-count">{{ selectedCompanies.length }} of {{ companies.length }} selected</div>
          </div>
          <svg class="collapse-arrow" :class="{ 'rotated': !companiesOpen }" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M6 9l6 6 6-6"/>
          </svg>
        </div>
        <div class="companies-list" v-show="companiesOpen">
          <label class="company-item all-option">
            <input 
              type="checkbox" 
              v-model="selectAllCompaniesChecked"
              @change="toggleAllCompanies"
            />
            <span class="checkmark"></span>
            <span class="company-name">ALL</span>
          </label>
          <label v-for="company in companies" :key="company" class="company-item">
            <input 
              type="checkbox" 
              :value="company" 
              v-model="selectedCompanies"
              @change="onCompaniesChange"
            />
            <span class="checkmark"></span>
            <span class="company-name">{{ company }}</span>
          </label>
        </div>
      </div>
      
      <div class="warehouses-filter" v-if="selectedCompanies.length > 0">
        <div class="filter-header" @click="toggleWarehouses">
          <div class="header-content">
            <h3>Filter by Warehouses</h3>
            <div class="selection-count">{{ selectedWarehouses.length }} of {{ warehouses.length }} selected</div>
          </div>
          <svg class="collapse-arrow" :class="{ 'rotated': !warehousesOpen }" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M6 9l6 6 6-6"/>
          </svg>
        </div>
        <div class="warehouses-list" v-show="warehousesOpen">
          <label class="warehouse-item all-option">
            <input 
              type="checkbox" 
              v-model="selectAllWarehousesChecked"
              @change="toggleAllWarehouses"
            />
            <span class="checkmark"></span>
            <span class="warehouse-name">ALL</span>
          </label>
          <label v-for="warehouse in warehouses" :key="warehouse" class="warehouse-item">
            <input 
              type="checkbox" 
              :value="warehouse" 
              v-model="selectedWarehouses"
              @change="onWarehousesChange"
            />
            <span class="checkmark"></span>
            <span class="warehouse-name">{{ warehouse }}</span>
          </label>
        </div>
      </div>
      
      <div class="item-group-filter">
        <div class="filter-header" @click="toggleItemGroups">
          <div class="header-content">
            <h3>Item Group</h3>
            <div class="selection-count">{{ selectedItemGroups.length }} of {{ itemGroups.length }} selected</div>
          </div>
          <svg class="collapse-arrow" :class="{ 'rotated': !itemGroupsOpen }" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M6 9l6 6 6-6"/>
          </svg>
        </div>
        <div class="item-groups-list" v-show="itemGroupsOpen">
          <label class="item-group-item all-option">
            <input 
              type="checkbox" 
              v-model="selectAllItemGroupsChecked"
              @change="toggleAllItemGroups"
            />
            <span class="checkmark"></span>
            <span class="item-group-name">ALL</span>
          </label>
          <label v-for="group in itemGroups" :key="group" class="item-group-item">
            <input 
              type="checkbox" 
              :value="group" 
              v-model="selectedItemGroups"
              @change="onItemGroupsChange"
            />
            <span class="checkmark"></span>
            <span class="item-group-name">{{ group }}</span>
          </label>
        </div>
      </div>
      
      <div class="brand-filter">
        <div class="filter-header" @click="toggleBrands">
          <div class="header-content">
            <h3>Brand</h3>
            <div class="selection-count">{{ selectedBrands.length }} of {{ brands.length }} selected</div>
          </div>
          <svg class="collapse-arrow" :class="{ 'rotated': !brandsOpen }" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M6 9l6 6 6-6"/>
          </svg>
        </div>
        <div class="brands-list" v-show="brandsOpen">
          <label class="brand-item all-option">
            <input 
              type="checkbox" 
              v-model="selectAllBrandsChecked"
              @change="toggleAllBrands"
            />
            <span class="checkmark"></span>
            <span class="brand-item-name">ALL</span>
          </label>
          <label v-for="brand in brands" :key="brand" class="brand-item">
            <input 
              type="checkbox" 
              :value="brand" 
              v-model="selectedBrands"
              @change="onBrandsChange"
            />
            <span class="checkmark"></span>
            <span class="brand-item-name">{{ brand }}</span>
          </label>
        </div>
      </div>
    </aside>
    
    <main class="main-content">
      
    <!-- Filters Section -->
    <div class="filters-section">
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
      <!-- Matrix Header Row with Tabs and Legend -->
      <div class="matrix-header-row">
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
        
        <!-- Matrix Legend -->
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
    </main>
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
      selectedItemGroups: [],
      selectedBrands: [],
      selectedCompanies: [],
      selectedWarehouses: [],
      stockStatusFilter: 'all',
      // Select all checkbox states
      selectAllCompaniesChecked: false,
      selectAllWarehousesChecked: false,
      selectAllItemGroupsChecked: false,
      selectAllBrandsChecked: false,
      // Collapse states - default closed
      companiesOpen: false,
      warehousesOpen: false,
      itemGroupsOpen: false,
      brandsOpen: false,
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
    // Watch for companies changes - fetch warehouses and refresh items
    selectedCompanies: {
      handler(newVal) {
        this.fetchWarehouses()
        this.fetchItemsByFilters()
      },
      deep: true
    },
    // Watch for item groups changes - refresh items
    selectedItemGroups: {
      handler(newVal) {
        this.fetchItemsByFilters()
      },
      deep: true
    },
    // Watch for brands changes - refresh items
    selectedBrands: {
      handler(newVal) {
        this.fetchItemsByFilters()
      },
      deep: true
    },
    // Watch for warehouses changes - refresh items
    selectedWarehouses: {
      handler(newVal) {
        this.fetchItemsByFilters()
      },
      deep: true
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
          item_groups: this.selectedItemGroups.length > 0 ? this.selectedItemGroups : null,
          brands: this.selectedBrands.length > 0 ? this.selectedBrands : null,
          warehouses: this.selectedWarehouses.length > 0 ? this.selectedWarehouses : null,
          companies: this.selectedCompanies.length > 0 ? this.selectedCompanies : null
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
    toggleAllCompanies() {
      if (this.selectAllCompaniesChecked) {
        this.selectedCompanies = [...this.companies]
      } else {
        this.selectedCompanies = []
      }
    },
    onCompaniesChange() {
      // Update the "ALL" checkbox state based on individual selections
      this.selectAllCompaniesChecked = this.selectedCompanies.length === this.companies.length && this.companies.length > 0
    },
    toggleAllWarehouses() {
      if (this.selectAllWarehousesChecked) {
        this.selectedWarehouses = [...this.warehouses]
      } else {
        this.selectedWarehouses = []
      }
      console.log('Warehouse selection changed:', this.selectedWarehouses)
    },
    onWarehousesChange() {
      // Update the "ALL" checkbox state based on individual selections
      this.selectAllWarehousesChecked = this.selectedWarehouses.length === this.warehouses.length && this.warehouses.length > 0
      console.log('Warehouse selection changed:', this.selectedWarehouses)
    },
    toggleAllItemGroups() {
      if (this.selectAllItemGroupsChecked) {
        this.selectedItemGroups = [...this.itemGroups]
      } else {
        this.selectedItemGroups = []
      }
      console.log('Item groups selection changed:', this.selectedItemGroups)
    },
    onItemGroupsChange() {
      // Update the "ALL" checkbox state based on individual selections
      this.selectAllItemGroupsChecked = this.selectedItemGroups.length === this.itemGroups.length && this.itemGroups.length > 0
      console.log('Item groups selection changed:', this.selectedItemGroups)
    },
    toggleAllBrands() {
      if (this.selectAllBrandsChecked) {
        this.selectedBrands = [...this.brands]
      } else {
        this.selectedBrands = []
      }
      console.log('Brands selection changed:', this.selectedBrands)
    },
    onBrandsChange() {
      // Update the "ALL" checkbox state based on individual selections
      this.selectAllBrandsChecked = this.selectedBrands.length === this.brands.length && this.brands.length > 0
      console.log('Brands selection changed:', this.selectedBrands)
    },
    // Toggle methods for collapsible sections
    toggleCompanies() {
      this.companiesOpen = !this.companiesOpen
    },
    toggleWarehouses() {
      this.warehousesOpen = !this.warehousesOpen
    },
    toggleItemGroups() {
      this.itemGroupsOpen = !this.itemGroupsOpen
    },
    toggleBrands() {
      this.brandsOpen = !this.brandsOpen
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
      // Fetch warehouses for selected companies
      if (this.selectedCompanies.length === 0) {
        this.warehouses = []
        this.selectedWarehouses = []
        console.log('No companies selected, clearing warehouses')
        return
      }
      
      try {
        // Get warehouses for all selected companies
        const allWarehouses = new Set()
        
        console.log('Fetching warehouses for companies:', this.selectedCompanies)
        for (const company of this.selectedCompanies) {
          const response = await this.$call('opti_stock.api.get_warehouses', {
            company: company
          })
          if (response && response.status === 'success') {
            console.log(`Warehouses for ${company}:`, response.data)
            response.data?.forEach(warehouse => allWarehouses.add(warehouse))
          }
        }
        
        this.warehouses = Array.from(allWarehouses).sort()
        console.log('Final warehouses list:', this.warehouses)
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
  display: flex;
  height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e7f1 100%);
  overflow: hidden;
}

/* Sidebar */
.sidebar {
  width: 280px;
  background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
  color: white;
  display: flex;
  flex-direction: column;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
  max-height: 100vh;
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.header-title-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.sidebar-header h2 {
  margin: 0;
  font-size: 1.4em;
  font-weight: 600;
  color: white;
}

.sidebar-back-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.9em;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.sidebar-back-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
  color: white;
  transform: translateY(-1px);
}

.sidebar-back-btn svg {
  width: 16px;
  height: 16px;
  transition: transform 0.2s ease;
}

.sidebar-back-btn:hover svg {
  transform: translateX(-2px);
}

/* Companies Filter */
.companies-filter {
  display: flex;
  flex-direction: column;
  padding: 0 16px 8px 16px;
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  cursor: pointer;
  border-radius: 8px;
  transition: background-color 0.2s ease;
  margin-bottom: 8px;
}

.filter-header:hover {
  background: rgba(255, 255, 255, 0.05);
}

.header-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
}

.filter-header h3 {
  margin: 0;
  font-size: 1em;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.8);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.selection-count {
  font-size: 0.75em;
  color: rgba(255, 255, 255, 0.6);
  font-weight: 400;
}

.collapse-arrow {
  width: 16px;
  height: 16px;
  color: rgba(255, 255, 255, 0.6);
  transition: transform 0.3s ease;
  flex-shrink: 0;
}

.collapse-arrow.rotated {
  transform: rotate(-90deg);
}

.item-group-filter,
.brand-filter {
  display: flex;
  flex-direction: column;
  padding: 0 16px 8px 16px;
}

.sidebar-select {
  width: 100%;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 10px;
  color: rgba(255, 255, 255, 0.95);
  font-size: 0.9em;
  font-weight: 500;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='rgba(255,255,255,0.6)' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6,9 12,15 18,9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 12px center;
  background-size: 16px;
  padding-right: 40px;
}

.sidebar-select:hover {
  background: rgba(255, 255, 255, 0.12);
  border-color: rgba(255, 255, 255, 0.25);
}

.sidebar-select:focus {
  outline: none;
  border-color: rgba(255, 255, 255, 0.4);
  background: rgba(255, 255, 255, 0.15);
  box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.1);
}

.sidebar-select option {
  background: #2c3e50;
  color: white;
  padding: 10px;
}

.filter-actions {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}

.action-btn {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.85em;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.action-btn.select-all {
  background: rgba(52, 152, 219, 0.2);
  border-color: #3498db;
}

.action-btn.clear-all {
  background: rgba(231, 76, 60, 0.2);
  border-color: #e74c3c;
}

.companies-list {
  flex: 1;
  overflow-y: auto;
  max-height: 400px;
}

.company-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.2s ease;
}

.company-item.all-option {
  font-weight: 600;
  background: rgba(52, 152, 219, 0.1);
  border: 1px solid rgba(52, 152, 219, 0.2);
  margin-bottom: 4px;
}

.company-item.all-option:hover {
  background: rgba(52, 152, 219, 0.2);
}

.company-item:hover {
  background: rgba(255, 255, 255, 0.1);
}

.company-item input[type="checkbox"] {
  display: none;
}

.checkmark {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 3px;
  position: relative;
  transition: all 0.2s ease;
}

.company-item input[type="checkbox"]:checked + .checkmark,
.warehouse-item input[type="checkbox"]:checked + .checkmark {
  background: #3498db;
  border-color: #3498db;
}

.company-item input[type="checkbox"]:checked + .checkmark::after,
.warehouse-item input[type="checkbox"]:checked + .checkmark::after {
  content: '';
  position: absolute;
  left: 3px;
  top: 0px;
  width: 5px;
  height: 9px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.company-name {
  flex: 1;
  font-size: 0.9em;
  color: rgba(255, 255, 255, 0.9);
}

.selected-count {
  padding: 12px;
  text-align: center;
  font-size: 0.8em;
  color: rgba(255, 255, 255, 0.6);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  margin-top: auto;
}

/* Item Groups Filter */
.item-groups-list {
  flex: 1;
}

.brands-list {
  flex: 1;
  overflow-y: auto;
  max-height: 200px;
}

.item-group-item,
.brand-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.2s ease;
}

.item-group-item.all-option,
.brand-item.all-option {
  font-weight: 600;
  background: rgba(52, 152, 219, 0.1);
  border: 1px solid rgba(52, 152, 219, 0.2);
  margin-bottom: 4px;
}

.item-group-item.all-option:hover,
.brand-item.all-option:hover {
  background: rgba(52, 152, 219, 0.2);
}

.item-group-item:hover,
.brand-item:hover {
  background: rgba(255, 255, 255, 0.1);
}

.item-group-item input[type="checkbox"],
.brand-item input[type="checkbox"] {
  display: none;
}

.item-group-item input[type="checkbox"]:checked + .checkmark,
.brand-item input[type="checkbox"]:checked + .checkmark {
  background: #3498db;
  border-color: #3498db;
}

.item-group-item input[type="checkbox"]:checked + .checkmark::after,
.brand-item input[type="checkbox"]:checked + .checkmark::after {
  content: '';
  position: absolute;
  left: 3px;
  top: 0px;
  width: 5px;
  height: 9px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.item-group-name,
.brand-item-name {
  flex: 1;
  font-size: 0.9em;
  color: rgba(255, 255, 255, 0.9);
}

/* Warehouses Filter */
.warehouses-filter {
  display: flex;
  flex-direction: column;
  padding: 0 16px 8px 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.warehouses-list {
  flex: 1;
}

.warehouse-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.2s ease;
}

.warehouse-item.all-option {
  font-weight: 600;
  background: rgba(52, 152, 219, 0.1);
  border: 1px solid rgba(52, 152, 219, 0.2);
  margin-bottom: 4px;
}

.warehouse-item.all-option:hover {
  background: rgba(52, 152, 219, 0.2);
}

.warehouse-item:hover {
  background: rgba(255, 255, 255, 0.1);
}

.warehouse-item input[type="checkbox"] {
  display: none;
}

.warehouse-name {
  flex: 1;
  font-size: 0.9em;
  color: rgba(255, 255, 255, 0.9);
}

/* Main Content */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 20px;
  gap: 20px;
  overflow: hidden;
  box-sizing: border-box;
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

/* Filters Section - Compact */
.filters-section {
  display: flex;
  gap: 12px;
  align-items: flex-end;
  padding: 12px 16px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  overflow-x: auto;
  flex-wrap: nowrap;
  flex-shrink: 0;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 0 0 auto;
  min-width: 140px;
  max-width: 180px;
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
  padding: 8px 10px;
  border: 2px solid #e1e8ed;
  border-radius: 6px;
  font-size: 0.85em;
  background: white;
  transition: border-color 0.2s;
  min-width: 140px;
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

/* Matrix Header Row */
.matrix-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 16px;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-bottom: 1px solid #dee2e6;
}

/* Matrix Tabs - Small & Square */
.matrix-tabs {
  display: flex;
  gap: 4px;
  justify-content: flex-start;
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
