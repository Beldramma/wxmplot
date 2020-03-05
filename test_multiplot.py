# -*- coding: utf-8 -*-
#!/usr/bin/python
"""
Created on Tue Feb 18 15:32:00 2020

@author: TonyTony
"""

import datetime as dt
import wx
import wxmplot.interactive as wi
import wxmplot

def fill_data(pathname):
    t=[]
    # Creating an empty dictionary 
    Data = {} 
    
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
                dt1 = dt.datetime(int(Year), int(Month), int(Day), int(hour), 
                                  int(minute),int(second))
                t.append(dt1)
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
        
        pframe = wxmplot.MultiPlotFrame(parent = parent, rows=2, cols=3, panelsize=(350, 275))
        pframe.plot(t, Data["voltage1"], panel=(0, 0), labelfontsize=6)
        pframe.plot(t, Data["voltage2"], panel=(1, 0), color='red',  labelfontsize=6)
        pframe.plot(t, Data["current1"], panel=(0, 1), color='black', labelfontsize=5)
        pframe.plot(t, Data["current2"], panel=(1, 1), fullbox=False)
        pframe.plot(t, Data["power1"], panel=(0, 2), show_grid=False)
        pframe.plot(t, Data["power2"], panel=(1, 2))
        pframe.set_title('Voltage1', panel=(0, 0))
        pframe.set_title('Voltage2', panel=(1, 0))
        pframe.set_title('Current1', panel=(0, 1))
        pframe.set_title('Current2', panel=(1, 1))
        pframe.set_title('Power1', panel=(0, 2))
        pframe.set_title('Power2', panel=(1, 2))
        #pframe.set_xlabel(r' $ R  (\AA) $ ', panel=(0,2))
        pframe.Show()
        pframe.Raise()
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