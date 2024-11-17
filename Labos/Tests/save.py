import json
amp=2
freq=20
saving = {'amplitude': amp, 'frequence': freq}
print("saving : ",saving)
json.dump(saving, open("signal.json","w"))