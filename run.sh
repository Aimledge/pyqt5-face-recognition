#!/usr/bin/env bash
export LD_LIBRARY_PATH=/home/ghegde/Env/sandwich/lib/python3.5/site-packages/PyQt5/Qt/lib:$LD_LIBRARY_PATH
export QT_PLUGIN_PATH=/usr/lib/x86_64-linux-gnu/qt5/plugins/
python $(dirname $0)/main.py