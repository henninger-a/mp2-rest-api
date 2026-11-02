def test_upload_csv(client, sample_csv_bytes):
    response = client.post("/upload", files={"file": ("sample.csv", sample_csv_bytes, "text/csv")})
    print(response)
    assert response.status_code == 200
    assert response.json()['rows'] == 6
    assert response.json()['columns'] == 2
    assert response.json()['id'] > 0
    assert isinstance(response.json()['id'], int)


def test_process_and_retrieve(
    client, uploaded_dataset_id, processing_body
):
    response = client.post(f'/datasets/{uploaded_dataset_id}/process', json=processing_body)
    assert response.status_code == 200
    assert response.json()['validation_rows_removed'] == 1
    assert response.json()['cleaning_report']['rows_before'] == 5
    assert response.json()['cleaning_report']['rows_after'] == 3

    response2 = client.get(f'/datasets/{uploaded_dataset_id}')
    assert response2.status_code == 200
    assert set([1, 2, 5]).issubset(item['student_id'] for item in response2.json()['Data'])
    assert set([80, 90, 85]).issubset(item['score'] for item in response2.json()['Data'])


def test_retrieve_missing_dataset(client):
    response = client.get("/datasets/15")
    assert response.status_code == 404
