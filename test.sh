od -Ax -tx1 -v ~/Downloads/example.gif > /tmp/dump
text2pcap -l 162 /tmp/dump /tmp/example.pcap
tshark -r /tmp/example.pcap -o "uat:user_dlts:\"User 15 (DLT=162)\",\"gif\",\"0\",\"\",\"0\",\"\"" -T json