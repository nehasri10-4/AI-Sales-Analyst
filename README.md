# AI Sales Analyst 📊

An interactive sales analytics dashboard that combines data analysis, business insights, and a locally running AI assistant to help users understand e-commerce sales data.

## 🚀 Features

- **Interactive Sales Dashboard** — View sales KPIs, charts, and sales performance.
- **Data Filtering** — Explore sales by category, region, and order status.
- **Automatic Business Insights** — Identify the top-performing category, region, and sales month.
- **AI Sales Analyst** — Ask questions about sales data and receive analysis results with business explanations.
- **Local AI Integration** — Uses Ollama with the `llama3.2:1b` model to interpret questions and generate explanations.
- **Power BI Integration** — Open the Power BI report for interactive charts, filters, and slicers.
- **Data Exploration** — Preview the dataset and download data where supported.

## 🛠️ Technologies Used

- Python
- Pandas
- Streamlit
- Ollama
- Llama 3.2 (1B)
- Power BI
- Excel

## 📂 Project Structure

```text
AI-Sales-Analyst/
├── app.py
├── ai_engine.py
├── analysis.py
├── app_backup.py
├── requirements.txt
├── data/
│   └── Ecommerce_Sales_Raw_Dataset - Copy.xlsx
└── pages/
    ├── AI_Analysis.py
    └── Power_BI.py
```

## ⚙️ Requirements

- Python installed on your computer
- Ollama installed and running
- The `llama3.2:1b` model downloaded
- Power BI Desktop for opening the local Power BI report

## ▶️ How to Run

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd AI-Sales-Analyst
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Python dependencies

```powershell
pip install -r requirements.txt
```

### 4. Set up Ollama

Make sure Ollama is running and download the model:

```powershell
ollama pull llama3.2:1b
```

### 5. Start the dashboard

```powershell
py -m streamlit run app.py
```

Open the local URL shown in the terminal.

## 📈 Dataset

The project uses an e-commerce sales Excel dataset containing order information, dates, customers, regions, product categories, quantities, prices, discounts, payment modes, order statuses, and sales amounts.

## 🎯 Project Objective

The objective is to make sales data easier to explore and interpret by combining interactive visualizations, business insights, and natural-language questions.

## 👩‍💻 Author

**Neha Sri**

Developed as a data analytics and AI project to explore the integration of Python-based analytics, interactive dashboards, and local language-model capabilities.
