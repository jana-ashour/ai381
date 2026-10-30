
# AI381 Lab 2 — Churn API


A churn prediction model (logistic regression) served with FastAPI, packaged in Docker,
and tested, scanned and published automatically by GitHub Actions.

## Run it (one command)

    docker compose up --build

Then open http://localhost:8000/docs

## Try it

    curl localhost:8000/health
    curl -X POST localhost:8000/predict -H "Content-Type: application/json" -d '{"tenure_months": 1, "monthly_charges": 110.0, "contract": "month-to-month", "internet_service": "fiber", "support_calls": 8}'

## How it works

- `src/train/train.py` trains the model from `data/churn_v1.csv`
- `src/app/main.py` is the API: `/health` and `/predict` (input checked by pydantic)
- `tests/` has 6 pytest tests
- `Dockerfile` is multi-stage, runs as a non-root user, uses a pinned base image, and has a HEALTHCHECK
- `.github/workflows/ci.yml`: lint and test on every pull request; on `main`, build the image, scan it with Trivy, and push it to GHCR tagged with the commit SHA
