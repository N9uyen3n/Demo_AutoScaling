@echo off
echo 🚀 Initializing Git Repository...
git init

echo.
echo 📜 Adding files...
git add .

echo.
echo 💾 Committing files...
git commit -m "Initial Release: Smart Autoscaling Demo with Hybrid Model & 3-Layer Defense"

echo.
echo 🔗 Linking to GitHub...
git remote add origin https://github.com/N9uyen3n/Demo_AutoScaling.git
git branch -M main

echo.
echo ☁️ Pushing to GitHub (Please enter credentials if prompted)...
git push -u origin main

echo.
echo ✅ Done! Access your repo at: https://github.com/N9uyen3n/Demo_AutoScaling
pause
