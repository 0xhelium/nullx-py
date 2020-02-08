import nullx
import sys
from nullx import crypto, log
from nullx.utils import printb

log.log_level = log.VERBOSE

'''
o = open('o.txt', 'r').read()
caesar = nxcrypto.shift.Caesar()
open('e.txt', 'w').write(caesar.encrypt(o, 13))
'''

'''
caesar = nxcrypto.shift.Caesar()
open('op.txt', 'w').write(caesar.decrypt(
    open('e.txt', 'r').read(),
    nxcrypto.shift.FrequencyAnalyzer()
))
'''

'''
o = open('o.txt', 'r').read()
polyalphabetic = nxcrypto.shift.Polyalphabetic()
open('e.txt', 'w').write(polyalphabetic.encrypt(o, 'freedom'))
'''

'''
polyalphabetic = nxcrypto.shift.Polyalphabetic()
o = polyalphabetic.decrypt(
    open('e.txt', 'r').read(),
    nxcrypto.shift.PolyalphabeticFrequencyAnalyzer(7)
    #"freedom"
)
print(o)
'''

'''
log.log_level = log.INFO

log.info("Givin' info")
log.warn("Givin' warning")
log.error("Givin' error")
log.error("Givin' ...\nMultiline ...\nError ...")

class MyError(Exception):
    pass
log.throw(MyError("Givin' throw"))
'''

'''
with nullx.net.connect("mngmnt-iface.ctfcompetition.com", 1337) as conn:
    conn.receive_until(lambda data: "2) Read EULA/patch notes" in data.decode('utf-8'))
    conn.send("2\n")
    conn.recvall()
    tr = conn.traffic_recorder = nullx.net.TrafficRecorder()
    conn.send("../main\n")
    conn.recvall()
    open("binary.bin", "wb").write(tr.bytedata(tr.IN))
'''
