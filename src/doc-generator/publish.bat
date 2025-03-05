@echo off
setlocal

rd .vitepress\dist /s/q > nul 2> nul
call npm run docs:build
rd ..\..\docs /s/q >nul 2> nul
md ..\..\docs
xcopy .vitepress\dist\* ..\..\docs /chrys

endlocal
