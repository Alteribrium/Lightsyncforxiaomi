from subprocess import call

class openfile():
   def get_status(ip_tok):
        f = open('lampstatus.bat','w')
        f.write('miiocli yeelight --ip '+str(ip_tok[0])+' --token '+str(ip_tok[1])+' status>lampstatus.txt')
        f.close()
        call('lampstatus.bat')
        fileinfo = open('lampstatus.txt','r').read()
        lamp_info =['','','']
        lamp_info[0] = int(fileinfo[fileinfo.find('Brightness')+12:fileinfo.find('Brightness')+15])
        lamp_info[1] = int(fileinfo[fileinfo.find('Temperature:')+13:fileinfo.find('Temperature:')+17])
        lamp_info[2] = str(fileinfo[fileinfo.find('Power:')+7:fileinfo.find('Power:')+8])
        if lamp_info[2] == 'T':
            lamp_info[2] = True
        else:
            lamp_info[2] = False
        return lamp_info


   def lampconfig():
       ip_tok = ['','']
       try:
           f = open('ip_token.txt','r')
           fileinfo = f.read()
           pos = 0
           i = 0
           while i< len(fileinfo):
               ip_tok[pos] += fileinfo[i]
               if fileinfo[i+1:i+2] == ('\n'):
                   if pos < (len(ip_tok)-1):
                       pos = 1
                       i+= 1
                   else:
                       break
               i+=1
           f.close()
       except:
           a=2
       return ip_tok


   def getip_tok():
       while True:
           ip_tok = openfile.lampconfig()
           if ip_tok[0] == '' or ip_tok[1] =='':
                while True:
                    ip_tok[0] = input('input lamp ip: ')
                    pieces = ip_tok[0].split('.')
                    if len(pieces) == 4:
                        if all(0<=int(i)<=255 for i in pieces):
                            break
                    else:
                        print('Input ip in Ipv4 format')
                while True:
                    ip_tok[1] = input('input Lamp Token: ')
                    if len(ip_tok[1]) ==32:
                        break
                    else:
                        print('Token must contain 32 sumbols')
                f = open('ip_token.txt','w')
                f.write(ip_tok[0] +'\n'+ip_tok[1]+'\n')
                f.close()
           else:
               return(ip_tok)


   def try_to_connect(ip_tok):
       print('Connecting...')
       while True:
           f = open('lampstatus.bat','w')
           f.write('miiocli yeelight --ip '+str(ip_tok[0])+' --token '+str(ip_tok[1])+' toggle>lampstatus.txt')
           f.close()
           call('lampstatus.bat')
           fileinfo = open('lampstatus.txt','r').read()
           if 'Error' in fileinfo:
               openfile.getip_tok()
           else:
               call('lampstatus.bat')
               break


   def getippassportname():
       try:
           f = open('rcon.txt','r')
           fileinfo = f.read()
           info = ['','','','']
           pos = 0
           i = 0
           while True:
               info[pos] += fileinfo[i]
               if fileinfo[i+1:i+2] == ('\n'):
                   if pos < (len(info)-1):
                       pos += 1
                       i+= 1
                   else:
                       break
               i+=1
           return info[0],info[1],int(info[2]),info[3]
       except:
           info = ['','','','']
           while True:
                info[0] = input('input rcon ip: ')
                pieces = info[0].split('.')
                if len(pieces) == 4:
                    if all(0<=int(i)<=255 for i in pieces):
                        break
                else:
                    print('Input ip in Ipv4 format')
           info[1] = str(input('input rcon password: '))
           while True:
               info[2] = input('Input rcon port: ')
               try:
                   info[2] = int(info[2])
                   info[2] = str(info[2])
                   break
               except:
                   print('Port is a number')
           info[3] = str(input('Input player Nickname: '))
           f = open('rcon.txt','w')
           f.write(info[0] +'\n'+info[1]+'\n'+info[2]+'\n'+info[3]+'\n')
           f.close()
           return info[0],info[1],int(info[2]),info[3]
           




class change():
    def brightness(ip_tok,brightness):
        f = open('change.bat','w')
        f.write('miiocli yeelight --ip '+ip_tok[0]+' --token '+ip_tok[1]+' set_brightness '+str(brightness))
        f.close()
        call('change.bat')
        return brightness 


    def color(ip_tok,color,new_color):
        for i in range(3):
            f = open('change.bat','w')
            f.write('miiocli yeelight --ip '+ip_tok[0]+' --token '+ip_tok[1]+' set_color_temp '+str(int(color+(new_color-color)*(i+1)/3)))
            f.close()
            call('change.bat')
        return new_color


    def turn(ip_tok):
        f = open('change.bat','w')
        f.write('miiocli yeelight --ip '+ip_tok[0]+' --token '+ip_tok[1]+' toggle')
        f.close()
        call('change.bat')


    def returned(ip_tok,lampstatus,lampstart):
        if lampstatus[0] != lampstart[0]:
            change.brightness(ip_tok,lampstart[0])
        if lampstatus[1] != lampstart[1]:
            change.color(ip_tok,lampstatus[1],lampstart[1])
        if lampstatus[2] != lampstart[2]:
            change.turn(ip_tok)

