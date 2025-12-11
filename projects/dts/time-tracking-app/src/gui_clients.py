"""
Time Tracking App - Client Management GUI
Allows adding, editing, and viewing clients with contact information
"""

import tkinter as tk
from tkinter import ttk, messagebox
from db_helper import db
from theme import COLORS, configure_text_widget

class ClientManagementFrame(ttk.Frame):
    """Client management screen"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.clients = []
        
        self.setup_ui()
        self.load_clients()
    
    def setup_ui(self):
        """Setup the user interface"""
        
        # Title
        title = ttk.Label(self, text="Client Management", 
                         style='Title.TLabel')
        title.grid(row=0, column=0, columnspan=3, pady=20, padx=20, sticky='w')
        
        # Client list frame
        list_frame = ttk.LabelFrame(self, text="Active Clients", padding=15)
        list_frame.grid(row=1, column=0, columnspan=3, sticky='nsew', 
                       padx=20, pady=10)
        
        # Treeview for client list
        columns = ('ID', 'Client Name', 'Rate', 'Contact', 'Email')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', 
                                height=12)
        
        # Column headings
        self.tree.heading('ID', text='ID')
        self.tree.heading('Client Name', text='Client Name')
        self.tree.heading('Rate', text='Hourly Rate')
        self.tree.heading('Contact', text='Contact Person')
        self.tree.heading('Email', text='Email')
        
        # Column widths
        self.tree.column('ID', width=50)
        self.tree.column('Client Name', width=200)
        self.tree.column('Rate', width=100)
        self.tree.column('Contact', width=180)
        self.tree.column('Email', width=200)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', 
                                 command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')
        
        list_frame.rowconfigure(0, weight=1)
        list_frame.columnconfigure(0, weight=1)
        
        # Button frame
        button_frame = ttk.Frame(self)
        button_frame.grid(row=2, column=0, columnspan=3, pady=15, padx=20)
        
        ttk.Button(button_frame, text="Add New Client", 
                  command=self.add_client,
                  style='Accent.TButton').pack(side='left', padx=5)
        ttk.Button(button_frame, text="Edit Selected", 
                  command=self.edit_client).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Deactivate Selected", 
                  command=self.deactivate_client).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Refresh", 
                  command=self.load_clients).pack(side='left', padx=5)
        
        # Configure grid weights
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
    
    def load_clients(self):
        """Load clients from database"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load clients
        self.clients = db.get_all_clients(active_only=True)
        
        # Populate treeview
        for client in self.clients:
            self.tree.insert('', 'end', values=(
                client['ClientID'],
                client['ClientName'],
                f"${client['DefaultRate']:.2f}",
                client['ContactName'] or '—',
                client['ContactEmail'] or '—'
            ))
    
    def add_client(self):
        """Open dialog to add new client"""
        dialog = ClientDialog(self, "Add New Client")
        self.wait_window(dialog)
        
        if dialog.result:
            try:
                client_id = db.add_client(
                    dialog.result['name'],
                    dialog.result['rate'],
                    dialog.result['terms'],
                    contact_name=dialog.result['contact_name'],
                    contact_email=dialog.result['contact_email'],
                    contact_phone=dialog.result['contact_phone'],
                    billing_address=dialog.result['billing_address']
                )
                messagebox.showinfo("Success", 
                                   f"Client '{dialog.result['name']}' added successfully!")
                self.load_clients()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add client: {str(e)}")
    
    def edit_client(self):
        """Open dialog to edit selected client"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", 
                                 "Please select a client to edit")
            return
        
        # Get selected client data
        item = self.tree.item(selection[0])
        client_id = item['values'][0]
        
        # Find client in list
        client = next((c for c in self.clients if c['ClientID'] == client_id), None)
        if not client:
            return
        
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
                db.update_client(
                    client_id,
                    client_name=dialog.result['name'],
                    default_rate=dialog.result['rate'],
                    payment_terms=dialog.result['terms'],
                    contact_name=dialog.result['contact_name'],
                    contact_email=dialog.result['contact_email'],
                    contact_phone=dialog.result['contact_phone'],
                    billing_address=dialog.result['billing_address']
                )
                messagebox.showinfo("Success", "Client updated successfully!")
                self.load_clients()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update client: {str(e)}")
    
    def deactivate_client(self):
        """Deactivate selected client"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", 
                                 "Please select a client to deactivate")
            return
        
        item = self.tree.item(selection[0])
        client_id = item['values'][0]
        client_name = item['values'][1]
        
        # Confirm deactivation
        if messagebox.askyesno("Confirm Deactivation", 
                              f"Deactivate client '{client_name}'?\n\n" +
                              "They will no longer appear in timesheets."):
            try:
                db.delete_client(client_id)
                messagebox.showinfo("Success", "Client deactivated successfully!")
                self.load_clients()
            except Exception as e:
                messagebox.showerror("Error", 
                                   f"Failed to deactivate client: {str(e)}")


class ClientDialog(tk.Toplevel):
    """Dialog for adding/editing a client with contact information"""
    
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
        
        # Center dialog
        self.update_idletasks()
        width = 500
        height = 600
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_ui(self):
        """Setup dialog UI"""
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Basic Information Section
        basic_section = ttk.LabelFrame(main_frame, text="Basic Information", padding=15)
        basic_section.grid(row=0, column=0, sticky='ew', pady=(0, 15))
        
        # Client Name
        ttk.Label(basic_section, text="Client Name:").grid(row=0, column=0, 
                                                           sticky='w', pady=5)
        self.name_var = tk.StringVar(value=self.initial_data.get('name', ''))
        name_entry = ttk.Entry(basic_section, textvariable=self.name_var, width=40)
        name_entry.grid(row=0, column=1, pady=5, sticky='ew')
        name_entry.focus()
        
        # Default Rate
        ttk.Label(basic_section, text="Hourly Rate ($):").grid(row=1, column=0, 
                                                               sticky='w', pady=5)
        self.rate_var = tk.StringVar(value=str(self.initial_data.get('rate', '150.00')))
        rate_entry = ttk.Entry(basic_section, textvariable=self.rate_var, width=20)
        rate_entry.grid(row=1, column=1, sticky='w', pady=5)
        
        # Payment Terms
        ttk.Label(basic_section, text="Payment Terms (days):").grid(row=2, column=0, 
                                                                    sticky='w', pady=5)
        self.terms_var = tk.StringVar(value=str(self.initial_data.get('terms', '30')))
        terms_entry = ttk.Entry(basic_section, textvariable=self.terms_var, width=20)
        terms_entry.grid(row=2, column=1, sticky='w', pady=5)
        
        basic_section.columnconfigure(1, weight=1)
        
        # Contact Information Section
        contact_section = ttk.LabelFrame(main_frame, text="Contact Information", padding=15)
        contact_section.grid(row=1, column=0, sticky='ew', pady=(0, 15))
        
        # Contact Name
        ttk.Label(contact_section, text="Contact Person:").grid(row=0, column=0, 
                                                                sticky='w', pady=5)
        self.contact_name_var = tk.StringVar(value=self.initial_data.get('contact_name', ''))
        contact_name_entry = ttk.Entry(contact_section, textvariable=self.contact_name_var, width=40)
        contact_name_entry.grid(row=0, column=1, pady=5, sticky='ew')
        
        # Contact Email
        ttk.Label(contact_section, text="Email:").grid(row=1, column=0, 
                                                       sticky='w', pady=5)
        self.contact_email_var = tk.StringVar(value=self.initial_data.get('contact_email', ''))
        contact_email_entry = ttk.Entry(contact_section, textvariable=self.contact_email_var, width=40)
        contact_email_entry.grid(row=1, column=1, pady=5, sticky='ew')
        
        # Contact Phone
        ttk.Label(contact_section, text="Phone:").grid(row=2, column=0, 
                                                       sticky='w', pady=5)
        self.contact_phone_var = tk.StringVar(value=self.initial_data.get('contact_phone', ''))
        contact_phone_entry = ttk.Entry(contact_section, textvariable=self.contact_phone_var, width=40)
        contact_phone_entry.grid(row=2, column=1, pady=5, sticky='ew')
        
        contact_section.columnconfigure(1, weight=1)
        
        # Billing Address Section
        address_section = ttk.LabelFrame(main_frame, text="Billing Address", padding=15)
        address_section.grid(row=2, column=0, sticky='nsew', pady=(0, 15))
        
        # Billing Address (Text widget for multi-line)
        self.billing_address_text = tk.Text(address_section, height=4, width=40, wrap='word')
        configure_text_widget(self.billing_address_text)
        self.billing_address_text.grid(row=0, column=0, sticky='nsew')
        
        # Insert initial value
        initial_address = self.initial_data.get('billing_address', '')
        if initial_address:
            self.billing_address_text.insert('1.0', initial_address)
        
        address_section.rowconfigure(0, weight=1)
        address_section.columnconfigure(0, weight=1)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, pady=10)
        
        ttk.Button(button_frame, text="Save", 
                  command=self.save,
                  style='Accent.TButton').pack(side='left', padx=5)
        ttk.Button(button_frame, text="Cancel", 
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
