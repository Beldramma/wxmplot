# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 16:44:26 2020

@author: TonyTony
"""

#import numpy as np
#import pandas as pd
import datetime as dt
#import time
#import matplotlib.pyplot as plt
#import matplotlib.animation as animation
#import matplotlib.dates as dates
#from matplotlib.dates import DateFormatter
#import sys
#from matplotlib.backends.backend_wx import NavigationToolbar2Wx
import wx
import wxmplot.interactive as wi

def fill_data(pathname):
    t=[]
    # Creating an empty dictionary 
    Data = {} 
      # Adding list as value 
#    Data["voltage1"] = [] 
#    Data["voltage1"] = np.array(Data["voltage1"])
#    Data["voltage2"]=[]
#    Data["voltage2"] = np.array(Data["voltage2"])
#    Data["current1"]=[]
#    Data["current1"] = np.array(Data["current1"])
#    Data["current2"]=[]
#    Data["current2"] = np.array(Data["current2"])
#    Data["power1"]=[]
#    Data["power1"] = np.array(Data["power1"])
#    Data["power2"]=[]
#    Data["power2"] = np.array(Data["power2"])
    
    Data["voltage1"] = [] 
    Data["voltage2"]=[]
    Data["current1"]=[]
    Data["current2"]=[]
    Data["power1"]=[]
    Data["power2"]=[]
    
    # Fill Year, Month, Day with the filename in format YYMMDD.txt
    sDate = pathname.strip().split('\\')[-1]
    Year = sDate[0:2]
    Month = sDate[2:4]
    Day = sDate[4:6]
    Year = "20"+Year
    # Get back the pathname
    file_path = pathname.replace('\\', '/')
    
    print(file_path)
    with open(file_path) as file_obj: # we open the file (we don't need to use file.close(), it is automated)
        # split : delete characters in the string mentionned in paramater of split
        # strip: delete beginning and ending characters in parameter
        # file_obj.readline()#permit to jump this line
           for line in file_obj:
                hour, minute, second, volt1, cur1, pow1, volt2, cur2, pow2 = line.strip().split(',')
                #datetime_str="10:02:2020:"+hour+":"+minute+":"+second
                #time1 = time.mktime(dt.datetime.strptime(datetime_str, "%d:%m:%Y:%H:%M:%S").timetuple())
                #datetime_str=hour+":"+minute+":"+second
                #datetime_obj = dt.datetime.strptime(datetime_str, '%H:%M:%S')
                #time1 = dates.date2num(datetime_obj)
                #☺time1 = (3600*int(hour) + 60*int(minute) + int(second))
                #time1 = dt.datetime(2020,2,10,float(hour),float(minute),float(second))
                dt1 = dt.datetime(int(Year), int(Month), int(Day), int(hour), 
                                  int(minute),int(second))
                t.append(dt1)
                #t.append(time.mktime(dt1.timetuple()))
                #t.append(dates.date2num(dt1))
                #t = np.append(t,[time.time()-20, time.time()])
                volt1 = float(volt1)
                volt2 = float(volt2)
                cur1 = float(cur1)
                cur2 = float(cur2)
                pow1 = float(pow1)
                pow2 = float(pow2)
                Data["voltage1"].append(volt1)
                Data["voltage2"].append(volt2) 
                Data["current1"].append(cur1) 
                Data["current2"].append(cur2) 
                Data["power1"].append(pow1) 
                Data["power2"].append(pow2) 
#                Data["voltage1"] = np.append(Data["voltage1"], [volt1, volt1])
#                Data["voltage2"] = np.append(Data["voltage2"], [volt2, volt2]) 
#                Data["current1"] = np.append(Data["current1"], [cur1, cur1]) 
#                Data["current2"] = np.append(Data["current2"], [cur2, cur2]) 
#                Data["power1"] = np.append(Data["power1"], [pow1, pow1]) 
#                Data["power2"] = np.append(Data["power2"], [pow2, pow2])
                if 'str' in line:
                    break
    return t, Data

class OtherFrame(wx.Frame):
    """
    Class used for creating frames other than the main one
    """
    
    def __init__(self, title, pathname, parent=None):
        #wx.Frame.__init__(self, parent=parent, title=title)
        t, Data = fill_data(pathname)
        print(pathname)
        # Fill Year, Month, Day with the filename in format YYMMDD.txt
        sDate = pathname.strip().split('\\')[-1]
        Year = sDate[0:2]
        Month = sDate[2:4]
        Day = sDate[4:6]
        Year = "20"+Year
        date1 = Day +'/'+ Month + '/' + Year
        
        Window1 = wi.get_plot_window(win=1, wintitle = "USB Energetics spy:Voltage", theme = 'matplotlib')
        
#        self.toolbar = NavigationToolbar2Wx(Window1.panel.canvas)
#        self.toolbar.Realize()
#        # By adding toolbar in sizer, we are able to put it at the bottom
#        # of the frame - so appearance is closer to GTK version.
#        #self.sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)
#        # update the axes menu on the toolbar
#        self.toolbar.update()
        
        
        
        wi.plot(t, Data["voltage1"], label='voltage1 '+date1, marker='+', xlabel='Date', 
                ylabel='Voltage',title='Voltages:', show_legend=True, use_dates=True,
                new = True, win =1)
        wi.plot(t, Data["voltage2"], label='voltage2 '+date1,use_dates=True, win =1)
        
        wi.get_plot_window(win=2, wintitle = "USB Energetics spy:Current", theme = 'seaborn-whitegrid')
        
        wi.plot(t, Data["current1"], label='current1 '+date1, marker='+', xlabel='Date', 
                ylabel='Current',title='Currents:', show_legend=True, use_dates=True,
                new = True, win =2)
        wi.plot(t, Data["current2"], label='current2 '+date1,use_dates=True, win =2)
        
        wi.get_plot_window(win=3, wintitle = "USB Energetics spy:Power", theme = 'seaborn-white')
        wi.plot(t, Data["power1"], label='power1 '+date1, marker='+', xlabel='Date', 
                ylabel='Power', title='Powers:', show_legend=True, use_dates=True, 
                new = True, win =3)
        wi.plot(t, Data["power2"], label='power2 '+date1,use_dates=True, win =3)
        #self.Show()
class MyPanel(wx.Panel):
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        btn = wx.Button(self, label='Print Plots')
        btn.Bind(wx.EVT_BUTTON, self.OnSelect)
        self.frame_number = 1
        
    def OnSelect(self, event):
    
        # otherwise ask the user what new file to open
        with wx.FileDialog(self, "Select TXT file", wildcard="TXT files (*.txt)|*.txt",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
    
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind
    
            # Proceed loading the file chosen by the user
            pathname1 = fileDialog.GetPath()
            self.on_new_frame(pathname = pathname1)
            
        
        
    def on_new_frame(self,pathname):
        title = 'SubFrame {}'.format(self.frame_number)
        frame = OtherFrame(title=title, parent=wx.GetTopLevelParent(self), pathname = pathname)
        self.frame_number += 1
        
class MainFrame(wx.Frame):
    
    def __init__(self):
        wx.Frame.__init__(self, None, title='USB Energetics spy', size=(800, 600))
        panel = MyPanel(self)
        self.Show()
        
if __name__ == '__main__':
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()