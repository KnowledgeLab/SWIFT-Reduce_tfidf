#!/bin/bash

#################CONFIGS###########################
# The config style to use
# Other configs let you connect to Beagle,midway,OpenScienceGrid,
# Cloud services etc.
# TODO : Add configs to a catalog
#TRUNK="/home/ybabuji/swift-trunk/cog/modules/swift/dist/swift-svn/bin"
#STABLE="/home/ybabuji/swift-0.94/cog/modules/swift/dist/swift-svn/bin"
CONFIG="hadoop"
STABLE="/home/$USER/swift-0.94.1/bin"
# Default input directory
#DIR="-data=./100_monthly_abstracts-abridged"
TRUNK="/home/ybabuji/swift-trunk/cog/modules/swift/dist/swift-svn/bin"
#STABLE="/home/ybabuji/swift-0.94.1/bin"
STABLE="/home/ybabuji/swift-0.94/cog/modules/swift/dist/swift-svn/bin"
#####################################################

TOPN=$1
MINF=$2
DIR=$3

if [ $CONFIG == "old" ]
then
    swift -tc.file old_configs/tc.data \
          -config  old_configs/cf \
          -sites.file old_configs/beagle.xml \
          tfidf.swift

elif [ $CONFIG == "hadoop" ]
then
    PATH=$STABLE:$PATH
    swift -tc.file hadoop_coasters/apps \
          -config  hadoop_coasters/swift.properties \
          -sites.file hadoop_coasters/sites.xml \
          tfidf.swift -data=./$DIR -topn=$TOPN -minf=$MINF

elif [ $CONFIG == "new" ]
then
    echo "New config [ Must load Swift manually ]"
    #export PATH=/scratch/midway/yadunand/swift-0.95/cog/modules/swift/dist/swift-svn/bin:$PATH
    export PATH=$TRUNK:$PATH
    swift -properties new_configs/swift.properties.midway.local tfidf.swift $DIR
fi
