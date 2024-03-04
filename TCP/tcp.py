import dpkt
import socket
import csv
from datetime import datetime 
import matplotlib.pyplot as plt
import pandas as pd
import time

def make_csv():
    f = open('mar4.pcap','rb')
    pcap = dpkt.pcap.Reader(f)
    

    with open('tcp_ack.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['sec', 'tcp.ack',"speed"]) 
        last_ack = 0
        last_time=0
        window = 30
        i = 0

        for ts, buf in pcap:

            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            if eth.type == dpkt.ethernet.ETH_TYPE_IP: 
                ip = eth.data
                if ip.p == dpkt.ip.IP_PROTO_TCP: 
                    tcp = ip.data 
                    src_ip = socket.inet_ntoa(ip.src)
                    dst_ip = socket.inet_ntoa(ip.dst)
                    if (src_ip =="10.133.15.227" and dst_ip=="52.206.68.26"):
                        # Calculate the number of seconds since starting download
                        # I started download at 1:53pm on March 4th                        
                        second = ts - time.mktime((2024, 3, 4, 13, 53, 0, 0, 0, 0))
                        if (i%window==0):    
                            last_ack = tcp.ack if last_ack == 0 else last_ack
                            speed = (tcp.ack-last_ack)/(second-last_time)
                            last_ack = tcp.ack
                            last_time = second

                        writer.writerow([second, tcp.ack,speed])
                        i+=1

    f.close()  


def plotdata(df):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))

    # Divide by 1 million to get MB/sec
    ax1.plot(df['sec'], df['tcp.ack']/1000000, color='blue')
    ax1.set_ylabel('Packets acknowledged (MB)')

    ax1.set_title(f'Number of unique/total TCP acknowledgments: {df["tcp.ack"].nunique()} / {len(df)} \n Acknowledgments of TCP over time')
    ax1.grid(True)


    # Plot the second subplot
    ax2.set_title(f'data throughput')

    ax2.plot(df['sec'], df['speed']/1000000, color='green')
    ax2.grid(True)
    ax2.set_ylabel('Connection speed MB/sec')
    ax2.set_xlabel('Time (seconds)')


    plt.tight_layout()
    plt.show()

if __name__ == "__main__": 
    make_csv()

    df = pd.read_csv("./tcp_ack.csv")
    df['sec'] = df['sec'].astype(float)
    df['tcp.ack'] = df['tcp.ack'].astype(float)
    df['speed'] = df['speed'].astype(float)
    print(f"Number of unique/total TCP acknowledgments: {df['tcp.ack'].nunique()} /{len(df)}")
    df = df[15:]
    
    plotdata(df)
    