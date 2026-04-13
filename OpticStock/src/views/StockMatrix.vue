<template>
  <div class="stock-matrix-page">
    <div class="matrix-header">
      <h1>Lens Stock Matrix</h1>
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

    <div class="matrix-container">
      <div class="matrix-table-wrapper">
        <table class="matrix-table">
          <thead>
            <tr>
              <th class="corner-cell">
                <div class="corner-label">
                  <span>SPH \ CLY</span>
                </div>
              </th>
              <th v-for="cly in clyValues" :key="cly" class="cly-header">
                {{ formatPower(cly) }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="sph in sphValues" :key="sph">
              <th class="sph-header">{{ formatPower(sph) }}</th>
              <td 
                v-for="cly in clyValues" 
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
  data() {
    return {
      // Generate SPH values: 0.00 to 20.00 in 0.25 steps
      sphValues: this.generatePowerValues(0, 20, 0.25),
      // Generate CLY values: 0.25 to 20.00 in 0.25 steps
      clyValues: this.generatePowerValues(0.25, 20, 0.25),
      // Mock stock data - in real app, this comes from backend
      stockData: {},
      // Editor modal state
      showEditor: false,
      selectedSph: 0,
      selectedCly: 0,
      editQuantity: 0
    }
  },
  created() {
    // Initialize with some mock data
    this.initializeMockData()
  },
  methods: {
    generatePowerValues(start, end, step) {
      const values = []
      for (let i = start; i <= end; i += step) {
        // Handle floating point precision
        values.push(Math.round(i * 100) / 100)
      }
      return values
    },
    formatPower(value) {
      // Format to 2 decimal places, removing trailing zeros
      const formatted = value.toFixed(2)
      return formatted
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
      const key = `${sph}-${cly}`
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
      const key = `${this.selectedSph}-${this.selectedCly}`
      this.stockData[key] = this.editQuantity
      this.closeEditor()
    }
  }
}
</script>

<style scoped>
.stock-matrix-page {
  padding: 20px;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e7f1 100%);
}

.matrix-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 0 10px;
}

.matrix-header h1 {
  font-size: 1.8em;
  color: #2c3e50;
  margin: 0;
}

.matrix-legend {
  display: flex;
  gap: 20px;
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

.matrix-container {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.matrix-table-wrapper {
  max-height: calc(100vh - 140px);
  overflow: auto;
}

.matrix-table {
  width: 100%;
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
