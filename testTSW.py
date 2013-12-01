#!/bin/bash
#./tvShowWatch.py --action init -c"test1.xml" --arg y,1,kavodboris,ecnerolf,front142.sdbx.co,50762,limonkavod,2jpGQ1iF19,6,y,download,y,smtp.gmail.com,587,y,y,brice.grichy@gmail.com,dlqapbsaushbtkwd,brice.grichy@gmail.com,,y,0
#./tvShowWatch.py -c"test1.xml" --action list
#./tvShowWatch.py -c"test1.xml" --action add --arg "x files,2,y,n,0"
#./tvShowWatch.py -c"test1.xml" --action add --arg "glee,1,y,y,0"
#./tvShowWatch.py -c"test1.xml" --action del --arg "2,0"
#./tvShowWatch.py -c"test1.xml" --action config --arg "2,kavodboris,0"
#./tvShowWatch.py -c"test1.xml" --action config --arg "4,vostfr1,vostfr,,0"
#./tvShowWatch.py -c"test1.xml" --action config --arg "4,vostfr,,0"
#./tvShowWatch.py -c"test1.xml" --action run

./TSW_api.py -c"test3.xml" -s"test4.xml" --admin --action init --arg "{\"conf\":{\"tracker\":{\"id\":\"t411\",\"user\":\"kavodboris\",\"password\":\"ecnerolf\"},\"transmission\":{\"server\":\"front142.sdbx.co\",\"port\":50762,\"user\":\"limonkavod\",\"password\":\"2jpGQ1iF19\",\"slotNumber\":6,\"folder\":\"download\"}}}"
./TSW_api.py -c"test3.xml" -s"test4.xml" --admin --action config --arg "{\"conf\":{\"smtp\":{\"server\":\"smtp.gmail.com\",\"port\":\"587\",\"user\":\"brice.grichy@gmail.com\",\"password\":\"dlqapbsaushbtkwd\",\"emailSender\":\"brice.grichy@gmail.com\",\"ssltls\":\"True\"}}}"
./TSW_api.py -c"test3.xml" -s"test4.xml" --action del --arg '{"id":"all"}'
./TSW_api.py -c"test3.xml" -s"test4.xml" --action add --arg '{"id":[153021,75760],"emails":"brice.Grichy@gmail.com"}'

