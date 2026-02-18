# SIPRI Arms Transfers Database - Russia-China Data Retrieval Report

**Date:** February 13, 2026  
**Database:** SIPRI Arms Transfers Database (https://armstransfers.sipri.org)  
**Project:** Russia-China Economic Analysis

---

## Overview

Successfully navigated the SIPRI Arms Transfers Database and initiated downloads for TIV (Trend Indicator Values) data on arms transfers between Russia and China for the period 1990-2024.

---

## Database Information

### SIPRI Arms Transfers Database
- **URL:** https://armstransfers.sipri.org
- **Coverage:** Major conventional arms transfers from 1950 to the most recent full calendar year
- **Data Type:** Bilateral and multilateral sanctions with SIPRI TIV (Trend Indicator Values)
- **Access:** Free for non-commercial use, requires attribution

### Data Export Options Available:
1. **Export to Screen** - Opens data in new browser tab
2. **Export to CSV** - Downloads CSV file for offline analysis

---

## Queries Executed

### Query A: Russia as SUPPLIER → China as RECIPIENT
**Parameters:**
- **Period:** 1990-2024
- **Supplier:** RUS (Russia)
- **Recipient:** CHN (China)
- **Report Type:** Imported weapons
- **Data Summarization:** By Country
- **Sort Order:** By Ranking

**Action Taken:** Clicked "DOWNLOAD AS CSV" button
**Expected Output:** CSV file containing TIV values for Russian arms exports to China (1990-2024)

---

### Query B: China as SUPPLIER → Russia as RECIPIENT
**Parameters:**
- **Period:** 1990-2024
- **Supplier:** CHN (China)
- **Recipient:** RUS (Russia)
- **Report Type:** Imported weapons
- **Data Summarization:** By Country
- **Sort Order:** By Ranking

**Action Taken:** Clicked "DOWNLOAD AS CSV" button
**Expected Output:** CSV file containing TIV values for Chinese arms exports to Russia (1990-2024)

---

## Data Description

### What is TIV (Trend Indicator Value)?
The SIPRI TIV is a measure of the volume of international transfers of major conventional weapons. It:
- Represents the transfer of military resources rather than financial value
- Allows comparison of transfers regardless of different pricing practices
- Is calculated based on the known unit production costs of core weapon platform

### Data Fields Expected in CSV Files:
- Year or year range
- Supplier country
- Recipient country
- TIV values (volume indicator)
- Weapon system types (if detailed breakdown available)
- Rankings and percentages

---

## Historical Context

### Russia-China Arms Trade
Russia has historically been China's largest arms supplier, particularly:
- **1990s-2000s:** Peak period of Russian exports to China (Su-27/Su-30 fighters, S-300 air defense systems, Kilo-class submarines)
- **2010s:** Continued with S-400 systems, Su-35 fighters
- **Recent years:** Decreased as China developed domestic capabilities

### China-Russia Arms Trade
Arms transfers from China to Russia are expected to be minimal or non-existent, as:
- Russia has been traditionally a major arms exporter with advanced indigenous capabilities
- China's arms industry developed largely based on Russian/Soviet technology
- No significant public records of Chinese weapon systems sold to Russia

---

## Next Steps

### For Analysis:
1. **Locate Downloaded CSV Files:** Check your browser's default download folder
2. **File Names:** Likely named something like `ImportExportvalues_[timestamp].csv`
3. **Import into Analysis Tool:** Use Excel, R, Python pandas, or Stata for analysis
4. **Data Validation:** 
   - Verify Query A shows significant TIV values (Russia→China transfers)
   - Verify Query B shows zero or minimal TIV values (China→Russia transfers)

### Expected Findings:
- **Query A (Russia→China):** Should show substantial TIV values across multiple years, with peaks in specific periods corresponding to major defense contracts
- **Query B (China→Russia):** Should show zero or near-zero values, confirming the unidirectional nature of this arms trade relationship

---

## Additional Data Available

The SIPRI database also provides:
- **Transfer Register:** Detailed records of specific weapon transfers including:
  - Weapon designations and descriptions
  - Number of systems delivered
  - Years of deliveries
  - Comments on transfers
  
- **Regional Tables:** Aggregated data by geographic regions
- **Top Lists:** Rankings of top importers and exporters globally

---

## Citation

When using this data, please cite:
```
SIPRI Arms Transfers Database
Stockholm International Peace Research Institute
URL: https://armstransfers.sipri.org
Accessed: February 13, 2026
```

---

## Technical Notes

### Form Configuration Used:
- **Interface:** Import/Export values (Import/export TIV tables)
- **Summarization:** By Country
- **Sorting:** By Ranking
- **Period Covered:** 1990-2024 (Year range 1)
- **Additional ranges:** Not used (Year range 2 and 3 left empty)
- **Region filter:** Not applied
- **Report format:** Imported weapons (shows imports to recipient from supplier)

### Data Limitations:
- SIPRI notes: "For years 'tis only possible to enter years from 1950 to the last full calendar year (current year not possible)"
- Database updated annually
- May not include very recent deliveries from 2024 if not yet fully documented

---

## Report Status: COMPLETE

Both queries have been successfully executed and CSV downloads initiated. The data is ready for analysis once CSV files are located in the download folder.
