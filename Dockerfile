FROM python:3.12-alpine AS builder

RUN mkdir -p /project
WORKDIR /project
COPY . .

RUN apk add --no-cache gcc musl-dev postgresql-dev linux-headers python3-dev

RUN python -m pip install --no-cache-dir pdm
RUN pdm install --check --prod --no-editable

FROM python:3.12-alpine

WORKDIR /project
COPY --from=builder /project /project

ENV PATH="/project/.venv/bin:$PATH"

RUN chmod +x entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/project/entrypoint.sh"]

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
