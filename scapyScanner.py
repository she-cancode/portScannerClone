from scapy.all import IP, TCP, sr1


def stealth_syn_scan(target_ip, port):
    print(f"Crafting raw SYN packet for {target_ip}:{port}...")

    # 1. Forge the Network Layer (IP)
    # We explicitly tell it where this packet is going.
    ip_layer = IP(dst=target_ip)

    # 2. Forge the Transport Layer (TCP)
    # We set the destination port, and explicitly set the TCP flag to "S" (SYN)
    tcp_layer = TCP(dport=port, flags="S")

    # 3. Stack the layers together using Scapy's '/' operator
    packet = ip_layer / tcp_layer

    # 4. Send the packet and wait for exactly 1 response (sr1)
    # verbose=0 stops Scapy from printing a bunch of default routing text
    response = sr1(packet, timeout=1, verbose=0)

    # 5. Analyze the raw response
    if response is None:
        print(f"[-] Port {port} is FILTERED (Firewall swallowed our packet)")

    elif response.haslayer(TCP):
        # 0x12 is the hexadecimal representation of the SYN-ACK flags
        if response.getlayer(TCP).flags == 0x12:
            print(f"[+] Success! Port {port} is OPEN (Received SYN-ACK)")

            # Here is where a true Nmap clone sends a RST (Reset) packet
            # to tear down the connection quietly.

        # 0x14 is the hexadecimal representation of the RST-ACK flags
        elif response.getlayer(TCP).flags == 0x14:
            print(f"[-] Port {port} is CLOSED (Target rejected us)")


if __name__ == "__main__":
    target = "8.8.8.8"
    test_port = 443

    stealth_syn_scan(target, test_port)
