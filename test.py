
from mainClass import MainClass

print(len(MainClass.token1))
print(len(MainClass.token2))

MainClass.send_message("TEST", MainClass.token1, timeOut=5)