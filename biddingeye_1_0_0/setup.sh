#!/bin/bash

#echo "0" > control/setup_idx_control.txt 
scrapy crawl BiddingEye > /dev/null  2>&1 &
