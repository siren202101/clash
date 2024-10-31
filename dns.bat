@echo off
chcp 65001

:: 执行dns.py脚本
python dns.py

:: 询问是否查看并删除refresh_log.txt
echo 查看 DNS正确统计记录 吗？(Y/N)
set /p choice=
if /i "%choice%"=="Y" (
    type refresh_log.txt
    echo 请按任意键继续... & pause
    echo 删除 DNS正确统计记录 吗？(Y/N)
    set /p choice=
    if /i "%choice%"=="Y" (
        del refresh_log.txt
        echo 文件已删除！
    )
)

:: 询问是否查看并删除no_keyword_pages_log.txt
echo 查看 DNS错误记录 吗？(Y/N)
set /p choice=
if /i "%choice%"=="Y" (
    type no_keyword_pages_log.txt
    echo 请按任意键继续... & pause
    echo 删除 DNS错误记录 吗？(Y/N)
    set /p choice=
    if /i "%choice%"=="Y" (
        del no_keyword_pages_log.txt
        echo 文件已删除！
    )
)