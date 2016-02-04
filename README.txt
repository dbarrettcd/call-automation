################################################################################
#                            CALL AUTOMATION                                   #
################################################################################

Note: ALL commands should be run from the call-automation/ directory
      Only fs18 servers should be used

Installing SIPp
---------------
1. install libpcap-dev 

   sudo apt-get install -y libpcap-dev

2. Download SIPp 3.3.990

   wget -O sipp.tar.gz http://sourceforge.net/projects/sipp/files/sipp/3.4/sipp-3.3.990.tar.gz/download
   
2. Configure SIPp

   tar -xvzf sipp.tar.gz && cd sipp-3.3.990 && ./configure --with-pcap && make

Running Load Tests
------------------
1. increase the number of CPUs that the Feature Server VM has
  
   on the box, edit the Vagrantfile - /home/<user>/chef-repo/resources/vagrant/environment/Vagrantfile  
   under ### Feature server 1.8 ### 
   change v.customize [ "modifyvm", :id, "--name", COMPONENTS[:fs18], "--memory", 512 ] 
   to v.customize [ "modifyvm", :id, "--name", COMPONENTS[:fs18], "--memory", 512, "--cpus", 2 ]
   
   vagrant reload fs18

2. The expected success rate is 100% for all scenarios


Web Requirements To Run Entire Suite
------------------------------------

1. Set button 0 and button 5 of Auto Attendant - Main to route to Auto Attendant - Main
2. Set the DID to route to Auto Attendant - Main
3. ???
4. Profit
  
     
Inbound Auto Attendant
----------------------
Web requirements:
1. Set button 0 and button 5 of Auto Attendant - Main to route to Auto Attendant - Main
2. Set the DID to route to Auto Attendant - Main

Functional: 
sipp-3.3.990/sipp qa4-fs18.dev.coredial.com -sf inbound/auto_attendant/functional/inbound_auto_attendant_direct.xml -inf inbound/auto_attendant/functional/from_sipp_to_qa4-fs18_auto_attendant.csv -aa -i 172.16.128.89 -nostdin -m 1 

bin/assertsuccess.py inbound/auto_attendant/functional/inbound_auto_attendant_voicemail_new.txt inbound/auto_attendant/functional/assertions.csv inbound/auto_attendant/functional/negative_assertions.csv inbound/auto_attendant/functional/inbound_auto_attendant_voicemail_base.txt

Load: 
sipp-3.3.990/sipp qa4-fs18.dev.coredial.com -sf inbound/auto_attendant/load/inbound_auto_attendant_direct_long.xml -inf inbound/auto_attendant/load/from_sipp_to_qa4-fs18_auto_attendant.csv -aa -i 172.16.128.89 -nostdin -r 2 -m 1800

Load Statistics
Concurrent calls: 300
Each call duration: 2.5 minutes
Expected test time: 17.5 minutes


Inbound Holiday
---------------
Functional: 

sipp-3.3.990/sipp qa4-fs18.dev.coredial.com -sf inbound/holiday/functional/inbound_holiday_direct.xml -inf inbound/holiday/functional/from_sipp_to_qa4-fs18_holiday.csv -aa -i 172.16.128.89 -nostdin -m 1 

bin/assertsuccess.py inbound/holiday/functional/inbound_holiday_voicemail_new.txt inbound/holiday/functional/assertions.csv inbound/holiday/functional/negative_assertions.csv inbound/holiday/functional/inbound_holiday_voicemail_base.txt

Load: 

sipp-3.3.990/sipp qa4-fs18.dev.coredial.com -sf inbound/holiday/load/inbound_holiday_direct.xml -inf inbound/holiday/load/from_sipp_to_qa4-fs18_holiday.csv -aa -i 172.16.128.89 -nostdin -r 13 -m 11700


Inbound Time Frame
-------------------------

Functional:

sipp-3.3.990/sipp qa4-fs18.dev.coredial.com -sf inbound/time_frame/functional/inbound_time_frame_direct.xml -inf inbound/time_frame/functional/from_sipp_to_qa4-fs18_time_frame.csv -aa -i 172.16.128.89 -nostdin -r 1 -m 1 

Load:

sipp-3.3.990/sipp qa4-fs18.dev.coredial.com -sf inbound/time_frame/load/inbound_time_frame_direct.xml -inf inbound/time_frame/load/from_sipp_to_qa4-fs18_time_frame.csv -aa -i 172.16.128.89 -nostdin -r 5 -m 9000 



Outbound International
-------------------------

Functional:

sipp-3.3.990/sipp qa4-fs18.dev.coredial.com -sf outbound/international/functional/outbound_international.xml -inf outbound/international/functional/from_qa4-fs18_softphone_to_international.csv -aa -i 172.16.128.89 -nostdin -r 1 -m 1

bin/assertsuccess.py outbound/international/functional/outbound_international_new.txt outbound/international/functional/assertions.csv outbound/international/functional/negative_assertions.csv outbound/international/functional/outbound_international_base.txt 

Load:

sipp-3.3.990/sipp qa4-fs18.dev.coredial.com -sf outbound/international/load/outbound_international.xml -inf outbound/international/load/from_qa4-fs18_softphone_to_international.csv -aa -i 172.16.128.89 -nostdin -r 13 -m 11700

Load Statistics
Concurrent calls: 150
Each call duration: 10 seconds
Expected test time: 15 minutes
