from datetime import datetime
import windowsapps, os, pyttsx3, asyncio
from speech_rec import speech_func
from json import loads
from subprocess import getoutput
from openai_azure import openai_func

def greet_user():
    hour = datetime.now().hour
    if hour > 4 and hour < 12:
        greeting = "Good morning!"
    elif hour < 17:
        greeting = "Good afternoon!"
    else:
        greeting = "Good evening!"
    return greeting

def say(x):
    engine = pyttsx3.init()
    voice = engine.getProperty('voices')
    engine.setProperty('voice', voice[1].id)
    engine.say(x)
    engine.runAndWait()

print("\n\n\t\t\t\t\t\t\t\tChatting with Glitch 2.0 🤖")
print(f"\t\t\t\t\t\t\t\tHey buddy!, {greet_user()}")
print("\t\t\t\t\t\t\t\tHow can I assist you?\n\n")
say(f"Hey buddy!, {greet_user()} How can I assist you?")


while(1):
    print("Press enter to proceed")
    input()
    say("You want to write instructions or speak instructions?")
    ch = input("\nWrite or Speak? [W/S]: ")
    if(ch == 'W' or ch == 'w'):
        x = input("😃 - ")
    elif(ch == 'S' or ch == 's'):
        x = speech_func() # Microsoft Azure API
    else:
        print("Please make correct choice 😒")
        say("Please make correct choice")
        continue
    x = x.replace('.', '')
    print("😃 - ", x)
    x = x.lower()
    s = x.split()
    count=0
    bye = 0
    for i in range(len(s)):
        if(s[i].lower() == "open" or s[i].lower() == "launch"):
            name = windowsapps.find_app(f"{s[i+1]}")
            if(name[0].lower() == s[i+1]):
                windowsapps.open_app(f"{s[i+1]}")
                print(f'🤖 - Opening {s[i+1].title()}')
                say(f'Opening {s[i+1].title()}')
            else:
                print("🤖 - I haven't found any app with this name😕")
                say("🤖 - I haven't found any app with this name")
                say("But, I can give you the list of all apps, do you want to choose from that?")
                ch = input("🤖 - But, I can give you the list of all apps, do you want to choose from that? ")
                if(ch=="yes"):
                    cmd = 'powershell -ExecutionPolicy Bypass "Get-StartApps|convertto-json"'
                    apps=loads(getoutput(cmd))
                    names = []
                    for each in apps:
                        names.append(each['Name'])
                    print(names)
                    say("These are all the apps stored in the system. If you want to use any, please write")
                    t = input("🤖 - App Name: ")
                    name = windowsapps.find_app(t)
                    if(name[0].lower() == t):
                        windowsapps.open_app(t)
                        print(f'🤖 - Opening {t}')
                        say(f'Opening {t}')
                    else:
                        print("🤖 - Error in finding app. Please try later")
                    
                elif(ch=="no"):
                    print("🤖 - Okay!")
                    say("Okay!")
                else:
                    print("🤖 - Whats that means? Please try again.")
                    say("Whats that means? Please try again.")
            count += 1
            break

        elif(s[i] == 'bye' or s[i] == 'exit' or s[i] == 'goodbye' or s[i] == 'end'):
            print(f"🤖 - Okay, {greet_user()}😃 Take Care")
            say(f"Okay, {greet_user()}, Take Care")
            count += 1
            bye += 1
            break
        
        elif(s[i] == 'sleep'):
            print("🤖 - Okay, Press any key to Wake Me Up Again!")
            say("Okay, Press any key to Wake Me Up Again!")
            os.system("start RUNDLL32.EXE powrprof.dll,SetSuspendState 0,1,0")
            count += 1
            break
        elif(s[i] == 'shutdown' or s[i] == 'shut' or s[i] == 'off'):
            print("🤖 - Shutting Down your system in 6 Seconds\nSave your work before leaving.")
            say("Shutting Down your system in 6 Seconds. Please Save your work before leaving.")
            os.system("shutdown /s /t 6")
            count += 1
            break

        if(count == 0):
            # azure openAI API
            ans = asyncio.run(openai_func(x))
            print(f"🤖 - {ans}")
            if(ans == None):
                print("Error in connection!")
            say(ans)
            break
    
    if(bye != 0):
        break