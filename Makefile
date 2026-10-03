repro:
	pytest -q tests
	python experiments/run_all.py
	PYTHONPATH=src python benchmarks/benchmark_suite.py

docker:
	docker compose up --build
