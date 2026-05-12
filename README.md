# Students Score Prediction

FastAPI inference API and Streamlit UI for predicting student math scores. Includes a training pipeline (ingestion → transformation → model selection/tuning) and Dockerized API/UI.

**Author:** kamran (kamranakmal6776@gmail.com)

## Project Structure
- API: [Backend/application.py](Backend/application.py)
- API schema: [Backend/schema/input_data.py](Backend/schema/input_data.py)
- Streamlit UI: [prediction_gui.py](prediction_gui.py)
- Training pipeline: [src/components/data_ingestion.py](src/components/data_ingestion.py), [src/components/data_transformation.py](src/components/data_transformation.py), [src/components/model_trainer.py](src/components/model_trainer.py)
- Utilities: [src/utils.py](src/utils.py)
- Docker: [Docker/Dockerfile](Docker/Dockerfile) (API), [Docker/Dockerfile.ui](Docker/Dockerfile.ui) (UI), [Docker/docker-compose.yml](Docker/docker-compose.yml)
- Notebooks: [notebook/EDA_Student_performance.ipynb](notebook/EDA_Student_performance.ipynb)
- Package metadata: [pyproject.toml](pyproject.toml)

## Prerequisites
- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- Docker and Docker Compose (for containerized run)

## Local Setup
1) **Install uv:** `curl -LsSf https://astral.sh/uv/install.sh | sh` (or see [uv docs](https://docs.astral.sh/uv/))
2) **Install dependencies:**
	- With uv: `uv pip install -e .` (installs from pyproject.toml)
	- Or: `uv pip install -r requirements.txt`
	- Fallback (pip): `pip install -r requirements.txt`
3) **Train pipeline** (produces artifacts/preprocessor.pkl and artifacts/model.pkl):
	- `uv run src/components/data_ingestion.py`
4) **Run API locally:**
	- `uvicorn Backend.application:app --host 0.0.0.0 --port 8000`
	- Open docs: http://127.0.0.1:8000/docs
5) **Run Streamlit locally** (uses API_URL env or defaults to localhost):
	- `API_URL=http://127.0.0.1:8000/predict streamlit run prediction_gui.py`

## Docker
Build from the repository root:
1) **Build API image:** `docker build -t 7903954268/mlproject-api:latest -f Docker/Dockerfile .`
2) **Build UI image:** `docker build -t 7903954268/mlproject-ui:latest -f Docker/Dockerfile.ui .`
3) **Run API:** `docker run --rm -p 8000:8000 7903954268/mlproject-api:latest`
4) **Run UI:** `docker run --rm -p 8501:8501 -e API_URL=http://host.docker.internal:8000/predict 7903954268/mlproject-ui:latest`
5) **Access:**
	- API: http://localhost:8000/docs
	- UI: http://localhost:8501

## Pushing images to Docker Hub
- Images are tagged as `7903954268/mlproject-api:latest` and `7903954268/mlproject-ui:latest`
- **Build and push:** `docker build -t 7903954268/mlproject-api:latest -f Docker/Dockerfile . && docker build -t 7903954268/mlproject-ui:latest -f Docker/Dockerfile.ui . && docker push 7903954268/mlproject-api:latest && docker push 7903954268/mlproject-ui:latest`

## Troubleshooting
- Ensure artifacts exist before starting API/UI (run training once).
- If port 8000 or 8501 is busy, change the host mapping in your `docker run` command or local server command.
- For uv issues, see [uv documentation](https://docs.astral.sh/uv/).
