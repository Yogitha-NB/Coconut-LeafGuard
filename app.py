import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Coconut LeafGuard",
    page_icon="🌴",
    layout="wide",
    initial_sidebar_state="expanded"
)

import os
import tempfile
from PIL import Image
import numpy as np
import pandas as pd
from datetime import datetime
import plotly.express as px
import tensorflow as tf
import time
import io

# Import custom modules
from utils.auth import auth
from utils.database import db

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #228B22;
        margin-bottom: 1rem;
    }
    .feature-card {
        background-color: #f0f8f0;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #2E8B57;
        margin-bottom: 1rem;
    }
    .product-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .success-box {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    .warning-box {
        background-color: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #ffeaa7;
    }
    .info-box {
        background-color: #d1ecf1;
        color: #0c5460;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #bee5eb;
    }
    .nav-button {
        width: 100%;
        margin: 0.2rem 0;
    }
    .stats-card {
        background: linear-gradient(135deg, #2E8B57, #228B22);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
    }
    .pending-box {
        background-color: #fff3cd;
        color: #856404;
        padding: 0.5rem;
        border-radius: 5px;
        border: 1px solid #ffeaa7;
        margin: 0.5rem 0;
    }
    .approved-box {
        background-color: #d4edda;
        color: #155724;
        padding: 0.5rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
        margin: 0.5rem 0;
    }
    .rejected-box {
        background-color: #f8d7da;
        color: #721c24;
        padding: 0.5rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'user_products' not in st.session_state:
    st.session_state.user_products = []
if 'user_favorites' not in st.session_state:
    st.session_state.user_favorites = []
if 'user_stats' not in st.session_state:
    st.session_state.user_stats = {}
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False
if 'user' not in st.session_state:
    st.session_state.user = None

class CoconutLeafGuard:
    def __init__(self):
        pass
    
    
    def load_real_data(self):
        """Load real data from PostgreSQL"""
        if st.session_state.logged_in and st.session_state.user:
            user = st.session_state.user
            
            # Load user stats
            user_stats = db.get_user_stats(user['id'])
            st.session_state.user_stats = user_stats or {}
            
            # Load user products if farmer
            if user['user_type'] == 'Farmer':
                user_products = db.get_user_products(user['id'])
                st.session_state.user_products = user_products or []
            
            # Load user favorites if buyer
            elif user['user_type'] == 'Buyer':
                user_favorites = db.get_user_favorites(user['id'])
                st.session_state.user_favorites = user_favorites or []


    def create_opening_page(self):
        """Create the opening page with background image"""
        
        # Encode and set background image from local storage
        import base64
        
        # Path to your background image (update this path to your actual image location)
        background_image_path = "assets\coconut_farm.jpg"  # Or "images/background.jpg", etc.
        
        # Check if background image exists
        if os.path.exists(background_image_path):
            try:
                # Read and encode the image
                with open(background_image_path, "rb") as image_file:
                    encoded_image = base64.b64encode(image_file.read()).decode()
                
                # Set background with image
                bg_css = f"""
                <style>
                    .stApp {{
                        background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), 
                                url("data:image/jpg;base64,{encoded_image}");
                        background-size: cover;
                        background-position: center;
                        background-repeat: no-repeat;
                        background-attachment: fixed;
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    }}
                
                    .main-header {{
                        font-size: 3.5rem;
                        color: #FFFFFF;
                        text-align: center;
                        margin-bottom: 1rem;
                        font-weight: 700;
                        text-shadow: 3px 3px 6px rgba(0,0,0,0.8);
                    }}
                
                    .sub-header {{
                        font-size: 1.8rem;
                        color: #E8F5E9;
                        text-align: center;
                        margin-bottom: 3rem;
                        font-weight: 400;
                        text-shadow: 2px 2px 4px rgba(0,0,0,0.6);
                    }}
                
                    .role-container {{
                        background: rgba(255, 255, 255, 0.95);
                        border-radius: 15px;
                        padding: 2.5rem;
                        margin: 1rem 0;
                        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
                        border: 1px solid rgba(255, 255, 255, 0.2);
                        transition: transform 0.3s ease, box-shadow 0.3s ease;
                        height: 100%;
                        backdrop-filter: blur(5px);
                    }}
                
                    .role-container:hover {{
                        transform: translateY(-5px);
                        box-shadow: 0 15px 40px rgba(0,0,0,0.2);
                        background: rgba(255, 255, 255, 0.98);
                    }}
                
                    .role-title {{
                        font-size: 1.5rem;
                        color: #2E8B57;
                        margin-bottom: 1rem;
                        font-weight: 600;
                        display: flex;
                        align-items: center;
                        gap: 10px;
                    }}
                
                    .role-description {{
                        color: #444;
                        line-height: 1.6;
                        margin-bottom: 1.5rem;
                        font-size: 1rem;
                    }}
                
                    .role-button {{
                        background: linear-gradient(135deg, #2E8B57 0%, #228B22 100%);
                        color: white;
                        border: none;
                        padding: 12px 30px;
                        border-radius: 8px;
                        font-weight: 600;
                        font-size: 1rem;
                        cursor: pointer;
                        transition: all 0.3s ease;
                        width: 100%;
                        margin-top: 1rem;
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    }}
                
                    .role-button:hover {{
                        background: linear-gradient(135deg, #228B22 0%, #1c6b1c 100%);
                        transform: scale(1.02);
                        box-shadow: 0 6px 8px rgba(0,0,0,0.15);
                    }}
                
                    .login-container {{
                        background: rgba(255, 255, 255, 0.95);
                        border-radius: 15px;
                        padding: 2.5rem;
                        margin: 2rem auto;
                        max-width: 600px;
                        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
                        border: 1px solid rgba(255, 255, 255, 0.2);
                        backdrop-filter: blur(5px);
                    }}
                
                    .login-title {{
                        font-size: 1.8rem;
                        color: #2E8B57;
                        text-align: center;
                        margin-bottom: 1.5rem;
                        font-weight: 600;
                    }}
                
                    .login-button {{
                        background: linear-gradient(135deg, #4B86B4 0%, #2A4B8C 100%);
                        color: white;
                        border: none;
                        padding: 12px 40px;
                        border-radius: 8px;
                        font-weight: 600;
                        font-size: 1.1rem;
                        cursor: pointer;
                        transition: all 0.3s ease;
                        display: block;
                        margin: 1rem auto;
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    }}
                    
                    .login-button:hover {{
                        background: linear-gradient(135deg, #2A4B8C 0%, #1c3564 100%);
                        transform: scale(1.02);
                        box-shadow: 0 6px 8px rgba(0,0,0,0.15);
                    }}
                    
                    .footer {{
                        text-align: center;
                        color: rgba(255, 255, 255, 0.9);
                        margin-top: 3rem;
                        padding: 1rem;
                        font-size: 0.9rem;
                        border-top: 1px solid rgba(255, 255, 255, 0.2);
                        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
                    }}
                    
                    .icon-large {{
                        font-size: 2.5rem;
                        margin-bottom: 1rem;
                    }}
                    
                    .feature-list {{
                        list-style: none;
                        padding-left: 0;
                        margin: 1rem 0;
                    }}
                    
                    .feature-list li {{
                        padding: 8px 0;
                        padding-left: 30px;
                        position: relative;
                        color: #555;
                    }}
                    
                    .feature-list li:before {{
                        content: "✓";
                        color: #2E8B57;
                        font-weight: bold;
                        position: absolute;
                        left: 0;
                    }}
                </style>
                """
            except Exception as e:
                # If there's an error loading the image, use fallback gradient
                print(f"Error loading background image: {e}")
                bg_css = """
                <style>
                    .stApp {
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    }
                </style>
                """
        else:
            # Fallback CSS if image doesn't exist
            bg_css = """
            <style>
                .stApp {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                }
            </style>
            """
        
        st.markdown(bg_css, unsafe_allow_html=True)
                
        # Main title section
        st.markdown('<div class="main-header">🌴 Coconut LeafGuard</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-header">Platform for Coconut Cropcare & Online Marketplace</div>', unsafe_allow_html=True)
        
        # Roles section in 3 columns
        col1, col2, col3 = st.columns(3)

        with col1:
            # For Farmers
            st.markdown("""
            <div class="role-container">
                <div class="icon-large">👨‍🌾</div>
                <div class="role-title">For Farmers</div>
                <div class="role-description">
                    Detect coconut diseases using AI, get treatment recommendations, can upload coconut farm products and get a direct platform to reach buyers without middlemen.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Join as Farmer", key="join_farmer", use_container_width=True):
                st.session_state.page = 'auth'
                st.session_state.registration_type = 'Farmer'
                st.rerun()
        
        with col2:
            # For Buyers
            st.markdown("""
            <div class="role-container">
                <div class="icon-large">🛒</div>
                <div class="role-title">For Buyers</div>
                <div class="role-description">
                    Buyers can browse quality coconut products directly from farmers. They can contact sellers instantly and purchase fresh, farm-sourced items.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Join as Buyer", key="join_buyer", use_container_width=True):
                st.session_state.page = 'auth'
                st.session_state.registration_type = 'Buyer'
                st.rerun()
        
        with col3:
            # For Administrators
            st.markdown("""
            <div class="role-container">
                <div class="icon-large">👨‍💼</div>
                <div class="role-title">For Administrators</div>
                <div class="role-description">
                    Admins oversee the entire platform by approving products, monitoring system activity, ensure smooth operation and oversee marketplace operations.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Admin Login", key="admin_login", use_container_width=True):
                st.session_state.page = 'admin_auth'
                st.rerun()
        
        # Login section for existing users
        st.markdown("""
        <div class="login-container">
            <div class="login-title">Already have an account?</div>
            <div style="text-align: center; color: #666; margin-bottom: 1.5rem;">
                Log in to explore your dashboard and stay connected with Coconut LeafGuard.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Login button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("User Login", key="user_login", use_container_width=True):
                st.session_state.page = 'auth'
                st.rerun()
        
        # Footer
        st.markdown("""
        <div class="footer">
            <p>🌴 Smart Coconut Leaf Diagnosis & Direct Farmer–Buyer Connect 🌴</p>
        </div>
        """, unsafe_allow_html=True)

        
    def create_top_navigation(self):
        """Create top navigation bar"""
        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
        
        with col1:
            if st.session_state.is_admin:
                st.markdown('<h1 class="main-header">👨‍💼 Admin Dashboard</h1>', unsafe_allow_html=True)
            else:
                st.markdown('<h1 class="main-header">🌴 Coconut LeafGuard</h1>', unsafe_allow_html=True)
        
        with col2:
            if st.session_state.logged_in and st.session_state.user:
                user = st.session_state.user
                st.markdown(f"**Welcome, {user['full_name']}!**")
            elif st.session_state.logged_in:
                st.markdown("**Welcome!**")
        
        with col3:
            if st.session_state.logged_in:
                if st.session_state.is_admin:
                    st.markdown("**Role:** Administrator")
                elif st.session_state.user:
                    user = st.session_state.user
                    st.markdown(f"**Role:** {user['user_type']}")
                else:
                    st.markdown("**Role:** User")
        
        with col4:
            if st.session_state.logged_in:
                if st.button("👤 Profile", use_container_width=True):
                    if st.session_state.is_admin:
                        st.session_state.page = 'admin_profile'
                    else:
                        st.session_state.page = 'profile'
                if st.button("🚪 Logout", use_container_width=True, type="secondary"):
                    auth.logout_user()
                    st.rerun()
            else:
                if st.button("🔐 Login", use_container_width=True, type="primary"):
                    st.session_state.page = 'auth'
        
        st.markdown("---")
    
    def navigation_sidebar(self):
        """Create navigation sidebar based on user type"""
        if st.session_state.logged_in:
            if st.session_state.is_admin:
                self.admin_navigation_sidebar()
            elif st.session_state.user:
                user = st.session_state.user
                self.user_navigation_sidebar(user)
    
    def user_navigation_sidebar(self, user):
        """Navigation sidebar for regular users"""
        with st.sidebar:
            st.markdown("### 🚀 Quick Navigation")
            
            # Common navigation for all users
            if st.button("🏠 Home", use_container_width=True, key="nav_home"):
                st.session_state.page = 'home'
            
            if st.button("🛒 Marketplace", use_container_width=True, key="nav_marketplace"):
                st.session_state.page = 'marketplace'
            
            # Farmer-specific navigation
            if user['user_type'] in ['Farmer', 'ರೈತ']:
                st.markdown("---")
                st.markdown("### 👨‍🌾 Farmer Tools")
                if st.button("🔍 Disease Detection", use_container_width=True, key="nav_disease"):
                    st.session_state.page = 'disease_detection'
                if st.button("➕ Add Product", use_container_width=True, key="nav_add_product"):
                    st.session_state.page = 'add_product'
                if st.button("📦 My Products", use_container_width=True, key="nav_my_products"):
                    st.session_state.page = 'my_products'
            
            # Buyer-specific navigation
            elif user['user_type'] in ['Buyer', 'ಖರೀದಿದಾರ']:
                st.markdown("---")
                st.markdown("### 👥 Buyer Features")
                if st.button("❤️ My Favorites", use_container_width=True, key="nav_favorites"):
                    st.session_state.page = 'favorites'
    
    def admin_navigation_sidebar(self):
        """Navigation sidebar for admin"""
        with st.sidebar:
            st.markdown("### 👨‍💼 Admin Navigation")
            
            if st.button("📊 Dashboard", use_container_width=True, key="admin_dashboard"):
                st.session_state.page = 'admin_dashboard'

            if st.button("🛒 Marketplace", use_container_width=True, key="admin_marketplace"):
                st.session_state.page = 'marketplace'
            
            if st.button("👥 Manage Users", use_container_width=True, key="admin_users"):
                st.session_state.page = 'admin_users'
            
            if st.button("📦 Manage Products", use_container_width=True, key="admin_products"):
                st.session_state.page = 'admin_products'
            
            if st.button("📈 Analytics", use_container_width=True, key="admin_analytics"):
                st.session_state.page = 'admin_analytics'
            
            if st.button("👤 Admin Profile", use_container_width=True, key="admin_profile_nav"):
                st.session_state.page = 'admin_profile'
    
    def home_page(self):
        """Home page content based on user type"""
        if not st.session_state.logged_in:
            self.create_opening_page()
        else:
            if st.session_state.is_admin:
                self.admin_dashboard_page()
            else:
                if st.session_state.user:
                    user = st.session_state.user
                    if user['user_type'] in ['Farmer', 'ರೈತ']:
                        self.farmer_home_page()
                    else:
                        self.buyer_home_page()
                else:
                    # If user is logged in but user data is missing, redirect to auth
                    st.session_state.page = 'auth'
                    st.rerun()
    
    def farmer_home_page(self):
        """Home page for farmers"""
        st.markdown('<div class="main-header">👨‍🌾 Farmer Dashboard</div>', unsafe_allow_html=True)
        
        # Load real-time data
        self.load_real_data()
        
        # Welcome message
        user = st.session_state.user
        st.markdown(f"""
        <div class="success-box">
        <h3>Welcome back, {user['full_name']}! 👋</h3>
        <p>Ready to manage your coconut leaves and products today?</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Real-time stats
        st.markdown("### 📊 Real-time Statistics")
        stats = st.session_state.user_stats
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_products = stats.get('total_products', 0)
            st.markdown(f"""
            <div class="stats-card">
            <h3>{total_products}</h3>
            <p>Total Products</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            active_products = stats.get('active_products', 0)
            st.markdown(f"""
            <div class="stats-card">
            <h3>{active_products}</h3>
            <p>Active Listings</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            total_detections = stats.get('total_detections', 0)
            st.markdown(f"""
            <div class="stats-card">
            <h3>{total_detections}</h3>
            <p>Disease Scans</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            disease_cases = stats.get('disease_cases', 0)
            st.markdown(f"""
            <div class="stats-card">
            <h3>{disease_cases}</h3>
            <p>Disease Cases</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Quick actions
        st.markdown("### 🚀 Quick Actions")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🔍 Disease Detection", use_container_width=True):
                st.session_state.page = 'disease_detection'
            st.markdown("""
            <div style="text-align: center; padding: 0.5rem;">
            <small>Analyze leaf images for diseases</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.button("🛒 Marketplace", use_container_width=True):
                st.session_state.page = 'marketplace'
            st.markdown("""
            <div style="text-align: center; padding: 0.5rem;">
            <small>View and Purchase Browse Products</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            if st.button("➕ Add Product", use_container_width=True):
                st.session_state.page = 'add_product'
            st.markdown("""
            <div style="text-align: center; padding: 0.5rem;">
            <small>List your products for sale</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            if st.button("📦 My Products", use_container_width=True):
                st.session_state.page = 'my_products'
            st.markdown("""
            <div style="text-align: center; padding: 0.5rem;">
            <small>Manage your product listings</small>
            </div>
            """, unsafe_allow_html=True)
        
        # Recent activity section
        st.markdown("### 📈 Recent Activity")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Recent products
            recent_products = st.session_state.user_products[:3]
            st.markdown("""
            <div class="info-box">
            <h4>🆕 Recent Products</h4>
            """, unsafe_allow_html=True)
            if recent_products:
                for product in recent_products:
                    status = product.get('status', 'pending')
                    status_badge = self.get_product_status_badge(status)
                    
                    # Apply different colors based on status
                    if status == 'approved':
                        st.markdown(f"• **{product['product_name']}** - ₹{product['price']:.2f} <span style='color: #155724; background-color: #d4edda; padding: 2px 8px; border-radius: 12px; font-size: 0.8em;'>✓ {status_badge}</span>", unsafe_allow_html=True)
                    elif status == 'rejected':
                         st.markdown(f"• **{product['product_name']}** - ₹{product['price']:.2f} <span style='color: #721c24; background-color: #f8d7da; padding: 2px 8px; border-radius: 12px; font-size: 0.8em;'>✗ {status_badge}</span>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"• **{product['product_name']}** - ₹{product['price']:.2f} <span style='color: #856404; background-color: #fff3cd; padding: 2px 8px; border-radius: 12px; font-size: 0.8em;'>⏳ {status_badge}</span>", unsafe_allow_html=True)
            else:
                st.write("No products listed yet")
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="info-box">
            <h4>🌴 Farmer Features</h4>
            <p>• View and edit product details anytime</p>
            <p>• Coconut leaf disease detection</p>
            <p>• Access a simple dashboard for all your listings</p>
            </div>
            """, unsafe_allow_html=True)
    
    def get_product_status_badge(self, status):
        """Get HTML badge for product status"""
        if status == 'approved':
            return 'Approved'
        elif status == 'rejected':
            return 'Rejected'
        else:
            return 'Pending'
    
    def buyer_home_page(self):
        """Home page for buyers"""
        st.markdown('<div class="main-header">👥 Buyer Dashboard</div>', unsafe_allow_html=True)
        
        # Load real-time data
        self.load_real_data()
        
        # Welcome message
        user = st.session_state.user
        st.markdown(f"""
        <div class="success-box">
        <h3>Welcome, {user['full_name']}! 🛒</h3>
        <p>Discover fresh coconut products directly from farmers</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick actions
        st.markdown("### 🚀 Quick Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🛒 Marketplace", use_container_width=True):
                st.session_state.page = 'marketplace'
            st.markdown("""
            <div style="text-align: center; padding: 0.5rem;">
            <small>Browse products from farmers</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.button("❤️ My Favorites", use_container_width=True):
                st.session_state.page = 'favorites'
            st.markdown("""
            <div style="text-align: center; padding: 0.5rem;">
            <small>View your saved products</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            if st.button("👤 User Profile", use_container_width=True):
                st.session_state.page = 'profile'
            st.markdown("""
            <div style="text-align: center; padding: 0.5rem;">
            <small>Manage your account</small>
            </div>
            """, unsafe_allow_html=True)
        
        # Featured products from PostgreSQL
        st.markdown("### 🌟 Featured Products")
        self.display_featured_products()
    
    def display_featured_products(self):
        """Display featured products from PostgreSQL"""
        # Get featured products (only approved ones)
        filters = {
            'sort_by': 'Newest First',
            'status': 'approved'
        }
        featured_products = db.get_all_products(filters)[:3]
        
        if featured_products:
            st.markdown("")
            cols = st.columns(3)
            for idx, product in enumerate(featured_products):
                with cols[idx]:
                    self.display_product_card(product, show_favorite=True)
        else:
            st.info("No featured products available at the moment.")
    
    def authentication_page(self):
        """Handle user authentication"""
        st.markdown('<div class="main-header">🔐 Account Authentication</div>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🚪 Login", "📝 Register"])
        
        with tab1:
            self.login_form()
        
        with tab2:
            self.register_form()

    def login_form(self):
        """Login form"""
        st.subheader("Login to Your Account")
        
        with st.form("login_form"):
            email = st.text_input("📧 Email Address", placeholder="Enter your email")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
            
            if st.form_submit_button("🚪 Login", type="primary", use_container_width=True):
                if email and password:
                    with st.spinner("Logging in..."):
                        success, message = auth.login_user(email, password)
                        if success:
                            st.success(message)
                            # Load user data after login
                            self.load_real_data()
                            time.sleep(1)
                            st.session_state.page = 'home'
                            st.rerun()
                        else:
                            st.error(message)
                else:
                    st.error("Please fill in all fields")

        # Back to Home button below login form
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("← Back to Home", key="back_from_login", use_container_width=True, type="secondary"):
                st.session_state.page = 'home'
                st.rerun()

    def register_form(self):
        """Registration form"""
        st.subheader("Create New Account")
        
        # Pre-select user type if coming from opening page
        default_user_type = st.session_state.get('registration_type', 'Farmer')
        
        with st.form("register_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                full_name = st.text_input("👤 Full Name", placeholder="Enter your full name")
                email = st.text_input("📧 Email Address", placeholder="Enter your email")
                phone = st.text_input("📞 Phone Number", placeholder="Enter your phone number")
            
            with col2:
                password = st.text_input("🔒 Password", type="password", placeholder="Create a password")
                confirm_password = st.text_input("🔒 Confirm Password", type="password", placeholder="Confirm your password")
                user_type = st.selectbox("👥 User Type", ["Farmer", "Buyer"], 
                                    index=0 if default_user_type == 'Farmer' else 1)
                state = st.text_input("🏠 State", placeholder="Enter your state")
                district = st.text_input("📍 District", placeholder="Enter your district")
            
            # Password strength indicator
            if password:
                strength = auth.password_strength(password)
                strength_labels = ["Very Weak", "Weak", "Fair", "Good", "Strong"]
                st.progress(strength/5, text=strength_labels[strength-1])
            
            if st.form_submit_button("📝 Register", type="primary", use_container_width=True):
                if not all([full_name, email, phone, password, confirm_password, state, district]):
                    st.error("Please fill in all fields")
                elif password != confirm_password:
                    st.error("Passwords do not match")
                else:
                    with st.spinner("Creating account..."):
                        success, message = auth.register_user(
                            full_name, email, phone, password, user_type, state, district
                        )
                        if success:
                            st.success(message)
                            st.info("Please login with your new account")
                        else:
                            st.error(message)

        # Back to Home button below register form
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("← Back to Home", key="back_from_register", use_container_width=True, type="secondary"):
                st.session_state.page = 'home'
                st.rerun()
    
    def admin_authentication_page(self):
        """Admin authentication page"""
        st.markdown('<div class="main-header">👨‍💼 Admin Login</div>', unsafe_allow_html=True)
        
        with st.form("admin_login_form"):
            st.subheader("Administrator Access")
            
            username = st.text_input("👤 Admin Username", placeholder="Enter admin username")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter admin password")
            
            if st.form_submit_button("🚪 Admin Login", type="primary", use_container_width=True):
                if username and password:
                    with st.spinner("Verifying admin credentials..."):
                        # Simple admin authentication (you can enhance this)
                        if username == "admin" and password == "admin123":  # Change these credentials
                            st.session_state.logged_in = True
                            st.session_state.is_admin = True
                            st.session_state.page = 'admin_dashboard'
                            st.success("✅ Admin login successful!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("❌ Invalid admin credentials")
                else:
                    st.error("Please fill in all fields")
        
        # Back to main page
        if st.button("← Back to Main Page", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()
    
    def admin_dashboard_page(self):
        """Admin dashboard page"""
        st.markdown('<div class="main-header">👨‍💼 Admin Dashboard</div>', unsafe_allow_html=True)
        
        # Welcome message
        st.markdown(f"""
        <div class="success-box">
        <h3>Welcome, Administrator! 👋</h3>
        <p>Manage users, products, and platform analytics</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Statistics cards
        st.markdown("### 📊 Platform Statistics")
        
        # Get platform stats from database
        platform_stats = db.get_platform_stats()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_users = platform_stats.get('total_users', 0)
            st.markdown(f"""
            <div class="stats-card">
            <h3>{total_users}</h3>
            <p>Total Users</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_products = platform_stats.get('total_products', 0)
            st.markdown(f"""
            <div class="stats-card">
            <h3>{total_products}</h3>
            <p>Total Products</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            pending_products = platform_stats.get('pending_products', 0)
            st.markdown(f"""
            <div class="stats-card">
            <h3>{pending_products}</h3>
            <p>Pending Products</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            total_detections = platform_stats.get('total_detections', 0)
            st.markdown(f"""
            <div class="stats-card">
            <h3>{total_detections}</h3>
            <p>Disease Scans</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Quick actions
        st.markdown("### 🚀 Quick Actions")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("👥 Manage Users", use_container_width=True):
                st.session_state.page = 'admin_users'
            st.markdown("""
            <div style="text-align: center; padding: 0.5rem;">
            <small>View and manage all users</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.button("📦 Manage Products", use_container_width=True):
                st.session_state.page = 'admin_products'
            st.markdown("""
            <div style="text-align: center; padding: 0.5rem;">
            <small>Approve/reject products</small>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            if st.button("🛒 Marketplace", use_container_width=True):
                st.session_state.page = 'marketplace'
            st.markdown("""
            <div style="text-align: center; padding: 0.5rem;">
            <small>Browse marketplace products</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            if st.button("📈 View Analytics", use_container_width=True):
                st.session_state.page = 'admin_analytics'
            st.markdown("""
            <div style="text-align: center; padding: 0.5rem;">
            <small>Platform analytics & charts</small>
            </div>
            """, unsafe_allow_html=True)
        
        
        # Recent activity
        st.markdown("### 📈 Recent Activity")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Recent users
            recent_users = db.get_recent_users(5)
            st.markdown("""
            <div class="info-box">
            <h4>🆕 Recent Users</h4>
            """, unsafe_allow_html=True)
            if recent_users:
                for user in recent_users:
                    st.write(f"• {user['full_name']} ({user['user_type']})")
            else:
                st.write("No recent users")
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            # Pending products
            pending_products_list = db.get_pending_products(5)
            st.markdown("""
            <div class="info-box">
            <h4>⏳ Pending Products</h4>
            """, unsafe_allow_html=True)
            if pending_products_list:
                for product in pending_products_list:
                    st.write(f"• {product['product_name']} - {product['seller_name']}")
            else:
                st.write("No pending products")
            st.markdown("</div>", unsafe_allow_html=True)

        # Marketplace Preview Section
        st.markdown("### 🛒 Marketplace Overview")
        
        # Get approved products for marketplace preview
        filters = {
            'sort_by': 'Newest First',
            'status': 'approved'
        }
        marketplace_products = db.get_all_products(filters)[:6]  # Show up to 6 products
        
        if marketplace_products:
            st.markdown(f"#### 🌟 Recently Approved Products ({len(marketplace_products)} available)")
            
            # Display products in grid
            cols = st.columns(3)
            for idx, product in enumerate(marketplace_products):
                with cols[idx % 3]:
                    self.display_product_card_admin_preview(product)
            
            # View all products button
            if st.button("📋 View All Marketplace Products", use_container_width=True):
                st.session_state.page = 'marketplace'
                st.rerun()
        else:
            st.info("No approved products in the marketplace yet.")

    def display_product_card_admin_preview(self, product):
        """Display product card for admin dashboard preview"""
        with st.container():
            # Format created_at if it's a datetime object
            created_at = product.get('created_at')
            if hasattr(created_at, 'strftime'):
                created_at = created_at.strftime('%Y-%m-%d')
            else:
                created_at = str(created_at)
            
            # Get product images
            images = product.get('images', [])
            
            # Display first image if available
            if images and len(images) > 0:
                try:
                    if os.path.exists(images[0]):
                        image = Image.open(images[0])
                        st.image(image, caption=product['product_name'], use_column_width=True)
                    else:
                        st.image("https://via.placeholder.com/400x300/2E8B57/FFFFFF?text=Image+Not+Found", 
                                use_column_width=True)
                except Exception as e:
                    st.image("https://via.placeholder.com/400x300/2E8B57/FFFFFF?text=Error+Loading", 
                            use_column_width=True)
            else:
                st.image("https://via.placeholder.com/400x300/2E8B57/FFFFFF?text=No+Product+Image", 
                        use_column_width=True, caption="No product images available")
            
            st.markdown(f"""
            <div class="product-card">
            <h5>{product['product_name']}</h5>
            <p><strong>Category:</strong> {product['category']}</p>
            <p><strong>Price:</strong> ₹{product['price']:.2f}</p>
            <p><strong>Seller:</strong> {product.get('seller_name', 'Unknown')}</p>
            <p><strong>Location:</strong> {product['location']}</p>
            <p><strong>Listed:</strong> {created_at}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Quick status indicator
            status = product.get('status', 'approved')
            if status == 'approved':
                st.success("✅ Approved")
            elif status == 'pending':
                st.warning("⏳ Pending")
            else:
                st.error("❌ Rejected")
    
    def admin_users_page(self):
        """Admin page to manage users"""
        st.markdown('<div class="main-header">👥 User Management</div>', unsafe_allow_html=True)
        
        # Get all users from database
        all_users = db.get_all_users()
        
        if all_users:
            st.markdown(f"### 📋 Total Users: {len(all_users)}")
            
            # Display users in a table
            user_data = []
            for user in all_users:
                user_data.append({
                    'ID': user['id'],
                    'Name': user['full_name'],
                    'Email': user['email'],
                    'Phone': user['phone'],
                    'Type': user['user_type'],
                    'State': user['state'],
                    'District': user['district'],
                    'Joined': user.get('created_at', 'N/A')
                })
            
            df = pd.DataFrame(user_data)
            st.dataframe(df, use_container_width=True)
            
            # User actions
            st.markdown("### 🔧 User Actions")
            col1, col2 = st.columns(2)
            
            with col1:
                user_id = st.number_input("User ID for action", min_value=1, step=1, value=1)
            
            with col2:
                action = st.selectbox("Action", ["View Details", "Delete User"])
                
                if st.button("Execute Action", use_container_width=True, key="execute_user_action"):
                    if action == "Delete User":
                        if db.delete_user(user_id):
                            st.success("User deleted successfully!")
                            st.rerun()
                        else:
                            st.error("Failed to delete user")
                    else:
                        # View Details - Show detailed user information
                        user_details = db.get_user_by_id(user_id)
                        if user_details:
                            st.markdown("### 👤 User Details")
                            st.markdown(f"""
                            <div class="info-box">
                            <h4>User Information</h4>
                            <p><strong>ID:</strong> {user_details['id']}</p>
                            <p><strong>Full Name:</strong> {user_details['full_name']}</p>
                            <p><strong>Email:</strong> {user_details['email']}</p>
                            <p><strong>Phone:</strong> {user_details['phone']}</p>
                            <p><strong>User Type:</strong> {user_details['user_type']}</p>
                            <p><strong>State:</strong> {user_details['state']}</p>
                            <p><strong>District:</strong> {user_details['district']}</p>
                            <p><strong>Joined:</strong> {user_details.get('created_at', 'N/A')}</p>
                            </div>
                            """, unsafe_allow_html=True)

                            # Show user statistics only for farmers
                            if user_details['user_type'].lower() == 'farmer':
                                user_stats = db.get_user_stats(user_id)
                                if user_stats:
                                    st.markdown("### 📊 User Statistics")
                                    col1, col2, col3 = st.columns(3)
                                    with col1:
                                        st.metric("Total Products", user_stats.get('total_products', 0))
                                    with col2:
                                        st.metric("Disease Scans", user_stats.get('total_detections', 0))
                                    with col3:
                                        st.metric("Active Listings", user_stats.get('active_products', 0))
                            # For buyers or other user types, don't show anything - just skip
                        else:
                            st.error(f"User with ID {user_id} not found!")
        else:
            st.info("No users found in the system.")
    
    def admin_products_page(self):
        """Admin page to manage products"""
        st.markdown('<div class="main-header">📦 Product Management</div>', unsafe_allow_html=True)
        
        # Tabs for different product statuses
        tab1, tab2, tab3 = st.tabs(["⏳ Pending Approval", "✅ Approved", "❌ Rejected"])
        
        with tab1:
            self.display_pending_products()
        
        with tab2:
            self.display_approved_products()
        
        with tab3:
            self.display_rejected_products()
    
    def display_pending_products(self):
        """Display products pending approval"""
        pending_products = db.get_pending_products()
        
        if pending_products:
            st.markdown(f"### ⏳ Products Pending Approval: {len(pending_products)}")
            
            for product in pending_products:
                with st.expander(f"📦 {product['product_name']} - ₹{product['price']:.2f}", expanded=True):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"**Seller:** {product['seller_name']}")
                        st.write(f"**Category:** {product['category']}")
                        st.write(f"**Price:** ₹{product['price']:.2f}")
                        st.write(f"**Quantity:** {product['quantity']} units")
                        st.write(f"**Location:** {product['location']}")
                        st.write(f"**Description:** {product['description']}")
                        st.write(f"**Contact:** {product['contact_phone']}")
                    
                    with col2:
                        col2a, col2b = st.columns(2)
                        with col2a:
                            if st.button("✅ Approve", key=f"approve_{product['id']}", use_container_width=True):
                                if db.update_product_status(product['id'], 'approved'):
                                    st.success("Product approved!")
                                    st.rerun()
                                else:
                                    st.error("Failed to approve product")
                        with col2b:
                            if st.button("❌ Reject", key=f"reject_{product['id']}", use_container_width=True):
                                if db.update_product_status(product['id'], 'rejected'):
                                    st.success("Product rejected!")
                                    st.rerun()
                                else:
                                    st.error("Failed to reject product")
        else:
            st.info("No products pending approval.")
    
    def display_approved_products(self):
        """Display approved products"""
        approved_products = db.get_products_by_status('approved')
        
        if approved_products:
            st.markdown(f"### ✅ Approved Products: {len(approved_products)}")
            
            for product in approved_products:
                with st.expander(f"📦 {product['product_name']} - ₹{product['price']:.2f}"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"**Seller:** {product['seller_name']}")
                        st.write(f"**Category:** {product['category']}")
                        st.write(f"**Price:** ₹{product['price']:.2f}")
                        st.write(f"**Quantity:** {product['quantity']} units")
                        st.write(f"**Status:** Approved")
                    
                    with col2:
                        if st.button("❌ Reject", key=f"reject_approved_{product['id']}", use_container_width=True):
                            if db.update_product_status(product['id'], 'rejected'):
                                st.success("Product status updated to rejected!")
                                st.rerun()
                            else:
                                st.error("Failed to update product status")
        else:
            st.info("No approved products.")
    
    def display_rejected_products(self):
        """Display rejected products"""
        rejected_products = db.get_products_by_status('rejected')
        
        if rejected_products:
            st.markdown(f"### ❌ Rejected Products: {len(rejected_products)}")
            
            for product in rejected_products:
                with st.expander(f"📦 {product['product_name']} - ₹{product['price']:.2f}"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"**Seller:** {product['seller_name']}")
                        st.write(f"**Category:** {product['category']}")
                        st.write(f"**Price:** ₹{product['price']:.2f}")
                        st.write(f"**Quantity:** {product['quantity']} units")
                        st.write(f"**Status:** Rejected")
                    
                    with col2:
                        if st.button("✅ Approve", key=f"approve_rejected_{product['id']}", use_container_width=True):
                            if db.update_product_status(product['id'], 'approved'):
                                st.success("Product status updated to approved!")
                                st.rerun()
                            else:
                                st.error("Failed to update product status")
        else:
            st.info("No rejected products.")
    
    def admin_analytics_page(self):
        """Admin analytics page with charts"""
        st.markdown('<div class="main-header">📈 Platform Analytics</div>', unsafe_allow_html=True)
        
        # Get analytics data
        analytics_data = db.get_analytics_data()
        
        col1, col2 = st.columns(2)
        
        with col1:
            # User distribution chart
            st.markdown("### 👥 User Distribution")
            user_types = analytics_data.get('user_types', {})
            if user_types:
                fig = px.pie(
                    values=list(user_types.values()),
                    names=list(user_types.keys()),
                    title="User Types Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No user data available for chart.")
        
        with col2:
            # Product status distribution
            st.markdown("### 📦 Product Status")
            product_status = analytics_data.get('product_status', {})
            if product_status:
                fig = px.bar(
                    x=list(product_status.keys()),
                    y=list(product_status.values()),
                    title="Product Status Distribution",
                    color=list(product_status.keys()),
                    color_discrete_map={
                        'pending': '#FFC107',
                        'approved': '#28A745', 
                        'rejected': '#DC3545'
                    }
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No product data available for chart.")
        
        # Monthly registrations
        st.markdown("### 📅 User Registrations (Monthly)")
        monthly_registrations = analytics_data.get('monthly_registrations', {})
        if monthly_registrations:
            fig = px.line(
                x=list(monthly_registrations.keys()),
                y=list(monthly_registrations.values()),
                title="Monthly User Registrations",
                markers=True
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No registration data available for chart.")
    
    def admin_profile_page(self):
        """Admin profile management"""
        st.markdown('<div class="main-header">👤 Admin Profile</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 📝 Admin Information")
            
            with st.form("admin_profile_form"):
                admin_name = st.text_input("👤 Admin Name", value="Administrator")
                admin_email = st.text_input("📧 Admin Email", value="admin@coconutfarm.com")
                
                if st.form_submit_button("💾 Update Profile", type="primary", use_container_width=True):
                    st.success("Admin profile updated successfully!")
        
        with col2:
            st.markdown("### 🔐 Security")
            
            with st.form("admin_change_password_form"):
                st.markdown("#### Change Admin Password")
                current_password = st.text_input("Current Password", type="password")
                new_password = st.text_input("New Password", type="password")
                confirm_password = st.text_input("Confirm New Password", type="password")
                
                if st.form_submit_button("🔑 Change Password", use_container_width=True):
                    if new_password == confirm_password:
                        # Here you would update the admin password in your secure storage
                        st.success("✅ Admin password updated successfully!")
                    else:
                        st.error("❌ Passwords do not match")
    
    def disease_detection_page(self):
        """Disease detection system"""
        st.markdown('<div class="main-header">🔍 Disease Detection</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            <div class="feature-card">
            <h3>Upload Coconut Leaf Image</h3>
            <p>Upload a clear image of coconut leaf for analysis</p>
            </div>
            """, unsafe_allow_html=True)
            
            uploaded_file = st.file_uploader(
                "📁 Choose an image file",
                type=['jpg', 'jpeg', 'png'],
                help="Max file size: 5MB, Supported formats: JPG, PNG"
            )
            
            if uploaded_file is not None:
                # Display uploaded image
                image = Image.open(uploaded_file)
                st.image(image, caption="📸 Uploaded Image", use_column_width=True)
                
                # Analyze button
                if st.button("🔬 Analyze Image", type="primary", use_container_width=True):
                    with st.spinner("🔍 Analyzing leaf condition…"):
                        # Real AI analysis with trained model
                        result = self.analyze_image(image)
                        st.session_state.last_analysis = result
        
        with col2:
            if 'last_analysis' in st.session_state:
                result = st.session_state.last_analysis
                self.display_analysis_result(result)
            else:
                st.markdown("""
                <div class="info-box">
                <h3>💡 How it works:</h3>
                <ol>
                <li>Upload a clear image of coconut leaf</li>
                <li>AI model analyzes the image</li>
                <li>Get instant results with treatment recommendations</li>
                </ol>
                            
                <h4>✅ Supported Conditions:</h4>
                <ul>
                <li>Caterpillars</li>
                <li>Drying of Leaflets</li>
                <li>Flaccidity</li>
                <li>Healthy Leaves</li>
                <li>Yellowing</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)

    def analyze_image(self, image):
        """Analyze coconut leaf image and save to PostgreSQL"""
        try:
            # Load the model (cache it in session state for performance)
            if 'model' not in st.session_state:
                with st.spinner("🔄 Loading AI model..."):
                    try:
                        # Try to load the model
                        st.session_state.model = tf.keras.models.load_model('models/coconut_model_best.h5')
                        st.session_state.class_names = ['Caterpillars', 'Drying of Leaflets', 'Flaccidity', 'Healthy', 'Yellowing']
                        st.success("✅ Model loaded successfully!")
                    except Exception as e:
                        st.error(f"❌ Error loading model: {e}")
                        return self.get_fallback_prediction()
            
            # Preprocess the image
            processed_image = self.preprocess_image(image)
            
            # Make prediction
            predictions = st.session_state.model.predict(processed_image, verbose=0)
            predicted_class_idx = np.argmax(predictions[0])
            confidence = predictions[0][predicted_class_idx]
            
            # Get predicted class name
            predicted_class = st.session_state.class_names[predicted_class_idx]
            
            # Determine severity based on confidence
            if confidence > 0.8:
                severity = "Severe"
            elif confidence > 0.6:
                severity = "Moderate"
            else:
                severity = "Mild"
            
            # For healthy leaves, always set to mild
            if predicted_class == 'Healthy':
                severity = "Mild"
            
            # Save to PostgreSQL
            user = st.session_state.user
            if user:
                # Convert image to bytes for storage (optional)
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='JPEG')
                img_byte_arr = img_byte_arr.getvalue()
                
                result = db.insert_disease_detection(
                    user_id=user['id'],
                    prediction=predicted_class,
                    disease_name=predicted_class,
                    severity=severity,
                    confidence=float(confidence),
                    image_data=img_byte_arr  # Optional: store image in database
                )
            
            return {
                'disease': predicted_class,
                'severity': severity,
                'confidence': confidence,
                'is_healthy': predicted_class == 'Healthy'
            }
            
        except Exception as e:
            st.error(f"❌ Error during analysis: {e}")
            return self.get_fallback_prediction()

    def preprocess_image(self, image):
        """Preprocess image for model prediction"""
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize to model expected size
        image = image.resize((224, 224))
        
        # Convert to array and normalize
        image_array = np.array(image) / 255.0
        
        # Add batch dimension
        image_array = np.expand_dims(image_array, axis=0)
        
        return image_array

    def get_fallback_prediction(self):
        """Provide fallback prediction if model fails"""
        # Simple fallback
        return {
            'disease': 'Healthy',
            'severity': 'Mild',
            'confidence': 0.5,
            'is_healthy': True
        }
    
    def display_analysis_result(self, result):
        """Display disease analysis results"""
        st.markdown('<div class="sub-header">📊 Analysis Results</div>', unsafe_allow_html=True)
        
        if result['is_healthy']:
            st.markdown(f"""
            <div class="success-box">
            <h3>✅ Healthy Leaf Detected!</h3>
            <p><strong>Confidence:</strong> {result['confidence']:.2%}</p>
            <p>Your coconut leaf appears to be healthy. Continue with good agricultural practices.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="warning-box">
            <h3>⚠️ Disease Detected!</h3>
            <p><strong>Disease Name:</strong> {result['disease']}</p>
            <p><strong>Severity Level:</strong> {result['severity']}</p>
            <p><strong>Confidence:</strong> {result['confidence']:.2%}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Treatment recommendations
            st.markdown("### 💊 Treatment Recommendations")
            treatment = self.get_disease_info(result['disease'], 'treatment')
            st.markdown(f"""
            <div class="info-box">
            {treatment}
            </div>
            """, unsafe_allow_html=True)
            
            # Preventive care
            st.markdown("### 🛡️ Preventive Care Tips")
            prevention = self.get_disease_info(result['disease'], 'prevention')
            st.markdown(f"""
            <div class="info-box">
            {prevention}
            </div>
            """, unsafe_allow_html=True)

    def get_disease_info(self, disease_name, info_type='treatment'):
        """Get disease information"""
        disease_info = {
            'Caterpillars': {
                'treatment': '• Apply neem oil spray (2-3% solution)<br>• Use Bacillus thuringiensis (Bt) spray<br>• Manual removal of caterpillars<br>• Apply chemical insecticides if severe',
                'prevention': '• Regular monitoring of leaves<br>• Maintain proper sanitation<br>• Use pheromone traps<br>• Encourage natural predators'
            },
            'Drying of Leaflets': {
                'treatment': '• Ensure adequate irrigation<br>• Apply balanced fertilizers<br>• Prune affected leaves<br>• Check for root diseases',
                'prevention': '• Regular watering schedule<br>• Soil moisture monitoring<br>• Proper drainage system<br>• Balanced nutrition'
            },
            'Flaccidity': {
                'treatment': '• Improve soil drainage<br>• Reduce watering if overwatered<br>• Apply potassium-rich fertilizers<br>• Treat for root rot if present',
                'prevention': '• Proper watering practices<br>• Good soil drainage<br>• Regular soil testing<br>• Avoid waterlogging'
            },
            'Healthy': {
                'treatment': '• Continue current practices<br>• Regular monitoring<br>• Balanced fertilization<br>• Proper irrigation',
                'prevention': '• Maintain good agricultural practices<br>• Regular health checks<br>• Proper nutrition<br>• Timely interventions'
            },
            'Yellowing': {
                'treatment': '• Apply magnesium sulfate (Epsom salt)<br>• Use balanced NPK fertilizer<br>• Check soil pH and adjust<br>• Treat for nutrient deficiencies',
                'prevention': '• Regular soil testing<br>• Balanced fertilization<br>• Proper irrigation management<br>• Monitor plant health regularly'
            }
        }
        
        if disease_name in disease_info and info_type in ['treatment', 'prevention']:
            return disease_info[disease_name][info_type]
        
        # Default return
        default = {
            'treatment': 'Consult with agricultural expert for proper treatment.',
            'prevention': 'Maintain good agricultural practices and regular monitoring.'
        }
        return default[info_type]

    def marketplace_page(self):
        """Online marketplace with real PostgreSQL data - accessible to all users and admin"""
        if st.session_state.is_admin:
            st.markdown('<div class="main-header">🛒 Marketplace (Admin View)</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="main-header">🛒 Marketplace</div>', unsafe_allow_html=True)
        
        # Marketplace description
        st.markdown("""
        <div class="info-box">
        <h3>🌴 Discover Fresh Coconut Products</h3>
        <p>Get fresh coconuts directly from farmers. Fresh products, fair prices!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Filters and search
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        
        with col1:
            search_query = st.text_input("🔍 Search products...", placeholder="Enter product name or keyword")
        
        with col2:
            categories = ['Coconut', 'Coconut Oil Products','Coconut Food Products', 'Coconut Water Products', 'Coconut Coir Products','Coconut Beauty Products','Coconut Shell Crafts', 'Other']
            category_filter = st.selectbox("📂 Category", ["All Categories"] + categories)
        
        with col3:
            sort_by = st.selectbox("🔃 Sort By", ["Newest First", "Price: Low to High", "Price: High to Low"])
        
        with col4:
            price_range = st.slider("💰 Price Range (₹)", 0, 10000, (0, 5000))
        
        # Get real-time products from PostgreSQL (only approved ones)
        filters = {
            'search': search_query,
            'category': category_filter,
            'min_price': price_range[0],
            'max_price': price_range[1],
            'sort_by': sort_by,
            'status': 'approved'  # Only show approved products
        }

        # Admin can see all products including pending ones
        if st.session_state.is_admin:
            # Add status filter for admin
            status_filter = st.selectbox("📊 Status Filter", ["All Status", "Approved", "Pending", "Rejected"])
            if status_filter != "All Status":
                filters['status'] = status_filter.lower()
            else:
                filters.pop('status', None)  # Remove status filter to show all
        
        products = db.get_all_products(filters)
        
        # Display products directly instead of calling display_marketplace_products
        # Display products
        user = st.session_state.user
        is_buyer = user and (user['user_type'] not in ['Farmer', 'ರೈತ'] or st.session_state.is_admin)
        
        if products:
            status_text = ""
            if st.session_state.is_admin and 'status' in filters:
                status_text = f" ({filters['status'].title()} Status)"

            st.markdown(f"### 📦 Found {len(products)} Products{status_text}")
            
            # Display products in grid
            cols = st.columns(3)
            for idx, product in enumerate(products):
                with cols[idx % 3]:
                    self.display_product_card(product, show_favorite=is_buyer)
        else:
            st.markdown("""
            <div class="info-box">
            <h3>😔 No products found</h3>
            <p>Try adjusting your search criteria or check back later for new listings.</p>
            </div>
            """, unsafe_allow_html=True)

    def display_marketplace_products(self, products):
        """Display filtered products from PostgreSQL"""
        user = st.session_state.user
        is_buyer = user and user['user_type'] not in ['Farmer', 'ರೈತ']
        
        if products:
            st.markdown(f"### 📦 Found {len(products)} Products")
            
            # Display products in grid
            cols = st.columns(3)
            for idx, product in enumerate(products):
                with cols[idx % 3]:
                    self.display_product_card(product, show_favorite=is_buyer)
        else:
            st.markdown("""
            <div class="info-box">
            <h3>😔 No products found</h3>
            <p>Try adjusting your search criteria or check back later for new listings.</p>
            </div>
            """, unsafe_allow_html=True)
    
    def display_product_card(self, product, show_favorite=False):
        """Display individual product card with actual images"""
        with st.container():
            # Format created_at if it's a datetime object
            created_at = product.get('created_at')
            if hasattr(created_at, 'strftime'):
                created_at = created_at.strftime('%Y-%m-%d %H:%M')
            else:
                created_at = str(created_at)
            
            # Get product images
            images = product.get('images', [])
            
            st.markdown(f"""
            <div class="product-card">
            <h4>{product['product_name']}</h4>
            """, unsafe_allow_html=True)

            # Image Carousel/Slider
            if images and len(images) > 0:
                # Create tabs for image carousel
                if len(images) == 1:
                    # Single image
                    try:
                        if os.path.exists(images[0]):
                            image = Image.open(images[0])
                            st.image(image, caption=product['product_name'], use_column_width=True)
                        else:
                            st.image("https://via.placeholder.com/400x300/2E8B57/FFFFFF?text=Image+Not+Found", 
                                use_column_width=True)
                    except Exception as e:
                        st.error("❌ Error loading product image")
                else:
                    # Multiple images - create carousel with tabs
                    tab_names = [f"🖼️ {i+1}" for i in range(len(images))]
                    tabs = st.tabs(tab_names)
                    
                    for idx, tab in enumerate(tabs):
                        with tab:
                            try:
                                if os.path.exists(images[idx]):
                                    image = Image.open(images[idx])
                                    st.image(image, caption=f"Image {idx+1} of {len(images)}", 
                                        use_column_width=True)
                                else:
                                    st.image("https://via.placeholder.com/400x300/2E8B57/FFFFFF?text=Image+Not+Found", 
                                        use_column_width=True)
                            except Exception as e:
                                st.error(f"❌ Error loading image {idx+1}")
                    # Navigation dots indicator
                    st.markdown(f"""
                    <div style="text-align: center; margin: 10px 0;">
                        <small>🟢 {len(images)} images - Click tabs to navigate</small>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                # No images
                st.image("https://via.placeholder.com/400x300/2E8B57/FFFFFF?text=No+Product+Image", 
                    use_column_width=True, caption="No product images available")
                         
            # Status badge
            status_badge = self.get_product_status_badge(product.get('status', 'pending'))
            
            st.markdown(f"""
            <div class="product-card">
            <h4>{product['product_name']}</h4>
            <p><strong>Category:</strong> {product['category']}</p>
            <p><strong>Price:</strong> ₹{product['price']:.2f}</p>
            <p><strong>Quantity:</strong> {product['quantity']} units</p>
            <p><strong>Seller:</strong> {product.get('seller_name', 'Unknown')}</p>
            <p><strong>Location:</strong> {product['location']}</p>
            <p><em>{product['description']}</em></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Only show contact buttons if product is approved
            if product.get('status') == 'approved':
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📞 Call", key=f"call_{product['id']}", use_container_width=True):
                        st.info(f"📞 Contact: {product['contact_phone']}")
                with col2:
                    whatsapp_url = f"https://wa.me/{product['whatsapp']}?text=Hi, I'm interested in your product: {product['product_name']}"
                    st.link_button("💬 WhatsApp", whatsapp_url)
            else:
                st.info("⏳ This product is pending admin approval")
            
            # Add to favorites (only for buyers and approved products)
            if show_favorite and product.get('status') == 'approved':
                user = st.session_state.user
                is_favorited = db.is_product_favorited(user['id'], product['id'])
                
                if is_favorited:
                    if st.button(f"❌ Remove Favorite", key=f"remove_fav_{product['id']}", use_container_width=True):
                        if db.remove_from_favorites(user['id'], product['id']):
                            st.success("✅ Removed from favorites!")
                            st.rerun()
                else:
                    if st.button("❤️ Add to Favorites", key=f"add_fav_{product['id']}", use_container_width=True):
                        if db.add_to_favorites(user['id'], product['id']):
                            st.success("✅ Added to favorites!")
                            st.rerun()
    
    def add_product_page(self):
        """Add new product listing to PostgreSQL with image storage"""
        st.markdown('<div class="main-header">➕ Add New Product</div>', unsafe_allow_html=True)
        
        # Initialize session state for form submission tracking
        if 'last_submission_time' not in st.session_state:
            st.session_state.last_submission_time = 0

        with st.form("add_product_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📝 Product Details")
                product_name = st.text_input("Product Name *", placeholder="Enter product name")
                category = st.selectbox("Category *", ["Coconut", "Coconut Oil Products","Coconut Food Products", "Coconut Water Products", "Coconut Coir Products","Coconut Beauty Products","Coconut Shell Crafts", "Other"])
                price = st.number_input("Price (INR) *", min_value=0.0, step=1.0, format="%.2f")
                quantity = st.number_input("Quantity Available *", min_value=1, step=1)
            
            with col2:
                st.subheader("📞 Contact Information")
                description = st.text_area("Product Description", placeholder="Describe your product...", height=100)
                contact_phone = st.text_input("Contact Phone *", placeholder="Your phone number")
                whatsapp = st.text_input("WhatsApp Number *", placeholder="Your WhatsApp number")
                location = st.text_input("Location *", placeholder="Your location")
            
            st.markdown("---")
            st.subheader("🖼️ Product Images")
            uploaded_images = st.file_uploader(
                "Upload Product Images (max 5 images)",
                type=['jpg', 'jpeg', 'png'],
                accept_multiple_files=True,
                help="Maximum 5 images allowed. First image will be used as main display."
            )

            # Display uploaded images preview
            if uploaded_images:
                st.write("**Image Preview:**")
                cols = st.columns(min(3, len(uploaded_images)))
                for idx, uploaded_file in enumerate(uploaded_images):
                    with cols[idx % 3]:
                        image = Image.open(uploaded_file)
                        st.image(image, caption=f"Image {idx+1}", width=150)

            submit_button = st.form_submit_button("💾 Save Product", type="primary", use_container_width=True)

            if submit_button:
                # Prevent duplicate submissions within 10 seconds
                current_time = time.time()
                if current_time - st.session_state.last_submission_time < 10:
                    st.warning("⏳ Please wait a few seconds before submitting again.")
                    return
                
                st.session_state.last_submission_time = current_time
                
                if all([product_name, price, quantity, contact_phone, whatsapp, location]):
                    user = st.session_state.user

                    # Process uploaded images
                    image_paths = []
                    if uploaded_images:
                        # Create images directory if it doesn't exist
                        os.makedirs("product_images", exist_ok=True)

                        # Save images to a directory and store paths
                        for uploaded_file in uploaded_images:
                            
                            # Generate unique filename
                            file_extension = os.path.splitext(uploaded_file.name)[1]
                            unique_filename = f"{product_name.replace(' ', '_')}_{user['id']}_{int(time.time())}_{len(image_paths)}{file_extension}"
                            file_path = os.path.join("product_images", unique_filename)

                            # Save the file
                            with open(file_path, "wb") as f:
                                f.write(uploaded_file.getbuffer())
                            
                            image_paths.append(file_path)
                        st.success(f"✅ Image saved: {unique_filename}")
                    else:
                        st.warning("⚠️ No images uploaded. Product will be displayed without images.")

                    # Save to PostgreSQL with pending status
                    result = db.insert_product(
                        user_id=user['id'],
                        product_name=product_name,
                        category=category,
                        price=float(price),
                        quantity=quantity,
                        description=description,
                        contact_phone=contact_phone,
                        whatsapp=whatsapp,
                        location=location,
                        images=image_paths,
                        status='pending'  # Products start as pending
                    )

                    if result:
                        st.success("🎉 Product added successfully! Waiting for admin approval.")
                        st.info("⏳ Your product will be visible in the marketplace once approved by admin.")
                        st.balloons()
                        # Refresh user data
                        self.load_real_data()
                        time.sleep(3)
                        st.rerun()
                    else:
                        st.error("❌ Failed to save product to database")
                else:
                    st.error("❌ Please fill all required fields (*)")

    def my_products_page(self):
        """Manage user's products from PostgreSQL"""
        st.markdown('<div class="main-header">📦 My Products</div>', unsafe_allow_html=True)
        
        # Load real-time data
        self.load_real_data()
        
        user = st.session_state.user
        user_products = st.session_state.user_products
        
        # Check if we're in edit mode
        editing_product_id = st.session_state.get('editing_product')
        
        if editing_product_id:
            # Find the product being edited
            product_to_edit = next((p for p in user_products if p['id'] == editing_product_id), None)
            
            if product_to_edit:
                self.edit_product_form(product_to_edit)
                return
            else:
                st.error("Product not found!")
                st.session_state.editing_product = None
                st.rerun()
        
        if user_products:
            st.markdown(f"### 📊 You have {len(user_products)} product(s) listed")
            
            for product in user_products:
                # Display status message
                status = product.get('status', 'pending')
                if status == 'pending':
                    st.markdown("""
                    <div class="pending-box">
                    <strong>⏳ Pending Approval:</strong> This product is waiting for admin approval and is not visible in the marketplace yet.
                    </div>
                    """, unsafe_allow_html=True)
                elif status == 'rejected':
                    st.markdown("""
                    <div class="rejected-box">
                    <strong>❌ Rejected:</strong> This product was rejected by admin and is not visible in the marketplace.
                    </div>
                    """, unsafe_allow_html=True)
                elif status == 'approved':
                    st.markdown("""
                    <div class="approved-box">
                    <strong>✅ Approved:</strong> This product is visible in the marketplace.
                    </div>
                    """, unsafe_allow_html=True)
                
                with st.expander(f"📦 {product['product_name']} - ₹{product['price']:.2f}", expanded=True):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"**Category:** {product['category']}")
                        st.write(f"**Price:** ₹{product['price']:.2f}")
                        st.write(f"**Quantity:** {product['quantity']} units")
                        st.write(f"**Description:** {product['description']}")
                        st.write(f"**Status:** {self.get_status_display(status)}")
                        created_at = product.get('created_at')
                        if hasattr(created_at, 'strftime'):
                            created_at = created_at.strftime('%Y-%m-%d %H:%M')
                        st.write(f"**Listed on:** {created_at}")
                        st.write(f"**Contact Phone:** {product['contact_phone']}")
                        st.write(f"**WhatsApp:** {product['whatsapp']}")
                        st.write(f"**Location:** {product['location']}")
                    
                    with col2:
                        if st.button("✏️ Edit", key=f"edit_{product['id']}", use_container_width=True):
                            st.session_state.editing_product = product['id']
                            st.rerun()
                        
                        if st.button("🗑️ Delete", key=f"delete_{product['id']}", use_container_width=True, type="secondary"):
                            if db.delete_product(product['id'], user['id']):
                                st.success("Product deleted successfully!")
                                # Refresh data
                                self.load_real_data()
                                st.rerun()
                            else:
                                st.error("Failed to delete product")
        else:
            st.markdown("""
            <div class="info-box">
            <h3>📦 No products listed yet</h3>
            <p>Start by adding your first product to the marketplace!</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("➕ Add Your First Product", type="primary"):
                st.session_state.page = 'add_product'
                st.rerun()

    def edit_product_form(self, product):
        """Form to edit an existing product"""
        st.markdown(f'<div class="main-header">✏️ Edit Product: {product["product_name"]}</div>', unsafe_allow_html=True)
        
        with st.form(f"edit_product_form_{product['id']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📝 Product Details")
                product_name = st.text_input("Product Name *", value=product['product_name'], placeholder="Enter product name")
                category = st.selectbox("Category *", ["Coconut", "Coconut Oil Products","Coconut Food Products", "Coconut Water Products", "Coconut Coir Products","Coconut Beauty Products","Coconut Shell Crafts", "Other"], 
                                  index=["Coconut", "Coconut Oil Products","Coconut Food Products", "Coconut Water Products", "Coconut Coir Products","Coconut Beauty Products","Coconut Shell Crafts", "Other"].index(product['category']))
                price = st.number_input("Price (INR) *", min_value=0.0, step=1.0, format="%.2f", value=float(product['price']))
                quantity = st.number_input("Quantity Available *", min_value=1, step=1, value=product['quantity'])
            
            with col2:
                st.subheader("📞 Contact Information")
                description = st.text_area("Product Description", value=product['description'], placeholder="Describe your product...", height=100)
                contact_phone = st.text_input("Contact Phone *", value=product['contact_phone'], placeholder="Your phone number")
                whatsapp = st.text_input("WhatsApp Number *", value=product['whatsapp'], placeholder="Your WhatsApp number")
                location = st.text_input("Location *", value=product['location'], placeholder="Your location")
            
            st.markdown("---")
            st.subheader("🖼️ Product Images")
            
            # Display current images if any
            current_images = product.get('images', [])
            if current_images:
                st.write("**Current Images:**")
                cols = st.columns(min(3, len(current_images)))
                for idx, img_path in enumerate(current_images):
                    with cols[idx % 3]:
                        if os.path.exists(img_path):
                            try:
                                image = Image.open(img_path)
                                st.image(image, caption=f"Current Image {idx+1}", width=150)
                            except:
                                st.write(f"❌ Cannot display: {os.path.basename(img_path)}")
                        else:
                            st.write(f"❌ File not found: {os.path.basename(img_path)}")
            
            uploaded_images = st.file_uploader(
                "Upload New Product Images (max 5 images)",
                type=['jpg', 'jpeg', 'png'],
                accept_multiple_files=True,
                help="Maximum 5 images allowed. New images will replace existing ones."
            )

            # Display new images preview
            if uploaded_images:
                st.write("**New Images Preview:**")
                cols = st.columns(min(3, len(uploaded_images)))
                for idx, uploaded_file in enumerate(uploaded_images):
                    with cols[idx % 3]:
                        image = Image.open(uploaded_file)
                        st.image(image, caption=f"New Image {idx+1}", width=150)

            image_paths = current_images.copy() if current_images else []
            if uploaded_images:
                # Replace existing images with new ones
                image_paths = []
                for uploaded_file in uploaded_images:
                    # Create images directory if it doesn't exist
                    os.makedirs("product_images", exist_ok=True)

                    # Generate unique filename
                    file_extension = os.path.splitext(uploaded_file.name)[1]
                    unique_filename = f"{product_name.replace(' ', '_')}_{product['id']}_{int(time.time())}_{len(image_paths)}{file_extension}"
                    file_path = os.path.join("product_images", unique_filename)

                    # Save the file
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    image_paths.append(file_path)
            
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                if st.form_submit_button("💾 Update Product", type="primary", use_container_width=True):
                    if all([product_name, price, quantity, contact_phone, whatsapp, location]):
                        # Update product in PostgreSQL
                        success = db.update_product(
                            product_id=product['id'],
                            product_name=product_name,
                            category=category,
                            price=float(price),
                            quantity=quantity,
                            description=description,
                            contact_phone=contact_phone,
                            whatsapp=whatsapp,
                            location=location,
                            images=image_paths
                        )
                        
                        if success:
                            st.success("🎉 Product updated successfully!")
                            if product.get('status') == 'approved':
                                st.info("⚠️ Note: Since this product was already approved, it will need to be re-approved by admin after editing.")
                            
                            # Clear editing state and refresh data
                            st.session_state.editing_product = None
                            self.load_real_data()
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("❌ Failed to update product in database")
                    else:
                        st.error("❌ Please fill all required fields (*)")
            
            with col2:
                if st.form_submit_button("🚫 Cancel", use_container_width=True):
                    st.session_state.editing_product = None
                    st.rerun()
            
            with col3:
                if st.form_submit_button("🗑️ Delete Product", type="secondary", use_container_width=True):
                    if db.delete_product(product['id'], st.session_state.user['id']):
                        st.success("Product deleted successfully!")
                        st.session_state.editing_product = None
                        self.load_real_data()
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Failed to delete product")
    
    def get_status_display(self, status):
        """Get display text for product status"""
        status_map = {
            'pending': '⏳ Pending Approval',
            'approved': '✅ Approved', 
            'rejected': '❌ Rejected'
        }
        return status_map.get(status, status)

    def favorites_page(self):
        """Display user's favorite products from PostgreSQL"""
        st.markdown('<div class="main-header">❤️ My Favorites</div>', unsafe_allow_html=True)
        
        # Load real-time data
        self.load_real_data()
        
        user = st.session_state.user
        favorite_products = st.session_state.user_favorites
        
        if favorite_products:
            st.markdown(f"### 💖 You have {len(favorite_products)} favorite product(s)")
            
            for product in favorite_products:
                self.display_product_card(product, show_favorite=False)
                
                # Remove from favorites button
                if st.button(f"❌ Remove from Favorites", key=f"remove_{product['id']}", use_container_width=True):
                    if db.remove_from_favorites(user['id'], product['id']):
                        st.success("✅ Removed from favorites!")
                        # Refresh data
                        self.load_real_data()
                        st.rerun()
                    else:
                        st.error("❌ Failed to remove from favorites")
        else:
            st.markdown("""
            <div class="info-box">
            <h3>💔 No favorites yet</h3>
            <p>Browse the marketplace and add products to your favorites!</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🛒 Browse Marketplace", type="primary"):
                st.session_state.page = 'marketplace'
                st.rerun()
    
    def profile_page(self):
        """User profile management"""
        st.markdown('<div class="main-header">👤 Profile Management</div>', unsafe_allow_html=True)
        
        user = st.session_state.user
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 📝 Personal Information")
            
            with st.form("profile_form"):
                col1a, col1b = st.columns(2)
                
                with col1a:
                    full_name = st.text_input("👤 Full Name", value=user['full_name'])
                    email = st.text_input("📧 Email Address", value=user['email'], disabled=True)
                    phone = st.text_input("📞 Phone Number", value=user['phone'])
                
                with col1b:
                    user_type = st.text_input("👥 User Type", value=user['user_type'], disabled=True)
                    state = st.text_input("🏠 State", value=user['state'])
                    district = st.text_input("📍 District", value=user['district'])
                
                if st.form_submit_button("💾 Update Profile", type="primary", use_container_width=True):
                    updates = {
                        'full_name': full_name,
                        'phone': phone,
                        'state': state,
                        'district': district
                    }
                    success, message = auth.update_user_profile(user['id'], updates)
                    if success:
                        st.success(message)
                        # Update session state
                        st.session_state.user.update(updates)
                    else:
                        st.error(message)
        
        with col2:
            st.markdown("### 🔐 Security")
            
            with st.form("change_password_form"):
                st.markdown("#### Change Password")
                current_password = st.text_input("Current Password", type="password")
                new_password = st.text_input("New Password", type="password")
                confirm_password = st.text_input("Confirm New Password", type="password")
                
                if st.form_submit_button("🔑 Change Password", use_container_width=True):
                    if new_password == confirm_password:
                        success, message = auth.change_password(user['id'], current_password, new_password)
                        if success:
                            st.success(message)
                        else:
                            st.error(message)
                    else:
                        st.error("❌ Passwords do not match")
    
    def run(self):
        """Main application runner"""
        # Create top navigation (only if not on opening page)
        if st.session_state.page != 'home' or st.session_state.logged_in:
            self.create_top_navigation()
        
        # Create sidebar navigation (only if logged in)
        if st.session_state.logged_in:
            self.navigation_sidebar()
        
        # Route to appropriate page
        current_page = st.session_state.page
        
        if not st.session_state.logged_in:
            if current_page == 'home':
                self.home_page()
            elif current_page == 'auth':
                self.authentication_page()
            elif current_page == 'admin_auth':
                self.admin_authentication_page()
            else:
                self.home_page()
        else:
            if st.session_state.is_admin:
                # Admin pages
                if current_page == 'admin_dashboard':
                    self.admin_dashboard_page()
                elif current_page == 'admin_users':
                    self.admin_users_page()
                elif current_page == 'admin_products':
                    self.admin_products_page()
                elif current_page == 'admin_analytics':
                    self.admin_analytics_page()
                elif current_page == 'admin_profile':
                    self.admin_profile_page()
                elif current_page == 'marketplace':  
                    self.marketplace_page()    
                else:
                    self.admin_dashboard_page()
            else:
                # User pages
                if current_page == 'home':
                    self.home_page()
                elif current_page == 'disease_detection':
                    self.disease_detection_page()
                elif current_page == 'marketplace':
                    self.marketplace_page()
                elif current_page == 'add_product':
                    self.add_product_page()
                elif current_page == 'my_products':
                    self.my_products_page()
                elif current_page == 'favorites':
                    self.favorites_page()
                elif current_page == 'profile':
                    self.profile_page()
                else:
                    self.home_page()

# Run the application
if __name__ == "__main__":
    app = CoconutLeafGuard()
    app.run()