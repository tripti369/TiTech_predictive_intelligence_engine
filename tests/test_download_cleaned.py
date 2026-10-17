import io
import json
import sys
from pathlib import Path

# Add backend directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_upload_and_download_cleaned():
    """Verify that uploading a noisy dataset cleans it and allows downloading cleaned data in CSV and JSON formats."""
    csv_sample = (
        "Customer ID ,Age,Gender ,Tenure (Months),Monthly_Charges ($),Total Spend,Support Calls,Payment Delay ,Subscription Plan ,Contract_Length,Churn Status\n"
        "101,29,Female ,14,$ 65.50,$ 917.00,2,0,Basic ,Monthly,0\n"
        "102,42,Male,36,$ 89.99,$ 3,239.64,5,3,Premium ,Annual,0\n"
        "103,,Female ,8,$ 45.00,$ 360.00,?,14,Basic,Monthly,1\n"
        "104,35,Male ,24,$ 75.20,$ 1,804.80,1,0,Standard ,Quarterly,0\n"
        "101,29,Female ,14,$ 65.50,$ 917.00,2,0,Basic ,Monthly,0\n"
        "105,58,Female,?,$ 110.00,null,8,7,Premium,Monthly,1\n"
    )

    # 1. Upload noisy dataset
    response = client.post(
        "/api/upload",
        files={"file": ("noisy_churn_test.csv", io.BytesIO(csv_sample.encode("utf-8")), "text/csv")},
    )
    assert response.status_code == 200, f"Upload failed: {response.text}"
    data = response.json()
    assert data["status"] == "success"
    assert "cleaned_filename" in data
    assert data["cleaned_filename"].startswith("cleaned_")
    assert "cleaning_summary" in data
    summary = data["cleaning_summary"]

    # Duplicates should be removed (1 duplicate of row 101)
    assert summary["duplicates_removed"] >= 1
    # Nulls / ? / missing values should have been imputed
    assert summary["nulls_imputed"] >= 1
    # Clean quality score should be high
    assert summary["clean_quality_score"] > summary["raw_quality_score"]

    clean_filename = data["cleaned_filename"]

    # 2. Download cleaned CSV via /api/download-cleaned
    res_csv = client.get(f"/api/download-cleaned?filename={clean_filename}")
    assert res_csv.status_code == 200, f"Download CSV failed: {res_csv.text}"
    assert "text/csv" in res_csv.headers.get("content-type", "")
    assert "attachment" in res_csv.headers.get("content-disposition", "")
    assert clean_filename in res_csv.headers.get("content-disposition", "")

    csv_text = res_csv.text
    # Verify cleaned column names exist in header
    header_line = csv_text.splitlines()[0]
    assert "customer_id" in header_line
    assert "monthly_charges" in header_line
    assert "subscription_plan" in header_line
    # Verify no raw duplicate row 101
    lines_with_101 = [l for l in csv_text.splitlines() if l.startswith("101,") or ",101," in l]
    assert len(lines_with_101) == 1, "Duplicate row 101 was not removed"

    # 3. Download cleaned CSV by original filename
    res_orig = client.get("/api/download-cleaned?filename=noisy_churn_test.csv")
    assert res_orig.status_code == 200
    assert "text/csv" in res_orig.headers.get("content-type", "")

    # 4. Download cleaned JSON format
    res_json = client.get(f"/api/download-cleaned?filename={clean_filename}&format=json")
    assert res_json.status_code == 200, f"Download JSON failed: {res_json.text}"
    records = res_json.json()
    assert isinstance(records, list)
    assert len(records) > 0
    assert "customer_id" in records[0]

    # 5. Check datasets inventory endpoint
    res_datasets = client.get("/api/datasets")
    assert res_datasets.status_code == 200
    datasets = res_datasets.json().get("datasets", [])
    found = [d for d in datasets if clean_filename in d.get("filename", "")]
    assert len(found) > 0
    assert "download_url" in found[0]
    assert "is_cleaned" in found[0]

    print("\n[SUCCESS] ALL CLEANED DATA DOWNLOAD TESTS PASSED!")


if __name__ == "__main__":
    test_upload_and_download_cleaned()
