@echo off
REM MediaCopyer 快速发布脚本 (Windows)

setlocal enabledelayedexpansion

REM 检查参数
if "%1"=="" goto :show_help
if "%1"=="help" goto :show_help
if "%1"=="--help" goto :show_help
if "%1"=="-h" goto :show_help

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python 未安装或不在 PATH 中
    exit /b 1
)

REM 检查make.py
if not exist "make.py" (
    echo ❌ 未找到 make.py 脚本
    exit /b 1
)

REM 执行命令
echo ℹ️  执行命令: python make.py %*
python make.py %*

if errorlevel 1 (
    echo ❌ 操作失败!
    exit /b 1
) else (
    echo ✅ 操作完成!
)

goto :eof

:show_help
echo MediaCopyer 快速发布脚本
echo ==========================
echo.
echo 用法:
echo   release.bat ^<命令^> [参数...]
echo.
echo 命令:
echo   build                    仅构建应用程序
echo   patch [changes...]       发布补丁版本 (x.y.Z)
echo   minor [changes...]       发布次版本 (x.Y.z)
echo   major [changes...]       发布主版本 (X.y.z)
echo   release ^<version^> [changes...]  发布指定版本
echo   version                  显示当前版本
echo   clean                    清理构建文件
echo.
echo 示例:
echo   release.bat build
echo   release.bat patch "修复重要bug"
echo   release.bat minor "添加新功能"
echo   release.bat release 1.2.0 "重大更新"

:eof