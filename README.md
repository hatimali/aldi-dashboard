# Aldi Süd Assignment by Hatim

Welcome to the ALDI Store Dashboard! This dashboard aims to help the imaginary grocery store chain detect sales, profit and customer demographics by providing insights into their data. The data used for this dashboard can be found in the "Sample - Superstore.xlsx" file.

## Features

- [Home]: This feature give you a overview of the data with sales analytics, profit analytics and customer demographics
- [Feature 2]: This features display the table data with dropdown filters, date filters and you can dynamically add data to your dashboard with some validation.
- [Feature 3]: The graph page displays the 2 plots.
- 1.   On the left side of the page, we have a fitting timeline graph for the following properties: Days to Ship, Discount, Profit, Profit Ratio, Quantity, Returns, Sales
- 2.   On the right side of the page, we have a Bubble chart that include two-axis dropdowns containing the
following properties: Days to Ship, Discount, Profit, Profit Ratio, Quantity, Returns, Sales.
By selecting one dropdown, the option should be excluded in the other. Also we have a third dropdown that breaks down the bubble chart and contains the following properties: Segment, Ship Mode, Customer Name, Category, SubCategory, Product Name

## Installation

To run this application locally, follow these steps:

1. Clone the repository to your local machine.
2. Navigate to the project data directory.
3. I have removed the data file from the data directory for privacy concerns so add 'Sample - EU Superstore.xls' file inside the data directory for the project to work. Make sure to use the same file name as mentioned.
4. Go back to the project main directoy where app.py file is located
5. Optional but Recommended: Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # For Linux/macOS
    # or
    .\venv\Scripts\activate   # For Windows
    ```
6. Install dependencies using `pip install -r requirements.txt`.
7. Run the application with `python app.py`.
8. Access the dashboard by visiting `http://localhost:8050` in your web browser.
9. Explore the Home Page, Table Page, and Graph Page to gain insights into grocery store data and detect potential losses.


## Dependencies
- Python 3.x

## Extendion

- Project can be extended by connecting to a SQL database like Postgres instead of excel data. Also make sure the data is normalized and well structured to avoid redeundany.
- Data should not be loaded on each page seperately. Infact if we have a database with different entities like Orders, Customers, Products, Order Details, Region. Then sql queries for fetching the required data would be optimal here.
- Project can have user interactions and customization where user can dynamicaly add or update the data or layout of the application.
- We can add LRU based cache mechanism to avoid redundant database hits.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add some feature'`).
5. Push to the branch (`git push origin feature/your-feature-name`).
6. Create a new Pull Request.

