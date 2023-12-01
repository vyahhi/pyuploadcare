# Make sure that a specific variable has been set.
check-env-%:
	@ if [ "${${*}}" = "" ]; then \
		echo "Environment variable $* not set"; \
		exit 1; \
	fi

format:
	poetry run black .
	poetry run isort .

lint:
	poetry run black --check .
	poetry run isort --check .
	poetry run flake8 .
	poetry run mypy --namespace-packages --show-error-codes .

test:
	poetry run pytest -v tests/ --cov=pyuploadcare

test-functional:
	poetry run pytest tests/functional --cov=pyuploadcare

test-django:
	poetry run pytest tests/dj --cov=pyuploadcare

test-integration:
	poetry run pytest tests/integration --cov=pyuploadcare

docs_html:
	poetry run sh -c "cd docs && make html"

run_django:
	poetry run python tests/test_project/manage.py migrate
	DJANGO_SUPERUSER_PASSWORD=admin poetry run python tests/test_project/manage.py createsuperuser --no-input --username=admin --email=admin@example.com
	poetry run python tests/test_project/manage.py runserver

update_bundled_static:
	blocks_version=$$(DJANGO_SETTINGS_MODULE=tests.test_project.settings poetry run python -c "from pyuploadcare.dj.conf import DEFAULT_CONFIG; print(DEFAULT_CONFIG['widget']['version'])"); \
	curl "https://cdn.jsdelivr.net/npm/@uploadcare/blocks@$${blocks_version}/web/blocks.min.js" -o pyuploadcare/dj/static/uploadcare/blocks.min.js; \
	curl "https://cdn.jsdelivr.net/npm/@uploadcare/blocks@$${blocks_version}/web/lr-file-uploader-inline.min.css" -o pyuploadcare/dj/static/uploadcare/lr-file-uploader-inline.min.css; \
	curl "https://cdn.jsdelivr.net/npm/@uploadcare/blocks@$${blocks_version}/web/lr-file-uploader-minimal.min.css" -o pyuploadcare/dj/static/uploadcare/lr-file-uploader-minimal.min.css; \
	curl "https://cdn.jsdelivr.net/npm/@uploadcare/blocks@$${blocks_version}/web/lr-file-uploader-regular.min.css" -o pyuploadcare/dj/static/uploadcare/lr-file-uploader-regular.min.css

