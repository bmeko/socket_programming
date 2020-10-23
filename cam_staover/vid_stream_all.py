import socket,cv2, pickle,struct
import multiprocessing

# create socket
global soc
global us
global pro_con
port = 9999

	

soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("for clinet input clinet")
print("for server input server")
us=input("type of connection:")
pro_con=0




def send():
	global p1

	global pro_con
	
	while True:
	   
	    if soc:
	        vid = cv2.VideoCapture(0)
	        
	        while(vid.isOpened()):
	            img,frame = vid.read()
	            a = pickle.dumps(frame)
	            message = struct.pack("Q",len(a))+a
	            soc.sendall(message)
	            
	            cv2.imshow(f'TRANSMITTING VIDEO {us}',frame)
	            key = cv2.waitKey(1) & 0xFF
	            if key ==ord('q'):
	            	break
	        soc.close()


def re():
	global p2
	global pro_con
	print(pro_con)
	data = b""
	payload_size = struct.calcsize("Q")
	while True:
		
		while len(data) < payload_size:
			packet = soc.recv(4*1024)# 4K
			if not packet:
				break
			data+=packet
		packed_msg_size = data[:payload_size]
		data = data[payload_size:]
		msg_size = struct.unpack("Q",packed_msg_size)[8]
		    
		while len(data) < msg_size:
			data += soc.recv(4*1024)
		frame_data = data[:msg_size]
		data  = data[msg_size:]
		frame = pickle.loads(frame_data)
		cv2.imshow(f"RECEIVING VIDEO {us}",frame)
		key = cv2.waitKey(1) & 0xFF
		if key  == ord('q'):
			break		   
	soc.close()



p1 = multiprocessing.Process(target=re)
p2 = multiprocessing.Process(target=send)


if us == "clinet":
	
	host_ip = input("input the servers ip: ") 
	soc.connect((host_ip,port)) 
	p1.start()
	p2.start()
elif us == "server":
	
	host_ip = input("input your machines ip: ")
	print("host ip:",host_ip)
	socket_address = (host_ip,port)
	soc.bind(socket_address)
	soc.listen(5)
	print("LISTENING AT:",socket_address)

	soc,addr = soc.accept()
	print('GOT CONNECTION FROM:',addr)
	p2.start()
	p1.start()

