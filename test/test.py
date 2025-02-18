import os
from supabase import create_client, Client

# -------------------------------
# Configuration
# -------------------------------

# Set your Supabase URL and service role key as environment variables
SUPABASE_URL = 'https://fnnwucmrdeqwjqasppdf.supabase.co'  # Replace with your Supabase URL
SUPABASE_KEY= 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZubnd1Y21yZGVxd2pxYXNwcGRmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzk2MjA0MTAsImV4cCI6MjA1NTE5NjQxMH0.g4WORTsV6WQnVbk4KRqvurVIfde8mHNBFzY81NjnKZY'

def initialize_supabase_client() -> Client:
    """
    Initializes and returns a Supabase client.
    """
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("Supabase client initialized successfully.")
        return supabase
    except Exception as e:
        print(f"Error initializing Supabase client: {e}")
        raise

# -------------------------------
# Execute SQL Command
# -------------------------------

def execute_sql_command(supabase: Client, sql_command: str) -> bool:
    """
    Executes a SQL command using the Supabase client.
    """
    try:
        response = supabase.rpc('execute_sql', {'sql': sql_command}).execute()
        print(f"Response: {response}")
        if response.status_code == 200:
            print("SQL command executed successfully.")
            return True
        else:
            print(f"Error executing SQL command: {response.json()}")
            return False
    except Exception as e:
        print(f"Exception during SQL execution: {e}")
        return False
# -------------------------------
# Main Execution
# -------------------------------

def main():
    # Initialize Supabase client
    supabase = initialize_supabase_client()

    # Define SQL command to create the 'purchase' table
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS public.purchasenew1 (
        id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
        user_id UUID NOT NULL,
        product_id UUID NOT NULL,
        quantity INTEGER NOT NULL,
        purchase_date TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
    );
    """

    # Execute the SQL command to create the table
    if execute_sql_command(supabase, create_table_sql):
        print("Table 'purchase' created successfully.")
    else:
        print("Failed to create table 'purchase'.")

if __name__ == "__main__":
    main()


###in supabase sql editor nned do ###

# DROP FUNCTION IF EXISTS public.execute_sql(text);

# CREATE OR REPLACE FUNCTION public.execute_sql(sql text)
# RETURNS void AS $$
# BEGIN
#     EXECUTE sql;
# END;
# $$ LANGUAGE plpgsql SECURITY DEFINER;

# GRANT EXECUTE ON FUNCTION public.execute_sql(text) TO anon;