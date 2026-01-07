Batch Importer App(ETL)
A high-performance Data Importer built with **Streamlit**, **Pandas**, and **PostgreSQL**. This application automates the process of extracting data from Excel, cleaning and validating it, and loading it into a database using efficient batch processing.

🌟 Key Features
* **Intelligent Column Matching:** Automatically handles inconsistent Excel headers (strips spaces and converts to lowercase).
* **Data Validation & Cleaning:** * Standardizes names to Title Case.
    * Cleans mobile numbers by removing non-digits and ensuring a 10-digit format.
    * Splits email strings into user and domain components.
* **Batch Insert Performance:** Uses `psycopg2.extras.execute_values` to insert data in chunks (up to 2000 rows at once), significantly reducing migration time compared to row-by-row insertion.
* **Live Error Reporting:** Captures row-specific validation errors without stopping the entire migration process.

🛠️ Technical Stack
* **Frontend:** Streamlit
* **Data Processing:** Pandas (Python)
* **Database:** PostgreSQL
* **Security:** Dotenv (Environment variable management)

⚙️ Setup & Installation

1. Clone the repository:
   git clone [https://github.com/tandukarmalisha/streamlit-app.git](https://github.com/tandukarmalisha/streamlit-app.git)
   cd streamlit-app
   
3. Set up Virtual Environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install Dependencies:
pip install streamlit pandas psycopg2-binary python-dotenv openpyxl

4. Configure Database: Create a .env file in the root directory based on your database credentials:
DB_HOST=localhost
DB_NAME=your_db_name
DB_USER=your_user
DB_PASS=your_password
DB_PORT=5432

5. Run the App:
streamlit run app.py

📂 Project Structure
app.py: Main Streamlit interface and database connection logic.

logic.py: Pure Python functions for data cleaning and validation.

.env: Secret credentials (ignored by git).

.gitignore: Prevents sensitive files from being tracked.
