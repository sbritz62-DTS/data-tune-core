"""
Time Tracking App - Weekly Timesheet GUI
Grid view for entering time (Mon-Sun x Clients)
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import timedelta
from db_helper import db
from theme import COLORS, configure_entry_widget

class TimesheetFrame(ttk.Frame):
    """Weekly timesheet grid screen"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.week_start = db.get_week_start()
        self.timesheet_data = {}
        self.entry_widgets = {}  # Store Entry widgets for easy access
        
        self.setup_ui()
        self.load_timesheet()
    
    def setup_ui(self):
        """Setup the user interface"""
        
        # Header frame
        header_frame = ttk.Frame(self)
        header_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
        
        # Title
        title = ttk.Label(header_frame, text="Weekly Timesheet", 
                         style='Title.TLabel')
        title.pack(side='left', padx=10)
        
        # Week navigation
        nav_frame = ttk.Frame(header_frame)
        nav_frame.pack(side='right')
        
        ttk.Button(nav_frame, text="← Previous Week", 
                  command=self.previous_week).pack(side='left', padx=5)
        
        self.week_label = ttk.Label(nav_frame, text="", 
                                    font=('Arial', 12, 'bold'),
                                    foreground=COLORS['accent'])
        self.week_label.pack(side='left', padx=15)
        
        ttk.Button(nav_frame, text="Next Week →", 
                  command=self.next_week).pack(side='left', padx=5)
        
        ttk.Button(nav_frame, text="Current Week", 
                  command=self.current_week).pack(side='left', padx=5)
        
        # Grid frame with scrollbar
        grid_container = ttk.Frame(self)
        grid_container.grid(row=1, column=0, sticky='nsew', padx=10, pady=5)
        
        # Canvas and scrollbar for scrolling
        canvas = tk.Canvas(grid_container, highlightthickness=0)
        scrollbar = ttk.Scrollbar(grid_container, orient='vertical', 
                                 command=canvas.yview)
        self.grid_frame = ttk.Frame(canvas)
        
        # Configure canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.create_window((0, 0), window=self.grid_frame, anchor='nw')
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Update scroll region when frame changes size
        self.grid_frame.bind('<Configure>', 
                            lambda e: canvas.configure(
                                scrollregion=canvas.bbox('all')))
        
        # Bottom frame for save and totals
        bottom_frame = ttk.Frame(self)
        bottom_frame.grid(row=2, column=0, sticky='ew', padx=10, pady=10)
        
        ttk.Button(bottom_frame, text="💾 Save All Changes", 
                  command=self.save_timesheet,
                  style='Accent.TButton').pack(side='left', padx=5)
        
        ttk.Button(bottom_frame, text="Refresh", 
                  command=self.load_timesheet).pack(side='left', padx=5)
        
        self.totals_label = ttk.Label(bottom_frame, text="", 
                                      font=('Arial', 10))
        self.totals_label.pack(side='right', padx=10)
        
        # Configure grid weights
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        grid_container.rowconfigure(0, weight=1)
        grid_container.columnconfigure(0, weight=1)
    
    def setup_grid(self):
        """Setup the timesheet grid"""
        # Clear existing grid
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        
        self.entry_widgets.clear()
        
        # Days of week
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
                'Friday', 'Saturday', 'Sunday']
        week_dates = db.get_week_dates(self.week_start)
        
        # Update week label
        week_end = week_dates[-1]
        self.week_label.config(
            text=f"{self.week_start.strftime('%b %d')} - " +
                 f"{week_end.strftime('%b %d, %Y')}"
        )
        
        # Header row - Days
        ttk.Label(self.grid_frame, text="Client", 
                 font=('Arial', 10, 'bold'),
                 borderwidth=1, relief='solid').grid(
                     row=0, column=0, sticky='nsew', padx=1, pady=1)
        
        for col, (day, date) in enumerate(zip(days, week_dates), start=1):
            header_text = f"{day}\n{date.strftime('%m/%d')}"
            ttk.Label(self.grid_frame, text=header_text, 
                     font=('Arial', 9, 'bold'),
                     borderwidth=1, relief='solid',
                     anchor='center').grid(
                         row=0, column=col, sticky='nsew', padx=1, pady=1)
        
        # Total column
        ttk.Label(self.grid_frame, text="Weekly\nTotal", 
                 font=('Arial', 9, 'bold'),
                 borderwidth=1, relief='solid',
                 anchor='center').grid(
                     row=0, column=8, sticky='nsew', padx=1, pady=1)
        
        # Client rows
        if not self.timesheet_data:
            ttk.Label(self.grid_frame, 
                     text="No active clients. Add clients first.",
                     font=('Arial', 10)).grid(
                         row=1, column=0, columnspan=9, pady=20)
            return
        
        row = 1
        for client_id, client_data in sorted(
                self.timesheet_data.items(), 
                key=lambda x: x[1]['ClientName']):
            
            # Client name
            ttk.Label(self.grid_frame, text=client_data['ClientName'],
                     borderwidth=1, relief='solid',
                     padding=5).grid(
                         row=row, column=0, sticky='nsew', padx=1, pady=1)
            
            # Days (Mon=1, Sun=7)
            weekly_total = 0
            for day_num in range(1, 8):
                col = day_num
                
                day_data = client_data['days'].get(day_num, {})
                hours = day_data.get('hours', 0.0)
                
                # Entry widget for hours
                entry_var = tk.StringVar(value=str(hours) if hours > 0 else '')
                entry = tk.Entry(self.grid_frame, textvariable=entry_var,
                                width=8, justify='center',
                                bg=COLORS['bg_medium'],
                                fg=COLORS['text_primary'],
                                insertbackground=COLORS['text_primary'],
                                selectbackground=COLORS['accent'],
                                selectforeground='white',
                                relief='flat',
                                borderwidth=1,
                                highlightthickness=1,
                                highlightcolor=COLORS['border_focus'],
                                highlightbackground=COLORS['border'])
                entry.grid(row=row, column=col, sticky='nsew', padx=1, pady=1)
                
                # Store reference
                self.entry_widgets[(client_id, day_num)] = {
                    'widget': entry,
                    'var': entry_var,
                    'rate': day_data.get('rate', client_data['DefaultRate']),
                    'entry_id': day_data.get('entry_id')
                }
                
                # Auto-save on focus out
                entry.bind('<FocusOut>', 
                          lambda e, cid=client_id, day=day_num: 
                          self.auto_save_entry(cid, day))
                
                weekly_total += hours
            
            # Weekly total
            total_label = ttk.Label(self.grid_frame, 
                                   text=f"{weekly_total:.2f}",
                                   font=('Arial', 10, 'bold'),
                                   borderwidth=1, relief='solid',
                                   anchor='center',
                                   padding=5)
            total_label.grid(row=row, column=8, sticky='nsew', padx=1, pady=1)
            
            row += 1
        
        # Configure column weights for resizing
        self.grid_frame.columnconfigure(0, weight=1, minsize=150)
        for col in range(1, 9):
            self.grid_frame.columnconfigure(col, weight=0, minsize=80)
    
    def load_timesheet(self):
        """Load timesheet data from database"""
        try:
            self.timesheet_data = db.get_weekly_timesheet(self.week_start)
            self.setup_grid()
            self.update_totals()
        except Exception as e:
            messagebox.showerror("Error", 
                               f"Failed to load timesheet: {str(e)}")
    
    def auto_save_entry(self, client_id, day_num):
        """Auto-save entry when focus leaves cell"""
        entry_info = self.entry_widgets.get((client_id, day_num))
        if not entry_info:
            return
        
        try:
            hours_str = entry_info['var'].get().strip()
            hours = float(hours_str) if hours_str else 0.0
            
            if hours < 0:
                messagebox.showerror("Invalid Input", "Hours cannot be negative")
                entry_info['var'].set('0')
                return
            
            # Save to database
            db.save_time_entry(
                client_id=client_id,
                week_start_date=self.week_start,
                day_of_week=day_num,
                hours_worked=hours,
                rate_used=entry_info['rate']
            )
            
        except ValueError:
            messagebox.showerror("Invalid Input", 
                               "Please enter a valid number for hours")
            entry_info['var'].set('0')
    
    def save_timesheet(self):
        """Save all timesheet entries"""
        try:
            saved_count = 0
            
            for (client_id, day_num), entry_info in self.entry_widgets.items():
                hours_str = entry_info['var'].get().strip()
                hours = float(hours_str) if hours_str else 0.0
                
                if hours < 0:
                    continue
                
                db.save_time_entry(
                    client_id=client_id,
                    week_start_date=self.week_start,
                    day_of_week=day_num,
                    hours_worked=hours,
                    rate_used=entry_info['rate']
                )
                saved_count += 1
            
            messagebox.showinfo("Success", 
                              f"Saved {saved_count} time entries!")
            self.load_timesheet()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save timesheet: {str(e)}")
    
    def update_totals(self):
        """Update total hours display"""
        total_hours = 0
        total_amount = 0
        
        for (client_id, day_num), entry_info in self.entry_widgets.items():
            try:
                hours_str = entry_info['var'].get().strip()
                hours = float(hours_str) if hours_str else 0.0
                rate = entry_info['rate']
                
                total_hours += hours
                total_amount += hours * rate
            except ValueError:
                pass
        
        self.totals_label.config(
            text=f"Total Hours: {total_hours:.2f} | " +
                 f"Total Amount: ${total_amount:,.2f}"
        )
    
    def previous_week(self):
        """Navigate to previous week"""
        self.week_start = self.week_start - timedelta(days=7)
        self.load_timesheet()
    
    def next_week(self):
        """Navigate to next week"""
        self.week_start = self.week_start + timedelta(days=7)
        self.load_timesheet()
    
    def current_week(self):
        """Navigate to current week"""
        self.week_start = db.get_week_start()
        self.load_timesheet()

