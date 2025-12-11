"""
Time Tracking App - Main Application Window
Dark theme with left sidebar navigation
"""

import tkinter as tk
from tkinter import ttk
from gui_clients import ClientManagementFrame
from gui_timesheet import TimesheetFrame
from theme import apply_dark_theme, COLORS

class TimeTrackingApp:
    """Main application class with dark theme and left sidebar"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Data Tune Solutions - Time Tracking")
        self.root.geometry("1300x750")
        
        # Set minimum window size
        self.root.minsize(1000, 650)
        
        # Apply dark theme
        self.style = apply_dark_theme(root)
        
        # Create main container
        self.setup_ui()
        
        # Show timesheet by default
        self.show_timesheet()
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_ui(self):
        """Setup the main user interface with left sidebar"""
        
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill='both', expand=True)
        
        # Left sidebar
        sidebar = ttk.Frame(main_container, style='Sidebar.TFrame', width=200)
        sidebar.pack(side='left', fill='y')
        sidebar.pack_propagate(False)  # Maintain fixed width
        
        # Sidebar header
        header_frame = ttk.Frame(sidebar, style='Sidebar.TFrame')
        header_frame.pack(side='top', fill='x', pady=20, padx=15)
        
        title_label = ttk.Label(header_frame, 
                               text="Data Tune\nSolutions", 
                               style='Sidebar.TLabel',
                               font=('Arial', 16, 'bold'),
                               justify='left')
        title_label.pack(anchor='w')
        
        subtitle_label = ttk.Label(header_frame,
                                  text="Time Tracking",
                                  style='Sidebar.TLabel',
                                  font=('Arial', 10),
                                  foreground=COLORS['text_secondary'])
        subtitle_label.pack(anchor='w', pady=(5, 0))
        
        # Separator
        sep = ttk.Separator(sidebar, orient='horizontal')
        sep.pack(fill='x', pady=15)
        
        # Navigation buttons
        nav_frame = ttk.Frame(sidebar, style='Sidebar.TFrame')
        nav_frame.pack(side='top', fill='x')
        
        self.timesheet_btn = ttk.Button(nav_frame, 
                                        text="📅  Timesheet",
                                        command=self.show_timesheet,
                                        style='Nav.TButton')
        self.timesheet_btn.pack(fill='x', pady=(0, 5))
        
        self.clients_btn = ttk.Button(nav_frame, 
                                      text="👥  Clients",
                                      command=self.show_clients,
                                      style='Nav.TButton')
        self.clients_btn.pack(fill='x')
        
        # Sidebar footer (version info)
        footer_frame = ttk.Frame(sidebar, style='Sidebar.TFrame')
        footer_frame.pack(side='bottom', fill='x', pady=15, padx=15)
        
        version_label = ttk.Label(footer_frame,
                                 text="Version 1.0\nPhase 2",
                                 style='Sidebar.TLabel',
                                 font=('Arial', 8),
                                 foreground=COLORS['text_disabled'],
                                 justify='center')
        version_label.pack()
        
        # Right content area
        content_container = ttk.Frame(main_container, style='Content.TFrame')
        content_container.pack(side='right', fill='both', expand=True)
        
        # Content frame (where screens will be shown)
        self.content_frame = ttk.Frame(content_container, style='Content.TFrame')
        self.content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Initialize frames (but don't show yet)
        self.timesheet_frame = None
        self.clients_frame = None
        self.current_frame = None
    
    def show_timesheet(self):
        """Show the timesheet screen"""
        # Update button styles
        self.timesheet_btn.configure(style='NavSelected.TButton')
        self.clients_btn.configure(style='Nav.TButton')
        
        # Hide current frame
        if self.current_frame:
            self.current_frame.pack_forget()
        
        # Create or show timesheet frame
        if self.timesheet_frame is None:
            self.timesheet_frame = TimesheetFrame(self.content_frame)
        
        self.timesheet_frame.pack(fill='both', expand=True)
        self.current_frame = self.timesheet_frame
        
        # Refresh data
        self.timesheet_frame.load_timesheet()
    
    def show_clients(self):
        """Show the client management screen"""
        # Update button styles
        self.clients_btn.configure(style='NavSelected.TButton')
        self.timesheet_btn.configure(style='Nav.TButton')
        
        # Hide current frame
        if self.current_frame:
            self.current_frame.pack_forget()
        
        # Create or show clients frame
        if self.clients_frame is None:
            self.clients_frame = ClientManagementFrame(self.content_frame)
        
        self.clients_frame.pack(fill='both', expand=True)
        self.current_frame = self.clients_frame
        
        # Refresh data
        self.clients_frame.load_clients()
    
    def on_closing(self):
        """Handle window closing"""
        from db_helper import db
        db.close_connection()
        self.root.destroy()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = TimeTrackingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
