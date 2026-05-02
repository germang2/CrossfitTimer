#!/bin/bash

# Exit on error
set -e

echo "Building the Docker image..."
# This builds the image named pyinstaller-windows using the provided Dockerfile
docker build -t pyinstaller-windows -f Dockerfile.windows-build .

echo "Starting PyInstaller build..."
# NOTE: PyInstaller needs all your project's dependencies to be installed in the Windows environment.
# You can uncomment and modify this line in the Dockerfile to install them automatically:
# RUN wine "C:\Python38\python.exe" -m pip install PyQt5 alembic ...

# Run pyinstaller using Wine in Docker
# We mount the current directory ($PWD) to /app inside the container
docker run --rm -v "$PWD:/app" pyinstaller-windows \
    --onefile \
    --windowed \
    --icon=belicos-icon.ico \
    --paths=C:\\Python38\\Lib\\site-packages\\PyQt5\\Qt\\bin \
    CrossfitTimer.py

echo "Build completed! Check the 'dist' folder for your executable."
