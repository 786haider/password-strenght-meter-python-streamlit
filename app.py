  #Password_Strenght_Meter

import streamlit as st
import re
import secrets
import string

def generate_strong_password(length=12):
    """
    Generate a strong, random password with a mix of characters.
    
    Args:
        length (int): Desired password length (default 12)
    
    Returns:
        str: A randomly generated strong password
    """
    # Define character sets
    uppercase_letters = string.ascii_uppercase
    lowercase_letters = string.ascii_lowercase
    digits = string.digits
    special_characters = '!@#$%^&*'
    
    # Ensure at least one character from each required set
    password = [
        secrets.choice(uppercase_letters),
        secrets.choice(lowercase_letters),
        secrets.choice(digits),
        secrets.choice(special_characters)
    ]
    
    # Fill the rest of the password with random characters
    all_characters = uppercase_letters + lowercase_letters + digits + special_characters
    password.extend(secrets.choice(all_characters) for _ in range(length - 4))
    
    # Shuffle the password characters
    secrets.SystemRandom().shuffle(password)
    
    return ''.join(password)

def check_password_strength(password):
    """
    Evaluate password strength based on multiple criteria.
    
    Args:
        password (str): Password to evaluate
    
    Returns:
        dict: Password evaluation results
    """
    # Initialize score and feedback
    score = 0
    feedback = []
    
    # Length Check (8-16 characters recommended)
    if len(password) >= 8:
        score += 1
        if len(password) >= 12:
            score += 1
    else:
        feedback.append("❌ Password should be at least 8 characters long.")
    
    # Uppercase Check
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("❌ Include at least one uppercase letter.")
    
    # Lowercase Check
    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("❌ Include at least one lowercase letter.")
    
    # Digit Check
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("❌ Add at least one number (0-9).")
    
    # Special Character Check
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("❌ Include at least one special character (!@#$%^&*).")
    
    # Blacklist Common Passwords
    common_passwords = [
        'password', '123456', 'qwerty', 'admin', 
        'letmein', 'welcome', 'monkey', 'password123'
    ]
    if any(common_pass in password.lower() for common_pass in common_passwords):
        score = min(score - 1, 0)
        feedback.append("❌ Avoid common password patterns.")
    
    # Determine Strength Rating
    if score == 5:
        strength = "Strong 💪"
        status_color = "green"
        status_message = "✅ Excellent! Your password is highly secure."
    elif score == 4:
        strength = "Moderate 🟡"
        status_color = "orange"
        status_message = "⚠️ Good password, but consider adding complexity."
    else:
        strength = "Weak 🚨"
        status_color = "red"
        status_message = "❌ Weak Password - Please improve using suggestions."
    
    return {
        'score': score,
        'strength': strength,
        'status_message': status_message,
        'status_color': status_color,
        'feedback': feedback
    }

def main():
    # Set page configuration
    st.set_page_config(
        page_title="🔐 Password Strength Meter By Haider",
        page_icon="🔑",
        layout="centered"
    )

    # Title and description
    st.title("🔐 Password Strength Meter By Haider")
    st.markdown("---")
    st.write("Evaluate and improve your password security!")

    # Tabs for different functionalities
    tab1, tab2 = st.tabs(["Check Password", "Generate Password"])

    with tab1:
        st.header("Password Strength Checker")
        
        # Password input
        password = st.text_input("Enter your password", type="password")
        
        # Check password when button is clicked
        if st.button("Check Strength", key="check_btn"):
            if password:
                # Evaluate password
                result = check_password_strength(password)
                
                # Display strength with color
                st.markdown(f"**Strength:** <span style='color:{result['status_color']}'>{result['strength']}</span>", 
                            unsafe_allow_html=True)
                
                # Status message
                st.markdown(f"**Status:** {result['status_message']}")
                
                # Feedback suggestions
                if result['feedback']:
                    st.subheader("Improvement Suggestions:")
                    for suggestion in result['feedback']:
                        st.markdown(f"- {suggestion}")
            else:
                st.warning("Please enter a password to check.")

    with tab2:
        st.header("Strong Password Generator")
        
        # Password length slider
        length = st.slider("Password Length", min_value=8, max_value=20, value=12)
        
        # Generate password button
        if st.button("Generate Strong Password", key="gen_btn"):
            # Generate password
            generated_password = generate_strong_password(length)
            
            # Display generated password
            st.success(f"Generated Password: {generated_password}")
            
            # Evaluate generated password
            result = check_password_strength(generated_password)
            st.markdown(f"**Strength:** <span style='color:{result['status_color']}'>{result['strength']}</span>", 
                        unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("""
    💡 **Password Security Tips:**
    - Use a mix of uppercase, lowercase, numbers, and special characters
    - Avoid common words or personal information
    - Use unique passwords for different accounts
    - Consider using a password manager
    """)

if __name__ == "__main__":
    main()