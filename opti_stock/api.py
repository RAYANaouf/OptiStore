import frappe
from frappe import _

@frappe.whitelist()
def get_products(fields=None, filters=None):
    """Get all products from ERPNext"""
    try:
        if not fields:
            fields = ['name', 'item_name']
        
        if not filters:
            filters = {}
        
        # Add default filters for stock items
        default_filters = {
            'disabled': 0
        }
        default_filters.update(filters)
        
        products = frappe.db.get_all(
            "Item",
            fields   = fields,
            filters  = default_filters,
            order_by = 'item_name asc'
        )
        
        return {
            'status': 'success',
            'data': products,
            'total_count': len(products)
        }
    except Exception as e:
        frappe.log_error(f"Error fetching products: {str(e)}")
        return {
            'status': 'error',
            'message': str(e)
        }

@frappe.whitelist()
def create_sales_invoice(customer, items):
    """Create sales invoice in ERPNext"""
    try:
        # Create new Sales Invoice
        doc = frappe.new_doc("Sales Invoice")
        doc.customer = customer
        doc.company = frappe.defaults.get_default("company")
        
        # Add items to invoice
        for item in items:
            doc.append("items", {
                "item_code": item.get("item_code"),
                "qty": item.get("qty"),
                "rate": item.get("rate"),
                "income_account": "Sales - " + frappe.defaults.get_default("company")
            })
        
        # Set default values
        doc.naming_series = "SINV-"
        doc.selling_price_list = "Standard Selling"
        
        # Insert and submit the document
        doc.insert()
        doc.submit()
        
        return {
            'status': 'success',
            'message': {
                'name': doc.name,
                'customer': doc.customer,
                'total': doc.grand_total
            }
        }
        
    except Exception as e:
        frappe.log_error(f"Error creating sales invoice: {str(e)}")
        return {
            'status': 'error',
            'message': str(e)
        }

@frappe.whitelist()
def get_stock_levels():
    """Get current stock levels for all items"""
    try:
        stock_levels = frappe.db.sql("""
            SELECT 
                item.item_code,
                item.item_name,
                item.standard_rate,
                SUM(sle.actual_qty) as stock_qty
            FROM `tabBin` as bin
            JOIN `tabItem` as item ON bin.item_code = item.name
            WHERE item.disabled = 0 AND item.is_stock_item = 1
            GROUP BY item.item_code, item.item_name, item.standard_rate
            ORDER BY item.item_name
        """)
        
        return {
            'status': 'success',
            'data': stock_levels
        }
    except Exception as e:
        frappe.log_error(f"Error fetching stock levels: {str(e)}")
        return {
            'status': 'error',
            'message': str(e)
        }

@frappe.whitelist()
def get_sales_history(limit=50):
    """Get recent sales history"""
    try:
        sales_history = frappe.db.get_all(
            "Sales Invoice",
            fields=['name', 'customer', 'posting_date', 'grand_total', 'status'],
            filters={'docstatus': 1},
            order_by='posting_date desc',
            limit=limit
        )
        
        return {
            'status': 'success',
            'data': sales_history
        }
    except Exception as e:
        frappe.log_error(f"Error fetching sales history: {str(e)}")
        return {
            'status': 'error',
            'message': str(e)
        }
