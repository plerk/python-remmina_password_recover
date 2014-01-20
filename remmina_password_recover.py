import base64
# apt-get install python-crypto
from Crypto.Cipher import DES3
from os.path import expanduser, join
from os import listdir, walk
import re
import ConfigParser

dir = expanduser("~/.remmina/")

(_,_,files) = walk(dir).next()
files = filter(lambda x:re.search(r'\.remmina', x), files);

config = ConfigParser.ConfigParser()
config.read(expanduser("~/.remmina/remmina.pref"))
secret = base64.decodestring(config.get('remmina_pref','secret'))

crypt = DES3.new(secret[:24], DES3.MODE_CBC, secret[24:])

for file in files:
  try:
    config = ConfigParser.ConfigParser()
    config.read(join(dir, file))
    name = config.get('remmina', 'name')
    password = config.get('remmina', 'password')
    if password != '':
      password = base64.decodestring(password)
      password = crypt.decrypt(password)
      print name, ':', password
  except:
    pass
