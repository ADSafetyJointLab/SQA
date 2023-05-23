# 这是一个示例 Python 脚本。
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。


def readcsv(filenumber):
    # 在下面的代码行中使用断点来调试脚本。

    name=os.listdir(datapath)
    filename=name[filenumber-1]
    csvname=filename+'_tracks.csv'
    csvpath=os.path.join(datapath,filename,csvname)
    trackdata=pd.read_csv(csvpath)
    #datagroup=trackdata.groupby(trackdata.id)
   # carid = list(datagroup.groups.keys())
    return trackdata

def identifycartype(filenumber):#识别哪个是cutin车，哪个是HWP车
    name = os.listdir(datapath)
    filename = name[filenumber - 1]
    csvname = filename + '_tracksMeta.csv'
    csvpath=os.path.join(datapath,filename,csvname)
    trackdata=pd.read_csv(csvpath)
    try:
        cutid=list(trackdata[(trackdata.numLaneChanges>0)]['id'].values)
        if len(cutid)>1:
            cutid = int(trackdata[(trackdata.numLaneChanges > 0) & (trackdata.initialFrame == 0)]['id'].values)
    except:
        print("cutin error in filenumber"+str(filenumber))

    egoid=trackdata[trackdata.numLaneChanges==0]['id']
    if len(egoid)==0:
        egoid=trackdata[trackdata.initialFrame!=0]['id']
    if len(egoid)>1:
        for i in egoid:
            mindhw=int(trackdata[trackdata.id == i]['minDHW'])
            iniframe=int(trackdata[trackdata.id == i]['initialFrame'])
            if (mindhw!=-1) and (iniframe!=0):
                egocarid=i
                break
    else:
        try:
            egocarid =int(egoid.values)
        except:
            print("ego error in filenumber" + str(filenumber))
    return  egocarid,cutid

def dec_startpoint_identify():#提取HWP识别到cutin车，开始减速的时间点
    data=[]
    dataindex=[]
    idata=[]
    idataindex=[]
    for i in range(1,40):
        trackdata = readcsv(i)
        egoid, cutinid = identifycartype(i)
        iniitialframe=trackdata[trackdata.id==egoid].frame.values[0]
        startframe=trackdata[(trackdata.id ==egoid)&(trackdata.xAcceleration<-0.5)&(trackdata.frame>iniitialframe+50)]['frame'].values[0]
        dectrackdata=trackdata[(trackdata.id == egoid) & (startframe + 300 > trackdata.frame) & (trackdata.frame > startframe - 50)].reset_index(drop=True)
        data.extend(dectrackdata['xAcceleration'])
        dataindex.extend(dectrackdata['xAcceleration'].index)
        for j in range(49):
            if dectrackdata[(dectrackdata.id ==egoid)&(dectrackdata.index==50-j)]['xAcceleration'].values>dectrackdata[(dectrackdata.id ==egoid)&(dectrackdata.index==50-j-1)]['xAcceleration'].values:
                decframe=50-j
                break
            elif j==48:
                decframe=0
                break

        idata.extend(dectrackdata[(dectrackdata.id==egoid)&(dectrackdata.index==decframe)]['xAcceleration'])
        idataindex.extend(dectrackdata[(dectrackdata.id==egoid)&(dectrackdata.index==decframe)]['xAcceleration'].index)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=(10,6))
    plt.scatter(x=idataindex, y=idata, s=200, c='r', marker='+', alpha=1, zorder=2,label='减速起始点')
    plt.scatter(x=dataindex, y=data, s=10, zorder=1,label='加速度')
    plt.legend(loc='lower left',fontsize=30)
    plt.xlabel('帧[1/30 s]',fontsize=30)
    plt.ylabel('加速度[m/s^2]',fontsize=30)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)

def xacc_dhw_compare():
    trackdata = readcsv(56)
    xAcceleration = trackdata[trackdata.id == 153].xAcceleration.values[5:]
    dhw = trackdata[trackdata.id == 153].dhw.values[5:]
    plt.rcParams['font.sans-serif'] = ['SimHei'] #载入中文字体
    plt.rcParams['axes.unicode_minus'] = False#载入中文字体
    plt.figure(figsize=(5,10))
    plt.subplot(2,1,1)
    plt.plot(xAcceleration)
    plt.subplot(2,1,2)
    plt.plot(dhw)
    plt.show()

# 按间距中的绿色按钮以运行脚本。

if __name__ == '__main__':
    datapath="D:\paper\HWP_4stage_evaluate\data"
    #dec_startpoint_identify()
    xacc_dhw_compare()

    #print(name)

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
