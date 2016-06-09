#!/bin/bash

find . -name "*.pyc" -delete
mkdir -p bin
rm -r build/*
rm -r pip/*
tools/download-pip-modules.sh
cwd=$(pwd)

function genbin {
  cd "$cwd"
  bin=$1
  dst=build/$bin
  mkdir -p $dst
  cp -rp lib $dst/
  cp -rp classes $dst/
  cp -rp pip $dst/
  cp $bin.py $dst/__main__.py
  cd $dst
  zip -r ../$bin.zip .
  cd "$cwd"
  cat <(echo '#!/usr/bin/env python') build/$bin.zip > bin/$bin
  chmod a+x bin/$bin
}

genbin upd89-daemon
genbin upd89-websrv
mv bin/upd89-websrv bin/upd89-websrv.py
