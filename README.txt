################################################################################
#                            CALL AUTOMATION                                   #
################################################################################

Note: ALL commands should be run from the call-automation/ directory

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
   
     
Inbound Auto Attendant
----------------------

Functional: 

sipp-3.3.990/sipp qa4-fs18.dev.coredial.com -sf inbound/auto_attendant/functional/inbound_auto_attendant_direct.xml -inf inbound/auto_attendant/functional/from_sipp_to_qa4-fs18_auto_attendant.csv -aa -i 172.16.128.89 -nostdin -m 1 

bin/assertsuccess.py inbound/auto_attendant/functional/inbound_auto_attendant_voicemail_new.txt inbound/auto_attendant/functional/assertions.csv inbound/auto_attendant/functional/inbound_auto_attendant_voicemail_base.txt

Load: 

sipp-3.3.990/sipp qa4-fs18.dev.coredial.com -sf inbound/auto_attendant/load/inbound_auto_attendant_direct.xml -inf inbound/auto_attendant/load/from_sipp_to_qa4-fs18_auto_attendant.csv -aa -i 172.16.128.89 -nostdin -r 10 -m 9000



Inbound Holiday
----------------------

Functional: 

sipp-3.3.990/sipp qa4-fs18.dev.coredial.com -sf inbound/holiday/functional/inbound_holiday_direct.xml -inf inbound/holiday/functional/from_sipp_to_qa4-fs18_holiday.csv -aa -i 172.16.128.89 -nostdin -m 1 

bin/assertsuccess.py inbound/holiday/functional/inbound_holiday_voicemail_new.txt inbound/holiday/functional/assertions.csv inbound/holiday/functional/inbound_holiday_voicemail_base.txt

Load: 

sipp-3.3.990/sipp qa4-fs18.dev.coredial.com -sf inbound/holiday/load/inbound_holiday_direct.xml -inf inbound/holiday/load/from_sipp_to_qa4-fs18_holiday.csv -aa -i 172.16.128.89 -nostdin -r 13 -m 11700

