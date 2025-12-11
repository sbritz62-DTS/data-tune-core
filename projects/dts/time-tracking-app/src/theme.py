"""
Dark Mode Theme Configuration
Claude-inspired dark theme for the application
"""

import tkinter as tk
from tkinter import ttk

# Claude-inspired Dark Theme Colors
COLORS = {
    # Backgrounds
    'bg_dark': '#1E1E1E',         # Main dark background
    'bg_medium': '#2F2F2F',        # Secondary background (panels, inputs)
    'bg_light': '#3A3A3A',         # Lighter background (hover states)
    'bg_sidebar': '#252525',       # Sidebar background
    
    # Text
    'text_primary': '#ECECEC',     # Main text color
    'text_secondary': '#B0B0B0',   # Secondary text
    'text_disabled': '#6B6B6B',    # Disabled text
    
    # Accent
    'accent': '#E57A3C',           # Claude's orange/coral accent
    'accent_hover': '#F08847',     # Lighter accent for hover
    'accent_dark': '#D06628',      # Darker accent for pressed
    
    # Status
    'success': '#4CAF50',          # Green for success
    'warning': '#FFA726',          # Orange for warnings
    'error': '#EF5350',            # Red for errors
    
    # Borders
    'border': '#404040',           # Border color
    'border_focus': '#E57A3C',     # Focused border
    
    # Grid
    'grid_header': '#333333',      # Grid header background
    'grid_alt': '#282828',         # Alternate row color
}


def apply_dark_theme(root):
    """Apply dark theme to the application"""
    
    style = ttk.Style(root)
    
    # Configure root window
    root.configure(bg=COLORS['bg_dark'])
    
    # Use clam theme as base (works well with dark colors)
    style.theme_use('clam')
    
    # Configure TFrame
    style.configure('TFrame',
                   background=COLORS['bg_dark'])
    
    style.configure('Sidebar.TFrame',
                   background=COLORS['bg_sidebar'])
    
    style.configure('Content.TFrame',
                   background=COLORS['bg_dark'])
    
    # Configure TLabel
    style.configure('TLabel',
                   background=COLORS['bg_dark'],
                   foreground=COLORS['text_primary'])
    
    style.configure('Title.TLabel',
                   background=COLORS['bg_dark'],
                   foreground=COLORS['text_primary'],
                   font=('Arial', 16, 'bold'))
    
    style.configure('Subtitle.TLabel',
                   background=COLORS['bg_dark'],
                   foreground=COLORS['text_secondary'],
                   font=('Arial', 10))
    
    style.configure('Sidebar.TLabel',
                   background=COLORS['bg_sidebar'],
                   foreground=COLORS['text_primary'])
    
    # Configure TButton
    style.configure('TButton',
                   background=COLORS['bg_medium'],
                   foreground=COLORS['text_primary'],
                   bordercolor=COLORS['border'],
                   lightcolor=COLORS['bg_light'],
                   darkcolor=COLORS['bg_dark'],
                   relief='flat',
                   font=('Arial', 10))
    
    style.map('TButton',
             background=[('active', COLORS['bg_light']),
                        ('pressed', COLORS['bg_dark'])],
             foreground=[('active', COLORS['text_primary'])])
    
    # Accent button style
    style.configure('Accent.TButton',
                   background=COLORS['accent'],
                   foreground='white',
                   bordercolor=COLORS['accent'],
                   font=('Arial', 10, 'bold'))
    
    style.map('Accent.TButton',
             background=[('active', COLORS['accent_hover']),
                        ('pressed', COLORS['accent_dark'])],
             foreground=[('active', 'white')])
    
    # Sidebar navigation buttons
    style.configure('Nav.TButton',
                   background=COLORS['bg_sidebar'],
                   foreground=COLORS['text_primary'],
                   borderwidth=0,
                   relief='flat',
                   font=('Arial', 11),
                   padding=(20, 15))
    
    style.map('Nav.TButton',
             background=[('active', COLORS['bg_medium']),
                        ('pressed', COLORS['bg_light'])],
             foreground=[('active', COLORS['accent'])])
    
    # Selected nav button
    style.configure('NavSelected.TButton',
                   background=COLORS['bg_light'],
                   foreground=COLORS['accent'],
                   borderwidth=0,
                   relief='flat',
                   font=('Arial', 11, 'bold'),
                   padding=(20, 15))
    
    # Configure TEntry
    style.configure('TEntry',
                   fieldbackground=COLORS['bg_medium'],
                   foreground=COLORS['text_primary'],
                   bordercolor=COLORS['border'],
                   lightcolor=COLORS['border'],
                   darkcolor=COLORS['border'],
                   insertcolor=COLORS['text_primary'])
    
    style.map('TEntry',
             fieldbackground=[('focus', COLORS['bg_light'])],
             bordercolor=[('focus', COLORS['border_focus'])])
    
    # Configure TLabelframe
    style.configure('TLabelframe',
                   background=COLORS['bg_dark'],
                   foreground=COLORS['text_primary'],
                   bordercolor=COLORS['border'],
                   lightcolor=COLORS['border'],
                   darkcolor=COLORS['border'])
    
    style.configure('TLabelframe.Label',
                   background=COLORS['bg_dark'],
                   foreground=COLORS['text_primary'],
                   font=('Arial', 10, 'bold'))
    
    # Configure Treeview
    style.configure('Treeview',
                   background=COLORS['bg_medium'],
                   foreground=COLORS['text_primary'],
                   fieldbackground=COLORS['bg_medium'],
                   borderwidth=0)
    
    style.configure('Treeview.Heading',
                   background=COLORS['grid_header'],
                   foreground=COLORS['text_primary'],
                   borderwidth=1,
                   relief='flat')
    
    style.map('Treeview',
             background=[('selected', COLORS['accent'])],
             foreground=[('selected', 'white')])
    
    style.map('Treeview.Heading',
             background=[('active', COLORS['bg_light'])])
    
    # Configure TSeparator
    style.configure('TSeparator',
                   background=COLORS['border'])
    
    # Configure TScrollbar
    style.configure('TScrollbar',
                   background=COLORS['bg_medium'],
                   troughcolor=COLORS['bg_dark'],
                   bordercolor=COLORS['bg_dark'],
                   arrowcolor=COLORS['text_secondary'],
                   lightcolor=COLORS['bg_medium'],
                   darkcolor=COLORS['bg_medium'])
    
    style.map('TScrollbar',
             background=[('active', COLORS['bg_light'])])
    
    return style


def configure_text_widget(text_widget):
    """Configure a Text widget for dark theme"""
    text_widget.configure(
        bg=COLORS['bg_medium'],
        fg=COLORS['text_primary'],
        insertbackground=COLORS['text_primary'],
        selectbackground=COLORS['accent'],
        selectforeground='white',
        relief='flat',
        borderwidth=1
    )


def configure_entry_widget(entry_widget):
    """Configure an Entry widget for dark theme"""
    entry_widget.configure(
        bg=COLORS['bg_medium'],
        fg=COLORS['text_primary'],
        insertbackground=COLORS['text_primary'],
        selectbackground=COLORS['accent'],
        selectforeground='white',
        relief='flat',
        borderwidth=1
    )


def get_color(color_name):
    """Get a color value by name"""
    return COLORS.get(color_name, COLORS['text_primary'])

