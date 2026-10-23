import hashlib
from database import get_connection

def verify_admin(username, password):
    """Verify admin credentials against stored hash."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM admins WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    if row:
        stored_hash = row["password_hash"]
        input_hash = hashlib.sha256(password.encode()).hexdigest()
        return stored_hash == input_hash
    return False

def change_password(username, old_password, new_password):
    """Verify old password and update to new password securely."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM admins WHERE username = ?", (username,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return False, "User not found."

    stored_hash = row["password_hash"]
    input_old_hash = hashlib.sha256(old_password.encode()).hexdigest()

    if stored_hash != input_old_hash:
        conn.close()
        return False, "Incorrect current password."

    new_hash = hashlib.sha256(new_password.encode()).hexdigest()
    try:
        cursor.execute("UPDATE admins SET password_hash = ? WHERE username = ?", (new_hash, username))
        conn.commit()
        success = True
        msg = "Password updated successfully."
    except Exception as e:
        success = False
        msg = f"Error: {str(e)}"
    finally:
        conn.close()
    return success, msg