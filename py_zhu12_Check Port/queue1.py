import queue

l = [1,2,3,4,5,6,7]

q = queue.Queue(2)

def put_ip_to_q(l):
    for i in l:
        q.put(i)
        q.task_done()


def check(ip,ports_list):
    print("Checking %s...",ip)
    row = [] 
    row.append(ip) 
    for j in range(len(ports_list)):              
        row.append(PortOpen(ip,ports_list[j]))
    return row


def multithread():    
    while 1:
        q.join()
        ip = q.get()
        thread = threading.Thread(target=check,args=(ip,ports_list))
        thread.start()
        thread.join()



    WORD_THREAD = 10
    threads = []
    for i in range(WORD_THREAD):
        thread = threading.Thread(target=tcping)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()