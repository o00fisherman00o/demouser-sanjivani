import hashlib
  
# initializing string
def str2has(strin):
    str2hash = strin
    result = hashlib.md5(str2hash.encode())
    return (result.hexdigest())