'''
List in descending order the top 10 most active hosts/IP addresses that have accessed the site

The script reads the log data, and writes the top 10 hosts with their frequency in hosts.txt
'''
import sys
import time
import re
import collections

from processLogFile import processLogFile

def host_table(file_path):
    
    # Read file line by line and create hash table with host count    
    host_counter = collections.defaultdict(int)
    log_processor = processLogFile()
    
    with open(file_path, "r") as fo:
        for line in fo:
            # 0th index in tuple stores host. Store host count
            host = log_processor.return_tuple(line)[0]
            host_counter[host] += 1
    return host_counter


# Use bucket sort to store top k hosts
def top_k_hosts(host_counter, k):
    
    # list to store top k result
    res = []

    # In case no. of hosts is less than specified k
    k = min(k, len(host_counter))


    # create bucket of size most frequent host
    max_bucket = max(host_counter.values())
    bucket = [[] for _ in range(max_bucket)]

    # place the host in appropriate bucket
    for host, freq in host_counter.items():
        bucket[freq - 1].append(host)

    # Store top k results and at the same time 
    # sort hosts lexicographically
    for idx in range(max_bucket - 1, -1, -1):
        for host in sorted(bucket[idx]):
            if k == 0:  
                break
            res.append((host, host_counter[host]))
            k -= 1
    return res
 

# Write result to hosts.txt
def write_hosts_output(data, file_path):
    with open(file_path, 'w') as f:
        for item in data:
            f.write(','.join(str(elem) for elem in item) + '\n')


def main(argv):
    
    start_time = time.time()
    filepath = argv[1]

    # create hash table with host/IP frequency. Roughly takes 35-40 sec for 
    # given input file of ~450MB.
    host_counter = host_table(filepath)
    print "----------------------------\n"
    print "Hash table of host/IP created. Time lapsed: " + \
            str(time.time()-start_time) + " seconds"


    # Here k = 10 
    result = top_k_hosts(host_counter, 10)
    print "----------------------------\n"
    print "Top 10 results extracted. Time lapsed: " + \
            str(time.time()-start_time) + " seconds"



    # Write result to hosts.txt
    result_dest_path = argv[2]
    write_hosts_output(result, result_dest_path)

    print "----------------------------\n"
    print "Results written to hosts.txt.\n"


if __name__ == "__main__":
    main(sys.argv)