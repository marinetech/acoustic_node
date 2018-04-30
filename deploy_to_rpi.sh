#!/bin/bash

src_dir="/home/ilan/projects/acoustic_node/rpi"
dply_dir="/home/ilan/projects/acoustic_node/rpi_dply"

if [ -d "$dply_dir" ]; then
  rm -rf $dply_dir
fi

cp -r $src_dir $dply_dir

rm -rf $dply_dir/lib/__pycache__
rm -rf $dply_dir/lib/detected_48
rm -rf $dply_dir/lib/*out*
rm -rf $dply_dir/lib/*bck
rm -rf $dply_dir/lib/*old.py
rm -rf $dply_dir/lib/stam*
rm -rf $dply_dir/lib/sdmsh
rm -rf $dply_dir/conf/__pycache__
rm -rf $dply_dir/logs/*
rm -rf $dply_dir/__pycache__
rm -rf $dply_dir/tasks/*

if [ -d "$dply_dir/bin/sdmsh.pi" ]; then
    cp -f $dply_dir/bin/sdmsh.pi $dply_dir/bin/sdmsh
fi


ssh rpi 'rm -rf ~/acoustic_node_prev && mv ~/acoustic_node ~/acoustic_node_prev'
scp -r $dply_dir rpi:~/acoustic_node