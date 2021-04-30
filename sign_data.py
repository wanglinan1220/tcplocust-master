import hashlib




data ={
      "useid":123123,
      "appid":1934342034809,
      "sid":234234234234
}
data =sorted(data.items(), key=lambda item:item[0])
for k,j in data:
      print(k,j)
data = [("%s"+"="+"%s")% (k,v) for k,v in data ]
data = ("&").join(data)
md5=hashlib.md5()
sign = md5.update(data.encode('UTF-8'))
sign=md5.hexdigest()
print(data)
