# Notion Dynamic API

## Description
The Notion Dynamic API project is a FastAPI-based application that interacts with the Notion API to manage customer data stored in Notion databases. This project provides a set of RESTful endpoints to create, read, update, and delete customer data, leveraging the powerful capabilities of Notion as a backend database.

## Features
- **Create Customer**: Create a new customer database in Notion and add initial data.
- **Read Customers**: Retrieve a list of all customers or specific customer data.
- **Update Customer**: Rename a customer database or update specific data within a customer database.
- **Delete Customer**: Archive a customer database or delete specific data within a customer database.

## Endpoints

### Read
- `GET /customers`: Retrieve a list of all customers.
- `GET /customers/{customer_id}`: Retrieve data for a specific customer.

### Create
- `POST /customers/{customer_id}`: Create a new customer database with initial data.
- `POST /customers/{customer_id}/data`: Add data to an existing customer database.

### Update
- `PUT /customers/{customer_id}`: Rename an existing customer database.
- `PUT /customers/{customer_id}/data`: Update specific data within a customer database.

### Delete
- `DELETE /customers/{customer_id}`: Archive a customer database.
- `DELETE /customers/{customer_id}/data`: Delete specific data within a customer database.

## Setup

1. **Clone the repository**:
    ```bash
    git clone <repository-url>
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the FastAPI application**:
    ```bash
    uvicorn main:app --reload
    ```

5. **Access the API documentation**: Open your browser and navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to view the interactive API documentation provided by Swagger UI.

## Configuration
- **Notion API Key**: Ensure you have a valid Notion API key and update the `NOTION_API_KEY` variable in `notion.py`.
- **Page ID**: Update the `PAGE_ID` variable in `notion.py` with the ID of the Notion page where customer databases will be created.

## Dependencies
- FastAPI
- Requests
- Pandas
- Notion-client
- Uvicorn

Refer to `requirements.txt` for the complete list of dependencies.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgements
- FastAPI
- Notion API
- Uvicorn

This project provides a seamless way to manage customer data using Notion as a backend database, offering a flexible and dynamic approach to data management.
