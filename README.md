# Insight Coding Challenge

#### Insight Data Engineering - Coding Challenge (April 2017 )
##### Submitted by: Partho Pratim Mandal

## Description of src folder

* `most_active_hosts.py` : Implements feature 1, does host / IP address count, and writes the top 10 hosts with  their frequency in `hosts.txt`. Uses bucket sort to extract the top 10 hosts.

* `most_bandwidth_customers.py` : Implements feature 2, writes the top 10 most bandwidth-intensive resources in `resources.txt`. Uses Max-heap implemented in `MaxHeap.py` to extract the top 10 resources.

* `most_busiest_hourwise.py` : Implements feature 3, writes the top 10 most frequently visited sites in `hours.txt`. Uses circular buffer of 3600 sec with provision for storing timestamp and its frequency, which is implemented in `HourlyCircularBuffer.py`. 

* `consecutive_failed_logins.py` : Implements feature 4, writes IP address / hosts blocked for 5 min window period. Uses two hash tables, one for storing potential block sites for 20 sec, and other storing blocked IP for 5 min.

* `processLogFile.py` : Tokenizes each line into host, timestamp, request method, URI, http version, reply code and reply bytes.

* `TimeUtility.py` : A time utility class providing basic functionalities like converting string to datetime, finding difference between two timestamps etc.

These scripts also show the runtime for various stages like running algo, extracting top 10 etc.


## Benchmark
The system used for building scripts, and testing runtime is Macbook Pro 2015, 8GB RAM, i5 dual-core processor. These are times taken for ~450 MB input log file. However, these times will vary by time and system, but gives a general idea about the average runtime.

* **Feature 1 :** 40.634 seconds

* **Feature 2 :** 38.733 seconds

* **Feature 3 :** 197.476 seconds

* **Feature 4 :** 162.668 seconds


## Other information

These files don't make use of any external libraries. Compatible python version is >= 2.7. 

All the scripts can be invoked by running `run.sh` on the root directory. Ensure that permisssions are set.
Changes can be made to this script file to set your input and output path. 

For more information on the coding-challenge check out https://github.com/InsightDataScience/fansite-analytics-challenge
