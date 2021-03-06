#!/usr/bin/env sh

set -e

DEFAULT_MODULE_NAME=app.main
DEFAULT_VARIABLE_NAME=app

DEFAULT_LOG_LEVEL=info
DEFAULT_ACCESS_LOGFILE="-"
DEFAULT_ERROR_LOGFILE="-"

DEFAULT_HOST=0.0.0.0
DEFAULT_PORT=80

DEFAULT_KEEP_ALIVE=5
DEFAULT_TIMEOUT=120
DEFAULT_GRACEFUL_TIMEOUT=120

DEFAULT_WORKER_CLASS=uvicorn.workers.UvicornWorker
DEFAULT_WORKER_TMP_DIR=/dev/shm
DEFAULT_WORKERS_PER_CORE=1
DEFAULT_MAX_WORKERS=""
DEFAULT_WEB_CONCURRENCY=2


MODULE_NAME=${MODULE_NAME:-$DEFAULT_MODULE_NAME}
VARIABLE_NAME=${VARIABLE_NAME:-$DEFAULT_VARIABLE_NAME}
export APP_MODULE=${APP_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}

export LOG_LEVEL=${LOG_LEVEL:-$DEFAULT_LOG_LEVEL}
export ACCESS_LOGFILE=${ACCESS_LOGFILE:-$DEFAULT_ACCESS_LOGFILE}
export ERROR_LOGFILE=${ERROR_LOGFILE:-$DEFAULT_ERROR_LOGFILE}

export HOST=${HOST:-$DEFAULT_HOST}
export PORT=${PORT:-$DEFAULT_PORT}
export BIND_ADDRESS=${BIND_ADDRESS:-"$HOST:$PORT"}

export KEEP_ALIVE=${KEEP_ALIVE:-$DEFAULT_KEEP_ALIVE}
export TIMEOUT=${TIMEOUT:-$DEFAULT_TIMEOUT}
export GRACEFUL_TIMEOUT=${GRACEFUL_TIMEOUT:-$DEFAULT_GRACEFUL_TIMEOUT}

export WORKER_CLASS=${WORKER_CLASS:-$DEFAULT_WORKER_CLASS}
export WORKER_TMP_DIR=${WORKER_TMP_DIR:-$DEFAULT_WORKER_TMP_DIR}
export WORKERS_PER_CORE=${WORKERS_PER_CORE:-$DEFAULT_WORKERS_PER_CORE}
export MAX_WORKERS=${MAX_WORKERS:-$DEFAULT_MAX_WORKERS}

# If WEB_CONCURRENCY is not set, try to predict optimal settings for workers
# WORKERS_PER_CORE x NUMBER_OF_CPU_CORES
# conditions:
# - no less than DEFAULT_WEB_CONCURRENCY
# - no more than MAX_WORKERS (if set)
if [ -z "$WEB_CONCURRENCY" ]; then
  CORES=$(nproc)
  AUTOTUNE_WEB_CONCURRENCY=$(( CORES * WORKERS_PER_CORE ))

  # use max(AUTOTUNE, DEFAULT)
  WEB_CONCURRENCY=$(( AUTOTUNE_WEB_CONCURRENCY>DEFAULT_WEB_CONCURRENCY \
                      ? AUTOTUNE_WEB_CONCURRENCY \
                      : DEFAULT_WEB_CONCURRENCY ))

  if [ -n "$MAX_WORKERS" ]; then
    # use min(WEB_CONCURRENCY, MAX_WORKERS)
    WEB_CONCURRENCY=$(( WEB_CONCURRENCY<MAX_WORKERS \
                        ? WEB_CONCURRENCY \
                        : MAX_WORKERS ))
  fi
  export WEB_CONCURRENCY
fi

if [ -n "$DEVELOPMENT_VERSION" ]; then
  sleep 5
  echo "#### \$DEVELOPMENT_VERSION environment variable is active ####"
  echo "################ Running in DEVELOPMENT MODE ################"
  exec uvicorn --reload --host "$HOST" --port "$PORT" \
               --log-level "$LOG_LEVEL" "$APP_MODULE"
fi

exec gunicorn -b "$BIND_ADDRESS" \
              -t "$TIMEOUT" \
              --graceful-timeout "$GRACEFUL_TIMEOUT" \
              --keep-alive "$KEEP_ALIVE" \
              -w "$WEB_CONCURRENCY" \
              -k "$WORKER_CLASS" \
              --worker-tmp-dir "$WORKER_TMP_DIR" \
              --log-level "$LOG_LEVEL" \
              --access-logfile "$ACCESS_LOGFILE" \
              --error-logfile "$ERROR_LOGFILE" \
              "$APP_MODULE"
