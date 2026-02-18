# IMF DOTS/IMTS Quick Access Summary
## Russia-China Bilateral Trade Data (Monthly, 2000-2024)

---

## ⚠️ Key Update

**DOTS (Direction of Trade Statistics)** has been **renamed to IMTS**  
**(International Trade in Goods by partner country)**

- Old portal retired: November 5, 2025
- New location: https://data.imf.org/

---

## 🚀 Quick Access Links

### Primary Access Point:
**Main Dataset Page**: https://data.imf.org/en/datasets/IMF.STA:IMTS

### Alternative Access:
- **Dashboard**: https://data.imf.org/en/Dashboards/IMTS%20Dashboard
- **Tables**: https://data.imf.org/en/Tables (Look for "Exports and Imports by Area and Countries")
- **API**: https://portal.api.imf.org/apis#tags=iData
- **Excel Add-in**: https://data.imf.org/en/Resource-Pages/Download-Excel-Add-in

---

## 📋 What You'll Find

### Data Available:
- ✅ **Bilateral exports** (Russia → China, China → Russia)
- ✅ **Bilateral imports** (Russia ← China, China ← Russia)
- ✅ **Monthly frequency** (2000-2024)
- ✅ **Values in USD millions**
- ✅ **CSV/Excel download** available

---

## 🔧 How to Extract Your Data

### Web Interface Method (Recommended for First-Time Users):

1. **Go to**: https://data.imf.org/Datasets/IMTS

2. **Click**: "VIEW DATA" button (blue/green button at top)

3. **Set Filters**:
   ```
   Reporter Country: Russia
   Partner Country: China
   Indicators: ☑ Exports  ☑ Imports
   Frequency: Monthly (M)
   Start Date: 2000-01
   End Date: 2024-12
   ```

4. **Download**: Click "DOWNLOAD" button → Select "CSV"

5. **Repeat** with:
   ```
   Reporter Country: China
   Partner Country: Russia
   ```
   (For cross-validation)

### Expected Data Structure:

| Reporter | Partner | Indicator | Period  | Value (USD mn) |
|----------|---------|-----------|---------|----------------|
| Russia   | China   | Exports   | 2000-01 | xxx.xx         |
| Russia   | China   | Exports   | 2000-02 | xxx.xx         |
| Russia   | China   | Imports   | 2000-01 | xxx.xx         |
| ...      | ...     | ...       | ...     | ...            |

---

## 📊 Dashboard Interface Features

When you click "VIEW DATA", you'll see:

### Selection Options:
- **Country/Area Selector**: Dropdown menu to select reporter country
- **Partner Country Selector**: Dropdown to select trading partner
- **Indicator Selector**: Checkboxes or dropdown for:
  - Goods, Value of Exports, FOB, US Dollars
  - Goods, Value of Imports, CIF/FOB, US Dollars
- **Frequency Selector**: Annual (A), Quarterly (Q), Monthly (M)
- **Date Range Selector**: Start/End date pickers or sliders

### Export/Download Options:
- 📥 **CSV** (recommended for analysis)
- 📊 **Excel** (.xlsx)
- 📄 **PDF** (for reports)
- 🖼️ **PowerPoint** (.pptx)
- 📷 **PNG** (charts/images)

---

## 🔍 Interface Elements to Look For

### Top Navigation Bar:
- **"VIEW DATA"** button → Opens the data query interface
- **"DOWNLOAD"** button → Direct bulk download option
- **"API"** link → For programmatic access
- **"Metadata"** link → Technical documentation

### Data Query Interface:
- **Left Panel**: Filters and selection options
  - Countries (Reporter)
  - Partner Countries
  - Indicators
  - Dates
  - Frequency
  
- **Main Panel**: Data preview/table
  - Shows selected data in tabular format
  - May include charts/visualizations
  
- **Right Panel** (may appear): Additional options
  - Layout options
  - Chart types
  - Table configuration

### Bottom/Footer Options:
- **Export/Download buttons**: Usually green or blue
- **Share**: Link sharing options
- **Chart/Table toggle**: Switch between views

---

## 💡 Pro Tips

### 1. **Check Data Coverage First**
- Not all months may have data
- Latest months (most recent 1-3 months) may not be published yet
- Check the "Last Updated" date on the dataset page

### 2. **Download Both Perspectives**
```
Set 1: Russia reports → exports to China, imports from China
Set 2: China reports → exports to Russia, imports from Russia
```
**Why?** 
- Russia's exports ≈ China's imports (should be similar but not identical)
- Differences due to FOB vs CIF valuation, timing, classification

### 3. **For Large Time Series**
- Monthly data from 2000-2024 = ~300 months × 2 indicators = 600 data points per direction
- Total dataset: ~1,200 rows (Russia perspective + China perspective)
- CSV format recommended for analysis in R, Python, or Excel

### 4. **Alternative: Use Excel Add-in**
- Install IMF Excel Add-in
- Query builder inside Excel
- Can refresh data automatically
- Easier for those comfortable with Excel

### 5. **If Web Interface is Confusing**
- Try the **Dashboard** first: https://data.imf.org/en/Dashboards/IMTS%20Dashboard
- Pre-configured visualizations may be easier to navigate
- Then export the underlying data

---

## 🌐 API Access (For Coders)

### Python Example Structure:
```python
import requests
import pandas as pd

# IMF SDMX API endpoint
base_url = "https://api.imf.org/data/IMTS"

# Query parameters
params = {
    "frequency": "M",  # Monthly
    "reporter": "RU",  # Russia
    "partner": "CN",   # China
    "indicator": "TX,TM",  # Exports, Imports
    "startPeriod": "2000-01",
    "endPeriod": "2024-12"
}

# Make request (actual syntax may vary - check IMF API docs)
response = requests.get(base_url, params=params)
data = response.json()

# Convert to pandas DataFrame
df = pd.DataFrame(data)
```

**Note**: Check official API documentation for exact syntax:
- https://portal.api.imf.org/apis
- Python guide: Available in IMF knowledge base

---

## 📧 Support & Help

### If You Get Stuck:
- **Email**: datahelp@imf.org
- **Knowledge Base**: https://datasupport.imf.org/knowledge
- **Help Button**: Available on data.imf.org pages

### Common Questions:
1. **"I can't find the download button"**
   → Look for green/blue button near top or bottom of data table
   → Try right-clicking on table → "Export" or "Download"

2. **"The data only shows annual, not monthly"**
   → Check the "Frequency" selector - make sure "Monthly" or "M" is selected
   → Some very old data (pre-2000) may only be annual

3. **"I get an error when downloading"**
   → Try reducing the date range (e.g., 2000-2010 first, then 2010-2024)
   → Try CSV instead of Excel format
   → Clear browser cache and try again

4. **"Values seem too high/low"**
   → Check units: Should be "US Dollars, Millions"
   → Verify you selected the right indicator (Exports vs Imports)
   → Compare with China's mirror statistics for validation

---

## 📚 Additional Resources

### Complementary Data Sources:
1. **UN Comtrade**: https://comtradeplus.un.org/
   - Product-level detail (HS codes)
   - Also has monthly bilateral trade
   
2. **National Statistics**:
   - Russia: Rosstat
   - China: General Administration of Customs

### For Product-Specific Trade:
- If you need breakdown by products (oil, gas, machinery, etc.)
- Use **UN Comtrade** with HS (Harmonized System) product codes

---

## ✅ Quick Checklist

Before you start:
- [ ] Confirmed you need **total merchandise trade** (not product-specific)
- [ ] Confirmed you need **monthly frequency** (not just annual)
- [ ] Have a clear plan for **data storage** (CSV format, ~1,200 rows)
- [ ] Decided whether to use **web interface**, **Excel add-in**, or **API**

After downloading:
- [ ] Verify data coverage: Check for missing months
- [ ] Verify units: USD millions
- [ ] Cross-check: Russia's exports ≈ China's imports
- [ ] Document: Save metadata (download date, data version)

---

## 🎯 Expected Workflow

**Total Time: 15-30 minutes (first time)**

```
Step 1: Navigate to IMTS page         [2 min]
Step 2: Set filters (Russia-China)    [3 min]
Step 3: Preview data table             [2 min]
Step 4: Download CSV                   [1 min]
Step 5: Repeat for China-Russia       [3 min]
Step 6: Verify and clean data         [10-15 min]
```

---

## 📞 Contact

For technical issues or questions about this guide:
- IMF Data Support: datahelp@imf.org
- IMF API Support: Check API portal documentation

---

**Guide Created**: February 13, 2026  
**IMF Portal Status**: Active (data.imf.org)  
**DOTS → IMTS Transition**: Completed November 2025
