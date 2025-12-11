"""
Time Tracking App - Weekly Timesheet GUI (CLEAN v7 with Amounts)
All totals in bottom row - includes weekly hours and amounts
10 columns: Client | Mon-Sun | Weekly Hours | Weekly Amount
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import timedelta
from db_helper import db, DatabaseError, ValidationError
from theme import COLORS

class TimesheetFrame(ttk.Frame):
    """Clean weekly timesheet with proper grid structure"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.week_start = db.get_week_start()
        self.timesheet_data = {}
        self.entry_widgets = {}
        self.weekly_hours_labels = {}
        self.weekly_amount_labels = {}
        self.day_total_labels = {}
        self.unsaved_changes = {}
        
        self.setup_ui()
        self.load_timesheet()
    
    def setup_ui(self):
        """Setup UI"""
        # Header
        header_frame = ttk.Frame(self)
        header_frame.grid(row=0, column=0, sticky='ew', padx=8, pady=6)
        
        title = ttk.Label(header_frame, text="Weekly Timesheet", 
                         style='Title.TLabel', font=('Calibri', 14, 'bold'))
        title.pack(side='left', anchor='w')
        
        nav_frame = ttk.Frame(header_frame)
        nav_frame.pack(side='right', anchor='e')
        
        ttk.Button(nav_frame, text="◀ Prev", command=self.previous_week).pack(side='left', padx=2)
        
        self.week_label = ttk.Label(nav_frame, text="", 
                                    font=('Calibri', 10, 'bold'),
                                    foreground=COLORS['accent'])
        self.week_label.pack(side='left', padx=10)
        
        ttk.Button(nav_frame, text="Next ▶", command=self.next_week).pack(side='left', padx=2)
        ttk.Button(nav_frame, text="Today", command=self.current_week).pack(side='left', padx=2)
        
        # Grid container
        grid_container = ttk.Frame(self)
        grid_container.grid(row=1, column=0, sticky='nsew', padx=0, pady=0)
        
        canvas = tk.Canvas(grid_container, highlightthickness=0, bg=COLORS['bg_dark'])
        scrollbar = ttk.Scrollbar(grid_container, orient='vertical', command=canvas.yview)
        self.grid_frame = ttk.Frame(canvas)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.create_window((0, 0), window=self.grid_frame, anchor='nw')
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.grid_frame.bind('<Configure>', 
                            lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Bottom
        bottom_frame = ttk.Frame(self)
        bottom_frame.grid(row=2, column=0, sticky='ew', padx=8, pady=4)
        
        button_group = ttk.Frame(bottom_frame)
        button_group.pack(side='left')
        
        ttk.Button(button_group, text="🗑️ Clear All", 
                  command=self.clear_all, style='Accent.TButton').pack(side='left', padx=2)
        
        self.unsaved_label = ttk.Label(button_group, text="", 
                                       font=('Calibri', 8),
                                       foreground=COLORS['warning'])
        self.unsaved_label.pack(side='left', padx=8)
        
        self.totals_label = ttk.Label(bottom_frame, text="", 
                                      font=('Calibri', 24, 'bold'),
                                      foreground=COLORS['accent'])
        self.totals_label.pack(side='right', anchor='e', padx=8)
        
        status_frame = ttk.Frame(self)
        status_frame.grid(row=3, column=0, sticky='ew', padx=8, pady=(2, 3))
        
        self.status_label = ttk.Label(status_frame, text="Ready", 
                                     font=('Calibri', 8),
                                     foreground=COLORS['text_secondary'])
        self.status_label.pack(anchor='w')
        
        self.rowconfigure(0, weight=0, minsize=45)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0, minsize=32)
        self.rowconfigure(3, weight=0, minsize=18)
        self.columnconfigure(0, weight=1)
        grid_container.rowconfigure(0, weight=1)
        grid_container.columnconfigure(0, weight=1)
    
    def setup_grid(self):
        """Setup the grid - 10 COLUMN LAYOUT"""
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        
        self.entry_widgets.clear()
        self.weekly_hours_labels.clear()
        self.weekly_amount_labels.clear()
        self.day_total_labels.clear()
        self.unsaved_changes.clear()
        
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        week_dates = db.get_week_dates(self.week_start)
        
        week_end = week_dates[-1]
        self.week_label.config(
            text=f"{self.week_start.strftime('%b %d')} - {week_end.strftime('%b %d, %Y')}"
        )
        
        header_bg = COLORS['grid_header']
        header_fg = COLORS['text_primary']
        weekend_bg = '#3a2a2a'
        
        # ROW 0: DAY HEADERS
        ttk.Label(self.grid_frame, text="Client", 
                 font=('Calibri', 10, 'bold'), background=header_bg, foreground=header_fg,
                 borderwidth=1, relief='solid', padding=10).grid(row=0, column=0, sticky='nsew', padx=0, pady=0)
        
        for col, (day, date) in enumerate(zip(days, week_dates), start=1):
            is_weekend = date.weekday() >= 5
            day_header_bg = weekend_bg if is_weekend else header_bg
            
            header_text = f"{day[:3]}\n{date.strftime('%m/%d')}"
            ttk.Label(self.grid_frame, text=header_text, 
                     font=('Calibri', 9, 'bold'), background=day_header_bg, foreground=header_fg,
                     borderwidth=1, relief='solid', anchor='center', padding=10).grid(
                         row=0, column=col, sticky='nsew', padx=0, pady=0)
        
        # Weekly hours and amount headers
        ttk.Label(self.grid_frame, text="Weekly\nHours", 
                 font=('Calibri', 9, 'bold'), background=header_bg, foreground=header_fg,
                 borderwidth=1, relief='solid', anchor='center', padding=10).grid(
                     row=0, column=8, sticky='nsew', padx=0, pady=0)
        
        ttk.Label(self.grid_frame, text="Weekly\nAmount", 
                 font=('Calibri', 9, 'bold'), background=header_bg, foreground=header_fg,
                 borderwidth=1, relief='solid', anchor='center', padding=10).grid(
                     row=0, column=9, sticky='nsew', padx=0, pady=0)
        
        # CLIENT ROWS
        if not self.timesheet_data:
            ttk.Label(self.grid_frame, text="No active clients. Add clients in the Clients tab.",
                     font=('Calibri', 10), foreground=COLORS['text_secondary']).grid(
                         row=1, column=0, columnspan=10, pady=30)
            self.update_status("No clients available")
            return
        
        row = 1
        total_hours_all = 0
        total_amount_all = 0
        
        for client_id, client_data in sorted(self.timesheet_data.items(), 
                                            key=lambda x: x[1]['ClientName']):
            client_bg = COLORS['bg_light'] if row % 2 == 0 else COLORS['bg_dark']
            
            # Client name
            ttk.Label(self.grid_frame, text=client_data['ClientName'],
                     font=('Calibri', 9), background=client_bg, foreground=COLORS['text_primary'],
                     borderwidth=1, relief='solid', padding=10, anchor='w').grid(
                         row=row, column=0, sticky='nsew', padx=0, pady=0)
            
            weekly_total_hours = 0
            weekly_total_amount = 0
            
            for day_num in range(1, 8):
                col = day_num
                is_weekend = (day_num >= 6)
                
                day_data = client_data['days'].get(day_num, {})
                hours = day_data.get('hours', 0.0)
                rate = day_data.get('rate', client_data['DefaultRate'])
                
                entry_var = tk.StringVar(value=str(hours) if hours > 0 else '')
                entry_bg = '#3a2a2a' if is_weekend else COLORS['bg_medium']
                
                entry = tk.Entry(self.grid_frame, textvariable=entry_var, width=10, 
                                justify='center', font=('Calibri', 9), bg=entry_bg,
                                fg=COLORS['text_primary'], insertbackground=COLORS['text_primary'],
                                selectbackground=COLORS['accent'], selectforeground='white',
                                relief='solid', borderwidth=1)
                entry.grid(row=row, column=col, sticky='nsew', padx=0, pady=0)
                
                self.entry_widgets[(client_id, day_num)] = {
                    'widget': entry, 'var': entry_var, 'rate': rate,
                    'entry_id': day_data.get('entry_id'), 'original_hours': hours
                }
                
                entry.bind('<FocusOut>', lambda e, cid=client_id, d=day_num: self.on_entry_change(cid, d))
                entry.bind('<KeyRelease>', lambda e, cid=client_id, d=day_num: self.on_entry_edit(cid, d))
                entry.bind('<Return>', lambda e, cid=client_id, d=day_num: self.on_enter_pressed(cid, d))
                entry.bind('<KeyPress>', lambda e: self.validate_entry_input(e))
                
                weekly_total_hours += hours
                weekly_total_amount += hours * rate
                total_hours_all += hours
                total_amount_all += hours * rate
            
            # Weekly hours label
            weekly_hours_label = ttk.Label(self.grid_frame, text=f"{weekly_total_hours:.2f}",
                                    font=('Calibri', 9, 'bold'), background=client_bg,
                                    foreground=COLORS['accent'], borderwidth=1, relief='solid',
                                    anchor='center', padding=10)
            weekly_hours_label.grid(row=row, column=8, sticky='nsew', padx=0, pady=0)
            self.weekly_hours_labels[client_id] = weekly_hours_label
            
            # Weekly amount label
            weekly_amount_label = ttk.Label(self.grid_frame, text=f"${weekly_total_amount:,.2f}",
                                    font=('Calibri', 9, 'bold'), background=client_bg,
                                    foreground=COLORS['accent'], borderwidth=1, relief='solid',
                                    anchor='center', padding=10)
            weekly_amount_label.grid(row=row, column=9, sticky='nsew', padx=0, pady=0)
            self.weekly_amount_labels[client_id] = weekly_amount_label
            
            row += 1
        
        # TOTALS ROW - ALL TOTALS HERE
        total_bg = '#1a1a1a'
        
        ttk.Label(self.grid_frame, text="TOTAL", 
                 font=('Calibri', 10, 'bold'), background=total_bg, foreground=COLORS['accent'],
                 borderwidth=2, relief='solid', padding=10, anchor='center').grid(
                     row=row, column=0, sticky='nsew', padx=0, pady=0)
        
        # Day total cells in TOTAL row
        for col in range(1, 8):
            day_label = ttk.Label(self.grid_frame, text="0.00",
                                 font=('Calibri', 10, 'bold'), background=total_bg,
                                 foreground=COLORS['accent'], borderwidth=2, relief='solid',
                                 anchor='center', padding=10)
            day_label.grid(row=row, column=col, sticky='nsew', padx=0, pady=0)
            self.day_total_labels[col] = day_label
        
        # Weekly total hours in TOTAL row
        self.total_hours_label = ttk.Label(self.grid_frame, text=f"{total_hours_all:.2f}",
                 font=('Calibri', 10, 'bold'), background=total_bg, foreground=COLORS['accent'],
                 borderwidth=2, relief='solid', anchor='center', padding=10)
        self.total_hours_label.grid(row=row, column=8, sticky='nsew', padx=0, pady=0)
        
        # Weekly total amount in TOTAL row
        self.total_amount_label = ttk.Label(self.grid_frame, text=f"${total_amount_all:,.2f}",
                 font=('Calibri', 10, 'bold'), background=total_bg, foreground=COLORS['accent'],
                 borderwidth=2, relief='solid', anchor='center', padding=10)
        self.total_amount_label.grid(row=row, column=9, sticky='nsew', padx=0, pady=0)
        
        # Configure columns - 10 TOTAL (Client + 7 days + Weekly Hours + Weekly Amount)
        self.grid_frame.columnconfigure(0, weight=1, minsize=150)
        for col in range(1, 10):
            self.grid_frame.columnconfigure(col, weight=1, minsize=100)
        
        self.update_status(f"Showing {len(self.timesheet_data)} clients")
        self.update_unsaved_indicator()
    
    def validate_entry_input(self, event):
        """Allow only numbers and decimal (backspace allowed)"""
        if event.keysym in ('BackSpace', 'Delete', 'Left', 'Right', 'Home', 'End', 'Tab'):
            return None
        if event.state & 0x4:  # Ctrl
            return None
        if not (event.char.isdigit() or event.char == '.' or event.char == ''):
            return 'break'
    
    def on_enter_pressed(self, client_id, day_num):
        """Enter moves to next row"""
        self.on_entry_change(client_id, day_num)
        
        clients_list = sorted(self.timesheet_data.items(), key=lambda x: x[1]['ClientName'])
        current_index = next((i for i, (cid, _) in enumerate(clients_list) if cid == client_id), -1)
        
        if current_index >= 0 and current_index < len(clients_list) - 1:
            next_client_id = clients_list[current_index + 1][0]
            next_entry = self.entry_widgets.get((next_client_id, day_num))
            if next_entry:
                next_entry['widget'].focus()
                next_entry['widget'].select_range(0, tk.END)
    
    def on_entry_edit(self, client_id, day_num):
        """Track unsaved changes"""
        entry_info = self.entry_widgets.get((client_id, day_num))
        if entry_info:
            current = entry_info['var'].get().strip()
            original = str(entry_info['original_hours']) if entry_info['original_hours'] > 0 else ''
            
            if current != original:
                self.unsaved_changes[(client_id, day_num)] = True
            else:
                self.unsaved_changes.pop((client_id, day_num), None)
        
        self.update_unsaved_indicator()
    
    def on_entry_change(self, client_id, day_num):
        """Auto-save entry"""
        entry_info = self.entry_widgets.get((client_id, day_num))
        if not entry_info:
            return
        
        try:
            hours_str = entry_info['var'].get().strip()
            hours = float(hours_str) if hours_str else 0.0
            
            if hours < 0:
                messagebox.showerror("Invalid Input", "Hours cannot be negative")
                entry_info['var'].set(str(entry_info['original_hours']))
                return
            
            if hours > 24:
                messagebox.showerror("Invalid Input", "Hours cannot exceed 24 per day")
                entry_info['var'].set(str(entry_info['original_hours']))
                return
            
            self.update_status("Saving...")
            
            db.save_time_entry(
                client_id=client_id, week_start_date=self.week_start,
                day_of_week=day_num, hours_worked=hours, rate_used=entry_info['rate']
            )
            
            entry_info['original_hours'] = hours
            self.unsaved_changes.pop((client_id, day_num), None)
            
            self.update_status("Saved", 1500)
            self.update_totals()
            self.update_weekly_totals_for_client(client_id)
            self.update_day_totals()
            self.update_unsaved_indicator()
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number")
            entry_info['var'].set(str(entry_info['original_hours']))
        except (ValidationError, DatabaseError) as e:
            messagebox.showerror("Error", str(e))
            entry_info['var'].set(str(entry_info['original_hours']))
    
    def update_day_totals(self):
        """Update day total cells in bottom TOTAL row"""
        for col in range(1, 8):
            day_total = 0.0
            for client_id in self.timesheet_data:
                entry_info = self.entry_widgets.get((client_id, col))
                if entry_info:
                    try:
                        hours = float(entry_info['var'].get().strip() or '0')
                        day_total += hours
                    except ValueError:
                        pass
            
            if col in self.day_total_labels:
                self.day_total_labels[col].config(text=f"{day_total:.2f}")
    
    def update_weekly_totals_for_client(self, client_id):
        """Update weekly hours and amount for client"""
        weekly_total_hours = 0.0
        weekly_total_amount = 0.0
        
        for day_num in range(1, 8):
            entry_info = self.entry_widgets.get((client_id, day_num))
            if entry_info:
                try:
                    hours = float(entry_info['var'].get().strip() or '0')
                    rate = entry_info['rate']
                    weekly_total_hours += hours
                    weekly_total_amount += hours * rate
                except ValueError:
                    pass
        
        if client_id in self.weekly_hours_labels:
            self.weekly_hours_labels[client_id].config(text=f"{weekly_total_hours:.2f}")
        
        if client_id in self.weekly_amount_labels:
            self.weekly_amount_labels[client_id].config(text=f"${weekly_total_amount:,.2f}")
    
    def clear_all(self):
        """Clear all hours"""
        if not self.timesheet_data:
            messagebox.showinfo("No Data", "No clients to clear")
            return
        
        if messagebox.askyesno("Clear All Hours",
                              "Are you sure? This cannot be undone."):
            try:
                cleared_count = 0
                
                for (client_id, day_num), entry_info in list(self.entry_widgets.items()):
                    if entry_info['original_hours'] > 0:
                        entry_info['var'].set('')
                        db.save_time_entry(client_id, self.week_start, day_num, 0.0, entry_info['rate'])
                        entry_info['original_hours'] = 0
                        cleared_count += 1
                
                self.unsaved_changes.clear()
                self.update_totals()
                self.update_day_totals()
                
                for client_id in self.timesheet_data:
                    self.update_weekly_totals_for_client(client_id)
                
                self.update_unsaved_indicator()
                messagebox.showinfo("Success", f"✓ Cleared {cleared_count} entries!")
                
            except DatabaseError as e:
                messagebox.showerror("Database Error", f"Failed to clear:\n{str(e)}")
    
    def load_timesheet(self):
        """Load timesheet"""
        try:
            self.update_status("Loading...")
            self.timesheet_data = db.get_weekly_timesheet(self.week_start)
            self.setup_grid()
            self.update_totals()
        except DatabaseError as e:
            messagebox.showerror("Database Error", f"Failed to load:\n{str(e)}")
    
    def update_totals(self):
        """Update bottom totals"""
        total_hours = 0
        total_amount = 0
        
        for (client_id, day_num), entry_info in self.entry_widgets.items():
            try:
                hours = float(entry_info['var'].get().strip() or '0')
                rate = entry_info['rate']
                total_hours += hours
                total_amount += hours * rate
            except ValueError:
                pass
        
        self.totals_label.config(text=f"{total_hours:.2f} hrs | ${total_amount:,.2f}")
        
        if hasattr(self, 'total_hours_label'):
            self.total_hours_label.config(text=f"{total_hours:.2f}")
        if hasattr(self, 'total_amount_label'):
            self.total_amount_label.config(text=f"${total_amount:,.2f}")
    
    def update_unsaved_indicator(self):
        """Update unsaved label"""
        if self.unsaved_changes:
            self.unsaved_label.config(
                text=f"● {len(self.unsaved_changes)} unsaved",
                foreground=COLORS['warning']
            )
        else:
            self.unsaved_label.config(text="")
    
    def update_status(self, message, timeout=0):
        """Update status"""
        self.status_label.config(text=message)
        if timeout > 0:
            self.after(timeout, lambda: self.status_label.config(text="Ready"))
    
    def previous_week(self):
        """Previous week"""
        self.week_start = self.week_start - timedelta(days=7)
        self.load_timesheet()
    
    def next_week(self):
        """Next week"""
        self.week_start = self.week_start + timedelta(days=7)
        self.load_timesheet()
    
    def current_week(self):
        """Current week"""
        self.week_start = db.get_week_start()
        self.load_timesheet()
