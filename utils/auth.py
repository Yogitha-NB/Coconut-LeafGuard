import streamlit as st
from .database import db

class Auth:
    def __init__(self):
        self.current_user = None
    
    def register_user(self, full_name, email, phone, password, user_type, state, district):
        """Register a new user"""
        return db.register_user(full_name, email, phone, password, user_type, state, district)
    
    def login_user(self, email, password):
        """Login user"""
        success, result = db.authenticate_user(email, password)
        if success:
            self.current_user = result
            st.session_state.logged_in = True
            st.session_state.user = result
            return True, "Login successful!"
        else:
            return False, result
    
    def logout_user(self):
        """Logout user"""
        self.current_user = None
        st.session_state.logged_in = False
        if 'user' in st.session_state:
            st.session_state.user = None
        st.session_state.is_admin = False
    
    def get_current_user(self):
        """Get current logged in user"""
        if st.session_state.logged_in and 'user' in st.session_state:
            return st.session_state.user
        return None
    
    def password_strength(self, password):
        """Check password strength"""
        score = 1
        if len(password) >= 8:
            score += 1
        if any(c.islower() for c in password) and any(c.isupper() for c in password):
            score += 1
        if any(c.isdigit() for c in password):
            score += 1
        if any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?`~' for c in password):
            score += 1
        return min(score, 5)
    
    def update_user_profile(self, user_id, updates):
        """Update user profile"""
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            
            set_clause = ", ".join([f"{key} = %s" for key in updates.keys()])
            values = list(updates.values())
            values.append(user_id)
            
            cur.execute(f"""
                UPDATE users 
                SET {set_clause}
                WHERE id = %s
            """, values)
            
            conn.commit()
            cur.close()
            
            # Update session state
            if st.session_state.logged_in and 'user' in st.session_state:
                st.session_state.user.update(updates)
            
            return True, "Profile updated successfully"
        except Exception as e:
            return False, f"Error updating profile: {e}"
    
    def change_password(self, user_id, current_password, new_password):
        """Change user password"""
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            
            # Verify current password
            cur.execute("SELECT id FROM users WHERE id = %s AND password = %s", (user_id, current_password))
            if not cur.fetchone():
                return False, "Current password is incorrect"
            
            # Update password
            cur.execute("UPDATE users SET password = %s WHERE id = %s", (new_password, user_id))
            conn.commit()
            cur.close()
            
            return True, "Password changed successfully"
        except Exception as e:
            return False, f"Error changing password: {e}"

# Create global auth instance
auth = Auth()