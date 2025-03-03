# S3-to-Redshift

![image](https://github.com/user-attachments/assets/2bad6449-4890-49f8-92d0-602eab6d54f9)

# Data Warehouse ETL Pipeline

## Project Overview

This project focuses on building an **ETL (Extract, Transform, Load)** pipeline that processes data from **AWS S3** into **AWS Redshift**. The data consists of **song** and **user activity logs** in JSON format, and the pipeline will transform and load it into **dimensional tables** for analytical purposes.

The pipeline is written in **Python** and uses **AWS Redshift** and **AWS S3** to store, process, and analyze the data. Below are the primary tasks the pipeline performs:

- **Extract** data from S3
- **Load** it into staging tables in Redshift
- **Transform** it into analytics-ready dimensional tables

---

## Key Technologies

- **AWS S3**: For storing raw data (song and user activity logs).
- **AWS Redshift**: Data warehouse where transformed data is stored and analyzed.
- **Python**: For managing the ETL pipeline logic.
- **SQL**: For interacting with Redshift and managing data transformation.

---

## Files in the Repository

### 1. `etl_pipeline.py`
   - The main Python script responsible for running the ETL process. It handles:
     - Connecting to Redshift
     - Dropping existing tables
     - Creating tables
     - Loading data into staging tables
     - Transforming and inserting data into final analytics tables

### 2. `sql_queries.py`
   - This file contains all SQL queries used in the ETL pipeline, including:
     - SQL for creating and dropping tables
     - Queries for inserting data into Redshift
     - Transformations to prepare the data for analytics

### 3. `dwh.cfg`
   - Configuration file that stores your AWS and Redshift connection credentials, including:
     - Redshift cluster endpoint
     - Database name
     - User credentials
     - AWS S3 bucket access credentials

### 4. `README.md`
   - Documentation providing an overview of the project, setup instructions, and how to run the ETL pipeline.
