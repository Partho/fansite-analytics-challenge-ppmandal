'''
List in descending order the site's 10 busiest 60-minute period.

The script reads the log data, and writes the top 10 most frequently 
visited sites in hours.txt
'''
import sys
import time

from TimeUtility import TimeUtility

from HourlyCircularBuffer import HourlyCircularBuffer
from processLogFile import processLogFile
from MaxHeap import MaxHeap



# Write output to hours.txt
def write_hours_output(data, file_path):
    with open(file_path, 'w') as f:
        for item in data:
            f.write(TimeUtility.date_to_str(item[0])+","+str(item[1]) + '\n')

def main(argv):
    
    start_time = time.time()
    
    input_filepath = argv[1]
    output_filepath = argv[2]

    log_processor = processLogFile()
    buf = HourlyCircularBuffer()
    heap = MaxHeap()

    with open(input_filepath, "r") as fo:
        for line in fo:
            timestamp = log_processor.return_tuple(line)[1]
            buf.runBufferInsideLog(timestamp, heap)

    # Read all timestamps from log file, maintain in circular
    # buffer and send 60-min window to max-heap. Roughly takes 
    # 3 min 30 sec for given input file of ~450MB.
    print "----------------------------\n"
    print "Reading all timestamps and forming most 60-min window done.\n" +\
          "Time lapsed: " + str(time.time()-start_time) + " seconds"

      
    # If log file terminates before first 60-min period from
    # init_time, we start extracting top 10 busiest period and
    # Else, iteration still left on buffer after file terminates 
    # and top 10 busiest period.
    
    if buf._isWindowHourShort():
        result = buf.emptyBufferHourShort(heap)
    else:
        result = buf.emptyBufferOutsideLog(heap)

    # Sending remaining 60-min window to max-heap 
    # and extracting top-10 windows done.
    print "----------------------------\n"
    print "Sending remaining 60-min window to max-heap and extracting top-10" +\
          " windows done\nTime lapsed: " + str(time.time()-start_time) + " seconds"


    # Write result to hours.txt
    output_dest_path = argv[2]
    write_hours_output(result, output_filepath)
    print "----------------------------\n"
    print "Results written to hours.txt.\n" 



if __name__ == "__main__":
    main(sys.argv)