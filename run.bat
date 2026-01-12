@echo off
set run=%1

:: Commands Mapping
if "%run%"=="-r"  set "cmd=python manage.py runserver"
if "%run%"=="-R"  set "cmd=python -m gunicorn --reload --log-level debug wooden.asgi:application -k uvicorn.workers.UvicornWorker"
if "%run%"=="-s"  set "cmd=python manage.py shell"
if "%run%"=="-d"  set "cmd=docker run --rm -p 6379:6379 redis:latest"
if "%run%"=="-mm" set "cmd=python manage.py makemigrations"
if "%run%"=="-m"  set "cmd=python manage.py migrate"
if "%run%"=="-a"  set "cmd=call env\Scripts\activate"
if "%run%"=="-c"  set "cmd=python manage.py check"
if "%run%"=="-cd" set "cmd=python manage.py check --deploy"
if "%run%"=="-st" set "cmd=python manage.py collectstatic --noinput"

:: Execution
if defined cmd (
    echo Executing: %cmd%
    %cmd%
) else (
    echo Invalid or missing flag.
)