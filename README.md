# Dashboard built with Python Dash

Welcome to the Sample EU SuperStore Dashboard! 

This Dash dashboard provides interactive visualizations and insights into the Sample SuperStore dataset. It allows users to explore sales data across different dimensions such as time, geography, product categories, customer segments and more.

## Features
- Home Page:
    The Home Page of the dashboard presents a strategic overview of the store's sales, profit and customer demographics data with an intuitive and informative interface. Intuitive charts allow for easy year-over-year sales trend analysis, profit analysis and demographic insights making data-driven decision-making both quick and effective.
- Table Page: 
    This page displays the table data with multiple hierarchal dropdown filters and date filters. This feature also gives you the flexibility to dynamically add data to your dashboard with some validation and verification.
- Graph Page:
    The graph page displays 2 plots side by side. We have date range and granularity filters at the top of the page which act as a parent filters to the data displayed on this page.
    1. On the left side we have a fitting timeline graph with dynamic metric selection.
    2. On the right side we have a Bubble chart that include two-axis dynamic dropdowns. By selecting a metric at any axis will result in automatically remove that metic from the other axis. Also we have a third dropdown that breaks down the bubble chart with color segmentation.

## Data Source
Where can I find Superstore Sales? 
- On a Tableau Quest - Confluence (atlassian.net) from Steven Martins
https://datawonders.atlassian.net/wiki/spaces/TABLEAU/blog/2022/10/26/1953431553/Where+Can+I+Find+Superstore+Sales#Workbooks-and-Data-Sources

- Download the data given as 'Sample - EU Superstore.xls'.
## Installation

To run this application locally, follow these steps:

1. Clone the repository to your local machine.
2. Navigate to the project data directory.
3. I have removed the data file from the data directory for privacy concerns so add 'Sample - EU Superstore.xls' file which you downloaded earlier inside the data directory for the project to work. Make sure to use the same file name as mentioned as project uses this file name.
4. Go back to the project root level where app.py file is located
5. Optional but Recommended: Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # For Linux/macOS
    # or
    .venv\Scripts\activate   # For Windows
    ```
6. Install dependencies using `pip install -r requirements.txt`.
7. Run the application with `python app.py`.
8. Access the dashboard by visiting `http://localhost:8050` in your web browser.
9. Explore the Home Page, Table Page, and Graph Page to gain insights into grocery store data and detect potential sales, profit and customer insights.


## Dependencies
- Python 3.x

## Extendion

- Project can be extended by connecting to a SQL database like Postgres instead of excel data. Also make sure the data is normalized and well structured to avoid redeundany.
- Data should not be loaded on each page seperately. Infact if we have a database with different entities like Orders, Customers, Products, Order Details, Region. Then sql queries for fetching the required data would be optimal here.
- Project can have user interactions and customization where user can dynamicaly add or update the data or layout of the application.
- We can add LRU based cache mechanism to avoid redundant database hits.
