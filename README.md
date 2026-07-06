Python Port Scanner Clone
💡 Inspiration
While diving into native Linux network commands to better understand system administration and infrastructure, I wanted to take my learning a step further. Earning my AWS Cloud Practitioner certification earlier this year really highlighted the importance of network security, traffic flow, and access control. Instead of just running pre-built tools like nmap or netcat from the terminal and accepting the output, I built this project to see exactly how TCP connections and packet forging work at the code level. This repository is my hands-on exploration of network interactions.

🛠️ Project Overview
This project contains two distinct approaches to network scanning written in Python. It demonstrates the evolution from a standard, loud TCP connection scanner to a more advanced, quiet SYN scanner using packet manipulation.

1. foundational.py - The Full Connect Scanner
This script uses Python's built-in socket library to perform a classic TCP Connect scan. It acts exactly like a normal application trying to connect to a service.

The Mechanism: It attempts a full 3-way TCP handshake (SYN -> SYN-ACK -> ACK) with the target for each specified port.

Concurrency: To speed up the process of scanning ports 1 through 1024, it implements ThreadPoolExecutor from the concurrent.futures module, allowing up to 100 simultaneous threads.

Data Structuring: It maps discovered open ports against a dictionary of common services (like HTTP, SSH, FTP) and outputs the final results as a cleanly formatted JSON object.

Pros & Cons: It is highly reliable and requires no special administrative privileges to run. However, completing a full handshake is "loud" and easily logged by firewalls and intrusion detection systems.

2. scapyScanner.py - The Stealth SYN Scanner
This script leverages the scapy library to craft raw network packets, bypassing the operating system's standard network stack to perform a "stealth" or half-open scan.

The Mechanism: It manually stacks the Network Layer (IP) and Transport Layer (TCP). It sends a single packet with the SYN flag set, asking the target to initiate a connection.

Traffic Analysis: * If the target replies with 0x12 (SYN-ACK), the port is Open. (In a full implementation, we would immediately send an RST packet to tear the connection down before logging occurs).

If the target replies with 0x14 (RST-ACK), the port is Closed.

If there is no response, the port is Filtered (likely dropped by a firewall).

Pros & Cons: This method is much stealthier because it never completes the TCP handshake, making it less likely to be flagged by basic application logs. However, crafting raw packets typically requires root/administrator privileges on the host machine.

🚀 How to Use
Prerequisites:

Python 3.x

scapy library (pip install scapy)

Running the Foundational Scanner:

Bash
python3 foundational.py
Running the Stealth Scanner (Requires Sudo/Admin):

Bash
sudo python3 scapyScanner.py
Disclaimer: This project was created for educational purposes to understand network protocols and security auditing. Only scan networks and targets you have explicit permission to test.