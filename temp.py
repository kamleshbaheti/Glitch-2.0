from json import loads
from subprocess import getoutput

cmd = 'powershell -ExecutionPolicy Bypass "Get-StartApps|convertto-json"'
apps=loads(getoutput(cmd))
names = []
for each in apps:
    names.append(each['Name'])
print(names)