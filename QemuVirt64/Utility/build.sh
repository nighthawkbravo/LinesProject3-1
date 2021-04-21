#!/bin/bash
PRJ_ROOT=$PWD
BR_NAME=buildroot-2021.02
BR_FILE=${BR_NAME}.tar.bz2
BR_DL=../${BR_FILE}
set -e
if [ ! -f ${BR_DL} ] || ! ( bzip2 -q -t ${BR_DL}); then
  (  
     cd ..
     rm -f ${BR_FILE}
     wget https://buildroot.org/downloads/${BR_FILE}
  )
fi
tar -xjf ${BR_DL}
cp BR_config ${BR_NAME}/.config
cd buildroot-2021.02
for i in ../patches/* ; do
   patch -p1 < $i
done

cd ..
# copy 
mkdir -p $BR_NAME/system/skeleton/etc/init.d
cp $PRJ_ROOT/lucas/utility-menuconfig.txt $BR_NAME/.config
cp $PRJ_ROOT/lucas/flask-file-server.tar.gz $BR_NAME/system/skeleton/root
cp $PRJ_ROOT/lucas/S60fileserver $BR_NAME/system/skeleton/etc/init.d/
cd buildroot-2021.02

make -j$(nproc)


