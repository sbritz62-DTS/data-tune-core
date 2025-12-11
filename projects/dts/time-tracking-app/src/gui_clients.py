"""
Time Tracking App - Client Management GUI (IMPROVED)
Enhanced UI with contact information display, detail view, and better feedback
"""

import tkinter as tk
from tkinter import ttk, messagebox
from db_helper import db, DatabaseError, ValidationError
from theme import COLORS, configure_text_widget

class ClientManagementFrame(ttk.Frame):
    """Enhanced client management screen with detail view"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.clients = []
        self.selected_client = None
        
        self.setup_ui()
        self.load_clients()
    
    def setup_ui(self):
        """Setup the user interface with two-panel layout"""
        
        # Top title and stats
        header_frame = ttk.Frame(self)
        header_frame.grid(row=0, column=0, columnspan=2, sticky='ew', 
                         padx=20, pady=15)
        
        title = ttk.Label(header_frame, text="Client Management", 
                         style='Title.TLabel')
        title.pack(side='left', anchor='w')
        
        self.stats_label = ttk.Label(header_frame, text="", 
                                     style='Subtitle.TLabel')
        self.stats_label.pack(side='right', anchor='e')
        
        # Main content: two columns
        # Left: Client list
        left_frame = ttk.Frame(self)
        left_frame.grid(row=1, column=0, sticky='nsew', padx=(20, 10), pady=10)
        
        list_label = ttk.Label(left_frame, text="Active Clients", 
                              font=('Arial', 11, 'bold'),
                              foreground=COLORS['text_primary'])
        list_label.pack(anchor='w', pady=(0, 10))
        
        # Client list frame with scrollbar
        list_container = ttk.Frame(left_frame)
        list_container.pack(fill='both', expand=True)
        
        columns = ('ClientName', 'Rate', 'Contact')
        self.tree = ttk.Treeview(list_container, columns=columns, 
                                show='headings', height=15)
        
        # Column headings
        self.tree.heading('ClientName', text='Client Name')
        self.tree.heading('Rate', text='Hourly Rate')
        self.tree.heading('Contact', text='Contact Person')
        
        # Column widths and alignment
        self.tree.column('ClientName', width=180, anchor='w')
        self.tree.column('Rate', width=100, anchor='center')
        self.tree.column('Contact', width=120, anchor='w')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_container, orient='vertical', 
                                 command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')
        
        list_container.rowconfigure(0, weight=1)
        list_container.columnconfigure(0, weight=1)
        
        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self.on_client_select)
        
        # Right: Client details panel
        right_frame = ttk.LabelFrame(self, text="Client Details", padding=15)
        right_frame.grid(row=1, column=1, sticky='nsew', padx=(10, 20), pady=10)
        
        self.details_frame = ttk.Frame(right_frame)
        self.details_frame.pack(fill='both', expand=True)
        
        self.setup_details_panel()
        
        # Bottom buttons
        button_frame = ttk.Frame(self)
        button_frame.grid(row=2, column=0, columnspan=2, sticky='ew', 
                         padx=20, pady=15)
        
        ttk.Button(button_frame, text="➕ Add New Client", 
                  command=self.add_client,
                  style='Accent.TButton').pack(side='left', padx=5)
        
        ttk.Button(button_frame, text="✏️ Edit Selected", 
                  command=self.edit_client).pack(side='left', padx=5)
        
        ttk.Button(button_frame, text="🗑️ Deactivate Selected", 
                  command=self.deactivate_client).pack(side='left', padx=5)
        
        ttk.Button(button_frame, text="🔄 Refresh", 
                  command=self.load_clients).pack(side='left', padx=5)
        
        # Status bar
        self.status_label = ttk.Label(button_frame, text="Ready", 
                                     foreground=COLORS['text_secondary'],
                                     font=('Arial', 9))
        self.status_label.pack(side='right', padx=10)
        
        # Configure grid weights
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        left_frame.rowconfigure(1, weight=1)
        left_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)
        right_frame.columnconfigure(0, weight=1)
    
    def setup_details_panel(self):
        """Setup the client details display panel"""
        # Clear existing widgets
        for widget in self.details_frame.winfo_children():
            widget.destroy()
        
        # Placeholder message
        placeholder = ttk.Label(self.details_frame, 
                               text="Select a client to view details",
                               font=('Arial', 10),
                               foreground=COLORS['text_secondary'])
        placeholder.pack(expand=True)
    
    def on_client_select(self, event):
        """Handle client selection in the list"""
        selection = self.tree.selection()
        if not selection:
            self.selected_client = None
            self.setup_details_panel()
            return
        
        # Get selected client data
        item = self.tree.item(selection[0])
        client_name = item['values'][0]
        
        # Find client in list
        self.selected_client = next(
            (c for c in self.clients if c['ClientName'] == client_name), 
            None
        )
        
        if self.selected_client:
            self.display_client_details()
    
    def display_client_details(self):
        """Display selected client details in the right panel"""
        if not self.selected_client:
            self.setup_details_panel()
            return
        
        # Clear panel
        for widget in self.details_frame.winfo_children():
            widget.destroy()
        
        c = self.selected_client
        
        # Create scrollable frame for details
        canvas = tk.Canvas(self.details_frame, highlightthickness=0,
                          bg=COLORS['bg_dark'])
        scrollbar = ttk.Scrollbar(self.details_frame, orient='vertical',
                                 command=canvas.yview)
        content_frame = ttk.Frame(canvas)
        
        content_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )
        
        canvas.create_window((0, 0), window=content_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Basic Information Section
        basic_frame = ttk.LabelFrame(content_frame, text="Basic Information", 
                                    padding=10)
        basic_frame.pack(fill='x', padx=5, pady=5)
        
        detail_items = [
            ("Client Name", c['ClientName']),
            ("Hourly Rate", f"${c['DefaultRate']:.2f}"),
            ("Payment Terms", f"{c['PaymentTerms']} days"),
            ("Status", "Active" if c['Active'] else "Inactive"),
        ]
        
        for label, value in detail_items:
            row_frame = ttk.Frame(basic_frame)
            row_frame.pack(fill='x', pady=3)
            
            ttk.Label(row_frame, text=f"{label}:", 
                     font=('Arial', 9, 'bold'),
                     width=15,
                     anchor='w').pack(side='left')
            
            ttk.Label(row_frame, text=value, 
                     font=('Arial', 9),
                     foreground=COLORS['accent']).pack(side='left', padx=10)
        
        # Contact Information Section
        contact_frame = ttk.LabelFrame(content_frame, text="Contact Information", 
                                      padding=10)
        contact_frame.pack(fill='x', padx=5, pady=5)
        
        contact_items = [
            ("Contact Person", c['ContactName']),
            ("Email", c['ContactEmail']),
            ("Phone", c['ContactPhone']),
        ]
        
        for label, value in contact_items:
            row_frame = ttk.Frame(contact_frame)
            row_frame.pack(fill='x', pady=3)
            
            ttk.Label(row_frame, text=f"{label}:", 
                     font=('Arial', 9, 'bold'),
                     width=15,
                     anchor='w').pack(side='left')
            
            value_text = value if value else "—"
            ttk.Label(row_frame, text=value_text, 
                     font=('Arial', 9)).pack(side='left', padx=10)
        
        # Billing Address Section
        if c['BillingAddress']:
            address_frame = ttk.LabelFrame(content_frame, 
                                          text="Billing Address", 
                                          padding=10)
            address_frame.pack(fill='x', padx=5, pady=5)
            
            addr_label = tk.Text(address_frame, height=4, width=35, 
                                wrap='word', relief='flat',
                                bg=COLORS['bg_medium'],
                                fg=COLORS['text_primary'])
            configure_text_widget(addr_label)
            addr_label.insert('1.0', c['BillingAddress'])
            addr_label.configure(state='disabled')
            addr_label.pack(fill='both', expand=True)
        
        # Timestamps
        meta_frame = ttk.LabelFrame(content_frame, text="Record Info", padding=10)
        meta_frame.pack(fill='x', padx=5, pady=5)
        
        meta_items = [
            ("Created", c['CreatedDate'].strftime('%Y-%m-%d %H:%M')),
            ("Modified", c['ModifiedDate'].strftime('%Y-%m-%d %H:%M')),
        ]
        
        for label, value in meta_items:
            row_frame = ttk.Frame(meta_frame)
            row_frame.pack(fill='x', pady=2)
            
            ttk.Label(row_frame, text=f"{label}:", 
                     font=('Arial', 8),
                     width=15,
                     anchor='w',
                     foreground=COLORS['text_secondary']).pack(side='left')
            
            ttk.Label(row_frame, text=value, 
                     font=('Arial', 8),
                     foreground=COLORS['text_secondary']).pack(side='left', padx=10)
        
        # Pack canvas and scrollbar
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def load_clients(self):
        """Load clients from database with error handling"""
        try:
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Load clients
            self.clients = db.get_all_clients(active_only=True)
            
            # Populate treeview
            for client in self.clients:
                self.tree.insert('', 'end', values=(
                    client['ClientName'],
                    f"${client['DefaultRate']:.2f}",
                    client['ContactName'] or '—'
                ))
            
            # Update stats
            self.stats_label.config(text=f"{len(self.clients)} active clients")
            self.update_status(f"Loaded {len(self.clients)} clients", 2000)
            
        except DatabaseError as e:
            messagebox.showerror("Database Error", 
                               f"Failed to load clients:\n{str(e)}")
            self.update_status("Error loading clients", 3000)
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")
            self.update_status("Error", 3000)
    
    def add_client(self):
        """Open dialog to add new client"""
        dialog = ClientDialog(self, "Add New Client")
        self.wait_window(dialog)
        
        if dialog.result:
            try:
                self.update_status("Adding client...", 0)
                
                db.add_client(
                    dialog.result['name'],
                    dialog.result['rate'],
                    dialog.result['terms'],
                    contact_name=dialog.result['contact_name'],
                    contact_email=dialog.result['contact_email'],
                    contact_phone=dialog.result['contact_phone'],
                    billing_address=dialog.result['billing_address']
                )
                
                messagebox.showinfo("Success", 
                                   f"✓ Client '{dialog.result['name']}' added!")
                self.load_clients()
                self.update_status("Client added successfully", 2000)
                
            except ValidationError as e:
                messagebox.showerror("Validation Error", str(e))
                self.update_status("Validation error", 3000)
            except DatabaseError as e:
                messagebox.showerror("Database Error", f"Failed to add client:\n{str(e)}")
                self.update_status("Error adding client", 3000)
            except Exception as e:
                messagebox.showerror("Error", f"Unexpected error: {str(e)}")
                self.update_status("Error", 3000)
    
    def edit_client(self):
        """Open dialog to edit selected client"""
        if not self.selected_client:
            messagebox.showwarning("No Selection", 
                                 "Please select a client to edit")
            return
        
        client = self.selected_client
        
        # Open edit dialog
        dialog = ClientDialog(self, "Edit Client", 
                            initial_data={
                                'name': client['ClientName'],
                                'rate': client['DefaultRate'],
                                'terms': client['PaymentTerms'],
                                'contact_name': client['ContactName'],
                                'contact_email': client['ContactEmail'],
                                'contact_phone': client['ContactPhone'],
                                'billing_address': client['BillingAddress']
                            })
        self.wait_window(dialog)
        
        if dialog.result:
            try:
                self.update_status("Updating client...", 0)
                
                db.update_client(
                    client['ClientID'],
                    client_name=dialog.result['name'],
                    default_rate=dialog.result['rate'],
                    payment_terms=dialog.result['terms'],
                    contact_name=dialog.result['contact_name'],
                    contact_email=dialog.result['contact_email'],
                    contact_phone=dialog.result['contact_phone'],
                    billing_address=dialog.result['billing_address']
                )
                
                messagebox.showinfo("Success", "✓ Client updated!")
                self.load_clients()
                self.update_status("Client updated successfully", 2000)
                
            except ValidationError as e:
                messagebox.showerror("Validation Error", str(e))
                self.update_status("Validation error", 3000)
            except DatabaseError as e:
                messagebox.showerror("Database Error", f"Failed to update:\n{str(e)}")
                self.update_status("Error updating client", 3000)
            except Exception as e:
                messagebox.showerror("Error", f"Unexpected error: {str(e)}")
                self.update_status("Error", 3000)
    
    def deactivate_client(self):
        """Deactivate selected client"""
        if not self.selected_client:
            messagebox.showwarning("No Selection", 
                                 "Please select a client to deactivate")
            return
        
        client = self.selected_client
        
        # Confirm deactivation
        if messagebox.askyesno("Confirm Deactivation", 
                              f"Deactivate '{client['ClientName']}'?\n\n" +
                              "They will no longer appear in timesheets."):
            try:
                self.update_status("Deactivating client...", 0)
                
                db.delete_client(client['ClientID'])
                
                messagebox.showinfo("Success", "✓ Client deactivated!")
                self.load_clients()
                self.selected_client = None
                self.setup_details_panel()
                self.update_status("Client deactivated", 2000)
                
            except DatabaseError as e:
                messagebox.showerror("Database Error", f"Failed to deactivate:\n{str(e)}")
                self.update_status("Error deactivating client", 3000)
            except Exception as e:
                messagebox.showerror("Error", f"Unexpected error: {str(e)}")
                self.update_status("Error", 3000)
    
    def update_status(self, message, timeout=0):
        """Update status bar with temporary message
        
        Args:
            message: Status message to display
            timeout: How long to show (ms), 0 = permanent
        """
        self.status_label.config(text=message)
        if timeout > 0:
            self.after(timeout, lambda: self.status_label.config(text="Ready"))


class ClientDialog(tk.Toplevel):
    """Enhanced dialog for adding/editing clients"""
    
    def __init__(self, parent, title, initial_data=None):
        super().__init__(parent)
        self.title(title)
        self.result = None
        self.initial_data = initial_data or {}
        
        # Configure dark theme
        self.configure(bg=COLORS['bg_dark'])
        
        # Make dialog modal
        self.transient(parent)
        self.grab_set()
        
        self.setup_ui()
        
        # Center dialog on parent
        self.update_idletasks()
        width = 550
        height = 680
        x = parent.winfo_x() + (parent.winfo_width() - width) // 2
        y = parent.winfo_y() + (parent.winfo_height() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
        
        # Focus on name field
        self.name_entry.focus()
    
    def setup_ui(self):
        """Setup dialog UI with improved layout"""
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Basic Information Section
        basic_section = ttk.LabelFrame(main_frame, text="Basic Information", 
                                      padding=15)
        basic_section.grid(row=0, column=0, sticky='ew', pady=(0, 15))
        
        # Client Name
        ttk.Label(basic_section, text="Client Name:").grid(row=0, column=0, 
                                                           sticky='w', pady=8)
        self.name_var = tk.StringVar(value=self.initial_data.get('name', ''))
        self.name_entry = ttk.Entry(basic_section, textvariable=self.name_var, 
                                   width=40)
        self.name_entry.grid(row=0, column=1, pady=8, sticky='ew')
        
        # Default Rate
        ttk.Label(basic_section, text="Hourly Rate ($):").grid(row=1, column=0, 
                                                               sticky='w', pady=8)
        self.rate_var = tk.StringVar(value=str(self.initial_data.get('rate', '150.00')))
        rate_entry = ttk.Entry(basic_section, textvariable=self.rate_var, width=15)
        rate_entry.grid(row=1, column=1, sticky='w', pady=8)
        
        # Payment Terms
        ttk.Label(basic_section, text="Payment Terms (days):").grid(row=2, column=0, 
                                                                    sticky='w', pady=8)
        self.terms_var = tk.StringVar(value=str(self.initial_data.get('terms', '30')))
        terms_entry = ttk.Entry(basic_section, textvariable=self.terms_var, width=15)
        terms_entry.grid(row=2, column=1, sticky='w', pady=8)
        
        basic_section.columnconfigure(1, weight=1)
        
        # Contact Information Section
        contact_section = ttk.LabelFrame(main_frame, text="Contact Information", 
                                        padding=15)
        contact_section.grid(row=1, column=0, sticky='ew', pady=(0, 15))
        
        # Contact Name
        ttk.Label(contact_section, text="Contact Person:").grid(row=0, column=0, 
                                                                sticky='w', pady=8)
        self.contact_name_var = tk.StringVar(
            value=self.initial_data.get('contact_name', ''))
        contact_name_entry = ttk.Entry(contact_section, 
                                      textvariable=self.contact_name_var, width=40)
        contact_name_entry.grid(row=0, column=1, pady=8, sticky='ew')
        
        # Contact Email
        ttk.Label(contact_section, text="Email:").grid(row=1, column=0, 
                                                       sticky='w', pady=8)
        self.contact_email_var = tk.StringVar(
            value=self.initial_data.get('contact_email', ''))
        contact_email_entry = ttk.Entry(contact_section, 
                                       textvariable=self.contact_email_var, width=40)
        contact_email_entry.grid(row=1, column=1, pady=8, sticky='ew')
        
        # Contact Phone
        ttk.Label(contact_section, text="Phone:").grid(row=2, column=0, 
                                                       sticky='w', pady=8)
        self.contact_phone_var = tk.StringVar(
            value=self.initial_data.get('contact_phone', ''))
        contact_phone_entry = ttk.Entry(contact_section, 
                                       textvariable=self.contact_phone_var, width=40)
        contact_phone_entry.grid(row=2, column=1, pady=8, sticky='ew')
        
        contact_section.columnconfigure(1, weight=1)
        
        # Billing Address Section
        address_section = ttk.LabelFrame(main_frame, text="Billing Address", 
                                        padding=15)
        address_section.grid(row=2, column=0, sticky='nsew', pady=(0, 15))
        
        # Billing Address (Text widget for multi-line)
        ttk.Label(address_section, text="Address:").pack(anchor='w', pady=(0, 5))
        self.billing_address_text = tk.Text(address_section, height=4, width=48, 
                                            wrap='word')
        configure_text_widget(self.billing_address_text)
        self.billing_address_text.pack(fill='both', expand=True)
        
        # Insert initial value
        initial_address = self.initial_data.get('billing_address', '')
        if initial_address:
            self.billing_address_text.insert('1.0', initial_address)
        
        address_section.rowconfigure(1, weight=1)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, pady=15, sticky='ew')
        
        ttk.Button(button_frame, text="✓ Save", 
                  command=self.save,
                  style='Accent.TButton').pack(side='left', padx=5)
        ttk.Button(button_frame, text="✕ Cancel", 
                  command=self.cancel).pack(side='left', padx=5)
        
        # Configure main frame weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Bind keys
        self.bind('<Return>', lambda e: self.save())
        self.bind('<Escape>', lambda e: self.cancel())
    
    def save(self):
        """Validate and save client data"""
        name = self.name_var.get().strip()
        rate_str = self.rate_var.get().strip()
        terms_str = self.terms_var.get().strip()
        contact_name = self.contact_name_var.get().strip()
        contact_email = self.contact_email_var.get().strip()
        contact_phone = self.contact_phone_var.get().strip()
        billing_address = self.billing_address_text.get('1.0', 'end').strip()
        
        # Validate
        if not name:
            messagebox.showerror("Validation Error", "Client name is required")
            self.name_entry.focus()
            return
        
        try:
            rate = float(rate_str)
            if rate < 0:
                raise ValueError("Rate must be positive")
        except ValueError:
            messagebox.showerror("Validation Error", 
                               "Please enter a valid hourly rate")
            return
        
        try:
            terms = int(terms_str)
            if terms < 0:
                raise ValueError("Terms must be positive")
        except ValueError:
            messagebox.showerror("Validation Error", 
                               "Please enter valid payment terms (days)")
            return
        
        # Set result
        self.result = {
            'name': name,
            'rate': rate,
            'terms': terms,
            'contact_name': contact_name,
            'contact_email': contact_email,
            'contact_phone': contact_phone,
            'billing_address': billing_address
        }
        
        self.destroy()
    
    def cancel(self):
        """Cancel dialog"""
        self.destroy()
