from lib import Lib


core = Lib()
args = core.manarger()

if not args[0]:
    #Server
    port = args[1]
    type = args[2]
    core.runserver(port, type)
else:
    #Client
    host = args[0]
    port = args[1]
    type = args[2]
    core.runclient(host, port, type)
