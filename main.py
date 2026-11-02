import io
import json
import logging
from pathlib import Path
import pandas as pd
from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from src import DatasetInfo, DatasetStorage, HealthResponse, setup_logging, ProcessConfig, ProcessingReport, log_requests
from data_pipeline import create_cleaning_report, process_data, validate_dataframe

setup_logging(verbose=True)
logger = logging.getLogger(__name__)

app = FastAPI(title="Data Processing API", version="1.0.0")
storage = DatasetStorage()
app.middleware("http")(log_requests)

@app.get("/health", response_model=HealthResponse)
def health_check():
    """Return the application status and version."""
    return {"status": "ok", "version": "1.0.0"}

@app.post("/upload", response_model=DatasetInfo)
async def upload_dataset(file: UploadFile = File(...)):
    """Read and store a CSV upload."""
    if Path(file.filename or '').suffix.lower() != '.csv':
        logger.warning(f"Unsupported file format: {Path(file.filename).suffix}")
        raise HTTPException( status_code=400, detail="Invalid file extension")
    contents = await file.read()
    try:
        df = pd.read_csv(io.BytesIO(contents))
    except (pd.errors.EmptyDataError,pd.errors.ParserError,UnicodeDecodeError) as error:
        logger.warning(f"Cannot read CSV: {error}")
        raise HTTPException(status_code=400, detail="Cannot read the uploaded CSV")
    data_id = storage.save(df, file.filename)
    logger.info(f'Dataset Id: {data_id}, Filename: {file.filename}, Rows: {len(df)}')
    return storage.get_metadata(data_id)

@app.get("/datasets/{dataset_id}")
def get_dataset(dataset_id: int, limit: int = Query(default=100, ge=1)):
    """Return up to limit rows from a stored dataset."""
    df = storage.get(dataset_id)
    if df is None:
        logger.warning(f"Dataset with id {dataset_id} not found")
        raise HTTPException( status_code=404, detail="Id not found")
    records = json.loads(df.head(limit).to_json(orient="records"))
    logger.info(f'Id: {dataset_id}, Rows Returned: {len(df.head(limit))}')
    return {'Id': dataset_id, 'Data': records, 'Total_rows': len(df)}

@app.post(
    "/datasets/{dataset_id}/process",
    response_model=ProcessingReport
)
def process_dataset(dataset_id: int, config: ProcessConfig):
    """Validate and process a stored dataset using MP1 functions."""
    # TODO: retrieve, validate, process, report, update, and return.
    result = storage.get(dataset_id)
    if result is None:
        raise HTTPException( status_code=404, detail="Id not found")
    config = config.model_dump()
    required_columns = config['validation']['required_columns']
    numeric_columns = config['validation']['numeric_columns']
    for col in numeric_columns:
        if col not in result.columns.to_list():
            raise HTTPException( status_code=400, detail="Column not found")
    try:
        df = validate_dataframe(result, required_columns, numeric_columns)
        rows_removed = len(result) - len(df)
        validated_df = df.copy()
        processed_df = process_data(validated_df, config)
    except ValueError:
        HTTPException(status_code=400, detail=str(ValueError))
    report = create_cleaning_report(validated_df, processed_df)
    storage.update(dataset_id, processed_df)
    logger.info(f'id: {dataset_id} validation row(s) removed: {rows_removed} processing row(s) removed {len(validated_df) - len(processed_df)}')
    return ProcessingReport(id = dataset_id, validation_rows_removed = rows_removed, cleaning_report = report)