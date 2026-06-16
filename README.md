# ⚡ UPI Merchant Category Pulse Dashboard

> **Live Demo:** [Deploy on Streamlit Cloud](https://streamlit.io/cloud) *(Insert your deployed Streamlit App URL here)*

An end-to-end P2M (Person-to-Merchant) transaction analytics dashboard that surfaces micro-consumer spending trends in India's payment ecosystem. It identifies which retail spending categories are outgrowing the overall UPI network.

---

## 1. The Business Problem

UPI crossed **228 billion transactions in 2025**, but aggregate numbers hide the real consumer story. Aggregate figures don't tell fintech product managers or risk teams which sectors are capturing the wallet share shift, which categories are premiumizing, and which are commoditizing with lower average ticket sizes. 

This dashboard addresses that visibility gap. By analyzing monthly category-level P2M transactions, it extracts actionable insights into consumer momentum, helping strategy teams allocate marketing capital, optimize checkout funnels, and adjust credit risk profiles.

---

## 2. Data Sources & Engineering Challenges

### Data Sources
*   **NPCI UPI Product Statistics:** Monthly MCC-category-wise transaction volume and value. [NPCI Product Statistics Portal](https://www.npci.org.in/what-we-do/upi/product-statistics)
*   **NPCI Archives:** Historical Excel files going back 3 years. [NPCI Archives](https://www.npci.org.in/what-we-do/upi/upi-ecosystem-statistics/archives)
*   **RBI DBIE Portal:** Baseline data for overall payment system indicators. [RBI DBIE Portal](https://dbie.rbi.org.in)

### Engineering Challenges
*   **Category Label Drift:** NPCI changes category labels across monthly releases (e.g., "Food & Beverages" becomes "F&B" or "Food Delivery" depending on the month). The ingestion pipeline maps these variations using a robust category mapping dictionary.
*   **Excel Layout Shifts:** Starting row indexes and headers shift between releases (starting on row 3 in some sheets, row 5 in others). The ingestion script solves this by dynamically scanning each spreadsheet to locate the header boundary before reading the data.

---

## 3. Methodology: The Momentum Score

To separate broad macro growth from category-specific momentum, we engineered the **Momentum Score**:

$$\text{Momentum Score} = \frac{\text{Category 3-Month Volume CAGR}}{\text{Overall UPI P2M 3-Month Volume CAGR}}$$

*   **Score > 1.0:** The category is growing faster than the overall UPI merchant network.
*   **Score = 1.0:** The category is growing at the exact speed of the network.
*   **Score < 1.0:** The category is lagging the network's growth rate.

### Worked Example:
If the overall UPI P2M volume grows by **5.0%** over a 3-month period, but the *Travel* category grows by **12.0%** over the same period:

$$\text{Momentum Score (Travel)} = \frac{12.0\%}{5.0\%} = 2.40$$

This indicates that Travel is outpacing the broader payments network by **2.4x**.

---

## 4. Key Analytical Insights

1.  **Travel & Hospitality Outpacing the Network:** Travel represents the highest momentum category post-2023, growing **2.4x faster** than the overall P2M network. It also commands the highest average ticket size at **₹3,200**.
2.  **Grocery Commoditization:** Grocery represents the volume engine of UPI but average ticket sizes dropped **27%** (from ₹800 to ₹580) over 36 months, proving that UPI is penetrating micro-payment scales (kirana stores).
3.  **Insurance Early Adoption:** Insurance and financial services are growing rapidly off a small base (Momentum Score > 1.8) but volume share remains under **5.0%**, indicating a significant headroom for growth.
4.  **Education Admissions Seasonality:** Education payments exhibit intense seasonality, spiking by **45%+** in May-July during admission periods (Seasonality Index > 1.45).
5.  **Utilities Near Saturation:** Bill payments maintain a stable volume share (~8.5%) but have a lagging Momentum Score of **0.85**, indicating it is a mature, fully penetrated category.

---

## 5. Business Recommendations

1.  **For Travel-Adjacent Fintechs:** Prioritize checkout page optimization and UPI Lite integrations in Q4. Since Q4 combines festive travel with high average ticket sizes, any checkout friction leads to significant revenue leakage.
2.  **For Kirana-focused Payment Processors:** Pivot monetization strategies from volume fees to value-added SaaS services (merchant lending, inventory dashboards). Average ticket sizes in groceries are shrinking, meaning transaction margins are compressable.
3.  **For Insurance Providers:** Focus on offering micro-premiums (e.g. sachet-size insurances) on checkout screens. The high financial services momentum proves consumer trust is shifting, but transaction ticket sizes are dropping, requiring smaller financial products.

---

## 6. How to Run Locally

Get the application running on your local machine in three steps:

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Process Raw Data
Place your manually downloaded NPCI Excel files in `data/raw/` and execute the notebooks or run the python pipeline:
```bash
jupyter nbconvert --to notebook --execute --inplace notebooks/01_cleaning.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/03_momentum_score.ipynb
```

### 3. Launch Streamlit
```bash
streamlit run app/dashboard.py
```
