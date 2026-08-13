from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
# ======================================
# PROJECT PATHS
# ======================================

BASE_DIR = Path(__file__).resolve().parent.parent

CLEAN_DATA = BASE_DIR / "02 Cleaned Data" / "HR Analytics_Cleaned.csv"

CHARTS_DIR = BASE_DIR / "04 Charts"

DASHBOARD_DIR = BASE_DIR / "05 Dashboard Data"

REPORT_FILE = DASHBOARD_DIR / "HR_Analytics_Report.xlsx"

# Create output folders if they don't exist

CHARTS_DIR.mkdir(exist_ok=True)

DASHBOARD_DIR.mkdir(exist_ok=True)
# ======================================
# LOAD DATA
# ======================================

df = pd.read_csv(CLEAN_DATA)

print("=" * 60)
print("HR ANALYTICS DATA LOADED")
print("=" * 60)

print(f"Rows    : {df.shape[0]:,}")
print(f"Columns : {df.shape[1]}")
# ======================================
# EXECUTIVE KPIs
# ======================================

kpis = pd.DataFrame({

    "KPI": [

        "Total Employees",
        "Active Employees",
        "Employees Left",
        "Attrition Rate %",
        "Average Monthly Income",
        "Overtime Rate %",
        "Average Job Satisfaction",
        "Average Work-Life Balance",
        "Average Years at Company"

    ],

    "Value": [

        len(df),

        (df["Attrition"] == "No").sum(),

        (df["Attrition"] == "Yes").sum(),

        round(df["Attrition_Num"].mean()*100,2),

        round(df["MonthlyIncome"].mean(),2),

        round((df["OverTime"]=="Yes").mean()*100,2),

        round(df["JobSatisfaction"].mean(),2),

        round(df["WorkLifeBalance"].mean(),2),

        round(df["YearsAtCompany"].mean(),2)

    ]

})

print()
print(kpis)
# ======================================
# DEPARTMENT ANALYSIS
# ======================================

department_analysis = (
    df.groupby("Department")
      .agg(
          Total_Employees=("EmployeeNumber", "count"),
          Employees_Left=("Attrition_Num", "sum"),
          Average_Income=("MonthlyIncome", "mean"),
          Average_Job_Satisfaction=("JobSatisfaction", "mean"),
          Average_WorkLifeBalance=("WorkLifeBalance", "mean")
      )
      .reset_index()
)

department_analysis["Attrition_Rate_%"] = (
    department_analysis["Employees_Left"] /
    department_analysis["Total_Employees"] * 100
).round(2)

department_analysis["Average_Income"] = (
    department_analysis["Average_Income"].round(2)
)

department_analysis["Average_Job_Satisfaction"] = (
    department_analysis["Average_Job_Satisfaction"].round(2)
)

department_analysis["Average_WorkLifeBalance"] = (
    department_analysis["Average_WorkLifeBalance"].round(2)
)

print("\n")
print("="*60)
print("DEPARTMENT ANALYSIS")
print("="*60)
print(department_analysis)
# ======================================
# JOB ROLE ANALYSIS
# ======================================

jobrole_analysis = (
    df.groupby("JobRole")
      .agg(
          Total_Employees=("EmployeeNumber", "count"),
          Employees_Left=("Attrition_Num", "sum"),
          Average_Income=("MonthlyIncome", "mean"),
          Average_Job_Satisfaction=("JobSatisfaction", "mean"),
          Average_WorkLifeBalance=("WorkLifeBalance", "mean")
      )
      .reset_index()
)

jobrole_analysis["Attrition_Rate_%"] = (
    jobrole_analysis["Employees_Left"] /
    jobrole_analysis["Total_Employees"] * 100
).round(2)

jobrole_analysis["Average_Income"] = (
    jobrole_analysis["Average_Income"].round(2)
)

jobrole_analysis["Average_Job_Satisfaction"] = (
    jobrole_analysis["Average_Job_Satisfaction"].round(2)
)

jobrole_analysis["Average_WorkLifeBalance"] = (
    jobrole_analysis["Average_WorkLifeBalance"].round(2)
)

# Highest attrition first

jobrole_analysis = jobrole_analysis.sort_values(
    by="Attrition_Rate_%",
    ascending=False
)

print("\n")
print("=" * 60)
print("JOB ROLE ANALYSIS")
print("=" * 60)
print(jobrole_analysis)
# ======================================
# OVERTIME ANALYSIS
# ======================================

overtime_analysis = (
    df.groupby("OverTime")
      .agg(
          Total_Employees=("EmployeeNumber", "count"),
          Employees_Left=("Attrition_Num", "sum"),
          Average_Income=("MonthlyIncome", "mean"),
          Average_Job_Satisfaction=("JobSatisfaction", "mean"),
          Average_WorkLifeBalance=("WorkLifeBalance", "mean")
      )
      .reset_index()
)

overtime_analysis["Attrition_Rate_%"] = (
    overtime_analysis["Employees_Left"] /
    overtime_analysis["Total_Employees"] * 100
).round(2)

overtime_analysis["Average_Income"] = (
    overtime_analysis["Average_Income"].round(2)
)

overtime_analysis["Average_Job_Satisfaction"] = (
    overtime_analysis["Average_Job_Satisfaction"].round(2)
)

overtime_analysis["Average_WorkLifeBalance"] = (
    overtime_analysis["Average_WorkLifeBalance"].round(2)
)

print("\n")
print("=" * 60)
print("OVERTIME ANALYSIS")
print("=" * 60)
print(overtime_analysis)
# ======================================
# INCOME ANALYSIS
# ======================================

income_analysis = (
    df.groupby("Attrition")
      .agg(
          Total_Employees=("EmployeeNumber", "count"),
          Average_Income=("MonthlyIncome", "mean"),
          Minimum_Income=("MonthlyIncome", "min"),
          Maximum_Income=("MonthlyIncome", "max"),
          Median_Income=("MonthlyIncome", "median")
      )
      .reset_index()
)

income_analysis["Average_Income"] = (
    income_analysis["Average_Income"].round(2)
)

income_analysis["Median_Income"] = (
    income_analysis["Median_Income"].round(2)
)

print("\n")
print("=" * 60)
print("INCOME ANALYSIS")
print("=" * 60)
print(income_analysis)
# ======================================
# AGE ANALYSIS
# ======================================

# Create Age Groups
df["Age_Group"] = pd.cut(
    df["Age"],
    bins=[17, 25, 35, 45, 55, 100],
    labels=["18-25", "26-35", "36-45", "46-55", "56+"]
)

age_analysis = (
    df.groupby("Age_Group")
    .agg(
        Total_Employees=("EmployeeNumber", "count"),
        Employees_Left=("Attrition_Num", "sum"),
        Average_Income=("MonthlyIncome", "mean"),
        Average_Job_Satisfaction=("JobSatisfaction", "mean"),
        Average_WorkLifeBalance=("WorkLifeBalance", "mean")
    )
    .reset_index()
)

age_analysis["Attrition_Rate_%"] = (
    age_analysis["Employees_Left"]
    / age_analysis["Total_Employees"]
    * 100
).round(2)

age_analysis["Average_Income"] = age_analysis["Average_Income"].round(2)
age_analysis["Average_Job_Satisfaction"] = age_analysis["Average_Job_Satisfaction"].round(2)
age_analysis["Average_WorkLifeBalance"] = age_analysis["Average_WorkLifeBalance"].round(2)

# Sort by age group (logical order)
age_analysis = age_analysis.sort_values("Age_Group")

print("\n")
print("=" * 60)
print("AGE ANALYSIS")
print("=" * 60)
print(age_analysis)
# ======================================
# RELATIONSHIP ANALYSIS - COMPLETE SUMMARY
# ======================================

print("\n")
print("=" * 60)
print("RELATIONSHIP ANALYSIS - COMPLETE SUMMARY")
print("=" * 60)

# 1. Overtime vs Attrition
print("\n📊 1. OVERTIME VS ATTRITION")
print("-" * 40)
overtime_summary = (
    df.groupby("OverTime")
    .agg(
        Total_Employees=("EmployeeNumber", "count"),
        Employees_Left=("Attrition_Num", "sum")
    )
    .reset_index()
)
overtime_summary["Attrition_Rate_%"] = (
    overtime_summary["Employees_Left"] / overtime_summary["Total_Employees"] * 100
).round(2)
print(overtime_summary.to_string(index=False))

# 2. Income vs Attrition
print("\n📊 2. INCOME VS ATTRITION")
print("-" * 40)
income_summary = (
    df.groupby("Attrition")
    .agg(
        Total_Employees=("EmployeeNumber", "count"),
        Average_Income=("MonthlyIncome", "mean"),
        Median_Income=("MonthlyIncome", "median"),
        Min_Income=("MonthlyIncome", "min"),
        Max_Income=("MonthlyIncome", "max")
    )
    .reset_index()
)
income_summary["Average_Income"] = income_summary["Average_Income"].round(2)
income_summary["Median_Income"] = income_summary["Median_Income"].round(2)
print(income_summary.to_string(index=False))

# 3. Job Satisfaction vs Attrition
print("\n📊 3. JOB SATISFACTION VS ATTRITION")
print("-" * 40)
satisfaction_summary = (
    df.groupby("Attrition")
    .agg(
        Total_Employees=("EmployeeNumber", "count"),
        Avg_Job_Satisfaction=("JobSatisfaction", "mean"),
        Avg_Environment_Satisfaction=("EnvironmentSatisfaction", "mean"),
        Avg_Relationship_Satisfaction=("RelationshipSatisfaction", "mean")
    )
    .reset_index()
)
satisfaction_summary["Avg_Job_Satisfaction"] = satisfaction_summary["Avg_Job_Satisfaction"].round(2)
satisfaction_summary["Avg_Environment_Satisfaction"] = satisfaction_summary["Avg_Environment_Satisfaction"].round(2)
satisfaction_summary["Avg_Relationship_Satisfaction"] = satisfaction_summary["Avg_Relationship_Satisfaction"].round(2)
print(satisfaction_summary.to_string(index=False))

# 4. Distance vs Attrition
print("\n📊 4. DISTANCE FROM HOME VS ATTRITION")
print("-" * 40)
distance_summary = (
    df.groupby("Attrition")
    .agg(
        Total_Employees=("EmployeeNumber", "count"),
        Avg_Distance=("DistanceFromHome", "mean"),
        Max_Distance=("DistanceFromHome", "max"),
        Min_Distance=("DistanceFromHome", "min")
    )
    .reset_index()
)
distance_summary["Avg_Distance"] = distance_summary["Avg_Distance"].round(2)
print(distance_summary.to_string(index=False))

# 5. Work-Life Balance vs Attrition
print("\n📊 5. WORK-LIFE BALANCE VS ATTRITION")
print("-" * 40)
wlb_summary = (
    df.groupby("Attrition")
    .agg(
        Total_Employees=("EmployeeNumber", "count"),
        Avg_WorkLifeBalance=("WorkLifeBalance", "mean")
    )
    .reset_index()
)
wlb_summary["Avg_WorkLifeBalance"] = wlb_summary["Avg_WorkLifeBalance"].round(2)
print(wlb_summary.to_string(index=False))

# 6. Years at Company vs Attrition
print("\n📊 6. YEARS AT COMPANY VS ATTRITION")
print("-" * 40)
tenure_summary = (
    df.groupby("Attrition")
    .agg(
        Total_Employees=("EmployeeNumber", "count"),
        Avg_YearsAtCompany=("YearsAtCompany", "mean"),
        Max_YearsAtCompany=("YearsAtCompany", "max")
    )
    .reset_index()
)
tenure_summary["Avg_YearsAtCompany"] = tenure_summary["Avg_YearsAtCompany"].round(2)
print(tenure_summary.to_string(index=False))

print("\n")
print("=" * 60)
print("✅ RELATIONSHIP ANALYSIS COMPLETE")
print("=" * 60)
# ======================================
# EXPORT TO EXCEL WORKBOOK
# ======================================

print("\n")
print("=" * 60)
print("EXPORTING TO EXCEL WORKBOOK")
print("=" * 60)

# Create output folder if it doesn't exist
DASHBOARD_DIR = BASE_DIR / "05 Dashboard Data"
DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)

EXPORT_PATH = DASHBOARD_DIR / "Dashboard_Data2.xlsx"

with pd.ExcelWriter(EXPORT_PATH, engine="openpyxl") as writer:

    # ======================================
    # EXECUTIVE KPIs
    # ======================================
    kpis.to_excel(
        writer,
        sheet_name="KPIs",
        index=False
    )

    # ======================================
    # DIMENSION ANALYSIS
    # ======================================
    department_analysis.to_excel(
        writer,
        sheet_name="Department",
        index=False
    )

    jobrole_analysis.to_excel(
        writer,
        sheet_name="JobRole",
        index=False
    )

    overtime_analysis.to_excel(
        writer,
        sheet_name="Overtime",
        index=False
    )

    income_analysis.to_excel(
        writer,
        sheet_name="Income",
        index=False
    )

    age_analysis.to_excel(
        writer,
        sheet_name="Age",
        index=False
    )

    # ======================================
    # RELATIONSHIP ANALYSIS
    # ======================================
    overtime_summary.to_excel(
        writer,
        sheet_name="Overtime_Summary",
        index=False
    )

    income_summary.to_excel(
        writer,
        sheet_name="Income_Summary",
        index=False
    )

    satisfaction_summary.to_excel(
        writer,
        sheet_name="Satisfaction_Summary",
        index=False
    )

    distance_summary.to_excel(
        writer,
        sheet_name="Distance_Summary",
        index=False
    )

    wlb_summary.to_excel(
        writer,
        sheet_name="WLB_Summary",
        index=False
    )

    tenure_summary.to_excel(
        writer,
        sheet_name="Tenure_Summary",
        index=False
    )

print("\n✅ Export Complete!")
print(f"📁 File saved to:\n{EXPORT_PATH}")

print("\n📊 12 Worksheets Exported Successfully")

print("\n📋 SHEETS INCLUDED")
print("-" * 35)
print("1. KPIs")
print("2. Department")
print("3. JobRole")
print("4. Overtime")
print("5. Income")
print("6. Age")
print("7. Overtime_Summary")
print("8. Income_Summary")
print("9. Satisfaction_Summary")
print("10. Distance_Summary")
print("11. WorkLifeBalance Summary")
print("12. Tenure Summary")