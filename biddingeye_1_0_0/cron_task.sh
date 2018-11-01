#!/bin/bash

#cron task log
date_info=`date`
echo "execut crontask on $date_info" >> /home/bee/BEE_PROJET/biddingeye_1_0_0/biddingeye_1_0_0/output/cron_task.log
source /home/bee/BEE_PROJET/bin/activate
export PYTHONPATH=/home/bee/BEE_PROJET/biddingeye_1_0_0

cd /home/bee/BEE_PROJET/biddingeye_1_0_0/biddingeye_1_0_0
#scrapy crawl BiddingEye -s CLOSESPIDER_PAGECOUNT=100
scrapy crawl BiddingEye > /dev/null  

cd /home/bee/BEE_PROJET/biddingeye_1_0_0/biddingeye_1_0_0/script
python ./postman.py


