# 🛠️ Data Engineering Coding Challenge

This repository contains the proof-of-concept (PoC) solution for a data engineering challenge focused on **big data migration** and **RESTful data services**. 

## 📌 Requirements

### Challenge 1 – Data Migration & REST API

1. **Migrate historical CSV data to SQL database**
   - Source: Comma-separated `.csv` files
   - Tables: `hired_employees.csv`, `departments.csv`, `jobs.csv`

2. **Build a REST API service for new data ingestion**
   - Must validate against a data dictionary
   - Support batch insertions (1–1000 rows)
   - Accept data for multiple tables in a single service
   - Enforce all data rules (all fields required, no invalid rows inserted)

3. **Backup feature**
   - Export table data in AVRO format to the file system

4. **Restore feature**
   - Restore a table from its AVRO backup

### Challenge 2 – Data Exploration API

Develop endpoints to return:

- ✅ **Quarterly hires per job and department for 2021**, ordered alphabetically  
  **Example output**:

  | department   | job       | Q1 | Q2 | Q3 | Q4 |
  |--------------|-----------|----|----|----|----|
  | Staff        | Recruiter | 3  | 0  | 7  | 11 |
  | Staff        | Manager   | 2  | 1  | 0  | 2  |

- ✅ **Departments that hired more than the mean number of employees in 2021**, ordered by number of hires (descending)  
  **Example output**:

  | id | department   | hired |
  |----|--------------|-------|
  | 7  | Staff        | 45    |
  | 9  | Supply Chain | 12    |



## 📦 Tech Stack & Notes

- ✅ Language: **Python**
- ✅ Destination DB: Any **SQL-compliant database**
- ✅ Data format: `.csv` for import, `.avro` for backup

---