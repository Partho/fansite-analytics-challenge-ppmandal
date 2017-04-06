'''
Detect patterns of three consecutive failed login attempts over 20 seconds,
and block all further attempts to reach the site from the same IP address
for the next 5 minutes.

The script reads the log data, and writes all blocked sites in blocked.txt
'''

import sys
import time

from processLogFile import processLogFile
from TimeUtility import TimeUtility


def main(argv):

    start_time = time.time()

    input_filepath = argv[1]
    output_filepath = argv[2]
    
    """
    Maintain two tables:
    
    potential_block_counter : site to store 
                              potentially block sites,
                              it's attempts and 20 sec
                              time window
    
    block_table : to store sites that are blocked
                  for 5 mins
    """
    potential_block_counter = dict()
    block_table = dict()
    
    log_processor = processLogFile()

    # String to check whether the login by
    # site is successful or not
    unsuccessful = "POST/loginHTTP/1.0401"
    successful = "POST/loginHTTP/1.0200"

    
    outfile = open(output_filepath, "w")

    
    with open(input_filepath, "r") as fo:
        for line in fo:
            
            """
            host : row[0]
            timestamp : row[1]
            request_method: row[2]
            URI: row[3]
            http_version: row[4]
            reply_code: row[5]
            """
            
            row = log_processor.return_tuple(line)
            
            host = row[0]
            timestamp = TimeUtility.str_to_date(row[1])

            # Concatenate string in this format
            # "POST/loginHTTP/1.0401" to 
            validate_success = ''.join(row[2:6])

            # If host is in block table, and the timestamp
            # falls within 5 min frame, block the site else
            # 5 min window expires, so remove it
            if host in block_table:
                if timestamp <= block_table[host]:
                    outfile.write(line)
                else:
                    del block_table[host]


            # In case the login fails, if the host not in potential table,
            # store the host, and keep it's attempt as 1, plus add 20 sec
            # timestamp. Otherwise, if timestamp falls with 20 sec period 
            # for the same host, increment attempt. If it reaches 3,
            # add the IP to blocked table
            if validate_success == unsuccessful:
                if host not in potential_block_counter:
                    potential_block_counter[host]= {"attempt":1, "end_time":TimeUtility.add_second(timestamp, 20)}

                elif timestamp <= potential_block_counter[host]["end_time"]:
                        
                        if potential_block_counter[host]["attempt"] < 3:
                            potential_block_counter[host]["attempt"] += 1
                        
                        if potential_block_counter[host]["attempt"] == 3:
                            if host not in block_table:
                                block_table[host] = TimeUtility.add_second(timestamp, 300)

            # In case the login succeeds, and if the host in potential
            # counter has less than 3 attempts, remove it from potential
            # host table, else keep it in blocked table.
            elif validate_success == successful:
                if host in potential_block_counter:
                    if potential_block_counter[host]["attempt"] < 3:
                        del potential_block_counter[host]


    outfile.close()

    print "----------------------------\n"
    print "Blocked IPs written to blocked.txt. Time lapsed : " + \
            str(time.time()-start_time) + " seconds\n"




if __name__ == "__main__":
    main(sys.argv)
