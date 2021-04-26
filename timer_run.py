import os
import datetime,requests,json

class Add_Distribute(object):

      def __init__(self):
            pass

      def get_distribute(self):
            #推送
            url = "http://182.92.11.33/eiotapi/app/api/appDistribute"
            headers = {
                  "Content-Type": "application/json",
                  "Authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MjAwMjE5OTQsInVzZXJpZCI6MSwiaWF0IjoxNjE4MjIxOTk0LCJsb2dpbl91c2VyX2tleSI6ImQ2NDVkYmIyLTczZGUtNDdlZS05YTFlLTM0MTYyODNhNmEwYyJ9.AvVWRBj76gsNf-j1zK593R0xuykz1YFJspiP8rypPxs"
            }
            data = '''{"allowRepeat":1,
                   "groupIds":[{"id":38}],
                   "packageName":"com.ypcang.android.shop",
                   "version":20200623
                   }'''
            res= requests.request("post",url=url,headers=headers,data=data)
            print(res.json())

      def timerFun(self,sched_Timer):
            # 定时任务
            flag = 0
            print(sched_Timer)
            while True:
                  now = datetime.datetime.now().minute

                  if now==sched_Timer and flag==0:
                        print("--------------时间到了------------------")
                        self.get_distribute()
                        flag = 1


                  else:
                        if flag == 1:
                              sched_Timer = sched_Timer + 10

                              if sched_Timer>=60:
                                    sched_Timer=sched_Timer-60

                              flag = 0
# 2021-04-15 14:18:16.006666
# 2021-04-15 14:20:04.481714

if __name__ == "__main__":
      cs = Add_Distribute()
      sched_Timer = datetime.datetime.now().minute
      cs.timerFun(sched_Timer)
      print(sched_Timer)
