import great_expectations as gx
from great_expectations.core.batch import BatchRequest

# Initialize the context
context = gx.get_context()

# List of tables for which you want to create expectation suites
tables = [
    "address", "countryregion", "creditcard", "customer", "date", "dim_address",
    "dim_credit_card", "dim_customer", "dim_date", "dim_order_status", "dim_product",
    "fct_sales", "obt_sales", "person", "product", "productcategory", "productsubcategory",
    "salesorderdetail", "salesorderheader", "salesorderheadersalesreason", "salesreason",
    "stateprovince", "store"
]

# Loop through each table and create an expectation suite
for table in tables:
    suite_name = f"{table}.basic"
    
    # Check if the suite already exists
    try:
        context.get_expectation_suite(suite_name)
        print(f"Expectation suite '{suite_name}' already exists. Skipping.")
        continue
    except gx.exceptions.DataContextError:
        pass

    # Create a new suite
    suite = context.add_expectation_suite(suite_name)
    
    # Define a batch request for the table
    batch_request = BatchRequest(
        datasource_name="my_postgres_db",
        data_connector_name="default_inferred_data_connector_name",
        data_asset_name=table
    )

    # Use validator to auto-generate the initial expectations
    validator = context.get_validator(batch_request=batch_request, expectation_suite_name=suite_name)
    
    # Adding a basic expectation to ensure data is present in the table
    validator.expect_table_row_count_to_be_between(min_value=1, max_value=None)
    
    # Save the expectation suite
    validator.save_expectation_suite()

    print(f"Created expectation suite '{suite_name}' for table '{table}'.")

print("All expectation suites created successfully.")
