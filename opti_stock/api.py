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
def get_price_lists():
    """Get price lists from ERPNext"""
    try:
        price_lists = frappe.db.get_all(
            "Price List",
            fields=['name', 'price_list_name'],
            filters={'enabled': 1 , 'selling':1},
            order_by='price_list_name asc'
        )
        
        return {
            'status': 'success',
            'data': price_lists
        }
    except Exception as e:
        frappe.log_error(f"Error fetching price lists: {str(e)}")
        return {
            'status': 'error',
            'message': str(e)
        }

@frappe.whitelist()
def get_customers():
    """Get customers from ERPNext"""
    try:
        customers = frappe.db.get_all(
            "Customer",
            fields=['name', 'customer_name'],
            filters={'disabled': 0},
            order_by='customer_name asc'
        )
        
        return {
            'status': 'success',
            'data': customers
        }
    except Exception as e:
        frappe.log_error(f"Error fetching customers: {str(e)}")
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

@frappe.whitelist()
def get_pos_profile():
    """Get the POS Profile assigned to current user"""
    try:
        # Get POS Profile for current user
        pos_profile = frappe.db.get_value(
            "POS Profile",
            {"user": frappe.session.user, "disabled": 0},
            ["name", "warehouse", "selling_price_list", "company"],
            as_dict=True
        )
        
        # If no user-specific profile, get any available one
        if not pos_profile:
            pos_profile = frappe.db.get_all(
                "POS Profile",
                fields=["name", "warehouse", "selling_price_list", "company"],
                filters={"disabled": 0},
                limit=1,
                order_by="creation desc"
            )
            if pos_profile:
                pos_profile = pos_profile[0]
        
        return {
            'status': 'success',
            'data': pos_profile
        }
    except Exception as e:
        frappe.log_error(f"Error fetching POS profile: {str(e)}")
        return {
            'status': 'error',
            'message': str(e)
        }

@frappe.whitelist()
def check_pos_opening_entry():
    """Check if user has an open POS Opening Entry and return profile"""
    try:
        # Check for open POS Opening Entry
        opening_entry = frappe.db.get_value(
            "POS Opening Entry",
            {
                "user": frappe.session.user,
                "status": "Open",
                "docstatus": 1
            },
            ["name", "pos_profile", "period_start_date"],
            as_dict=True
        )
        
        pos_profile = None
        if opening_entry and opening_entry.pos_profile:
            # Get full POS Profile details
            pos_profile = frappe.db.get_value(
                "POS Profile",
                opening_entry.pos_profile,
                ["name", "warehouse", "selling_price_list", "company"],
                as_dict=True
            )
        
        return {
            'status': 'success',
            'has_open_entry': bool(opening_entry),
            'opening_entry': opening_entry,
            'pos_profile': pos_profile
        }
    except Exception as e:
        frappe.log_error(f"Error checking POS opening entry: {str(e)}")
        return {
            'status': 'error',
            'message': str(e)
        }

@frappe.whitelist()
def get_item_groups():
    """Get all Item Groups from ERPNext"""
    try:
        item_groups = frappe.db.get_all(
            "Item Group",
            fields=['name', 'item_group_name'],
            filters={ },
            order_by='name asc'
        )
        
        return {
            'status': 'success',
            'data': [g['name'] for g in item_groups],
            'total_count': len(item_groups)
        }
    except Exception as e:
        frappe.log_error(f"Error fetching item groups: {str(e)}")
        return {
            'status': 'error',
            'message': str(e)
        }

@frappe.whitelist()
def get_brands():
    """Get all Brands from ERPNext"""
    try:
        brands = frappe.db.get_all(
            "Brand",
            fields=['name'],
            filters={},
            order_by='name asc'
        )
        
        return {
            'status': 'success',
            'data': [b['name'] for b in brands],
            'total_count': len(brands)
        }
    except Exception as e:
        frappe.log_error(f"Error fetching brands: {str(e)}")
        return {
            'status': 'error',
            'message': str(e)
        }

@frappe.whitelist()
def get_companies():
    """Get all Companies from ERPNext"""
    try:
        companies = frappe.db.get_all(
            "Company",
            fields=['name', 'company_name'],
            filters={},
            order_by='name asc'
        )
        
        return {
            'status': 'success',
            'data': [c['name'] for c in companies],
            'total_count': len(companies)
        }
    except Exception as e:
        frappe.log_error(f"Error fetching companies: {str(e)}")
        return {
            'status': 'error',
            'message': str(e)
        }

@frappe.whitelist()
def get_warehouses(company=None):
    """Get all Warehouses from ERPNext, optionally filtered by company"""
    try:
        filters = {'is_group': 0}
        if company:
            filters['company'] = company
            
        warehouses = frappe.db.get_all(
            "Warehouse",
            fields=['name', 'warehouse_name'],
            filters=filters,
            order_by='name asc'
        )
        
        return {
            'status': 'success',
            'data': [w['name'] for w in warehouses],
            'total_count': len(warehouses)
        }
    except Exception as e:
        frappe.log_error(f"Error fetching warehouses: {str(e)}")
        return {
            'status': 'error',
            'message': str(e)
        }

def get_child_item_groups(parent_group):
    """Recursively get all child item groups including the parent"""
    all_groups = [parent_group]
    
    # Find direct children
    children = frappe.db.get_all(
        "Item Group",
        filters={'parent_item_group': parent_group},
        pluck='name'
    )
    
    # Recursively get children's children
    for child in children:
        all_groups.extend(get_child_item_groups(child))
    
    return all_groups

@frappe.whitelist()
def get_items_by_filters(item_group=None, brand=None, warehouse=None, company=None, companies=None):
    """Get items filtered by item group (including children), brand, warehouse and/or company/companies"""
    try:
        items = []
        
        if item_group:
            # Get all child groups recursively
            all_groups = get_child_item_groups(item_group)
            
            # Fetch items from all groups
            for group in all_groups:
                filters = {'disabled': 0, 'item_group': group}
                if brand:
                    filters['brand'] = brand
                
                group_items = frappe.db.get_all(
                    "Item",
                    fields=['name', 'item_name', 'item_group', 'brand', 'stock_uom'],
                    filters=filters,
                    order_by='item_name asc'
                )
                items.extend(group_items)
        else:
            # No group filter - fetch by brand only if provided
            filters = {'disabled': 0}
            if brand:
                filters['brand'] = brand
            
            items = frappe.db.get_all(
                "Item",
                fields=['name', 'item_name', 'item_group', 'brand', 'stock_uom'],
                filters=filters,
                order_by='item_name asc'
            )
        
        # Get stock quantities for each item
        for item in items:
            bin_filters = {"item_code": item.name.strip()}
            if warehouse:
                bin_filters['warehouse'] = warehouse
            
            # Filter by companies if provided
            if companies:
                # Get stock from all specified companies
                total_stock = 0
                for company in companies:
                    company_bin_filters = bin_filters.copy()
                    company_bin_filters['company'] = company
                    
                    stock_balance = frappe.db.get_value(
                        "Bin",
                        company_bin_filters,
                        'actual_qty'
                    )
                    total_stock += stock_balance or 0
                item['stock_qty'] = total_stock
            elif company:
                # Single company filter (backward compatibility)
                bin_filters['company'] = company
                stock_balance = frappe.db.get_value(
                    "Bin",
                    bin_filters,
                    'actual_qty'
                )
                item['stock_qty'] = stock_balance or 0
            else:
                # No company filter
                stock_balance = frappe.db.get_value(
                    "Bin",
                    bin_filters,
                    'actual_qty'
                )
                item['stock_qty'] = stock_balance or 0
        
        return {
            'status': 'success',
            'data': items,
            'total_count': len(items)
        }
    except Exception as e:
        frappe.log_error(f"Error fetching items by filters: {str(e)}")
        return {
            'status': 'error',
            'message': str(e)
        }
