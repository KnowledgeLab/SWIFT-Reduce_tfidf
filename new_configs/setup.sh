#!/bin/bash

installdir=/tmp/python
sleeptime=20
install_lock=$install_dir/install.in_progress
install_done=$install_dir/install.done


load_install()
{
    echo "Path udpate"
}

do_install()
{
    echo "Installing..."
}


attempts=5
while [ $attempts -gt 0 ]
do


    # Check if install is done
    if [ -d $install_done ]; then
        #If install is done execute the path setup code
        load_install()
    else
        #if install is not done, try to get the install_lock
        if mkdir -p $install_lock 2>/dev/null; then
        # lock acquired for installion
            do_install()
            # create the install_done folder
            mkdir -p $install_done
            # unlock
            rm -rf $install_lock 2>/dev/null
        else
            # Could not acquire install lock. Spin lock on install_done
            attempts=$(($attempts - 1))
            sleep $sleeptime;
        done

fi


if [ ! -d $installdir$ ]; then
  if mkdir $dssattmp 2>/dev/null; then
    echo $$ copying
    savewd=$PWD
    cd $dssattmp

    mkdir -p refdata
    cp $refdata/* refdata/

    mkdir -p campaign
    cp $campaign/*.MZX campaign/

    mkdir -p binpath
    cp $binpath/*.EXE binpath/

    cd $savewd
    mv $dssattmp $installdir
  else
    while [ ! -d $installdir ]; do
     # echo $$ sleeping
      sleep 1;
    done
  fi
fi
