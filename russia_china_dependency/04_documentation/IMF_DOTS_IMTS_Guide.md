# IMF Direction of Trade Statistics (DOTS/IMTS) - Data Access Guide
## Russia-China Bilateral Trade Data (2000-2024)

---

## Important Update: DOTS → IMTS

**The Direction of Trade Statistics (DOTS) has been renamed to:**
**International Trade in Goods (by partner country) - IMTS**

- **New URL**: https://data.imf.org/en/datasets/IMF.STA:IMTS
- **Old URL** (redirects): https://data.imf.org/?sk=9d6028d4-f14a-464c-a2f2-59b2cd424b85
- **Effective Date**: The legacy IMF data portal was retired on November 5, 2025

---

## Dataset Overview

### What IMTS Contains:
- **Merchandise (goods) export and import statistics** disaggregated by trading partners
- **Bilateral trade data** between any two countries
- **World, regional, and country group aggregates**
- **Time coverage**: Historical data from 1950s to present (check portal for latest available year)
- **Frequency**: Monthly, quarterly, and annual data available

### Key Indicators:
1. **Exports from Country A to Country B** (FOB - Free on Board basis)
2. **Imports to Country A from Country B** (CIF - Cost, Insurance, Freight basis typically, or FOB)
3. Values typically in **US Dollars (millions)**

---

## How to Access the Data

### Method 1: Web Interface (Interactive Dashboard)

**Main Dataset Page**: https://data.imf.org/en/datasets/IMF.STA:IMTS

**Step-by-Step Process:**

1. **Navigate to the IMTS Dataset Page**
   - Go to: https://data.imf.org/Datasets/IMTS
   - Click the **"VIEW DATA"** button (top of page)

2. **Select Countries**
   - **Reporter Country**: Select "Russia" (the country whose trade you're measuring)
   - **Partner Country**: Select "China" (Russia's trading partner)
   - Note: You can reverse this to also get China's reported trade with Russia

3. **Select Indicators**
   - Look for dropdown or filter options for:
     - **Exports** (Russia to China)
     - **Imports** (Russia from China)
   - Indicators may be labeled as:
     - "Goods, Value of Exports, FOB, US Dollars"
     - "Goods, Value of Imports, CIF, US Dollars"

4. **Set Time Period**
   - **Frequency**: Select "Monthly" (M)
   - **Start Date**: January 2000 (2000-01 or 2000M01)
   - **End Date**: December 2024 (2024-12 or 2024M12)
   - Note: Check data availability - some months may not be reported yet for 2024

5. **Download Data**
   - Click the **"DOWNLOAD"** button (usually green)
   - Select format: **CSV**, Excel (.xlsx), or other formats
   - Options may include: .xlsx, .csv, .pdf, .pptx, .png

### Method 2: Interactive Dashboard

**Dashboard URL**: https://data.imf.org/en/Dashboards/IMTS%20Dashboard

The dashboard provides:
- **Pre-built tables and charts** of merchandise trade statistics
- **Visualization** of trade flows by country and partner
- **Export capabilities** for reports

**Process:**
1. Navigate to the dashboard
2. Select Russia as the reporting country
3. Filter for China as the partner country
4. Choose your time period (2000-2024)
5. Select monthly frequency
6. Export the visualization or underlying data

### Method 3: Predefined Tables

**Tables URL**: https://data.imf.org/en/Tables

Look for table: **"Exports and Imports by Area and Countries"**

**Process:**
1. Click on the relevant "...by Country" data table
2. Use the country drop-down menu to select Russia and China
3. Select your desired dates (2000-2024, monthly)
4. Use the green report button to export data in preferred format (.xlsx, .csv, .pdf, .pptx, or .png)

---

## Method 4: API Access (For Programmatic Retrieval)

**API Portal**: https://portal.api.imf.org/apis#tags=iData

**Available APIs:**
- SDMX 2.1 API
- SDMX 3.0 API

**Code Libraries/Integrations:**
- **Python**: IMF provides Python code examples
- **R**: IMF provides R code examples
- **Stata**: Integration available
- **MATLAB**: Integration available
- **Excel Add-in**: Direct Excel integration

**General API Structure** (SDMX format):
```
https://api.imf.org/data/[DatasetCode]/[Frequency].[Country].[Indicator].[Partner]
```

Example query structure for IMTS:
```
Dataset: IMF.STA:IMTS
Frequency: M (monthly), Q (quarterly), A (annual)
Country: RU (Russia), CN (China)
Indicators: TX (exports), TM (imports)
```

**Resources:**
- API Documentation: https://data.imf.org/en/Resource-Pages/IMF-API
- Python Guide: Check IMF knowledge base
- R Guide: Check IMF knowledge base
- For help: datahelp@imf.org

---

## Method 5: Excel Add-in

**Download Page**: https://data.imf.org/en/Resource-Pages/Download-Excel-Add-in

**Benefits:**
- Direct integration with Excel
- Query builder interface
- Automatic data refresh capabilities
- Easy filtering and selection of countries, indicators, and time periods

**Process:**
1. Download and install the IMF Excel Add-in
2. Open Excel and activate the IMF Data add-in
3. Use the query builder to:
   - Select IMTS dataset
   - Choose Russia as reporter, China as partner
   - Select export/import indicators
   - Set monthly frequency and 2000-2024 date range
4. Insert data directly into your spreadsheet
5. Data can be refreshed to get updates

---

## Data Structure for Russia-China Bilateral Trade

### Expected Data Columns (CSV/Excel format):

| Column | Description | Example |
|--------|-------------|---------|
| **Country** or **Reporter** | Reporting country | Russia |
| **Partner Country** | Trading partner | China |
| **Indicator** | Type of trade flow | Exports / Imports |
| **Frequency** | Data frequency | Monthly |
| **Time Period** | Date | 2000-01, 2000-02, ... 2024-12 |
| **Value** | Trade value in USD millions | 1234.56 |
| **Unit** | Unit of measurement | US Dollars, Millions |

### Key Variables to Extract:

**For Russia → China trade:**
1. **Russia's Exports to China** (monthly, 2000-2024)
2. **Russia's Imports from China** (monthly, 2000-2024)

**Note**: You may also want to extract:
3. **China's Exports to Russia** (for comparison/validation)
4. **China's Imports from Russia** (for comparison/validation)

> **Mirror Statistics Note**: Trade statistics from both sides (reporter and partner) may differ due to:
> - Different valuation methods (FOB vs CIF)
> - Time of recording
> - Classification differences
> - Re-exports and transshipments

---

## Important Data Considerations

### 1. **Monthly Data Availability**
- Monthly frequency is typically available for recent years
- Older historical data (1950s-1990s) may only be annual or quarterly
- For 2000-2024 period, monthly data should be well-covered
- **Latest data**: Check the portal for most recent months available (may lag by 1-3 months)

### 2. **Data Revisions**
- Trade statistics are often revised as more complete information becomes available
- Check the "Date last updated" on the dataset page

### 3. **Currency**
- All values are standardized in **US Dollars (millions)**
- Original reporting may be in local currency, then converted by IMF

### 4. **Valuation**
- **Exports**: Generally FOB (Free on Board) - excludes freight and insurance
- **Imports**: May be CIF (Cost, Insurance, Freight) or FOB depending on country reporting standards

### 5. **Seasonality**
- Monthly trade data often shows seasonal patterns
- Consider seasonal adjustment if analyzing trends

### 6. **Missing Data**
- Some months may have missing or incomplete data
- Check for data gaps, especially in earlier years (2000-2005)

---

## Data Quality and Validation

### Cross-Checking Your Data:

1. **Check Both Directions**:
   - Russia's reported exports to China vs. China's reported imports from Russia
   - Russia's reported imports from China vs. China's reported exports to Russia

2. **Validate Against Other Sources**:
   - UN Comtrade: https://comtradeplus.un.org/
   - National statistics: Rosstat (Russia), China Customs (China)
   - OECD Trade Statistics

3. **Check for Anomalies**:
   - Sudden unexplained spikes or drops
   - Long periods of missing data
   - Zero or negative values (investigate)

---

## Citation

When using IMTS/DOTS data, cite as:

**Format:**
> International Monetary Fund (IMF). [Year]. International Trade in Goods (by partner country) (IMTS) [Dataset]. IMF Data Portal. https://data.imf.org/en/datasets/IMF.STA:IMTS

**Example for your research:**
> International Monetary Fund (IMF). 2025. International Trade in Goods (by partner country) (IMTS) [Dataset]. IMF Data Portal. https://data.imf.org/en/datasets/IMF.STA:IMTS. Accessed February 13, 2026.

---

## Contact and Support

### Getting Help:
- **Email**: datahelp@imf.org or datasupport@imf.org
- **Knowledge Base**: https://datasupport.imf.org/knowledge
- **Help Portal**: Look for "Help" link on data.imf.org

### Common Issues to Report:
- Data access problems
- Missing data for specific country-partner pairs
- Questions about methodology
- Technical issues with downloads or API

---

## Summary: Quick Start Checklist

✅ **Step 1**: Go to https://data.imf.org/Datasets/IMTS

✅ **Step 2**: Click "VIEW DATA" button

✅ **Step 3**: Select filters:
   - Reporter: Russia
   - Partner: China
   - Indicators: Exports, Imports
   - Frequency: Monthly (M)
   - Period: 2000-01 to 2024-12

✅ **Step 4**: Click "DOWNLOAD" → Select CSV format

✅ **Step 5**: Repeat with China as reporter and Russia as partner (for validation)

✅ **Step 6**: Save data and verify:
   - Check for missing months
   - Validate values are in USD millions
   - Compare Russia's exports vs China's imports (should be similar but not identical)

---

## Additional Notes

### Alternative/Complementary Data Sources:

1. **UN Comtrade** (https://comtradeplus.un.org/)
   - More detailed product-level trade data
   - Uses HS (Harmonized System) classification
   - Also bilateral, monthly data available
   
2. **National Sources**:
   - **Russia**: Rosstat (Federal State Statistics Service)
   - **China**: General Administration of Customs

3. **OECD Statistics**: 
   - Monthly International Merchandise Trade
   - Similar to IMTS but OECD member focus

### For Detailed Product-Level Analysis:
If you need trade broken down by products (e.g., oil, gas, machinery):
- Use **UN Comtrade** with HS codes
- UN Comtrade provides product classifications at 2, 4, 6-digit HS levels

---

## Questions to Verify Before Starting:

Before downloading, confirm:

1. ✅ Do you need **total bilateral trade** (all products) or **specific products**?
   - Total → IMTS is perfect
   - Specific products → Consider UN Comtrade

2. ✅ Do you need data in **current prices** or **constant prices**?
   - IMTS provides current USD values
   - For constant prices, you'll need to deflate using price indices

3. ✅ Monthly is truly required, or would **quarterly/annual** suffice?
   - Monthly gives most detail but larger dataset
   - Consider your analysis needs

4. ✅ Do you need **mirror statistics** (both reporter and partner perspectives)?
   - Recommended for validation
   - Doubles your data collection effort

---

**Last Updated**: February 13, 2026
**Dataset Reviewed**: IMF IMTS (International Trade in Goods by partner country)
**URL**: https://data.imf.org/en/datasets/IMF.STA:IMTS
