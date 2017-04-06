# Class implementing circular buffer of 3600 sec
# to store timestamp and no. of times site accessed
# at that timestamp

from TimeUtility import TimeUtility

class HourlyCircularBuffer:

    def __init__(self):
        
        # init_time is first timestamp occurring log file
        # and self.window_end_time will be set to init_time
        self.init_time =  None
        self.window_end_time = None

        
        # Maintain an hour based circular queue of tuple maintaining 
        # timestamp and frequency at that timestamp. 
        self.circular_queue = [[None, 0]]*3600

        
        # Counter to indicate no. of times site 
        # accessed over 60-min window
        self.times_site_accessed = 0
        
        
        # Index of circular queue initialized to 0
        self.queue_idx = 0

        # Store frequency of previous timestamp.
        # Will see the usage later in code
        self.prev_old_freq = None

        
        # Store the previous value of buffer at that timestamp
        # to update the times_site_accessed. Will see the usage 
        # later in code
        self.old_timestamp = None
        self.old_freq = None

    
    

    # Check if log file terminates before first 60-min period
    def _isWindowHourShort(self):
        return self.window_end_time < TimeUtility.add_second(self.init_time, 3600)
    

    

    # If log file terminates before first 60-min period from
    # self.init_time, we start extracting top 10 busiest period
    def emptyBufferHourShort(self, heap):
        
        idx = 0

        while self.circular_queue[idx][0] != None and idx <=self.queue_idx:
            key = self.circular_queue[idx][0]
            value = self.times_site_accessed
            heap.add(key, value)
            
            self.times_site_accessed -= self.circular_queue[idx][1]
            idx += 1

        # Extract top-10 busiest 60-min window
        result = heap.extract_k_largest(10)

        return result

    

    # If log file terminates after eof, we start extracting 
    # top 10 busiest period after end of file
    def emptyBufferOutsideLog(self, heap):

        self.times_site_accessed += self.circular_queue[(self.queue_idx)%3600][1] - self.prev_old_freq
        
        #send the first timestamp where the buffer stopped, to max-heap
        key = TimeUtility.add_second(self.circular_queue[(self.queue_idx)%3600][0], -3600)
        value = self.times_site_accessed

        heap.add(key, value)

        for idx in range(self.queue_idx+1, 3600+self.queue_idx):
            remnant_start_time = self.circular_queue[(idx)%3600][0]
            prev_freq = self.circular_queue[(idx-1)%3600][1]
            self.times_site_accessed -= prev_freq

            #send to max-heap
            heap.add(remnant_start_time, self.times_site_accessed)

        # Extract top-10 busiest 60-min window
        result = heap.extract_k_largest(10)

        return result


            
    def runBufferInsideLog(self, timestamp, heap):

        # Convert the date in string to datetime format
        # for easier computation
        time_key = TimeUtility.str_to_date(timestamp)

        
        # Init time is the timestamp where the log starts
        # Window end time is the time 
        if self.init_time == None:
            self.init_time =  time_key
            self.window_end_time = self.init_time


        
        # Iterate self.window_end_time till the incoming timestamp
        # and make them 0 in case they aren't there

        while self.window_end_time < time_key:
            
            # Condition to start sending time windows with frequency 
            # to max_heap. Will start in case the circular buffer
            # completes one cycle, i.e., fills data for all 3600 sec
            # of a particular window
            
            if TimeUtility.time_diff(self.window_end_time, self.init_time) >= 3600:

                # Init sliding window start condition
                if self.old_timestamp == self.init_time:
                    
                    # Initialize previous old frequency for updating 
                    # global counter of next timestamp
                    self.prev_old_freq = self.old_freq
                    
                    self.times_site_accessed += self.circular_queue[self.queue_idx][1] 
                
               
                else:
                    # once sliding window starts, self.times_site_accessed will update continuously
                    # with this formula
                    self.times_site_accessed += self.circular_queue[self.queue_idx][1] - self.prev_old_freq
                    
                    # Update previous old frequency
                    self.prev_old_freq = self.old_freq
                    
                
                # send to max_heap
                #print self.old_timestamp, self.times_site_accessed
                heap.add(self.old_timestamp, self.times_site_accessed)


            # Increment the window end time
            self.window_end_time = TimeUtility.add_second(self.window_end_time, 1)

            # Find the queue index where the timestamp 
            # with frequency will be inserted using 
            # timestamp itself
            minute = self.window_end_time.minute
            second = self.window_end_time.second
            self.queue_idx = (minute * 60 + second) - 1
            
            # Store the previous value of buffer at that timestamp
            # to update the self.times_site_accessed
            self.old_timestamp, self.old_freq = self.circular_queue[self.queue_idx][0], \
                                                self.circular_queue[self.queue_idx][1]
            
            # Replace the old value with new one
            self.circular_queue[self.queue_idx] = [self.window_end_time, 0]
            
            # DEBUG : To check the count at that index
            #print self.queue_idx, self.circular_queue[self.queue_idx][0], self.circular_queue[self.queue_idx][1]
           

        # In case window end time reaches incoming timestamp
        # we store the frequency of the incoming timestamp
        if self.window_end_time == time_key:
            if self.circular_queue[self.queue_idx][0] == None:
                 self.circular_queue[self.queue_idx][0] = self.window_end_time
            
            # Maintain the frequency of the particular timestamp
            self.circular_queue[self.queue_idx][1] += 1 
            
            # In case the first cycle of circular buffer not complete
            # we increment the global counter in sync with circular queue
            if TimeUtility.time_diff(self.window_end_time, self.init_time) < 3600:
                self.times_site_accessed += 1
        
        # DEBUG : To check the count at that index
        # print self.queue_idx, self.circular_queue[self.queue_idx][0], self.circular_queue[self.queue_idx][1]
