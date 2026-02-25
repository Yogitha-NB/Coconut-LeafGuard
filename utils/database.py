import psycopg2
import streamlit as st
from datetime import datetime
import pandas as pd

class Database:
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        """Connect to PostgreSQL database"""
        try:
            self.connection = psycopg2.connect(
                host="localhost",
                database="coconut_leafguard",
                user="postgres",  
                password="your password",  
                port="your port"
            )
            return True
        except Exception as e:
            st.error(f"Database connection failed: {e}")
            return False
        

    def reset_connection(self):
        """Reset the database connection to clear any transaction errors"""
        try:
            if self.connection and not self.connection.closed:
                self.connection.close()
            self.connection = None
            return self.connect()
        except Exception as e:
            st.error(f"Error resetting connection: {e}")
            return False

    
    def get_connection(self):
        """Get database connection with error handling"""
        try:
            if self.connection is None or self.connection.closed:
                self.connect()
            # Test the connection
            cur = self.connection.cursor()
            cur.execute("SELECT 1")
            cur.close()
            return self.connection
        except Exception as e:
            st.error(f"Database connection error: {e}")
            # Try to reset the connection
            self.reset_connection()
            return self.connection

        
    def create_tables(self):
        """Create necessary tables if they don't exist"""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    full_name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    phone VARCHAR(20),
                    password VARCHAR(255) NOT NULL,
                    user_type VARCHAR(50) NOT NULL,
                    state VARCHAR(100),
                    district VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT TRUE
                )
            """)
        
        
            cur.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    product_name VARCHAR(255) NOT NULL,
                    category VARCHAR(100) NOT NULL,
                    price DECIMAL(10,2) NOT NULL,
                    quantity INTEGER NOT NULL,
                    description TEXT,
                    contact_phone VARCHAR(20),
                    whatsapp VARCHAR(20),
                    location VARCHAR(255),
                    images TEXT[],  -- Array to store image paths
                    status VARCHAR(20) DEFAULT 'pending',  -- pending, approved, rejected
                    is_available BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            
            cur.execute("""
                CREATE TABLE IF NOT EXISTS disease_detections (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    prediction VARCHAR(100),
                    disease_name VARCHAR(100),
                    severity VARCHAR(50),
                    confidence DECIMAL(5,4),
                    image_data BYTEA,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            
            cur.execute("""
                CREATE TABLE IF NOT EXISTS favorites (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    product_id INTEGER REFERENCES products(id),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(user_id, product_id)
                )
            """)
            
            
            
            conn.commit()
            cur.close()
            return True
            
        except Exception as e:
            st.error(f"Error creating tables: {e}")
            return False
    
    
    def register_user(self, full_name, email, phone, password, user_type, state, district):
        """Register a new user"""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            cur.execute("""
                INSERT INTO users (full_name, email, phone, password, user_type, state, district)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (full_name, email, phone, password, user_type, state, district))
            
            user_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
            return True, "Registration successful"
            
        except Exception as e:
            return False, f"Registration failed: {e}"
    
    def authenticate_user(self, email, password):
        """Authenticate user login"""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            cur.execute("""
                SELECT id, full_name, email, phone, user_type, state, district 
                FROM users 
                WHERE email = %s AND password = %s AND is_active = TRUE
            """, (email, password))
            
            user = cur.fetchone()
            cur.close()
            
            if user:
                return True, {
                    'id': user[0],
                    'full_name': user[1],
                    'email': user[2],
                    'phone': user[3],
                    'user_type': user[4],
                    'state': user[5],
                    'district': user[6]
                }
            else:
                return False, "Invalid credentials"
                
        except Exception as e:
            return False, f"Authentication error: {e}"
        

    def get_user_by_id(self, user_id):
        """Get user details by ID"""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            cur.execute("""
                SELECT id, full_name, email, phone, user_type, state, district, created_at 
                FROM users 
                WHERE id = %s
            """, (user_id,))
            
            row = cur.fetchone()
            cur.close()
            
            if row:
                return {
                    'id': row[0],
                    'full_name': row[1],
                    'email': row[2],
                    'phone': row[3],
                    'user_type': row[4],
                    'state': row[5],
                    'district': row[6],
                    'created_at': row[7]
                }
            else:
                return None
                
        except Exception as e:
            st.error(f"Error getting user by ID: {e}")
            return None
    
    def insert_product(self, user_id, product_name, category, price, quantity, description, 
                      contact_phone, whatsapp, location, images, status='pending'):
        """Insert a new product"""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            cur.execute("""
                INSERT INTO products 
                (user_id, product_name, category, price, quantity, description, 
                 contact_phone, whatsapp, location, images, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (user_id, product_name, category, price, quantity, description,
                  contact_phone, whatsapp, location, images, status))
            
            product_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
            return True
            
        except Exception as e:
            st.error(f"Error inserting product: {e}")
            return False
        


    def update_product(self, product_id, product_name, category, price, quantity, description, 
                  contact_phone, whatsapp, location, images=None, status='pending'):
        """Update an existing product in the database"""
        try:
            conn = self.get_connection()
            cur = conn.cursor()

            # First, check the current status in a separate query
            cur.execute("SELECT status FROM products WHERE id = %s", (product_id,))
            result = cur.fetchone()

            if result:
                current_status = result[0]
                # If the product was approved and is being edited, set status to pending for re-approval
                if current_status == 'approved':
                    status = 'pending'
            else:
                # Product not found
                cur.close()
                return False
        
            query = """
            UPDATE products 
            SET product_name = %s, category = %s, price = %s, quantity = %s, 
                description = %s, contact_phone = %s, whatsapp = %s, location = %s,
                images = %s, status = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
            """
        
            cur.execute(query, (
                product_name, category, price, quantity, description,
                contact_phone, whatsapp, location, images, status, product_id
            ))
        
            conn.commit()
            cur.close()
            return True
        
        except Exception as e:
            st.error(f"Error updating product: {e}")
            if 'conn' in locals():
                conn.rollback()
            return False    
    
    def get_all_products(self, filters=None):
        """Get all products with optional filters"""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            query = """
                SELECT p.*, u.full_name as seller_name 
                FROM products p 
                JOIN users u ON p.user_id = u.id 
                WHERE p.is_available = TRUE
            """
            params = []
            
            if filters:
                if filters.get('status'):
                    query += " AND p.status = %s"
                    params.append(filters['status'])
                else:
                    query += " AND p.status = 'approved'"  
                
                if filters.get('search'):
                    query += " AND (p.product_name ILIKE %s OR p.description ILIKE %s)"
                    params.extend([f"%{filters['search']}%", f"%{filters['search']}%"])
                
                if filters.get('category') and filters['category'] != 'All Categories':
                    query += " AND p.category = %s"
                    params.append(filters['category'])
                
                if filters.get('min_price'):
                    query += " AND p.price >= %s"
                    params.append(filters['min_price'])
                
                if filters.get('max_price'):
                    query += " AND p.price <= %s"
                    params.append(filters['max_price'])
            
    
            if filters and filters.get('sort_by'):
                if filters['sort_by'] == 'Price: Low to High':
                    query += " ORDER BY p.price ASC"
                elif filters['sort_by'] == 'Price: High to Low':
                    query += " ORDER BY p.price DESC"
                else:  
                    query += " ORDER BY p.created_at DESC"
            else:
                query += " ORDER BY p.created_at DESC"
            
            cur.execute(query, params)
            products = []
            for row in cur.fetchall():
                products.append({
                    'id': row[0],
                    'user_id': row[1],
                    'product_name': row[2],
                    'category': row[3],
                    'price': float(row[4]),
                    'quantity': row[5],
                    'description': row[6],
                    'contact_phone': row[7],
                    'whatsapp': row[8],
                    'location': row[9],
                    'images': row[10],
                    'status': row[11],
                    'is_available': row[12],
                    'created_at': row[13],
                    'seller_name': row[15]
                })
            
            cur.close()
            return products
            
        except Exception as e:
            st.error(f"Error getting products: {e}")
            return []
    
    def get_user_products(self, user_id):
        """Get products for a specific user"""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            cur.execute("""
                SELECT p.*, u.full_name as seller_name 
                FROM products p 
                LEFT JOIN users u ON p.user_id = u.id 
                WHERE p.user_id = %s 
                ORDER BY p.created_at DESC
            """, (user_id,))
            
            products = []
            for row in cur.fetchall():
                products.append({
                    'id': row[0],
                    'user_id': row[1],
                    'product_name': row[2],
                    'category': row[3],
                    'price': float(row[4]),
                    'quantity': row[5],
                    'description': row[6],
                    'contact_phone': row[7],
                    'whatsapp': row[8],
                    'location': row[9],
                    'images': row[10],
                    'status': row[11],
                    'is_available': row[12],
                    'created_at': row[13],
                    'seller_name': row[15] if len(row) > 15 else 'Unknown'
                })
            
            cur.close()
            return products
            
        except Exception as e:
            st.error(f"Error getting user products: {e}")
            # Ensure we get a fresh connection if there was an error
            if 'conn' in locals():
                conn.rollback()
            return []
    
    def update_product_status(self, product_id, status):
        """Update product status (approve/reject)"""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            cur.execute("""
                UPDATE products 
                SET status = %s, updated_at = CURRENT_TIMESTAMP 
                WHERE id = %s
            """, (status, product_id))
            
            conn.commit()
            cur.close()
            return True
            
        except Exception as e:
            st.error(f"Error updating product status: {e}")
            return False
    
    def get_pending_products(self, limit=None):
        """Get products pending approval"""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            query = """
                SELECT p.*, u.full_name as seller_name 
                FROM products p 
                JOIN users u ON p.user_id = u.id 
                WHERE p.status = 'pending' 
                ORDER BY p.created_at DESC
            """
            
            if limit:
                query += " LIMIT %s"
                cur.execute(query, (limit,))
            else:
                cur.execute(query)
            
            products = []
            for row in cur.fetchall():
                products.append({
                    'id': row[0],
                    'user_id': row[1],
                    'product_name': row[2],
                    'category': row[3],
                    'price': float(row[4]),
                    'quantity': row[5],
                    'description': row[6],
                    'contact_phone': row[7],
                    'whatsapp': row[8],
                    'location': row[9],
                    'images': row[10],
                    'status': row[11],
                    'is_available': row[12],
                    'created_at': row[13],
                    'seller_name': row[15]
                })
            
            cur.close()
            return products
            
        except Exception as e:
            st.error(f"Error getting pending products: {e}")
            return []
    
    def get_products_by_status(self, status):
        """Get products by status"""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            cur.execute("""
                SELECT p.*, u.full_name as seller_name 
                FROM products p 
                JOIN users u ON p.user_id = u.id 
                WHERE p.status = %s 
                ORDER BY p.created_at DESC
            """, (status,))
            
            products = []
            for row in cur.fetchall():
                products.append({
                    'id': row[0],
                    'user_id': row[1],
                    'product_name': row[2],
                    'category': row[3],
                    'price': float(row[4]),
                    'quantity': row[5],
                    'description': row[6],
                    'contact_phone': row[7],
                    'whatsapp': row[8],
                    'location': row[9],
                    'images': row[10],
                    'status': row[11],
                    'is_available': row[12],
                    'created_at': row[13],
                    'seller_name': row[15]
                })
            
            cur.close()
            return products
            
        except Exception as e:
            st.error(f"Error getting products by status: {e}")
            return []
    
    
    def get_all_users(self):
        """Get all users for admin management"""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            cur.execute("""
                SELECT id, full_name, email, phone, user_type, state, district, created_at 
                FROM users 
                ORDER BY created_at DESC
            """)
            
            users = []
            for row in cur.fetchall():
                users.append({
                    'id': row[0],
                    'full_name': row[1],
                    'email': row[2],
                    'phone': row[3],
                    'user_type': row[4],
                    'state': row[5],
                    'district': row[6],
                    'created_at': row[7]
                })
            
            cur.close()
            return users
            
        except Exception as e:
            st.error(f"Error getting users: {e}")
            return []
    
    def get_recent_users(self, limit=5):
        """Get recent users for admin dashboard"""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            cur.execute("""
                SELECT id, full_name, email, user_type, created_at 
                FROM users 
                ORDER BY created_at DESC 
                LIMIT %s
            """, (limit,))
            
            users = []
            for row in cur.fetchall():
                users.append({
                    'id': row[0],
                    'full_name': row[1],
                    'email': row[2],
                    'user_type': row[3],
                    'created_at': row[4]
                })
            
            cur.close()
            return users
            
        except Exception as e:
            st.error(f"Error getting recent users: {e}")
            return []
    
    def get_platform_stats(self):
        """Get platform statistics for admin dashboard"""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            stats = {}
            
        
            cur.execute("SELECT COUNT(*) FROM users")
            stats['total_users'] = cur.fetchone()[0]
            
        
            cur.execute("SELECT COUNT(*) FROM products")
            stats['total_products'] = cur.fetchone()[0]
            
            
            cur.execute("SELECT COUNT(*) FROM products WHERE status = 'pending'")
            stats['pending_products'] = cur.fetchone()[0]
            
            
            cur.execute("SELECT COUNT(*) FROM disease_detections")
            stats['total_detections'] = cur.fetchone()[0]
            
            cur.close()
            return stats
            
        except Exception as e:
            st.error(f"Error getting platform stats: {e}")
            return {}
    
    def get_analytics_data(self):
        """Get analytics data for charts"""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            analytics = {}
            
            
            cur.execute("""
                SELECT user_type, COUNT(*) 
                FROM users 
                GROUP BY user_type
            """)
            analytics['user_types'] = dict(cur.fetchall())
            
            
            cur.execute("""
                SELECT status, COUNT(*) 
                FROM products 
                GROUP BY status
            """)
            analytics['product_status'] = dict(cur.fetchall())
            
            
            cur.execute("""
                SELECT 
                    TO_CHAR(created_at, 'YYYY-MM') as month,
                    COUNT(*) as count
                FROM users 
                WHERE created_at >= CURRENT_DATE - INTERVAL '6 months'
                GROUP BY TO_CHAR(created_at, 'YYYY-MM')
                ORDER BY month
            """)
            analytics['monthly_registrations'] = dict(cur.fetchall())
            
            cur.close()
            return analytics
            
        except Exception as e:
            st.error(f"Error getting analytics data: {e}")
            return {}
    
   
    def add_to_favorites(self, user_id, product_id):
        """Add product to user favorites"""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            cur.execute("""
                INSERT INTO favorites (user_id, product_id) 
                VALUES (%s, %s)
            """, (user_id, product_id))
            
            conn.commit()
            cur.close()
            return True
            
        except Exception as e:
            
            return False
    
    def remove_from_favorites(self, user_id, product_id):
        """Remove product from user favorites"""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            cur.execute("""
                DELETE FROM favorites 
                WHERE user_id = %s AND product_id = %s
            """, (user_id, product_id))
            
            conn.commit()
            cur.close()
            return True
            
        except Exception as e:
            st.error(f"Error removing favorite: {e}")
            return False
    
    def is_product_favorited(self, user_id, product_id):
        """Check if product is in user favorites"""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            cur.execute("""
                SELECT 1 FROM favorites 
                WHERE user_id = %s AND product_id = %s
            """, (user_id, product_id))
            
            result = cur.fetchone() is not None
            cur.close()
            return result
            
        except Exception as e:
            return False
    
    def get_user_favorites(self, user_id):
        """Get user's favorite products"""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            cur.execute("""
                SELECT p.*, u.full_name as seller_name 
                FROM products p 
                JOIN favorites f ON p.id = f.product_id 
                JOIN users u ON p.user_id = u.id 
                WHERE f.user_id = %s AND p.status = 'approved'
                ORDER BY f.created_at DESC
            """, (user_id,))
            
            products = []
            for row in cur.fetchall():
                products.append({
                    'id': row[0],
                    'user_id': row[1],
                    'product_name': row[2],
                    'category': row[3],
                    'price': float(row[4]),
                    'quantity': row[5],
                    'description': row[6],
                    'contact_phone': row[7],
                    'whatsapp': row[8],
                    'location': row[9],
                    'images': row[10],
                    'status': row[11],
                    'is_available': row[12],
                    'created_at': row[13],
                    'seller_name': row[15]
                })
            
            cur.close()
            return products
            
        except Exception as e:
            st.error(f"Error getting user favorites: {e}")
            return []
    
    
    def insert_disease_detection(self, user_id, prediction, disease_name, severity, confidence, image_data=None):
        """Save disease detection result"""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            cur.execute("""
                INSERT INTO disease_detections 
                (user_id, prediction, disease_name, severity, confidence, image_data)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (user_id, prediction, disease_name, severity, confidence, image_data))
            
            conn.commit()
            cur.close()
            return True
            
        except Exception as e:
            st.error(f"Error saving detection: {e}")
            return False
    
   
    def get_user_stats(self, user_id):
        """Get statistics for a user"""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            stats = {}
            
            # Total products
            cur.execute("SELECT COUNT(*) FROM products WHERE user_id = %s", (user_id,))
            stats['total_products'] = cur.fetchone()[0]
            
            # Active products
            cur.execute("SELECT COUNT(*) FROM products WHERE user_id = %s AND is_available = TRUE", (user_id,))
            stats['active_products'] = cur.fetchone()[0]
            
            
            cur.execute("SELECT COUNT(*) FROM disease_detections WHERE user_id = %s", (user_id,))
            stats['total_detections'] = cur.fetchone()[0]
            
            
            cur.execute("SELECT COUNT(*) FROM disease_detections WHERE user_id = %s AND disease_name != 'Healthy'", (user_id,))
            stats['disease_cases'] = cur.fetchone()[0]
            
            cur.close()
            return stats
            
        except Exception as e:
            st.error(f"Error getting user stats: {e}")
            # Ensure we get a fresh connection if there was an error
            if 'conn' in locals():
                conn.rollback()
            return {}
    
    def delete_product(self, product_id, user_id):
        """Delete a product and handle foreign key constraints"""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
        
            # First, delete any favorites that reference this product
            cur.execute("DELETE FROM favorites WHERE product_id = %s", (product_id,))
        
            # Then delete the product
            cur.execute("DELETE FROM products WHERE id = %s AND user_id = %s", (product_id, user_id))
        
            rows_affected = cur.rowcount
            conn.commit()
            cur.close()
        
            return rows_affected > 0
        
        except Exception as e:
            st.error(f"Error deleting product: {e}")
            if 'conn' in locals():
                conn.rollback()
            return False
    
            
    
    def delete_user(self, user_id):
        """Delete a user (admin only)"""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            
            cur.execute("DELETE FROM favorites WHERE user_id = %s", (user_id,))
            cur.execute("DELETE FROM disease_detections WHERE user_id = %s", (user_id,))
            cur.execute("DELETE FROM products WHERE user_id = %s", (user_id,))
            cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
            
            conn.commit()
            cur.close()
            return True
            
        except Exception as e:
            st.error(f"Error deleting user: {e}")
            return False


db = Database()


db.create_tables()
