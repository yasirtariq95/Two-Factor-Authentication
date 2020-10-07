import os, subprocess
import sys
from base64 import b64encode
import crypt

if os.getuid()!=0:               #checking whether program is running as a root or not.
        print "Please, run as root."
        sys.exit()

print ("Welcome to 2FA!")

print ("(1) Create User Account \n(2) Login \n(3) Update Password \n(4) Delete User Account")

selection=raw_input("Your selection: ")

if selection=='1':
    uname=raw_input("Enter Username you want to add: ")
    with open('/etc/shadow','r') as fp:      #Opening shadow file in read mode
        arr=[]
        for line in fp:                 #Enumerating through all the enteries in shadow file
                temp=line.split(':')
                if temp[0]==uname:      #checking whether entered username exist or not
                    print ("FAILURE: user "+uname+" already exist.")
                    sys.exit()
    passwd=raw_input("Enter Password for the user: ")
    re_passwd=raw_input("Renter Password for the user: ")
    if passwd!=re_passwd:           #just making sure you know what you are entering in password
        print ("Paswword do not match")
        sys.exit()
    salt=raw_input("Enter the salt: ")
    initial_token=raw_input("Enter the initial token: ")
    combined=passwd+initial_token
    hash=crypt.crypt(combined,'$6$'+salt)         #generating hash
    line=uname+':'+hash+":17710:0:99999:7:::"
    file1=open("/etc/shadow","a+")   #Opening shadow file in append+ mode
    file1.write(line+'\n')
    try:
        os.mkdir("/home/"+uname)        #Making home file for the user
    except:
        print("Directory: /home/"+uname+" already exist")
    file2=open("/etc/passwd","a+")          #Opening passwd file in append+ mode
    count=1000
    with open('/etc/passwd','r') as f:              #Opening passwd file in read mode
        arr1=[]
        for line in f:
                temp1=line.split(':')
                while (int(temp1[3])>=count and int(temp1[3])<65534): #checking number of existing UID
                        count=int(temp1[3])+1          #assigning new uid = 1000+number of UIDs +1
    count=str(count)
    str1=uname+':x:'+count+':'+count+':,,,:/home/'+uname+':/bin/bash'
    file2.write(str1+'\n')   #creating entry in passwd file for new user
    file2.close()
    file1.close()
    print("SUCCESS "+uname+" created")

elif selection == '2':

    uname = raw_input("Enter your username please! ")
    flag=0

    with open('/etc/shadow','r') as fp:

        extraFile = open('temp', 'wt') # opening a new file to update the password hash in order to update in shadow file
        arr=[]
        for line in fp:                 #Enumerating through all the enteries in shadow file
            temp=line.split(':')
            if temp[0]==uname:      #checking whether entered username exist or not
                passwd = raw_input("Enter your password please! ")
                ct_token = raw_input("Enter your current token please! ")
                nt_token = raw_input("Enter your next token please! ")
                passwithct = passwd+ct_token
                flag = 1
                salt_and_pass=(temp[1].split('$')) #retrieving salt against the user
                salt=salt_and_pass[2]
                result=crypt.crypt(passwithct,'$6$'+salt) #calculating hash via salt and password entered by user
                if result==temp[1]:                   #comparing generated salt with existing salt entery                                
                    print ("SUCCESS: Login successful.")
                    passwithnt = passwd+nt_token
                    updatedResult = crypt.crypt(passwithnt,'$6$'+salt) #calculating hash via salt and updated password entered by user
                    extraFile.write(line.replace(temp[1], updatedResult)) # writing this line to the temporary file created
                else:
                    print ("FAILURE: password/token incorrect")
                    extraFile.write(line.replace("","")) # if it is not validated dont write anything to the file
            else:
                extraFile.write(line.replace("","")) # again if user does not exist dont write anything to the file cause if i dont use this
                                                    # it will clean the file because it is open in write mode

    extraFile.close()
    fp.close()

    # Now trying to update the entry from my temporary file to shadow file

    with open('temp') as file1:
        readFile = file1.read()
    with open('/etc/shadow', 'w') as file2:
        file2.write(readFile)

    # Now the update has been done and deleting the temporary file

    os.remove('temp')

    # Now if our flag value doesnt change it means user doesnt exist

    if flag == 0:
        print ("FAILURE: user " + uname + " does not exist")

elif selection == '3':

    uname = raw_input("Enter your username please! ")
    flag=0

    with open('/etc/shadow','r') as fp:

        extraFile = open('temp', 'wt') # opening a new file to update the password hash in order to update in shadow file
        arr=[]
        for line in fp:                 #Enumerating through all the enteries in shadow file
            temp=line.split(':')
            if temp[0]==uname:      #checking whether entered username exist or not
                passwd = raw_input("Enter your password please! ")
                newPasswd = raw_input("Enter your new password please! ")
                newSalt = raw_input("Enter new salt value please! ")
                ct_token = raw_input("Enter your current token please! ")
                nt_token = raw_input("Enter your next token please! ")
                passwithct = passwd+ct_token
                flag = 1
                salt_and_pass=(temp[1].split('$')) #retrieving salt against the user
                salt=salt_and_pass[2]
                result=crypt.crypt(passwithct,'$6$'+salt) #calculating hash via salt and password entered by user
                if result==temp[1]:                   #comparing generated salt with existing salt entery
                    passwithnt = newPasswd+nt_token
                    updatedResult = crypt.crypt(passwithnt,'$6$'+newSalt) #calculating hash via salt and updated password entered by user
                    extraFile.write(line.replace(temp[1], updatedResult)) # writing this line to the temporary file created
                    print ("SUCCESS: user " + uname + " updated")
                else:
                    print ("FAILURE: password/token incorrect")
                    extraFile.write(line.replace("","")) # if it is not validated dont write anything to the file
            else:
                extraFile.write(line.replace("","")) # again if user does not exist dont write anything to the file cause if i dont use this
                                                    # it will clean the file because it is open in write mode

    extraFile.close()
    fp.close()

    # Now trying to update the entry from my temporary file to shadow file

    with open('temp') as file1:
        readFile = file1.read()
    with open('/etc/shadow', 'w') as file2:
        file2.write(readFile)

    # Now the update has been done and deleting the temporary file

    os.remove('temp')

    # Now if our flag value doesnt change it means user doesnt exist

    if flag == 0:
        print ("FAILURE: user " + uname + " does not exist")


elif selection == '4':

    uname = raw_input("Enter your username please! ")
    flag=0

    with open('/etc/shadow','r') as fp:

        extraFile = open('temp', 'wt') # opening a new file to update the password hash in order to update in shadow file
        arr=[]
        for line in fp:                 #Enumerating through all the enteries in shadow file
            temp=line.split(':')
            if temp[0]==uname:      #checking whether entered username exist or not
                passwd = raw_input("Enter your password please! ")
                ct_token = raw_input("Enter your current token please! ")
                passwithct = passwd+ct_token
                flag = 1
                salt_and_pass=(temp[1].split('$')) #retrieving salt against the user
                salt=salt_and_pass[2]
                result=crypt.crypt(passwithct,'$6$'+salt) #calculating hash via salt and password entered by user
                if result==temp[1]:                   #comparing generated salt with existing salt entery

                    extraFile.write(line.replace(line, "")) # writing this line to the temporary file created, since we are deleting the 
                                                            # entry i replace the line with empty string
                    print ("SUCCESS: user " + uname + " Deleted")
                    flag = 2 # changing the flaf value cause need to update entry in /etc/passwd file as well
                else:
                    print ("FAILURE: password/token incorrect")
                    extraFile.write(line.replace("","")) # if it is not validated dont write anything to the file
            else:
                extraFile.write(line.replace("","")) # again if user does not exist dont write anything to the file cause if i dont use this
                                                    # it will clean the file because it is open in write mode

    extraFile.close()
    fp.close()

    # Now trying to update the entry from my temporary file to shadow file

    with open('temp') as file1:
        readFile = file1.read()
    with open('/etc/shadow', 'w') as file2:
        file2.write(readFile) # shadow file entry is removed

    # Now the update has been done and deleting the temporary file

    os.remove('temp')

    # Now removing the entry from passwd file

    with open('/etc/passwd', 'r') as passFile:

        extraFileForPasswd = open('temp2', 'wt')

        for line in passFile:
            splitLine = line.split(':')

            if splitLine[0] == uname:
                if flag == 2:
                    extraFileForPasswd.write(line.replace(line, ""))

                    try:
                        os.rmdir("/home/"+uname)        # Deleting home file for the user
                    except:
                        print("Directory: /home/"+uname+" does not exist")

            else:
                extraFileForPasswd.write(line.replace("",""))

    extraFileForPasswd.close()
    passFile.close()

    with open('temp2') as file1:
        readFile = file1.read()
    with open('/etc/passwd', 'w') as file2:
        file2.write(readFile) # shadow file entry is removed

    # Now the update has been done and deleting the temporary file

    os.remove('temp2')

    # Now if our flag value remains 0 it means user doesnt exist

    if flag == 0:
        print ("FAILURE: user " + uname + " does not exist")

