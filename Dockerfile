FROM apache/airflow:2.10.2

# Install dbt-postgres and Great Expectations
RUN pip install dbt-core==1.8.2  \
	&& pip install dbt-postgres==1.8.2\
    && pip install great_expectations \
    && pip install apache-airflow-providers-postgres \
    && pip install psycopg2-binary \
	&& pip install apache-airflow-providers-odbc \
	&& pip install pyodbc\
	&& pip install dbt-airflow \
    && pip install airflow-provider-great-expectations 
    
USER root
RUN apt-get update && apt-get install -y git




# Switch back to airflow user
USER airflow
RUN airflow db migrate
