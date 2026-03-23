# Airline Passengers Forecast API

This microservice exposes a forecasting model derived from the airline-passenger forecasting assignment. It accepts the previous 12 monthly passenger counts and returns a prediction for the next month.

## Endpoints

- `GET /` - basic service info
- `GET /health` - health check
- `POST /predict` - forecast next month

## Request format

```json
{
  "history": [360, 342, 406, 396, 420, 472, 548, 559, 463, 407, 362, 405]
}
```

## Response format

```json
{
  "input_window": [360, 342, 406, 396, 420, 472, 548, 559, 463, 407, 362, 405],
  "predicted_next_month": 420.16,
  "model_name": "Lag-12 linear regression forecaster",
  "units": "monthly passengers"
}
```

## Local run

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

Then open:
- `http://127.0.0.1:8000/docs`

## Local test

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"history":[360,342,406,396,420,472,548,559,463,407,362,405]}'
```

## Render deployment

1. Create a new GitHub repo and upload the contents of this folder.
2. In Render, choose **New + > Web Service**.
3. Connect the GitHub repo.
4. Render will detect `render.yaml`; approve the settings.
5. After deployment, copy the public URL.
6. Replace the placeholder URL in `service_summary.docx` or `service_summary.md`.

## Instructor invocation steps

1. Open the public URL followed by `/docs`.
2. Expand `POST /predict`.
3. Click **Try it out**.
4. Paste this JSON:

```json
{
  "history": [360, 342, 406, 396, 420, 472, 548, 559, 463, 407, 362, 405]
}
```

5. Click **Execute**.
6. A successful call returns a numeric forecast in `predicted_next_month`.
