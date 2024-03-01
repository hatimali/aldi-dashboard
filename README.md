# Aldi Süd Assignment by Hatim

Welcome to the ALDI Store Dashboard! This dashboard aims to help the imaginary grocery store chain detect sales, profit and customer demographics by providing insights into their data. The data used for this dashboard can be found in the "Sample - Superstore.xlsx" file.

## Features

- [Home]: This feature give you a overview of the data with sales analytics, profit analytics and customer demographics
- [Table]: This features display the table data with dropdown filters, date filters and you can dynamically add data to your dashboard with some validation.
- [Graph]: The graph page displays the 2 plots.
- 1.   On the left side of the page, we have a fitting timeline graph for the following properties: Days to Ship, Discount, Profit, Profit Ratio, Quantity, Returns, Sales
- 2.   On the right side of the page, we have a Bubble chart that include two-axis dropdowns containing the
following properties: Days to Ship, Discount, Profit, Profit Ratio, Quantity, Returns, Sales.
By selecting one dropdown, the option should be excluded in the other. Also we have a third dropdown that breaks down the bubble chart and contains the following properties: Segment, Ship Mode, Customer Name, Category, SubCategory, Product Name

## Installation

To run this application locally, follow these steps:

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # For Linux/macOS
    # or
    .\venv\Scripts\activate   # For Windows
    ```
4. Install dependencies using `pip install -r requirements.txt`.
5. Run the application with `python app.py`.
6. Access the dashboard by visiting `http://localhost:8050` in your web browser.
7. Explore the Home Page, Table Page, and Graph Page to gain insights into grocery store data and detect potential losses.


## Dependencies

- Python 3.x
- Dash

## Usage

- [Brief instructions on how to use the application].

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add some feature'`).
5. Push to the branch (`git push origin feature/your-feature-name`).
6. Create a new Pull Request.

