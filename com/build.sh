#!/bin/sh
pyinstaller -F perfmonitor.py
pyinstaller -F perfstat.py
pyinstaller -F perfcoremonitor.py
cp ./dist/* .
rm -rf build dist *.spec
