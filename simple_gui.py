import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np
from datetime import datetime

class CovidAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("COVID-19 Death Rate Analysis")
        self.root.geometry("1200x800")
        
        # Load data
        self.load_data()
        
        # Create UI
        self.create_ui()
        
        # Initialize with default values
        self.update_analysis()
    
    def load_data(self):
        # Load the dataset
        self.worldometer_df = pd.read_csv('worldometer_snapshots_April18_to_May18.csv')
        self.available_dates = sorted(self.worldometer_df['Date'].unique().tolist())
        
    def create_ui(self):
        # Create control panel frame
        control_frame = ttk.LabelFrame(self.root, text="Controls")
        control_frame.pack(fill="x", padx=10, pady=10)
        
        # Date selection
        ttk.Label(control_frame, text="Select Date:").grid(row=0, column=0, padx=5, pady=5)
        self.date_var = tk.StringVar()
        self.date_combo = ttk.Combobox(control_frame, textvariable=self.date_var, values=self.available_dates)
        self.date_combo.grid(row=0, column=1, padx=5, pady=5)
        self.date_combo.current(len(self.available_dates)-1)  # Default to last date
        self.date_combo.bind("<<ComboboxSelected>>", lambda e: self.update_analysis())
        
        # Minimum cases threshold
        ttk.Label(control_frame, text="Minimum Cases:").grid(row=0, column=2, padx=5, pady=5)
        self.min_cases_var = tk.IntVar(value=1000)
        min_cases_scale = ttk.Scale(control_frame, from_=100, to=10000, variable=self.min_cases_var, 
                               orient="horizontal", length=200, command=lambda e: self.update_scale_label())
        min_cases_scale.grid(row=0, column=3, padx=5, pady=5)
        self.min_cases_label = ttk.Label(control_frame, text="1000")
        self.min_cases_label.grid(row=0, column=4, padx=5, pady=5)
        min_cases_scale.bind("<ButtonRelease-1>", lambda e: self.update_analysis())
        
        # Testing quality threshold
        ttk.Label(control_frame, text="Testing Quality Threshold:").grid(row=1, column=2, padx=5, pady=5)
        self.testing_quality_var = tk.IntVar(value=50)
        testing_quality_scale = ttk.Scale(control_frame, from_=5, to=100, variable=self.testing_quality_var, 
                                     orient="horizontal", length=200, command=lambda e: self.update_scale_label())
        testing_quality_scale.grid(row=1, column=3, padx=5, pady=5)
        self.testing_quality_label = ttk.Label(control_frame, text="50")
        self.testing_quality_label.grid(row=1, column=4, padx=5, pady=5)
        testing_quality_scale.bind("<ButtonRelease-1>", lambda e: self.update_analysis())
        
        # Update button
        update_button = ttk.Button(control_frame, text="Update Analysis", command=self.update_analysis)
        update_button.grid(row=1, column=1, padx=5, pady=5)
        
        # Create tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tab 1: Histogram
        self.histogram_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.histogram_frame, text="Death Rate Histogram")
        
        # Tab 2: Scatter Plot
        self.scatter_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.scatter_frame, text="Testing vs Death Rate")
        
        # Tab 3: Good Testing Countries
        self.good_testing_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.good_testing_frame, text="Good Testing Countries")
        
        # Tab 4: Results
        self.results_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.results_frame, text="Results")
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief="sunken", anchor="w")
        self.status_bar.pack(fill="x", side="bottom", padx=10, pady=5)
        
    def update_scale_label(self):
        self.min_cases_label.config(text=str(self.min_cases_var.get()))
        self.testing_quality_label.config(text=str(self.testing_quality_var.get()))
        
    def update_analysis(self):
        self.status_var.set("Analyzing data...")
        self.root.update_idletasks()
        
        # Get selected values
        selected_date = self.date_var.get()
        min_cases = self.min_cases_var.get()
        testing_quality = self.testing_quality_var.get()
        
        # Filter data based on selected date
        date_df = self.worldometer_df.loc[self.worldometer_df['Date'] == selected_date, :].reset_index(drop=True)
        
        # Calculate death rate
        date_df['Case Fatality Ratio'] = date_df['Total Deaths'] / date_df['Total Cases']
        date_df['Num Tests per Positive Case'] = date_df['Total Tests'] / date_df['Total Cases']
        
        # Filter countries by case threshold
        filtered_df = date_df.loc[date_df['Total Cases'] > min_cases, :].copy()
        
        # Update Histogram Tab
        for widget in self.histogram_frame.winfo_children():
            widget.destroy()
            
        if not filtered_df.empty:
            # Create histogram
            fig1, ax1 = plt.subplots(figsize=(10, 6))
            ax1.hist(100 * np.array(filtered_df['Case Fatality Ratio']), bins=np.arange(35))
            ax1.set_xlabel('Death Rate (%)', fontsize=14)
            ax1.set_ylabel('Number of Countries', fontsize=14)
            ax1.set_title(f'Histogram of Death Rates (Countries with >{min_cases} cases)', fontsize=16)
            
            canvas1 = FigureCanvasTkAgg(fig1, self.histogram_frame)
            canvas1.draw()
            canvas1.get_tk_widget().pack(fill="both", expand=True)
        else:
            ttk.Label(self.histogram_frame, text="No data available for the selected criteria").pack(padx=20, pady=20)
        
        # Update Scatter Plot Tab
        for widget in self.scatter_frame.winfo_children():
            widget.destroy()
            
        if not filtered_df.empty:
            # Calculate parameters for scatter plot
            x_axis_limit = 80
            
            # Prepare data
            death_rate_percent = 100 * np.array(filtered_df['Case Fatality Ratio'])
            num_test_per_positive = np.array(filtered_df['Num Tests per Positive Case'])
            num_test_per_positive[num_test_per_positive > x_axis_limit] = x_axis_limit
            total_num_deaths = np.array(filtered_df['Total Deaths'])
            population = np.array(filtered_df['Population'])
            
            # Create scatter plot
            fig2, ax2 = plt.subplots(figsize=(10, 6))
            scatter = ax2.scatter(x=num_test_per_positive, y=death_rate_percent, 
                              s=0.5*np.power(np.log(1+population),2), 
                              c=np.log10(1+total_num_deaths), cmap='viridis')
            
            plt.colorbar(scatter, ax=ax2)
            ax2.set_ylabel('Death Rate (%)', fontsize=14)
            ax2.set_xlabel('Number of Tests per Positive Case', fontsize=14)
            ax2.set_title('Death Rate as function of Testing Quality', fontsize=16)
            ax2.set_xlim(-1, x_axis_limit + 12)
            ax2.set_ylim(-0.2,17)
            
            # Add country labels for selected countries
            countries_to_display = ['USA', 'Russia', 'Spain', 'Brazil', 'UK', 'Italy', 'France', 
                                'Germany', 'India', 'Canada', 'Belgium', 'Mexico', 'Netherlands']
            
            for country_name in countries_to_display:
                country_indices = filtered_df.index[filtered_df['Country'] == country_name].tolist()
                if country_indices:  # Check if the country exists in the dataframe
                    country_index = country_indices[0]
                    ax2.annotate(country_name, 
                             xy=(num_test_per_positive[country_index], death_rate_percent[country_index]),
                             xytext=(5, 0), textcoords='offset points', fontsize=10)
            
            canvas2 = FigureCanvasTkAgg(fig2, self.scatter_frame)
            canvas2.draw()
            canvas2.get_tk_widget().pack(fill="both", expand=True)
        else:
            ttk.Label(self.scatter_frame, text="No data available for the selected criteria").pack(padx=20, pady=20)
        
        # Update Good Testing Countries Tab
        for widget in self.good_testing_frame.winfo_children():
            widget.destroy()
            
        # Filter for good testing countries
        good_testing_df = filtered_df.loc[filtered_df['Num Tests per Positive Case'] > testing_quality, :].copy()
        
        if not good_testing_df.empty:
            # Create table with good testing countries
            columns = ('Country', 'Total Cases', 'Total Deaths', 'Total Tests', 'Tests/Case', 'Death Rate (%)')
            tree = ttk.Treeview(self.good_testing_frame, columns=columns, show='headings')
            
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=100)
            
            for i, row in good_testing_df.iterrows():
                tree.insert('', 'end', values=(
                    row['Country'],
                    int(row['Total Cases']),
                    int(row['Total Deaths']),
                    int(row['Total Tests']),
                    round(row['Num Tests per Positive Case'], 2),
                    round(100 * row['Case Fatality Ratio'], 2)
                ))
            
            tree.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Calculate the estimated death rate for good testing countries
            if good_testing_df['Total Cases'].sum() > 0:  # Avoid division by zero
                estimated_death_rate = 100 * good_testing_df['Total Deaths'].sum() / good_testing_df['Total Cases'].sum()
                ttk.Label(self.good_testing_frame, 
                      text=f"Estimated COVID-19 Death Rate (countries with good testing): {estimated_death_rate:.2f}%",
                      font=('Arial', 12, 'bold')).pack(padx=20, pady=20)
        else:
            ttk.Label(self.good_testing_frame, text="No countries meet the selected testing quality threshold. Try adjusting the filters.").pack(padx=20, pady=20)
        
        # Update Results Tab
        for widget in self.results_frame.winfo_children():
            widget.destroy()
            
        result_text = f"""
        Analysis Results:
        
        Date: {selected_date}
        Countries with more than {min_cases} cases: {len(filtered_df)}
        Countries with testing quality > {testing_quality}: {len(good_testing_df)}
        
        Conclusions:
        
        1. There's a wide spread of COVID-19 death rates across countries
        2. After filtering out countries with fewer than {min_cases} cases, the spread is still substantial
        3. When looking at testing quality (tests per positive case), we see a clear pattern: 
           countries with better testing tend to have more consistent and lower death rates
        """
        
        if not good_testing_df.empty and good_testing_df['Total Cases'].sum() > 0:
            estimated_death_rate = 100 * good_testing_df['Total Deaths'].sum() / good_testing_df['Total Cases'].sum()
            result_text += f"\n4. The most accurate estimate of the COVID-19 death rate comes from countries with good testing (>{testing_quality} tests per positive case), which is approximately {estimated_death_rate:.2f}%"
        
        results_label = ttk.Label(self.results_frame, text=result_text, justify='left', font=('Arial', 12))
        results_label.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.status_var.set(f"Analysis completed for {selected_date} | Min Cases: {min_cases} | Testing Quality: {testing_quality}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CovidAnalysisApp(root)
    root.mainloop() 