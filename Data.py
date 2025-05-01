import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import os
import seaborn as sns

class DataVisualizationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Data Visualization App")
        self.root.geometry("1200x1200")
        self.root.configure(bg="#f5f5f5")
        
        # Set theme and style
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#f5f5f5")
        self.style.configure("TButton", font=("Arial", 10), background="#4CAF50")
        self.style.configure("TLabel", font=("Arial", 11), background="#f5f5f5")
        self.style.configure("Header.TLabel", font=("Arial", 14, "bold"), background="#f5f5f5")
        self.style.configure("Subheader.TLabel", font=("Arial", 12), background="#f5f5f5")
        
        # Initialize variables
        self.df = None
        self.column_names = tk.StringVar()
        self.x_column = tk.StringVar()
        self.y_column = tk.StringVar()
        self.graph_option = tk.StringVar(value="Line")
        self.color_option = tk.StringVar(value="blue")
        self.title_text = tk.StringVar(value="Data Visualization")
        self.show_grid = tk.BooleanVar(value=True)
        self.group_column = tk.StringVar()
        self.current_figure = None
        self.canvas = None
        
        # Create main frames
        self.create_main_layout()
        
        # Create menu
        self.create_menu()
        
    def create_main_layout(self):
        # Main container with two panels
        main_container = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel for controls
        self.left_frame = ttk.Frame(main_container, padding="10")
        
        # Right panel for visualization
        self.right_frame = ttk.Frame(main_container, padding="10")
        
        main_container.add(self.left_frame, weight=30)
        main_container.add(self.right_frame, weight=70)
        
        # Setup control panel
        self.setup_control_panel()
        
        # Setup visualization panel
        self.setup_visualization_panel()
        
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load Data", command=self.load_data)
        file_menu.add_command(label="Save Plot", command=self.save_plot)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Clear Plot", command=self.clear_plot)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
    def setup_control_panel(self):
        # Data section
        data_frame = ttk.LabelFrame(self.left_frame, text="Data", padding="10")
        data_frame.pack(fill=tk.X, expand=False, pady=5)
        
        ttk.Button(data_frame, text="Load Data", command=self.load_data).pack(fill=tk.X, pady=5)
        
        ttk.Label(data_frame, text="Available Columns:").pack(anchor=tk.W, pady=(10, 0))
        columns_display = ttk.Label(data_frame, textvariable=self.column_names, wraplength=300)
        columns_display.pack(fill=tk.X, pady=5)
        
        # Data preview button
        ttk.Button(data_frame, text="Preview Data", command=self.preview_data).pack(fill=tk.X, pady=5)
        
        # Plot configuration section
        plot_frame = ttk.LabelFrame(self.left_frame, text="Plot Configuration", padding="10")
        plot_frame.pack(fill=tk.X, expand=False, pady=10)
        
        # X and Y axis selection
        ttk.Label(plot_frame, text="X-axis Column:").pack(anchor=tk.W, pady=(5, 0))
        self.x_column_combo = ttk.Combobox(plot_frame, textvariable=self.x_column, state="readonly")
        self.x_column_combo.pack(fill=tk.X, pady=5)
        
        ttk.Label(plot_frame, text="Y-axis Column:").pack(anchor=tk.W, pady=(5, 0))
        self.y_column_combo = ttk.Combobox(plot_frame, textvariable=self.y_column, state="readonly")
        self.y_column_combo.pack(fill=tk.X, pady=5)
        
        ttk.Label(plot_frame, text="Group by Column (optional):").pack(anchor=tk.W, pady=(5, 0))
        self.group_column_combo = ttk.Combobox(plot_frame, textvariable=self.group_column, state="readonly")
        self.group_column_combo.pack(fill=tk.X, pady=5)
        
        # Graph type selection
        ttk.Label(plot_frame, text="Select Graph Type:").pack(anchor=tk.W, pady=(5, 0))
        graph_types = ["Line", "Bar", "Scatter", "Pie", "Histogram", "Box", "Violin", "Heatmap", "Area", "Bubble"]
        self.graph_dropdown = ttk.Combobox(plot_frame, textvariable=self.graph_option, values=graph_types, state="readonly")
        self.graph_dropdown.pack(fill=tk.X, pady=5)
        
        # Appearance section
        appearance_frame = ttk.LabelFrame(self.left_frame, text="Appearance", padding="10")
        appearance_frame.pack(fill=tk.X, expand=False, pady=10)
        
        ttk.Label(appearance_frame, text="Plot Title:").pack(anchor=tk.W, pady=(5, 0))
        ttk.Entry(appearance_frame, textvariable=self.title_text).pack(fill=tk.X, pady=5)
        
        ttk.Label(appearance_frame, text="Color Theme:").pack(anchor=tk.W, pady=(5, 0))
        color_options = ["blue", "green", "red", "purple", "orange", "viridis", "plasma", "inferno", "magma", "cividis"]
        ttk.Combobox(appearance_frame, textvariable=self.color_option, values=color_options, state="readonly").pack(fill=tk.X, pady=5)
        
        ttk.Checkbutton(appearance_frame, text="Show Grid", variable=self.show_grid).pack(anchor=tk.W, pady=5)
        
        # Action buttons
        action_frame = ttk.Frame(self.left_frame, padding="10")
        action_frame.pack(fill=tk.X, expand=False, pady=10)
        
        ttk.Button(action_frame, text="Plot Graph", command=self.plot_graph, style="TButton").pack(fill=tk.X, pady=5)
        ttk.Button(action_frame, text="Save Plot", command=self.save_plot).pack(fill=tk.X, pady=5)
        ttk.Button(action_frame, text="Clear Plot", command=self.clear_plot).pack(fill=tk.X, pady=5)
        
    def setup_visualization_panel(self):
        # Create a frame for the plot
        self.plot_container = ttk.Frame(self.right_frame, padding="10")
        self.plot_container.pack(fill=tk.BOTH, expand=True)
        
        # Initial message
        ttk.Label(self.plot_container, text="Load data and configure plot options to visualize", 
                 style="Header.TLabel").pack(pady=50)
        
    def load_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx;*.xls"), ("All Files", "*.*")])
        if not file_path:
            return
            
        try:
            # Determine file type and load accordingly
            if file_path.endswith(('.xlsx', '.xls')):
                self.df = pd.read_excel(file_path)
            else:  # Default to CSV
                self.df = pd.read_csv(file_path)
                
            # Update column names display
            self.column_names.set(", ".join(self.df.columns))
            
            # Update comboboxes with column names
            self.update_column_comboboxes()
            
            # Show success message
            messagebox.showinfo("Success", f"Data loaded successfully: {len(self.df)} rows, {len(self.df.columns)} columns")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
            
    def update_column_comboboxes(self):
        if self.df is not None:
            columns = list(self.df.columns)
            
            self.x_column_combo['values'] = columns
            self.y_column_combo['values'] = columns
            self.group_column_combo['values'] = [""] + columns  # Empty option for no grouping
            
            # Set default values if possible
            if len(columns) > 0:
                self.x_column.set(columns[0])
            if len(columns) > 1:
                self.y_column.set(columns[1])
            self.group_column.set("")
            
    def preview_data(self):
        if self.df is None:
            messagebox.showinfo("Info", "No data loaded yet.")
            return
            
        # Create a new window for data preview
        preview_window = tk.Toplevel(self.root)
        preview_window.title("Data Preview")
        preview_window.geometry("800x600")
        
        # Create a frame for the preview
        frame = ttk.Frame(preview_window, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Add a treeview to display the data
        columns = list(self.df.columns)
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        
        # Set column headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        # Add data rows (limit to first 100 for performance)
        for i, row in self.df.head(100).iterrows():
            values = [str(row[col]) for col in columns]
            tree.insert("", "end", values=values)
        
        # Add scrollbars
        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid layout
        tree.grid(column=0, row=0, sticky='nsew')
        vsb.grid(column=1, row=0, sticky='ns')
        hsb.grid(column=0, row=1, sticky='ew')
        
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        
        # Add info label
        if len(self.df) > 100:
            ttk.Label(frame, text=f"Showing first 100 of {len(self.df)} rows").grid(column=0, row=2, sticky='w')
            
    def plot_graph(self):
        if self.df is None:
            messagebox.showinfo("Info", "Please load data first.")
            return
            
        x_col = self.x_column.get()
        y_col = self.y_column.get()
        group_col = self.group_column.get()
        graph_type = self.graph_option.get()
        
        # Validate column selections
        if not x_col or not y_col:
            messagebox.showwarning("Warning", "Please select both X and Y columns.")
            return
            
        if x_col not in self.df.columns or y_col not in self.df.columns:
            messagebox.showerror("Error", "Selected columns not found in data.")
            return
            
        if group_col and group_col not in self.df.columns:
            messagebox.showerror("Error", "Selected group column not found in data.")
            return
            
        # Clear previous plot
        self.clear_plot()
        
        try:
            # Create figure and axis
            fig = Figure(figsize=(8, 6), dpi=100)
            ax = fig.add_subplot(111)
            
            # Set color map/cycle based on selection
            color = self.color_option.get()
            if color in ['viridis', 'plasma', 'inferno', 'magma', 'cividis']:
                cmap = plt.get_cmap(color)
            else:
                cmap = None
                
            # Handle different plot types
            if graph_type == "Line":
                self.create_line_plot(ax, x_col, y_col, group_col, color)
            elif graph_type == "Bar":
                self.create_bar_plot(ax, x_col, y_col, group_col, color)
            elif graph_type == "Scatter":
                self.create_scatter_plot(ax, x_col, y_col, group_col, color)
            elif graph_type == "Pie":
                self.create_pie_chart(ax, x_col, y_col)
            elif graph_type == "Histogram":
                self.create_histogram(ax, x_col, y_col, color)
            elif graph_type == "Box":
                self.create_box_plot(ax, x_col, y_col, group_col, color)
            elif graph_type == "Violin":
                self.create_violin_plot(ax, x_col, y_col, group_col, color)
            elif graph_type == "Heatmap":
                self.create_heatmap(fig, ax, color)
            elif graph_type == "Area":
                self.create_area_plot(ax, x_col, y_col, group_col, color)
            elif graph_type == "Bubble":
                self.create_bubble_plot(ax, x_col, y_col, group_col, color)
            else:
                messagebox.showerror("Error", f"Unknown graph type: {graph_type}")
                return
                
            # Set title and grid
            ax.set_title(self.title_text.get())
            ax.grid(self.show_grid.get())
            
            # Create canvas
            self.current_figure = fig
            self.canvas = FigureCanvasTkAgg(fig, master=self.plot_container)
            canvas_widget = self.canvas.get_tk_widget()
            canvas_widget.pack(fill=tk.BOTH, expand=True)
            
            # Add toolbar
            from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
            toolbar = NavigationToolbar2Tk(self.canvas, self.plot_container)
            toolbar.update()
            
            # Draw the plot
            self.canvas.draw()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create plot: {str(e)}")
            
    def create_line_plot(self, ax, x_col, y_col, group_col, color):
        if group_col:
            for name, group in self.df.groupby(group_col):
                ax.plot(group[x_col], group[y_col], marker='o', linestyle='-', label=str(name))
            ax.legend()
        else:
            ax.plot(self.df[x_col], self.df[y_col], marker='o', linestyle='-', color=color)
        
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        
    def create_bar_plot(self, ax, x_col, y_col, group_col, color):
        if group_col:
            # Grouped bar chart
            groups = self.df[group_col].unique()
            x_values = self.df[x_col].unique()
            
            bar_width = 0.8 / len(groups)
            
            for i, group_name in enumerate(groups):
                group_data = self.df[self.df[group_col] == group_name]
                x_positions = np.arange(len(x_values))
                
                # Create a dictionary to map x values to their corresponding y values
                y_values = []
                for x_val in x_values:
                    matching_rows = group_data[group_data[x_col] == x_val]
                    if not matching_rows.empty:
                        y_values.append(matching_rows[y_col].iloc[0])
                    else:
                        y_values.append(0)
                
                ax.bar(x_positions + i * bar_width - 0.4 + bar_width/2, 
                       y_values, 
                       width=bar_width, 
                       label=str(group_name))
                
            ax.set_xticks(np.arange(len(x_values)))
            ax.set_xticklabels([str(x) for x in x_values])
            ax.legend()
        else:
            # Simple bar chart
            ax.bar(self.df[x_col], self.df[y_col], color=color)
        
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        
    def create_scatter_plot(self, ax, x_col, y_col, group_col, color):
        if group_col:
            for name, group in self.df.groupby(group_col):
                ax.scatter(group[x_col], group[y_col], label=str(name), alpha=0.7)
            ax.legend()
        else:
            ax.scatter(self.df[x_col], self.df[y_col], color=color, alpha=0.7)
        
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        
    def create_pie_chart(self, ax, x_col, y_col):
        # For pie charts, we need to aggregate data
        pie_data = self.df.groupby(x_col)[y_col].sum()
        
        # Only show top 10 categories if there are too many
        if len(pie_data) > 10:
            top_data = pie_data.nlargest(9)
            other_sum = pie_data.sum() - top_data.sum()
            top_data['Other'] = other_sum
            pie_data = top_data
            
        ax.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        
    def create_histogram(self, ax, x_col, y_col, color):
        # For histogram, we only need one column
        ax.hist(self.df[x_col], bins=20, color=color, alpha=0.7)
        ax.set_xlabel(x_col)
        ax.set_ylabel('Frequency')
        
    def create_box_plot(self, ax, x_col, y_col, group_col, color):
        if group_col:
            # Create a box plot grouped by the group column
            sns.boxplot(x=x_col, y=y_col, hue=group_col, data=self.df, ax=ax)
        else:
            # Create a simple box plot
            sns.boxplot(x=x_col, y=y_col, data=self.df, ax=ax, color=color)
            
    def create_violin_plot(self, ax, x_col, y_col, group_col, color):
        if group_col:
            # Create a violin plot grouped by the group column
            sns.violinplot(x=x_col, y=y_col, hue=group_col, data=self.df, ax=ax)
        else:
            # Create a simple violin plot
            sns.violinplot(x=x_col, y=y_col, data=self.df, ax=ax, color=color)
            
    def create_heatmap(self, fig, ax, color):
        # For heatmap, we need numerical columns only
        numeric_df = self.df.select_dtypes(include=[np.number])
        
        if numeric_df.empty:
            messagebox.showwarning("Warning", "No numerical columns found for heatmap.")
            return
            
        # Calculate correlation matrix
        corr = numeric_df.corr()
        
        # Create heatmap
        sns.heatmap(corr, annot=True, cmap=color if color in ['viridis', 'plasma', 'inferno', 'magma', 'cividis'] else 'coolwarm', 
                   linewidths=.5, ax=ax)
                   
    def create_area_plot(self, ax, x_col, y_col, group_col, color):
        if group_col:
            # Create a stacked area plot
            pivot_df = self.df.pivot_table(index=x_col, columns=group_col, values=y_col, aggfunc='sum')
            pivot_df.plot.area(ax=ax, stacked=True)
        else:
            # Create a simple area plot
            ax.fill_between(self.df[x_col], self.df[y_col], color=color, alpha=0.5)
            ax.plot(self.df[x_col], self.df[y_col], color=color)
            
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        
    def create_bubble_plot(self, ax, x_col, y_col, group_col, color):
        # For bubble plot, we need a third dimension for size
        # Use the mean of all numeric columns as size if no group column is specified
        
        if group_col:
            # Use group column for color and mean of numeric columns for size
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            size_col = numeric_cols[0] if len(numeric_cols) > 0 else None
            
            if size_col:
                for name, group in self.df.groupby(group_col):
                    ax.scatter(group[x_col], group[y_col], 
                              s=group[size_col] * 20,  # Scale size for visibility
                              label=str(name), alpha=0.7)
                ax.legend()
            else:
                messagebox.showwarning("Warning", "No numerical column found for bubble size.")
                return
        else:
            # Use a constant size if no group column
            ax.scatter(self.df[x_col], self.df[y_col], 
                      s=100,  # Constant size
                      color=color, alpha=0.7)
            
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        
    def clear_plot(self):
        # Clear the plot container
        for widget in self.plot_container.winfo_children():
            widget.destroy()
            
        self.current_figure = None
        self.canvas = None
        
    def save_plot(self):
        if self.current_figure is None:
            messagebox.showinfo("Info", "No plot to save.")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("PDF files", "*.pdf"), ("SVG files", "*.svg")]
        )
        
        if file_path:
            try:
                self.current_figure.savefig(file_path, dpi=300, bbox_inches='tight')
                messagebox.showinfo("Success", f"Plot saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save plot: {str(e)}")
                
    def show_about(self):
        about_text = """
        Enhanced Data Visualization App
        
        A powerful tool for visualizing and analyzing data.
        
        Features:
        - Load CSV and Excel files
        - Multiple plot types
        - Customizable appearance
        - Data preview
        - Save plots in various formats
        
        Created with Python, Tkinter, Pandas, and Matplotlib.
        """
        
        messagebox.showinfo("About", about_text)

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = DataVisualizationApp(root)
    root.mainloop()