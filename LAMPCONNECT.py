from open_txt import openfile
from open_txt import change
from subprocess import call 
from time import sleep
from mcrcon import MCRcon


ip_tok = openfile.getip_tok()#get ip and token [ip,token]
openfile.try_to_connect(ip_tok)
lampstart = openfile.get_status(ip_tok)# lamp start status [color_temp,brightness]
lampstatus = lampstart

rcon_ip,rcon_pass,rcon_port,player_name = openfile.getippassportname()

#try:
while True:
    sleep(0.5)
    with MCRcon(rcon_ip, rcon_pass, rcon_port) as mcr:
        resp = mcr.command("lightsync "+ player_name )
        print(resp)
        if (resp == 'E1\n') or (resp == 'E0\n'):
                print('\n Is not founded') 
                break
        print('\rMinecraft lightlevel is: ' + str(resp) + ' ',end='')
        resp = int(resp)
        new_brightness = (resp-5)*10
        print(new_brightness)
        if new_brightness <0:
            new_brightness =0
        if new_brightness !=0 and lampstatus[2] == True:
            if new_brightness !=lampstatus[0]:
                lampstatus[0] = change.brightness(ip_tok,new_brightness)
            else:
                continue
        elif new_brightness == 0 and lampstatus[2] == True:
            lampstatus[2] =False
            change.turn(ip_tok)
        elif new_brightness !=0 and lampstatus[2] == False:
            lampstatus[2] =True
            change.turn(ip_tok)
            lampstatus[0] = change.brightness(ip_tok,new_brightness)
#except KeyboardInterrupt:
#    print("\rFinished by user")
#    input()
#except:
#    print("Error ocured")
#    input()

change.returned(ip_tok,lampstatus,lampstart)
input()