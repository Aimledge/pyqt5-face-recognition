#!/usr/bin/env bash
script_dir=$(dirname $0)
ui_files=$(ls ${script_dir}/gui/*.ui)
for ui_file in ${ui_files[@]}
do
    out_file="${ui_file%.*}_ui.py"
    echo "Generating $out_file"
    pyuic5 -o $out_file -x $ui_file
done
