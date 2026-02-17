@echo off
echo Running checks before push...

echo Checking migrations
python manage.py makemigrations --check

echo Running tests
python manage.py test

IF %ERRORLEVEL% NEQ 0 (
    echo Tests failed. Push aborted.
    exit /b 1
)

echo Checks passed. Pushing...
exit /b 0