import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import string
import random
import pyperclip
import platform
from functools import partial
import time

# Configuration dictionary for easy customization
CONFIG = {
    'bg': '#2B2D42',
    'fg': '#EDF2F4',
    'accent': '#007BFF',
    'font': ('Roboto Mono', 12),
    'button_font': ('Roboto Mono', 11, 'bold'),
    'progress_colors': {
        'weak': '#FF5555',
        'medium': '#FFD700',
        'strong': '#28A745'
    }
}

class Tooltip:
    """Custom tooltip class for widgets."""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x, y = self.widget.winfo_pointerxy()
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x+10}+{y+10}")
        label = tk.Label(self.tooltip, text=self.text, bg="#FFFFE0", fg="black",
                         relief="solid", borderwidth=1, font=("Helvetica", 10))
        label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

def debounce(wait):
    """Decorator to debounce function calls."""
    def decorator(func):
        last_call = 0
        def wrapper(*args, **kwargs):
            nonlocal last_call
            now = time.time()
            if now - last_call >= wait:
                last_call = now
                return func(*args, **kwargs)
        return wrapper
    return decorator

def check_strength(pw):
    """Evaluate password strength and provide improvement suggestions."""
    suggestions = []
    strength = 0

    if len(pw) >= 8:
        strength += 1
    else:
        suggestions.append("Use at least 8 characters")

    if any(c.islower() for c in pw):
        strength += 1
    else:
        suggestions.append("Add lowercase letters")

    if any(c.isupper() for c in pw):
        strength += 1
    else:
        suggestions.append("Add uppercase letters")

    if any(c.isdigit() for c in pw):
        strength += 1
    else:
        suggestions.append("Add numbers")

    if any(c in string.punctuation for c in pw):
        strength += 1
    else:
        suggestions.append("Add special characters")

    if len(pw) >= 16:
        strength += 1
        suggestions.append("Great length! Consider adding more complexity.")

    return min(strength, 5), suggestions

@debounce(0.3)
def update_strength_bar(*args):
    """Update strength bar and suggestions based on input password."""
    pw = password_var.get()
    strength, suggestions = check_strength(pw)
    strength_bar['value'] = strength * 20
    strength_label.config(text=f"Strength: {strength}/5")
    suggestions_text.set("No suggestions" if not suggestions else "\n".join(suggestions))
    
    if strength <= 2:
        strength_bar.configure(bootstyle="danger")
    elif strength <= 4:
        strength_bar.configure(bootstyle="warning")
    else:
        strength_bar.configure(bootstyle="success")

def toggle_password():
    """Toggle password visibility."""
    entry_password.configure(show='' if show_var.get() else '•')

def generate_password():
    """Generate a random password based on selected length."""
    length = round(length_var.get())
    if length < 8:
        messagebox.showwarning("Invalid Length", "Password length must be at least 8 characters.")
        length_var.set(12)
        length_label.configure(text="12")
        return

    characters = string.ascii_letters + string.digits + string.punctuation
    new_pw = ''.join(random.choices(characters, k=length))
    generated_password_var.set(new_pw)
    generated_pw_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")  # Use grid instead of pack
    copy_generated_button.configure(state="normal")
    password_history.append(new_pw)
    update_history_list()
    update_generated_strength()

def update_generated_strength():
    """Update strength display for generated password."""
    pw = generated_password_var.get()
    strength, _ = check_strength(pw)
    generated_strength_label.configure(text=f"Generated Strength: {strength}/5")

def copy_password():
    """Copy input password to clipboard."""
    pw = password_var.get()
    if pw:
        pyperclip.copy(pw)
        messagebox.showinfo("Copied", "Password copied to clipboard!")
    else:
        messagebox.showwarning("Empty Password", "Please enter a password to copy.")

def copy_generated_password():
    """Copy generated password to clipboard."""
    pw = generated_password_var.get()
    if pw:
        pyperclip.copy(pw)
        messagebox.showinfo("Copied", "Generated password copied to clipboard!")
    else:
        messagebox.showwarning("Empty Password", "No generated password to copy.")

def update_length_label(*args):
    """Update the length label to show integer value."""
    length = round(length_var.get())
    length_label.configure(text=str(length))

def clear_history():
    """Clear the password history."""
    password_history.clear()
    history_text.set("No passwords in history")
    generated_password_var.set("")
    generated_pw_frame.grid_forget()  # Use grid_forget instead of pack_forget

def update_history_list():
    """Update the displayed password history."""
    history_text.set("Recent Passwords:\n" + "\n".join(password_history[-5:]) if password_history else "No passwords in history")

def create_input_section(root):
    """Create the input password section."""
    input_frame = ttk.Frame(root)
    input_frame.grid(row=0, column=0, padx=20, pady=15, sticky="ew")

    ttk.Label(input_frame, text="Enter Password:", font=CONFIG['font']).grid(row=0, column=0, sticky="w")
    password_subframe = ttk.Frame(input_frame)
    password_subframe.grid(row=1, column=0, sticky="ew", pady=(5, 10))
    global entry_password
    entry_password = ttk.Entry(password_subframe, textvariable=password_var, show='•', width=30)
    entry_password.grid(row=0, column=0, padx=(0, 10))
    entry_password.focus()
    Tooltip(entry_password, "Enter your password to check its strength")
    ttk.Button(password_subframe, text="Copy", command=copy_password, style='secondary.TButton').grid(row=0, column=1)
    ttk.Checkbutton(input_frame, text="Show Password", variable=show_var, command=toggle_password).grid(row=2, column=0, sticky="w")

    global strength_label, strength_bar
    strength_label = ttk.Label(input_frame, text="Strength: 0/5", font=CONFIG['font'])
    strength_label.grid(row=3, column=0, sticky="w", pady=(10, 5))
    strength_bar = ttk.Progressbar(input_frame, length=300, maximum=100, bootstyle="danger")
    strength_bar.grid(row=4, column=0, sticky="ew", pady=5)

    ttk.Label(input_frame, text="Suggestions:", font=CONFIG['font']).grid(row=5, column=0, sticky="w", pady=(10, 5))
    global suggestions_label
    suggestions_label = ttk.Label(input_frame, textvariable=suggestions_text, style="danger.TLabel", font=CONFIG['font'])
    suggestions_label.grid(row=6, column=0, sticky="w")

def create_generate_section(root):
    """Create the password generation section."""
    generate_frame = ttk.Frame(root)
    generate_frame.grid(row=1, column=0, padx=20, pady=15, sticky="ew")

    ttk.Label(generate_frame, text="Password Length:", font=CONFIG['font']).grid(row=0, column=0, sticky="w")
    ttk.Scale(generate_frame, from_=8, to_=20, orient='horizontal', variable=length_var, length=300).grid(row=1, column=0, sticky="ew", pady=5)
    global length_label
    length_label = ttk.Label(generate_frame, text="12", font=CONFIG['font'])
    length_label.grid(row=2, column=0, sticky="w", pady=(0, 10))
    generate_button = ttk.Button(generate_frame, text="Generate Password", command=generate_password, style='primary.TButton', width=25)
    generate_button.grid(row=3, column=0, pady=10)
    Tooltip(generate_button, "Generate a random password")

    global generated_pw_frame, copy_generated_button, generated_strength_label
    generated_pw_frame = ttk.Frame(root)
    generated_pw_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
    ttk.Label(generated_pw_frame, text="Generated Password:", font=CONFIG['font']).grid(row=0, column=0, sticky="w")
    generated_password_subframe = ttk.Frame(generated_pw_frame)
    generated_password_subframe.grid(row=1, column=0, sticky="ew", pady=(5, 10))
    generated_password_entry = ttk.Entry(generated_password_subframe, textvariable=generated_password_var, width=30, state="readonly")
    generated_password_entry.grid(row=0, column=0, padx=(0, 10))
    copy_generated_button = ttk.Button(generated_password_subframe, text="Copy", command=copy_generated_password, state="disabled", style='secondary.TButton')
    copy_generated_button.grid(row=0, column=1)
    generated_strength_label = ttk.Label(generated_pw_frame, text="Generated Strength: 0/5", font=CONFIG['font'])
    generated_strength_label.grid(row=2, column=0, sticky="w")
    generated_pw_frame.grid_forget()  # Initially hide the frame

def create_history_section(root):
    """Create the password history section."""
    history_frame = ttk.Frame(root)
    history_frame.grid(row=3, column=0, padx=20, pady=15, sticky="ew")
    ttk.Label(history_frame, text="Password History:", font=CONFIG['font']).grid(row=0, column=0, sticky="w")
    global history_text
    history_text = tk.StringVar(value="No passwords in history")
    history_label = ttk.Label(history_frame, textvariable=history_text, font=CONFIG['font'])
    history_label.grid(row=1, column=0, sticky="w")
    clear_button = ttk.Button(history_frame, text="Clear History", command=clear_history, style='secondary.TButton')
    clear_button.grid(row=2, column=0, pady=10)
    Tooltip(clear_button, "Clear the password history")

def create_gui():
    """Set up the main GUI for the password strength checker."""
    try:
        import ttkbootstrap
    except ImportError:
        print("Please install ttkbootstrap: pip install ttkbootstrap")
        return None

    root = ttk.Window(themename="darkly")
    root.title(" Password Strength Checker")
    root.geometry("300x700")
    root.resizable(True, True)
    root.minsize(400, 500)

    # Global variables
    global password_var, generated_password_var, suggestions_text, show_var, length_var
    global entry_password, strength_bar, strength_label, suggestions_label
    global generated_pw_frame, copy_generated_button, generated_strength_label
    global history_text, password_history
    password_var = tk.StringVar()
    generated_password_var = tk.StringVar()
    suggestions_text = tk.StringVar(value="No suggestions")
    show_var = tk.BooleanVar(value=False)
    length_var = tk.IntVar(value=12)
    password_history = []

    create_input_section(root)
    create_generate_section(root)
    create_history_section(root)

    # Keyboard shortcuts
    root.bind('<Control-c>', lambda event: copy_password())
    root.bind('<Control-g>', lambda event: generate_password())

    # Bind input and scale events
    password_var.trace_add('write', update_strength_bar)
    length_var.trace_add('write', update_length_label)

    return root

if __name__ == "__main__":
    if platform.system() == "Emscripten":
        print("This application requires a desktop environment to run.")
    else:
        try:
            import pyperclip
            root = create_gui()
            if root:
                root.mainloop()
        except ImportError:
            print("Please install pyperclip: pip install pyperclip")