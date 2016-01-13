################################################################################
#                            CALL AUTOMATION                                   #
################################################################################

Note: ALL commands should be run from the call-automation/ directory

Installing SIPp
---------------
1. Download SIPp 3.3.990

   wget -O sipp.tar.gz http://sourceforge.net/projects/sipp/files/sipp/3.4/sipp-3.3.990.tar.gz/download
   
2. Configure SIPp

   tar -xvzf sipp.tar.gz ; cd sipp ; ./configure --with-pcap ; make


Inbound Auto Attendant
----------------------

Functional: 

sipp-3.3.990/sipp qa4-fs18.dev.coredial.com -sf inbound/auto_attendant/functional/inbound_auto_attendant_direct.xml -inf inbound/auto_attendant/functional/from_sipp_to_qa4-fs18_auto_attendant.csv -aa -i 172.16.128.89 -nostdin -m 1 

bin/assertsuccess.py inbound/auto_attendant/functional/inbound_auto_attendant_voicemail_new.txt inbound/auto_attendant/functional/inbound_from_pstn_to_auto_attendant.csv

Load: 

sipp-3.3.990/sipp qa4-fs18.dev.coredial.com -sf inbound/auto_attendant/load/inbound_auto_attendant_direct.xml -inf inbound/auto_attendant/load/from_sipp_to_qa4-fs18_auto_attendant.csv -aa -i <local_ip> -nostdin -r 10 -m 9000


