FROM python:3.12-slim
WORKDIR /work
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src
COPY experiments ./experiments
COPY benchmarks ./benchmarks
COPY data ./data
COPY tests ./tests
ENV PYTHONPATH=/work/src
CMD ["bash", "-lc", "pytest -q tests && python experiments/run_all.py && python benchmarks/benchmark_suite.py"]
