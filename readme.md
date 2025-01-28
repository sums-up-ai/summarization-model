conda create -n local-server python=3.9

conda env export > environment.yml
conda env create -f environment.yml

uvicorn main:app --reload --host 127.0.0.1 --port 8000
