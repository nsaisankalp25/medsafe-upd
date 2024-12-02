import os

os.chdir(r"c:\Users\saisa\Desktop\Coding\Medsafe Btech\medsafe-main\templates\notify")


#print(os.listdir())
# atorvastatin: "{% static 'pics/atorvastatin.jpg' %}"
for i in os.listdir():
    if i.endswith('.jpg'):
        title = i.split('.')[0]
        line = f" {title}: \"(% static 'pics/{i}' %)\","
        line = line.replace("(", "{")
        line = line.replace(")", "}")
        print(line)