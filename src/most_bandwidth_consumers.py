'''
Identify the 10 resources that consume the most bandwidth on the site

The script reads the log data, and writes the top 10 most bandwidth-intensive resources in resources.txt
'''
import sys
import time
import re
import collections
import heapq

from processLogFile import processLogFile
from MaxHeap import MaxHeap


# Read file line by line and create hash table with URI 
# bandwidth consumption
def URI_bytes_table(file_path):

    URI_bytes_counter = collections.defaultdict(int)
    log_processor = processLogFile()
    
    with open(file_path, "r") as fo:
        for line in fo:
            # 3rd and 6th index in tuple stores URI and bytes.
            token = log_processor.return_tuple(line)
            if token[6].isdigit():
                URI_bytes_counter[token[3].strip('"')] += int(token[6])
            else:
                URI_bytes_counter[token[3].strip('"')] += 0
    return URI_bytes_counter



# Use max-heap to extract top k resources consuming most bandwidth
# O(k+(n-k)lgk) time complexity 
def top_k_consumers(URI_byte_counter, k=10):
    
    heap = MaxHeap()
    # In case no. of hosts is less than specified k
    k = min(k, len(URI_byte_counter))

    # Push the elements in dictionary to heap
    for URI, byte in URI_byte_counter.iteritems():
        heap.add(URI, byte)

    # Extract top-10 bandwidth consumers
    result = heap.extract_k_largest(k)

    return result


# Write output to resources.txt
def write_resource_output(data, file_path):
    with open(file_path, 'w') as f:
        for item in data:
            f.write(item[0] + '\n')


def main(argv):
    
    start_time = time.time()
    filepath = argv[1]

    # create hash table of URI bytes consumption. Roughly takes 45-48 sec for 
    # given input file of ~450MB.
    URI_byte_counter = URI_bytes_table(filepath)
    print "----------------------------\n"
    print "Hash table of URI bytes consumption created. Time lapsed: " + \
            str(time.time()-start_time) + " seconds"


    # Here k = 10 
    result = top_k_consumers(URI_byte_counter)
    print "----------------------------\n"
    print "Top 10 results extracted. Time lapsed: " + \
            str(time.time()-start_time) + " seconds"



    # Write result to resources.txt
    output_dest_path = argv[2]
    write_resource_output(result, output_dest_path)

    print "----------------------------\n"
    print "Results written to resources.txt.\n"



if __name__ == "__main__":
    main(sys.argv)
