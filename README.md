# ysoserial payload generator
Outputs ysoserial payloads to file(s). Files are intended to be used by BurpSuite Intruder.

Payload is based on user supplied windows and/or linux command. For each supplied command a file will be created. The payloads will be new line separated and may be base64 encoded if desired. Note, the unencoded output does not currently work with intruder due to newline encoding - to be fixed.

The list of payloads available was manually generated from ysoserial-master-6eca5bc740-1 on 26 Dec 2020. Future revisions are intended to parse the help output of the user supplied ysoserial jar to obtain possible payloads.

usage: serial_brute.py [-h] [-w WIN] [-l LIN] [-b] [-v] [-p] name ysoserial

Script Generates payloads from all possible ysoserial payload options. Uses a Windows and/or a Linux command to generate the payload

positional arguments:
  name               postfix applied to create filename
  ysoserial          path to ysoserial jar

optional arguments:
  -h, --help         show this help message and exit
  -w WIN, --win WIN  Command for Windows OS
  -l LIN, --lin LIN  Command for Linux OS
  -b, --b64          Base64 encode payload
  -v, --verbose      Output Java trace to stdout on payload failure
  -p, --payload      Output full payload to stdout as well as file

This work is based on blog posts by [Petre Popescu](https://securitycafe.ro/2017/11/03/tricking-java-serialization-for-a-treat/) and [n00py](https://www.n00py.io/2017/11/exploiting-blind-java-deserialization-with-burp-and-ysoserial/)
