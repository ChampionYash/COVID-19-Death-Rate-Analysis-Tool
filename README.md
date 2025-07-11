# COVID-19 Death Rate Analysis Tool

An interactive data analysis tool to explore COVID-19 death rates across countries. This project visualizes the relationship between testing quality and mortality rates using data from Worldometer (April-May 2020).

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-1.3+-green.svg)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.4+-red.svg)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-orange.svg)

## 📊 Overview

This tool analyzes how COVID-19 testing quality correlates with reported death rates across countries. The analysis reveals that countries with more comprehensive testing programs (>50 tests per positive case) show a more accurate picture of mortality rates, estimated at approximately 1.3%.

## ✨ Key Features

- **Interactive Data Exploration**: Filter by date, minimum case threshold, and testing quality
- **Multiple Visualization Types**: Histograms showing death rate distribution and scatter plots displaying the relationship between testing quality and mortality
- **Country Comparison**: Analyze how different countries performed in terms of testing and mortality rates
- **User-Friendly Interface**: GUI built with Tkinter offering multiple views and interactive elements
- **Statistical Analysis**: Estimates true COVID-19 death rate based on countries with reliable testing data

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Required packages: pandas, numpy, matplotlib, tkinter

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/ChampionYash/COVID-19-Death-Rate-Analysis-Tool.git
   cd COVID-19-Death-Rate-Analysis-Tool
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

Run the GUI application:
```bash
python simple_gui.py
```

Alternatively, you can use the Python script for analysis:
```bash
python covid_death_rate_analysis.py
```

Or explore the Jupyter notebook for step-by-step analysis:
```bash
jupyter notebook covid_death_rate_analysis.ipynb
```

## 📈 Analysis Highlights

The analysis shows:

1. A wide spread of COVID-19 death rates across countries, which shouldn't be expected if humans are affected similarly by the disease
2. After filtering out countries with fewer than 1,000 cases, the spread remains substantial
3. Countries with better testing tend to have more consistent and lower death rates
4. The most accurate estimate of the COVID-19 death rate comes from countries with good testing (>50 tests per positive case), which is approximately 1.3%

## 📁 Project Structure

- `covid_death_rate_analysis.py` - Python script for data analysis
- `covid_death_rate_analysis.ipynb` - Jupyter notebook with detailed analysis
- `simple_gui.py` - Tkinter-based graphical user interface
- `worldometer_snapshots_April18_to_May18.csv` - Dataset containing COVID-19 data
- `requirements.txt` - Required Python packages

## 🛠️ Technologies Used

- **Python**: Core programming language
- **Pandas**: Data manipulation and analysis
- **Matplotlib**: Data visualization
- **Tkinter**: GUI development
- **NumPy**: Numerical operations

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📊 Data Source

The analysis uses Worldometer COVID-19 data from April 18 to May 18, 2020, which is included in the project. 