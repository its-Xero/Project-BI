from extract import main as extract_from_sqlserver
from transform import main as transform_data
from load import main as load_to_sqlite

def run_pipeline():
    print("\n=== STEP 1 — EXTRACT ===")
    extract_from_sqlserver()

    print("\n=== STEP 2 — TRANSFORM ===")
    transform_data()

    print("\n=== STEP 3 — LOAD ===")
    load_to_sqlite()

    print("\n[✔] ETL Pipeline finished successfully!")

if __name__ == "__main__":
    run_pipeline()
