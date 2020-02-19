#!/usr/bin/python
# coding: utf-8

import os
import time
import random
import wx
import json
import ConfigParser




class BaseConfig:
    """configure"""
    
    def __init__(self):

        self.mahjong_player_count = 0
        self.mahjong_banker_seat_id = 0
        self.mahjong_test_count = 0
        self.mahjong_total_count = 0
        self.heap_mahjong_datas = []
        self.player_mahjong_datas = []
        
    def Reset(self):
        
        self.mahjong_player_count = 0
        self.mahjong_banker_seat_id = 0
        self.mahjong_test_count = 0
        self.mahjong_total_count = 0
        self.heap_mahjong_datas = []
        self.player_mahjong_datas = []
        

    def Read(self, path):
        
        config = ConfigParser.ConfigParser()
        try:
            config.readfp(open(path,'r'))
        except:
            print "read error!"
            return False
        
        self.Reset()

        if config.has_section("Options"):

            if config.has_option("Options", "player_count"):
                self.mahjong_player_count = config.getint("Options", "player_count")
                
            if config.has_option("Options", "banker_seat_id"):
                self.mahjong_banker_seat_id = config.getint("Options", "banker_seat_id")
            
            if config.has_option("Options", "test_count"):
                self.mahjong_test_count = config.getint("Options", "test_count")
            
            if config.has_option("Options", "total_count"):
                self.mahjong_total_count = config.getint("Options", "total_count")                
            
        
        if config.has_section("MahjongDatas"):
         
            if config.has_option("MahjongDatas","heap_mahjong_datas"):
                mahjong_datas = config.get("MahjongDatas", "heap_mahjong_datas")
                mahjong_datas = mahjong_datas.split(",")
                
                for mahjong_data in mahjong_datas:
                    if len(mahjong_data) > 0:
                        self.heap_mahjong_datas.append(int(mahjong_data, 16))
            
            if self.mahjong_player_count > 0:
                for seat_id in range(self.mahjong_player_count):
                    if config.has_option("MahjongDatas", "player_mahjong_datas%d"%(seat_id)):
                        mahjong_datas = config.get("MahjongDatas", "player_mahjong_datas%d"%(seat_id))
                        mahjong_datas = mahjong_datas.split(",")
                        
                        player_mahjong_datas = []
                        for mahjong_data in mahjong_datas:
                            if len(mahjong_data) > 0:
                                player_mahjong_datas.append(int(mahjong_data, 16))
                            
                        self.player_mahjong_datas.append(player_mahjong_datas)
                
            
        return True
    
    

    def Write(self, path):
        
        config = ConfigParser.ConfigParser()
        if not config.has_section("Options"):
            config.add_section("Options")

        if not config.has_section("MahjongDatas"):
            config.add_section("MahjongDatas")
            
        config.set("Options", "player_count", self.mahjong_player_count)
        config.set("Options", "banker_seat_id", self.mahjong_banker_seat_id)
        config.set("Options", "test_count", self.mahjong_test_count)
        config.set("Options", "total_count", self.mahjong_total_count)
        
        heap_mahjong_datas = []
        for mahjong_data in self.heap_mahjong_datas:
            heap_mahjong_datas.append("0x{:0>2X}".format(mahjong_data))
        heap_mahjong_datas = ",".join(heap_mahjong_datas)
        config.set("MahjongDatas", "heap_mahjong_datas", heap_mahjong_datas)
        
        if self.mahjong_player_count > 0:
            for seat_id in range(self.mahjong_player_count):
                if seat_id < len(self.player_mahjong_datas):
                    one_player_mahjong_datas = self.player_mahjong_datas[seat_id]
                    if len(one_player_mahjong_datas) > 0:
                        mahjong_datas = []
                        for mahjong_data in one_player_mahjong_datas:
                            mahjong_datas.append("0x{:0>2X}".format(mahjong_data))
                        one_player_mahjong_datas = ",".join(mahjong_datas)
                        config.set("MahjongDatas", "player_mahjong_datas%d"%(seat_id), one_player_mahjong_datas)

        try:
            config.write(open(path, 'w'))
        except:
            print "wirte error!"
            return False
        
        return True
    

class MahjongConfig(BaseConfig):

    def __init__(self):
        
        BaseConfig.__init__(self)
        
    def ReadJson(self, path):
    
        try:
            fp = open(path, 'r')
        except:
            print("open json file error!")
            return False
        
        self.Reset()
        
        config = {}
        with fp:
            try:
                check_bom = fp.read(3)
                if check_bom == '\xef\xbb\xbf':
                    fp.seek(3)
                else:
                    fp.seek(0)
                config = json.load(fp, "utf-8")
            except BaseException as err:
                print("json read error",err)
                return False, err
            
            
        if type(config) == type({}) and len(config) > 0:
            if config.has_key("Options"):
                
                if config["Options"].has_key("player_count"):
                    self.mahjong_player_count = config["Options"]["player_count"]
                
                if config["Options"].has_key("banker_seat_id"):
                    self.mahjong_banker_seat_id = config["Options"]["banker_seat_id"]
                    
                if config["Options"].has_key("test_count"):
                    self.mahjong_test_count = config["Options"]["test_count"]
                    
                if config["Options"].has_key("total_count"):
                    self.mahjong_total_count = config["Options"]["total_count"]                        
                
            if config.has_key("MahjongDatas"):
                
                if config["MahjongDatas"].has_key("heap_mahjong_datas"):
                    mahjong_datas = config["MahjongDatas"]["heap_mahjong_datas"]
                    mahjong_datas = mahjong_datas.split(",")
                    
                    for mahjong_data in mahjong_datas:
                        if len(mahjong_data) > 0:                       
                            self.heap_mahjong_datas.append(int(mahjong_data, 16))   
                        
                if config["MahjongDatas"].has_key("player_mahjong_datas") and len(config["MahjongDatas"]["heap_mahjong_datas"]) > 0:
                    if self.mahjong_player_count > 0:
                        for seat_id in range(self.mahjong_player_count):
                            if seat_id < len(config["MahjongDatas"]["heap_mahjong_datas"]):     
                                mahjong_datas = config["MahjongDatas"]["heap_mahjong_datas"][seat_id]
                                mahjong_datas = mahjong_datas.split(",")
                            
                                player_mahjong_datas = []
                                for mahjong_data in mahjong_datas:
                                    if len(mahjong_data) > 0:
                                        player_mahjong_datas.append(int(mahjong_data, 16))
                                    
                                self.player_mahjong_datas.append(player_mahjong_datas)                
    
        return True
    
    def WriteJson(self, path):
        
        heap_mahjong_datas = []
        for mahjong_data in self.heap_mahjong_datas:
            heap_mahjong_datas.append("0x{:0>2X}".format(mahjong_data))
        heap_mahjong_datas = ",".join(heap_mahjong_datas)
            
        player_mahjong_datas = []
        if self.mahjong_player_count > 0:
            for seat_id in range(self.mahjong_player_count):
                if seat_id < len(self.player_mahjong_datas):            
                    one_player_mahjong_datas = self.player_mahjong_datas[seat_id]
                    if len(one_player_mahjong_datas) > 0:
                        mahjong_datas = []
                        for mahjong_data in one_player_mahjong_datas:
                            mahjong_datas.append("0x{:0>2X}".format(mahjong_data))
                        one_player_mahjong_datas = ",".join(mahjong_datas)
                        player_mahjong_datas.append(one_player_mahjong_datas)
            
        config = { 
            "Options" : {
                "player_count" : self.mahjong_player_count,
                "banker_seat_id" : self.mahjong_banker_seat_id,
                "test_count" : self.mahjong_test_count,
                "total_count" : self.mahjong_total_count            
            }, 
            "MahjongDatas" : {
                "heap_mahjong_datas" : heap_mahjong_datas,
                "player_mahjong_datas" : player_mahjong_datas
            } 
        }
        
        try:
            fp = open(path, 'w')
        except:
            print("open json file error!")
            return False
            
        with fp:
            try:
                json.dump(config, fp, indent=4, separators=(',',': '))
            except BaseException as err:
                print("json write error", err)
                return False, err
                
        return True    
    
        
#----------------------------------------------------------------------

class DragShape:
    
    def __init__(self, bmp = None):
        
        self.pos = wx.Point()
        self.shown = True
        self.fullscreen = False
        self.bmp = None
        
    def SetBitmap(self, bmp):
        
        self.bmp = bmp
        
    def SetPos(self, pt):
        
        self.pos = pt
        
    def GetPos(self):
        
        return self.pos
    
    def GetPosX(self):
        
        return self.pos.x
    
    def GetPosY(self):
        
        return self.pos.y
    
    def GetWidth(self):
        
        return self.GetRect().GetWidth()
    
    def GetHeight(self):
        
        return self.GetRect().GetHeight()
    

    def HitTest(self, pt):
        
        rect = self.GetRect()
        return rect.InsideXY(pt.x, pt.y)

    def GetRect(self):
        
        if self.bmp == None:
            return wx.Rect(self.pos.x, self.pos.y, 1, 1)
        
        return wx.Rect(self.pos.x, self.pos.y, self.bmp.GetWidth(), self.bmp.GetHeight())

    def Draw(self, dc, op = wx.COPY):
        
        if self.bmp != None and self.bmp.Ok():
            memDC = wx.MemoryDC()
            memDC.SelectObject(self.bmp)

            dc.Blit(self.pos.x, self.pos.y,
                    self.bmp.GetWidth(), self.bmp.GetHeight(),
                    memDC, 0, 0, op, True)

            return True
        else:
            return False



MAHJONG_MAX_INDEX = 9 + 9 + 9 + 7 + 8
MAHJONG_MASK_COLOR = 0xF0
MAHJONG_MASK_VALUE = 0x0F

MahjongType_Unknow = 0
MahjongType_Heap = 1
MahjongType_Left = 2
MahjongType_Top = 3
MahjongType_Right = 4
MahjongType_Bottom = 5



class DragMahjong(DragShape):
    
    def __init__(self, mahjong_data, mahjong_type = MahjongType_Unknow):
        
        DragShape.__init__(self)
        
        self.fullscreen = True
        self.mahjong_data = 0
        self.mahjong_type = mahjong_type
        self.SetMahjongData(mahjong_data)
        
    def  GetMahjongData(self):
        
        return self.mahjong_data
        
    def GetMahjongType(self):
        
        return self.mahjong_type
        
    def SetMahjongData(self, mahjong_data):
        
        try:
            self._SetMahjongImage(mahjong_data)
        except:
            print("set mahjong image exception!")
            
        self.mahjong_data = mahjong_data
        
        
    def _SetMahjongImage(self, mahjong_data):
        
        assert(False)
        pass
        

# 牌堆麻将        
class HeapMahjong(DragMahjong):
    
    def __init__(self, mahjong_data):
        
        DragMahjong.__init__(self, mahjong_data, MahjongType_Heap)
        

    def _SetMahjongImage(self, mahjong_data):
        
        if self.mahjong_data == mahjong_data:
            return 
        
        if mahjong_data == 0:
            self.SetBitmap(None)
            return
        
        color = (((mahjong_data & MAHJONG_MASK_COLOR) >> 4) & 0xFF)
        value = ((mahjong_data & MAHJONG_MASK_VALUE) & 0xFF)
        file_name = 'mj.png'
        if color == 0 :
            file_name = "mj_w_%d_t" % (value)
        elif color == 1: 
            file_name = "mj_tiao_%d_t" % (value)
        elif color == 2:
            file_name = "mj_tong_%d_t" % (value)
        elif color == 3:
            if value <= 7 :
                file_name = "mj_%02x_t" % (mahjong_data)
            else:
                file_name = "mj_h_%d_t" % (value - 7)
        
        mahjong_img = wx.Bitmap('images/mj_top/%s.png' % (file_name))
        mahjong_bg = wx.Bitmap('images/mj_bg/mj_small_bg_t.png') 
        
        mahjong_bmp = wx.EmptyBitmapRGBA(mahjong_bg.GetWidth(), mahjong_bg.GetHeight())
        memDC = wx.MemoryDC()
        memDC.SelectObject(mahjong_bmp)  
        
        mahjong_img = mahjong_img.ConvertToImage().Scale(mahjong_bg.GetWidth() - 8, mahjong_bg.GetHeight() - 20)
        mahjong_img = mahjong_img.ConvertToBitmap()        
        memDC.DrawBitmap(mahjong_bg, 0, 0, True)
        memDC.DrawBitmap(mahjong_img, (mahjong_bg.GetWidth()-mahjong_img.GetWidth()) / 2, 0, True)             
        self.SetBitmap(mahjong_bmp)        
    
         
# 左边麻将    
class LeftMahjong(DragMahjong):
    
    def __init__(self, mahjong_data):
        
        DragMahjong.__init__(self, mahjong_data, MahjongType_Left)
    
        
    def _SetMahjongImage(self, mahjong_data):     
    
        if self.mahjong_data == mahjong_data:
            return 
        
        if mahjong_data == 0:
            self.SetBitmap(None)
            return
        
        color = (((mahjong_data & MAHJONG_MASK_COLOR) >> 4) & 0xFF)
        value = ((mahjong_data & MAHJONG_MASK_VALUE) & 0xFF)
        file_name = 'mj.png'
        if color == 0 :
            file_name = "mj_w_%d_l" % (value)
        elif color == 1: 
            file_name = "mj_tiao_%d_l" % (value)
        elif color == 2:
            file_name = "mj_tong_%d_l" % (value)
        elif color == 3:
            if value <= 7 :
                file_name = "mj_%02x_l" % (mahjong_data)
            else:
                file_name = "mj_h_%d_l" % (value - 7)
            
        mahjong_img = wx.Bitmap('images/mj_left/%s.png' % (file_name))     
        mahjong_bg = wx.Bitmap('images/mj_bg/mj_small_bg_l.png')
        
        mahjong_bmp = wx.EmptyBitmapRGBA(mahjong_bg.GetWidth(), mahjong_bg.GetHeight())
        memDC = wx.MemoryDC()
        memDC.SelectObject(mahjong_bmp)  
        memDC.DrawBitmap(mahjong_bg, 0, 0, True)
        memDC.DrawBitmap(mahjong_img, (mahjong_bg.GetWidth()-mahjong_img.GetWidth()) / 2, 6, True)  
        self.SetBitmap(mahjong_bmp)
        
        
# 上面麻将
class TopMahjong(DragMahjong):
    
    def __init__(self, mahjong_data):
        
        DragMahjong.__init__(self, mahjong_data, MahjongType_Top)
        
        
    def _SetMahjongImage(self, mahjong_data):   
        
        if self.mahjong_data == mahjong_data:
            return 
        
        if mahjong_data == 0:
            self.SetBitmap(None)
            return
        
        color = (((mahjong_data & MAHJONG_MASK_COLOR) >> 4) & 0xFF)
        value = ((mahjong_data & MAHJONG_MASK_VALUE) & 0xFF)
        file_name = 'mj.png'
        if color == 0 :
            file_name = "mj_w_%d_t" % (value)
        elif color == 1: 
            file_name = "mj_tiao_%d_t" % (value)
        elif color == 2:
            file_name = "mj_tong_%d_t" % (value)
        elif color == 3:
            if value <= 7 :
                file_name = "mj_%02x_t" % (mahjong_data)
            else:
                file_name = "mj_h_%d_t" % (value - 7)
            
        mahjong_img = wx.Bitmap('images/mj_top/%s.png' % (file_name))
        mahjong_bg = wx.Bitmap('images/mj_bg/mj_small_bg_t.png')
        
        mahjong_bmp = wx.EmptyBitmapRGBA(mahjong_bg.GetWidth(), mahjong_bg.GetHeight())
        memDC = wx.MemoryDC()
        memDC.SelectObject(mahjong_bmp)  
        
        mahjong_img = mahjong_img.ConvertToImage().Scale(mahjong_bg.GetWidth() - 8, mahjong_bg.GetHeight() - 20)
        mahjong_img = mahjong_img.ConvertToBitmap()        
        memDC.DrawBitmap(mahjong_bg, 0, 0, True)
        memDC.DrawBitmap(mahjong_img, (mahjong_bg.GetWidth()-mahjong_img.GetWidth()) / 2, 0, True)             
        self.SetBitmap(mahjong_bmp)
        
         
# 右边麻将  
class RightMahjong(DragMahjong):
    
    def __init__(self, mahjong_data):
        
        DragMahjong.__init__(self, mahjong_data, MahjongType_Right)
    
        
    def _SetMahjongImage(self, mahjong_data):   
        
        if self.mahjong_data == mahjong_data:
            return 
        
        if mahjong_data == 0:
            self.SetBitmap(None)
            return
        
        color = (((mahjong_data & MAHJONG_MASK_COLOR) >> 4) & 0xFF)
        value = ((mahjong_data & MAHJONG_MASK_VALUE) & 0xFF)
        file_name = 'mj.png'
        if color == 0 :
            file_name = "mj_w_%d_r" % (value)
        elif color == 1: 
            file_name = "mj_tiao_%d_r" % (value)
        elif color == 2:
            file_name = "mj_tong_%d_r" % (value)
        elif color == 3:
            if value <= 7 :
                file_name = "mj_%02x_r" % (mahjong_data)
            else:
                file_name = "mj_h_%d_r" % (value - 7)
            
        mahjong_img = wx.Bitmap('images/mj_right/%s.png' % (file_name))
        mahjong_bg = wx.Bitmap('images/mj_bg/mj_small_bg_r.png')
        
        mahjong_bmp = wx.EmptyBitmapRGBA(mahjong_bg.GetWidth(), mahjong_bg.GetHeight())
        memDC = wx.MemoryDC()
        memDC.SelectObject(mahjong_bmp)  
        memDC.DrawBitmap(mahjong_bg, 0, 0, True)
        memDC.DrawBitmap(mahjong_img, (mahjong_bg.GetWidth()-mahjong_img.GetWidth()) / 2, 6, True)   
        self.SetBitmap(mahjong_bmp)
        
      
# 底部麻将   
class BottomMahjong(DragMahjong):
    
    def __init__(self, mahjong_data):
        
        DragMahjong.__init__(self, mahjong_data, MahjongType_Bottom)
        
        
    def _SetMahjongImage(self, mahjong_data):   
        
        if self.mahjong_data == mahjong_data:
            return 
        
        if mahjong_data == 0:
            self.SetBitmap(None)
            return
        
        color = (((mahjong_data & MAHJONG_MASK_COLOR) >> 4) & 0xFF)
        value = ((mahjong_data & MAHJONG_MASK_VALUE) & 0xFF)
        file_name = 'mj.png'
        if color == 0 :
            file_name = "mj_w_%d" % (value)
        elif color == 1: 
            file_name = "mj_tiao_%d" % (value)
        elif color == 2:
            file_name = "mj_tong_%d" % (value)
        elif color == 3:
            if value <= 7 :
                file_name = "mj_%02x" % (mahjong_data)
            else:
                file_name = "mj_h_%d" % (value - 7)
            
        mahjong_img = wx.Bitmap('images/mj_bottom/%s.png' % (file_name))
        mahjong_bg = wx.Bitmap('images/mj_bg/mj_hand_bg.png')
        
        mahjong_bmp = wx.EmptyBitmapRGBA(mahjong_bg.GetWidth(), mahjong_bg.GetHeight())
        memDC = wx.MemoryDC()
        memDC.SelectObject(mahjong_bmp)         
        memDC.DrawBitmap(mahjong_bg, 0, 0, True)
        memDC.DrawBitmap(mahjong_img, (mahjong_bg.GetWidth()-mahjong_img.GetWidth()) / 2, 28, True)     
        
        mahjong_bmp = mahjong_bmp.ConvertToImage().Scale(mahjong_bmp.GetWidth() - 18, mahjong_bmp.GetHeight() - 30)
        mahjong_bmp = mahjong_bmp.ConvertToBitmap()  
        self.SetBitmap(mahjong_bmp)
 
 
SeatDirection_Left = 0
SeatDirection_Top = 1
SeatDirection_Right = 2
SeatDirection_Bottom = 3


# 堆立麻将
class PlaneHeapMahjong:
    
    def __init__(self, parent, mahjong_datas = []):
        
        self.parent = parent
        self.layout_mode = wx.ALIGN_INVALID
        self.view_rect = wx.Rect()     
        self.display_col_count = 16
        self.mahjong_views = []
        
        self.InitMahjongView(mahjong_datas)
    
    
    def SetHandMahjongs(self, mahjong_datas):

        if len(mahjong_datas) == len(self.mahjong_views):

            for index in len(mahjong_datas):
                mahjong_data = mahjong_datas[index]
                self.mahjong_views[index].SetMahjongData(mahjong_data) 

            return True

        return False

    def SetHandMahJong(self, index, mahjong_data):

        if index < len(self.mahjong_views):
            self.mahjong_views[index].SetMahjongData(mahjong_data) 
            return True

        return False

    def GetHandMahjongs(self):

        mahjong_datas = []
        for mahjong_view in self.mahjong_views:
            data = mahjong_view.GetMahjongData()
            mahjong_datas.append(data)

        return mahjong_datas


    def GetHandMahjong(self, index):

        mahjong_data = 0
        if index < len(self.mahjong_views):
            mahjong_data = self.mahjong_views[index].GetMahjongData()

        return mahjong_data

    def InitMahjongView(self, mahjong_datas):

        for mahjong_data in mahjong_datas:
            mahjong_view = HeapMahjong(mahjong_data)
            self.mahjong_views.append(mahjong_view) 
            self.parent.shapes.append(mahjong_view)  

        self.UpdateView()
        
            
    def SetPosition(self, pt, mode = None):
        
        self.view_rect.SetPosition(pt)
        self.layout_mode = mode or self.layout_mode
        self.UpdateView()
        

    def UpdateView(self):

        x = self.view_rect.GetX()
        y = self.view_rect.GetY()
        h_space = -5
        v_space = -20
        x_count = 0
        y_count = 0
        for mahjong_view in self.mahjong_views:
            mahjong_view.SetPos(wx.Point(x + x_count * (mahjong_view.GetWidth() + h_space), y + y_count * (mahjong_view.GetHeight() + v_space)))
            self.view_rect = self.view_rect.Union(mahjong_view.GetRect())
            x_count += 1
            if x_count >= self.display_col_count:
                x_count = 0
                y_count += 1


            
   
# 手上麻将
class HandMahjong:
    
    def __init__(self, parent, seat_id, seat_direction, mahjong_datas = []):
        
        self.parent = parent
        self.seat_id = seat_id
        self.seat_direction = seat_direction 
        self.layout_mode = wx.ALIGN_INVALID
        self.view_rect = wx.Rect()
        self.mahjong_views = []
             
        self.InitMahjongView(mahjong_datas)
            
    
    def SetHandMahjongs(self, mahjong_datas):
        
        if len(mahjong_datas) == len(self.mahjong_views):
            
            for index in len(mahjong_datas):
                mahjong_data = mahjong_datas[index]
                self.mahjong_views[index].SetMahjongData(mahjong_data) 
            
            return True
        
        return False
        
    def SetHandMahJong(self, index, mahjong_data):
        
        if index < len(self.mahjong_views):
            self.mahjong_views[index].SetMahjongData(mahjong_data) 
            return True
        
        return False
    
    def GetHandMahjongs(self):
        
        mahjong_datas = []
        for mahjong_view in self.mahjong_views:
            data = mahjong_view.GetMahjongData()
            mahjong_datas.append(data)
            
        return mahjong_datas
    
    
    def GetHandMahjong(self, index):
        
        mahjong_data = 0
        if index < len(self.mahjong_views):
            mahjong_data = self.mahjong_views[index].GetMahjongData()
            
        return mahjong_data
    
    def InitMahjongView(self, mahjong_datas):
        
        if self.seat_direction == SeatDirection_Left:
            self.InitLeftMahjongView(mahjong_datas)
        elif self.seat_direction == SeatDirection_Top:
            self.InitTopMahjongView(mahjong_datas)
        elif self.seat_direction == SeatDirection_Right:
            self.InitRightMahjongView(mahjong_datas)
        else:
            self.InitBottomMahjongView(mahjong_datas)
            
        self.UpdateView()
            
    
    def InitLeftMahjongView(self, mahjong_datas):
        
        for mahjong_data in mahjong_datas:
            mahjong_view = LeftMahjong(mahjong_data)
            self.mahjong_views.append(mahjong_view) 
            self.parent.shapes.append(mahjong_view)  
            
        
    def InitTopMahjongView(self, mahjong_datas):                    
                   
        for mahjong_data in mahjong_datas:
            mahjong_view = TopMahjong(mahjong_data)
            self.mahjong_views.append(mahjong_view) 
            self.parent.shapes.append(mahjong_view)  
                
                
    def InitRightMahjongView(self, mahjong_datas):
     
        for mahjong_data in mahjong_datas:
            mahjong_view = RightMahjong(mahjong_data)
            self.mahjong_views.append(mahjong_view) 
            self.parent.shapes.append(mahjong_view)  
        
                
    def InitBottomMahjongView(self, mahjong_datas):
        
        for mahjong_data in mahjong_datas:
            mahjong_view = BottomMahjong(mahjong_data)
            self.mahjong_views.append(mahjong_view) 
            self.parent.shapes.append(mahjong_view)      
     
            
    def SetPosition(self, pt, mode = None):
        
        self.view_rect.SetPosition(pt)
        self.layout_mode = mode or self.layout_mode
        self.UpdateView()
                
    def UpdateView(self):
       
        if self.seat_direction == SeatDirection_Left:
            self.UpdateLeftMahjongView()
        elif self.seat_direction == SeatDirection_Top:
            self.UpdateTopMahjongView()
        elif self.seat_direction == SeatDirection_Right:
            self.UpdateRightMahjongView()
        else:
            self.UpdateBottomMahjongView() 
            
        self.parent.RefreshRect(self.view_rect)
        
        
    def UpdateLeftMahjongView(self):
        
        x = self.view_rect.GetX()
        y = self.view_rect.GetY()
        v_space = -20
        count = 0
        for mahjong_view in self.mahjong_views:
            mahjong_view.SetPos(wx.Point(x, y + count * (mahjong_view.GetHeight() + v_space)))
            self.view_rect = self.view_rect.Union(mahjong_view.GetRect())
            count += 1
            
        
    def UpdateTopMahjongView(self):                    
            
        x = self.view_rect.GetX()
        y = self.view_rect.GetY()
        h_space = -5  
        count = 0
        for mahjong_view in self.mahjong_views:
            mahjong_view.SetPos(wx.Point(x + count * (mahjong_view.GetWidth() + h_space), y))
            self.view_rect = self.view_rect.Union(mahjong_view.GetRect())
            count += 1
                
                
    def UpdateRightMahjongView(self):
     
        x = self.view_rect.GetX()
        y = self.view_rect.GetY()
        v_space = -20
        count = 0
        for mahjong_view in self.mahjong_views:
            mahjong_view.SetPos(wx.Point(x, y + count * (mahjong_view.GetHeight() + v_space)))
            self.view_rect = self.view_rect.Union(mahjong_view.GetRect())
            count += 1
        
                
    def UpdateBottomMahjongView(self):   
        
        x = self.view_rect.GetX()
        y = self.view_rect.GetY()
        h_space = 0  
        count = 0
        for mahjong_view in self.mahjong_views:
            mahjong_view.SetPos(wx.Point(x + count * (mahjong_view.GetWidth() + h_space), y))
            self.view_rect = self.view_rect.Union(mahjong_view.GetRect())
            count += 1      

#----------------------------------------------------------------------

class DragCanvas(wx.ScrolledWindow):
    
    def __init__(self, parent, ID = -1):
        
        wx.ScrolledWindow.__init__(self, parent, ID)
        
        self.parent = parent
        self.shapes = []
        self.dragImage = None
        self.dragShape = None
        self.hiliteShape = None  

        self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
        self.SetBackgroundStyle(wx.BG_STYLE_ERASE)       
        #self.SetBackgroundColour(wx.Colour(255,255,255))
        
        self.bg_bmp = wx.Bitmap('images/mj_bg/sc_room_bg.jpg')
        self.bg_bmp2 = None

        # Make a shape from an image and mask.  This one will demo
        # dragging outside the window
        self.InitMahjong()
        
        # add event
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        
        
    def InitMahjong(self):
        
        config = self.parent.config

        self.plane_heap_mahjong = PlaneHeapMahjong(self, config.heap_mahjong_datas)
        self.hand_mahjong_ctrls = []
        if config.mahjong_player_count > 0:
            for seat_id in range(config.mahjong_player_count): 
                player_mahjong_datas = []
                if seat_id < len(config.player_mahjong_datas):   
                    if seat_id == 0:
                        seat_direction = SeatDirection_Top
                        player_mahjong_datas = config.player_mahjong_datas[seat_id]
                    elif seat_id == 1:
                        seat_direction = SeatDirection_Left
                        player_mahjong_datas = config.player_mahjong_datas[seat_id]                
                    elif seat_id == 2:
                        seat_direction = SeatDirection_Right
                        player_mahjong_datas = config.player_mahjong_datas[seat_id]                
                    elif seat_id == 3:
                        seat_direction = SeatDirection_Bottom
                        player_mahjong_datas = config.player_mahjong_datas[seat_id]
                    else:
                        continue
                
                hand_mahjong = HandMahjong(self, seat_id, seat_direction, player_mahjong_datas)
                self.hand_mahjong_ctrls.append(hand_mahjong)

    
    def AdjustMahjongDatas(self, mahjong_datas):
        
        config = self.parent.config
        
        if len(mahjong_datas) > 0:
            random.shuffle(mahjong_datas)
        
        config.heap_mahjong_datas = []
        config.player_mahjong_datas = []
        if config.mahjong_player_count > 0:
            
            for seat_id in range(config.mahjong_player_count):
                mahjong_count = 13 if seat_id != config.mahjong_banker_seat_id else 14
                if len(mahjong_datas) >= mahjong_count: 
                    player_mahjong_datas = mahjong_datas[0 : mahjong_count]
                    del mahjong_datas[0 : mahjong_count]
                    config.player_mahjong_datas.append(player_mahjong_datas)
                
        if len(mahjong_datas) > 0:
            for mahjong_data in mahjong_datas:
                config.heap_mahjong_datas.append(mahjong_data)
                
    
    def UpdateMahjongView(self):
        
        pass    
    
        
    # window size
    def OnSize(self, evt):
        
        size = self.GetClientSize()
        if size.width != 0 and size.height != 0 :
            image = self.bg_bmp.ConvertToImage().Scale(size.width, size.height)
            self.bg_bmp2 = image.ConvertToBitmap()
         
        self.Refresh()

    # We're not doing anything here, but you might have reason to.
    # for example, if you were dragging something, you might elect to
    # 'drop it' when the cursor left the window.
    def OnLeaveWindow(self, evt):
        pass


    # tile the background bitmap
    def TileBackground(self, dc):
        sz = self.GetClientSize()
        w = self.bg_bmp.GetWidth()
        h = self.bg_bmp.GetHeight()
        x = 0
        
        if self.bg_bmp2 == None:
            image = self.bg_bmp.ConvertToImage().Scale(sz.width,sz.height)
            self.bg_bmp2 = image.ConvertToBitmap()
        
        if self.bg_bmp2 != None:
            dc.DrawBitmap(self.bg_bmp2, 0, 0)


    # Go through our list of shapes and draw them in whatever place they are.
    def DrawShapes(self, dc):
        
        for shape in self.shapes:
            if shape.shown:
                shape.Draw(dc)

    # This is actually a sophisticated 'hit test', but in this
    # case we're also determining which shape, if any, was 'hit'.
    def FindShape(self, pt):
        
        for shape in self.shapes:
            if shape.HitTest(pt):
                return shape
            
        return None


    # Clears the background, then redraws it. If the DC is passed, then
    # we only do so in the area so designated. Otherwise, it's the whole thing.
    def OnEraseBackground(self, evt):
        dc = evt.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        self.TileBackground(dc)

    # Fired whenever a paint event occurs
    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        self.PrepareDC(dc)
        self.DrawShapes(dc)

    # Left mouse button is down.
    def OnLeftDown(self, evt):

        shape = self.FindShape(evt.GetPosition())
        if shape:
            self.dragShape = shape
            self.dragStartPos = evt.GetPosition()

    # Left mouse button up.
    def OnLeftUp(self, evt):
        if not self.dragImage or not self.dragShape:
            self.dragImage = None
            self.dragShape = None
            return

        # Hide the image, end dragging, and nuke out the drag image.
        self.dragImage.Hide()
        self.dragImage.EndDrag()
        self.dragImage = None

        if self.hiliteShape:
            self.RefreshRect(self.hiliteShape.GetRect())
            self.hiliteShape = None
            

        shape = self.FindShape(evt.GetPosition())
        if shape:        
            mahjong_data1 = shape.GetMahjongData()
            mahjong_data2 = self.dragShape.GetMahjongData()
            shape.SetMahjongData(mahjong_data2)
            self.dragShape.SetMahjongData(mahjong_data1)
    
            self.dragShape.shown = True      
            self.RefreshRect(shape.GetRect())
            self.RefreshRect(self.dragShape.GetRect())
            self.Refresh()
            self.dragShape = None            
        else:
            self.dragShape.shown = True
            self.RefreshRect(self.dragShape.GetRect())
            self.dragShape = None


    # The mouse is moving
    def OnMotion(self, evt):
        # Ignore mouse movement if we're not dragging.
        if not self.dragShape or not evt.Dragging() or not evt.LeftIsDown():
            return

        # if we have a shape, but haven't started dragging yet
        if self.dragShape and not self.dragImage:

            # only start the drag after having moved a couple pixels
            tolerance = 2
            pt = evt.GetPosition()
            dx = abs(pt.x - self.dragStartPos.x)
            dy = abs(pt.y - self.dragStartPos.y)
            if dx <= tolerance and dy <= tolerance:
                return

            # refresh the area of the window where the shape was so it
            # will get erased.
            self.dragShape.shown = False
            self.RefreshRect(self.dragShape.GetRect(), True)
            self.Update()

            self.dragImage = wx.DragImage(self.dragShape.bmp,
                                              wx.StockCursor(wx.CURSOR_HAND))
            
            hotspot = self.dragStartPos - self.dragShape.pos
            self.dragImage.BeginDrag(hotspot, self, self.dragShape.fullscreen)

            self.dragImage.Move(pt)
            self.dragImage.Show()


        # if we have shape and image then move it, posibly highlighting another shape.
        elif self.dragShape and self.dragImage:
            onShape = self.FindShape(evt.GetPosition())
            unhiliteOld = False
            hiliteNew = False

            # figure out what to hilite and what to unhilite
            if self.hiliteShape:
                if onShape is None or self.hiliteShape is not onShape:
                    unhiliteOld = True

            if onShape and onShape is not self.hiliteShape and onShape.shown:
                hiliteNew = True

            # if needed, hide the drag image so we can update the window
            if unhiliteOld or hiliteNew:
                self.dragImage.Hide()

            if unhiliteOld:
                dc = wx.ClientDC(self)
                self.hiliteShape.Draw(dc)
                self.hiliteShape = None

            if hiliteNew:
                dc = wx.ClientDC(self)
                self.hiliteShape = onShape
                self.hiliteShape.Draw(dc, wx.INVERT)

            # now move it and show it again if needed
            self.dragImage.Move(evt.GetPosition())
            if unhiliteOld or hiliteNew:
                self.dragImage.Show()

    
    
class MahjongSettingDlg(wx.Dialog):
    
    def __init__(self, parent = None, id = -1,):
        
        wx.Dialog.__init__(self, parent, id, title=u"麻将设置", size=(640, 530))
        
        self.parent = parent
        self.panel = wx.Panel(self)
        frame_sizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.panel.SetSizer(frame_sizer)        
        
        static_box = wx.StaticBox(self.panel, label=u"麻将游戏配置：")
        static_box_sizer = wx.StaticBoxSizer(static_box, orient=wx.HORIZONTAL)
        frame_sizer.Add(static_box_sizer, 1, wx.LEFT|wx.RIGHT|wx.EXPAND, 6)
        
        label_mahjong_total_count = wx.StaticText(static_box, label = u"麻将总数目：")
        self.spin_mahjong_total_count = wx.SpinCtrl(static_box, value='136', size=(60,-1))    
        self.spin_mahjong_total_count.SetRange(0, 168)
        self.spin_mahjong_total_count.SetValue(136)
        self.spin_mahjong_total_count.Disable()
        static_box_sizer.Add(label_mahjong_total_count, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 6)
        static_box_sizer.Add(self.spin_mahjong_total_count, 0, wx.ALIGN_CENTER_VERTICAL)
        static_box_sizer.AddSpacer(18)
        
        label_mahjong_player_count = wx.StaticText(static_box, label = u"游戏人数：")
        self.spin_mahjong_player_count = wx.SpinCtrl(static_box, value='4', size=(60,-1))    
        self.spin_mahjong_player_count.SetRange(2, 4)
        self.spin_mahjong_player_count.SetValue(4)
        static_box_sizer.Add(label_mahjong_player_count, 0, wx.ALIGN_CENTER_VERTICAL)
        static_box_sizer.Add(self.spin_mahjong_player_count, 0, wx.ALIGN_CENTER_VERTICAL)    
        
        label_mahjong_banker_seat_id = wx.StaticText(static_box, label = u"庄家座位：")
        self.spin_mahjong_banker_seat_id = wx.SpinCtrl(static_box, value='0', size=(60,-1))    
        self.spin_mahjong_banker_seat_id.SetRange(0, 3)
        self.spin_mahjong_banker_seat_id.SetValue(0)
        static_box_sizer.Add(label_mahjong_banker_seat_id, 0, wx.ALIGN_CENTER_VERTICAL)
        static_box_sizer.Add(self.spin_mahjong_banker_seat_id, 0, wx.ALIGN_CENTER_VERTICAL)  
        
        label_mahjong_test_count = wx.StaticText(static_box, label = u"测试次数：")
        self.spin_mahjong_test_count = wx.SpinCtrl(static_box, value='1', size=(60,-1))    
        self.spin_mahjong_test_count.SetRange(0, 1000)
        self.spin_mahjong_test_count.SetValue(1)
        static_box_sizer.Add(label_mahjong_test_count, 0, wx.ALIGN_CENTER_VERTICAL)
        static_box_sizer.Add(self.spin_mahjong_test_count, 0, wx.ALIGN_CENTER_VERTICAL)          
        
        
        static_box1 = wx.StaticBox(self.panel, label=u"麻将数目配置：")
        static_box_sizer1 = wx.StaticBoxSizer(static_box1, orient=wx.VERTICAL)
        frame_sizer1_1 = wx.BoxSizer(orient=wx.HORIZONTAL)
        frame_sizer1_2 = wx.BoxSizer(orient=wx.HORIZONTAL)
        frame_sizer1_3 = wx.BoxSizer(orient=wx.HORIZONTAL)
        frame_sizer1_4 = wx.BoxSizer(orient=wx.HORIZONTAL)
        frame_sizer1_5 = wx.BoxSizer(orient=wx.HORIZONTAL)
        static_box_sizer1.Add(frame_sizer1_1)
        static_box_sizer1.AddSpacer(4)
        static_box_sizer1.Add(frame_sizer1_2)
        static_box_sizer1.AddSpacer(4)
        static_box_sizer1.Add(frame_sizer1_3)
        static_box_sizer1.AddSpacer(4)
        static_box_sizer1.Add(frame_sizer1_4)
        static_box_sizer1.AddSpacer(4)
        static_box_sizer1.Add(frame_sizer1_5)
        frame_sizer.Add(static_box_sizer1, 1, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 6)
        
        label_mahjong_type_wan  = wx.StaticText(static_box1, label = u"麻将\"萬\"：")
        label_mahjong_type_suo = wx.StaticText(static_box1, label = u"麻将\"索\"：")
        label_mahjong_type_tong = wx.StaticText(static_box1, label = u"麻将\"筒\"：")
        label_mahjong_type_zi   = wx.StaticText(static_box1, label = u"麻将\"字\"：")
        label_mahjong_type_hua  = wx.StaticText(static_box1, label = u"麻将\"花\"：")
        font = label_mahjong_type_wan.GetFont()
        font.SetPointSize(11) 
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        label_mahjong_type_wan.SetFont(font)
        label_mahjong_type_suo.SetFont(font)
        label_mahjong_type_tong.SetFont(font)
        label_mahjong_type_zi.SetFont(font)
        label_mahjong_type_hua.SetFont(font)
        frame_sizer1_1.Add(label_mahjong_type_wan, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 6)
        frame_sizer1_2.Add(label_mahjong_type_suo, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 6)
        frame_sizer1_3.Add(label_mahjong_type_tong, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 6)
        frame_sizer1_4.Add(label_mahjong_type_zi, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 6)
        frame_sizer1_5.Add(label_mahjong_type_hua, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 6)
        
        self.mahjong_wan_list = []
        self.mahjong_suo_list = []
        self.mahjong_tong_list = []
        self.mahjong_zi_list = []
        self.mahjong_hua_list = []
        
        mahjong_bg = wx.Bitmap('images/mj_bg/mj_small_bg_t.png')
        for i in range(9):
        
            file_name = "mj_w_%d_t" % (i+1)
            mahjong_img = wx.Bitmap('images/mj_top/%s.png'%(file_name))
            mahjong_bmp = self.ImageMerge(mahjong_img, mahjong_bg)            
            img_mahjong = wx.StaticBitmap(static_box1, bitmap=mahjong_bmp)
            spin_mahjong_count = wx.SpinCtrl(static_box1, size=(mahjong_bmp.GetWidth()-10,-1), value='4', min=0, max=4)
            self.mahjong_wan_list.append({"image": img_mahjong, "mahjong_data": i+1, "mahjong_count": spin_mahjong_count})
            mahjong_sizer = wx.BoxSizer(orient=wx.VERTICAL)
            mahjong_sizer.Add(img_mahjong, 0, wx.CENTER)
            mahjong_sizer.Add(spin_mahjong_count, 0, wx.CENTER)
            frame_sizer1_1.Add(mahjong_sizer)
            frame_sizer1_1.AddSpacer(8)
            
            file_name = "mj_tiao_%d_t" % (i+1)
            mahjong_img = wx.Bitmap('images/mj_top/%s.png'%(file_name))
            mahjong_bmp = self.ImageMerge(mahjong_img, mahjong_bg)               
            img_mahjong = wx.StaticBitmap(static_box1, bitmap=mahjong_bmp)
            spin_mahjong_count = wx.SpinCtrl(static_box1, size=(mahjong_bmp.GetWidth()-10,-1), value='4', min=0, max=4)
            self.mahjong_suo_list.append({"image": img_mahjong, "mahjong_data": 0x10+i+1, "mahjong_count": spin_mahjong_count})
            mahjong_sizer = wx.BoxSizer(orient=wx.VERTICAL)
            mahjong_sizer.Add(img_mahjong, 0, wx.CENTER)
            mahjong_sizer.Add(spin_mahjong_count, 0, wx.CENTER)
            frame_sizer1_2.Add(mahjong_sizer)
            frame_sizer1_2.AddSpacer(8)
            
            file_name = "mj_tong_%d_t" % (i+1)
            mahjong_img = wx.Bitmap('images/mj_top/%s.png'%(file_name))
            mahjong_bmp = self.ImageMerge(mahjong_img, mahjong_bg)               
            img_mahjong = wx.StaticBitmap(static_box1, bitmap=mahjong_bmp)
            spin_mahjong_count = wx.SpinCtrl(static_box1, size=(mahjong_bmp.GetWidth()-10,-1), value='4', min=0, max=4)
            self.mahjong_tong_list.append({"image": img_mahjong, "mahjong_data": 0x20+i+1, "mahjong_count": spin_mahjong_count})
            mahjong_sizer = wx.BoxSizer(orient=wx.VERTICAL)
            mahjong_sizer.Add(img_mahjong, 0, wx.CENTER)
            mahjong_sizer.Add(spin_mahjong_count, 0, wx.CENTER)
            frame_sizer1_3.Add(mahjong_sizer)
            frame_sizer1_3.AddSpacer(8)
            
        
        for i in range(7):
            file_name = "mj_%02x_t" % (0x30+i+1) 
            mahjong_img = wx.Bitmap('images/mj_top/%s.png'%(file_name))
            mahjong_bmp = self.ImageMerge(mahjong_img, mahjong_bg)               
            img_mahjong = wx.StaticBitmap(static_box1, bitmap=mahjong_bmp)
            spin_mahjong_count = wx.SpinCtrl(static_box1, size=(mahjong_bmp.GetWidth()-10,-1), value='4', min=0, max=4)
            self.mahjong_zi_list.append({"image": img_mahjong, "mahjong_data": 0x30+i+1, "mahjong_count": spin_mahjong_count})
            mahjong_sizer = wx.BoxSizer(orient=wx.VERTICAL)
            mahjong_sizer.Add(img_mahjong, 0, wx.CENTER)
            mahjong_sizer.Add(spin_mahjong_count, 0, wx.CENTER)
            frame_sizer1_4.Add(mahjong_sizer)
            frame_sizer1_4.AddSpacer(8)
            
        for i in range(8):
            file_name = "mj_h_%d_t" % (i+1) 
            mahjong_img = wx.Bitmap('images/mj_top/%s.png'%(file_name))
            mahjong_bmp = self.ImageMerge(mahjong_img, mahjong_bg)               
            img_mahjong = wx.StaticBitmap(static_box1, bitmap=mahjong_bmp)
            spin_mahjong_count = wx.SpinCtrl(static_box1, size=(mahjong_bmp.GetWidth()-10,-1), value='0', min=0, max=4)
            self.mahjong_hua_list.append({"image": img_mahjong, "mahjong_data": 0x37+i+1, "mahjong_count": spin_mahjong_count})
            mahjong_sizer = wx.BoxSizer(orient=wx.VERTICAL)
            mahjong_sizer.Add(img_mahjong, 0, wx.CENTER)
            mahjong_sizer.Add(spin_mahjong_count, 0, wx.CENTER)
            frame_sizer1_5.Add(mahjong_sizer)
            frame_sizer1_5.AddSpacer(8)       
            
        
        self.check_all_mahjong_wan = wx.CheckBox(static_box1, label=u"全选", style=wx.CHK_3STATE)
        self.check_all_mahjong_suo = wx.CheckBox(static_box1, label=u"全选", style=wx.CHK_3STATE)
        self.check_all_mahjong_tong = wx.CheckBox(static_box1, label=u"全选", style=wx.CHK_3STATE)
        self.check_all_mahjong_zi = wx.CheckBox(static_box1, label=u"全选", style=wx.CHK_3STATE)
        self.check_all_mahjong_hua = wx.CheckBox(static_box1, label=u"全选", style=wx.CHK_3STATE)
        self.check_all_mahjong_wan.Set3StateValue(wx.CHK_CHECKED)
        self.check_all_mahjong_suo.Set3StateValue(wx.CHK_CHECKED)
        self.check_all_mahjong_tong.Set3StateValue(wx.CHK_CHECKED)
        self.check_all_mahjong_zi.Set3StateValue(wx.CHK_CHECKED)
        self.check_all_mahjong_hua.Set3StateValue(wx.CHK_UNCHECKED)        
        frame_sizer1_1.Add(self.check_all_mahjong_wan, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 2)
        frame_sizer1_2.Add(self.check_all_mahjong_suo, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 2)
        frame_sizer1_3.Add(self.check_all_mahjong_tong, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 2)
        frame_sizer1_4.Add(self.check_all_mahjong_zi, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 2)
        frame_sizer1_5.Add(self.check_all_mahjong_hua, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 2)        
        
        self.UpdateSettings()
        self.UpdateMahjongTotalCount()
        
        
        # 控件事件绑定
        self.Bind(wx.EVT_SPINCTRL, self.OnSelectedSpinMahjongTotalCount, self.spin_mahjong_total_count)
        self.Bind(wx.EVT_TEXT, self.OnChangeSpinMahjongTotalCount, self.spin_mahjong_total_count) 
        
        self.Bind(wx.EVT_SPINCTRL, self.OnSelectedSpinValue, self.spin_mahjong_player_count)
        self.Bind(wx.EVT_TEXT, self.OnChangeSpinValue, self.spin_mahjong_player_count)        
        self.Bind(wx.EVT_SPINCTRL, self.OnSelectedSpinValue, self.spin_mahjong_banker_seat_id)
        self.Bind(wx.EVT_TEXT, self.OnChangeSpinValue, self.spin_mahjong_banker_seat_id)      
        self.Bind(wx.EVT_SPINCTRL, self.OnSelectedSpinValue, self.spin_mahjong_test_count)
        self.Bind(wx.EVT_TEXT, self.OnChangeSpinValue, self.spin_mahjong_test_count)    
        
        self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox, self.check_all_mahjong_wan) 
        self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox, self.check_all_mahjong_suo)  
        self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox, self.check_all_mahjong_tong)  
        self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox, self.check_all_mahjong_zi) 
        self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox, self.check_all_mahjong_hua)   
        
        for mahjong_ctrl in self.mahjong_wan_list:
            self.Bind(wx.EVT_SPINCTRL, self.OnSelectedSpinMahjongTotalCount, mahjong_ctrl["mahjong_count"])
            self.Bind(wx.EVT_TEXT, self.OnChangeSpinMahjongTotalCount, mahjong_ctrl["mahjong_count"]) 
        for mahjong_ctrl in self.mahjong_suo_list:
            self.Bind(wx.EVT_SPINCTRL, self.OnSelectedSpinMahjongTotalCount, mahjong_ctrl["mahjong_count"])
            self.Bind(wx.EVT_TEXT, self.OnChangeSpinMahjongTotalCount, mahjong_ctrl["mahjong_count"]) 
        for mahjong_ctrl in self.mahjong_tong_list:
            self.Bind(wx.EVT_SPINCTRL, self.OnSelectedSpinMahjongTotalCount, mahjong_ctrl["mahjong_count"])
            self.Bind(wx.EVT_TEXT, self.OnChangeSpinMahjongTotalCount, mahjong_ctrl["mahjong_count"]) 
        for mahjong_ctrl in self.mahjong_zi_list:
            self.Bind(wx.EVT_SPINCTRL, self.OnSelectedSpinMahjongTotalCount, mahjong_ctrl["mahjong_count"])
            self.Bind(wx.EVT_TEXT, self.OnChangeSpinMahjongTotalCount, mahjong_ctrl["mahjong_count"]) 
        for mahjong_ctrl in self.mahjong_hua_list:
            self.Bind(wx.EVT_SPINCTRL, self.OnSelectedSpinMahjongTotalCount, mahjong_ctrl["mahjong_count"])
            self.Bind(wx.EVT_TEXT, self.OnChangeSpinMahjongTotalCount, mahjong_ctrl["mahjong_count"])         
   
        
        
    def ImageMerge(self, mahjong_img, mahjong_bg): 
        mahjong_bmp = wx.EmptyBitmapRGBA(mahjong_bg.GetWidth(), mahjong_bg.GetHeight())
        memDC = wx.MemoryDC()
        memDC.SelectObject(mahjong_bmp)  
        mahjong_img = mahjong_img.ConvertToImage().Scale(mahjong_bg.GetWidth() - 8, mahjong_bg.GetHeight() - 20)
        mahjong_img = mahjong_img.ConvertToBitmap()        
        memDC.DrawBitmap(mahjong_bg, 0, 0, True)
        memDC.DrawBitmap(mahjong_img, (mahjong_bg.GetWidth()-mahjong_img.GetWidth()) / 2, 0, True)  
        
        mahjong_bmp = mahjong_bmp.ConvertToImage().Scale(mahjong_bmp.GetWidth() - 4, mahjong_bmp.GetHeight() - 6)
        mahjong_bmp = mahjong_bmp.ConvertToBitmap()            
        
        return mahjong_bmp
    
    
    def UpdateSettings(self):
        
        self.spin_mahjong_player_count.SetValue(self.parent.config.mahjong_player_count)
        self.parent.config.mahjong_player_count = self.spin_mahjong_player_count.GetValue()
        if self.parent.config.mahjong_player_count > 0:
            self.spin_mahjong_banker_seat_id.SetRange(0, self.parent.config.mahjong_player_count - 1)
        else:
            self.spin_mahjong_banker_seat_id.SetRange(0, 0)
        
        if self.parent.config.mahjong_banker_seat_id >= self.spin_mahjong_player_count:
            self.parent.config.mahjong_banker_seat_id = self.spin_mahjong_player_count - 1
        self.spin_mahjong_banker_seat_id.SetValue(self.parent.config.mahjong_banker_seat_id)
        self.parent.config.mahjong_banker_seat_id = self.spin_mahjong_banker_seat_id.GetValue()
        
        self.spin_mahjong_test_count.SetValue(self.parent.config.mahjong_test_count)
        self.parent.config.mahjong_test_count = self.spin_mahjong_test_count.GetValue()        
        
        mahjong_indexs = [0 for i in range(MAHJONG_MAX_INDEX)]
        for mahjong_data in self.parent.config.heap_mahjong_datas:
            index = self.SwitchMahjongToIndex(mahjong_data)
            if index < MAHJONG_MAX_INDEX:                
                mahjong_indexs[index] += 1
                
        for player_mahjong_datas in self.parent.config.player_mahjong_datas:
            for mahjong_data in player_mahjong_datas:
                index = self.SwitchMahjongToIndex(mahjong_data)
                if index < MAHJONG_MAX_INDEX:                
                    mahjong_indexs[index] += 1                
            
        for mahjong_control in self.mahjong_wan_list:
            mahjong_index = self.SwitchMahjongToIndex(mahjong_control["mahjong_data"])
            if mahjong_index < MAHJONG_MAX_INDEX:
                mahjong_control["mahjong_count"].SetValue(mahjong_indexs[mahjong_index])
                
        for mahjong_control in self.mahjong_suo_list:
            mahjong_index = self.SwitchMahjongToIndex(mahjong_control["mahjong_data"])
            if mahjong_index < MAHJONG_MAX_INDEX:
                mahjong_control["mahjong_count"].SetValue(mahjong_indexs[mahjong_index])    
                
        for mahjong_control in self.mahjong_tong_list:
            mahjong_index = self.SwitchMahjongToIndex(mahjong_control["mahjong_data"])
            if mahjong_index < MAHJONG_MAX_INDEX:
                mahjong_control["mahjong_count"].SetValue(mahjong_indexs[mahjong_index])    
                
        for mahjong_control in self.mahjong_zi_list:
            mahjong_index = self.SwitchMahjongToIndex(mahjong_control["mahjong_data"])
            if mahjong_index < MAHJONG_MAX_INDEX:
                mahjong_control["mahjong_count"].SetValue(mahjong_indexs[mahjong_index])    
                
        for mahjong_control in self.mahjong_hua_list:
            mahjong_index = self.SwitchMahjongToIndex(mahjong_control["mahjong_data"])
            if mahjong_index < MAHJONG_MAX_INDEX:
                mahjong_control["mahjong_count"].SetValue(mahjong_indexs[mahjong_index])
                
            
    @staticmethod
    def SwitchMahjongToIndex(mahjong_data):
        
        mahjong_color = ((mahjong_data & MAHJONG_MASK_COLOR) >> 4) & 0xFF
        mahjong_value = (mahjong_data & MAHJONG_MASK_VALUE) & 0xFF
        mahjong_index = mahjong_color * 9 + mahjong_value - 1
        
        return mahjong_index
    
    def GetMahjongDatas(self):
        
        mahjong_datas = []
        for mahjong_control in self.mahjong_wan_list:
            mahjong_index = self.SwitchMahjongToIndex(mahjong_control["mahjong_data"])
            if mahjong_index < MAHJONG_MAX_INDEX and mahjong_control["mahjong_count"].GetValue() > 0:
                for index in range(mahjong_control["mahjong_count"].GetValue()):
                    mahjong_datas.append(mahjong_control["mahjong_data"])
                
        for mahjong_control in self.mahjong_suo_list:
            mahjong_index = self.SwitchMahjongToIndex(mahjong_control["mahjong_data"])
            if mahjong_index < MAHJONG_MAX_INDEX and mahjong_control["mahjong_count"].GetValue() > 0:
                for index in range(mahjong_control["mahjong_count"].GetValue()):
                    mahjong_datas.append(mahjong_control["mahjong_data"])   
                
        for mahjong_control in self.mahjong_tong_list:
            mahjong_index = self.SwitchMahjongToIndex(mahjong_control["mahjong_data"])
            if mahjong_index < MAHJONG_MAX_INDEX and mahjong_control["mahjong_count"].GetValue() > 0:
                for index in range(mahjong_control["mahjong_count"].GetValue()):
                    mahjong_datas.append(mahjong_control["mahjong_data"]) 
                
        for mahjong_control in self.mahjong_zi_list:
            mahjong_index = self.SwitchMahjongToIndex(mahjong_control["mahjong_data"])
            if mahjong_index < MAHJONG_MAX_INDEX and mahjong_control["mahjong_count"].GetValue() > 0:
                for index in range(mahjong_control["mahjong_count"].GetValue()):
                    mahjong_datas.append(mahjong_control["mahjong_data"])  
                
        for mahjong_control in self.mahjong_hua_list:
            mahjong_index = self.SwitchMahjongToIndex(mahjong_control["mahjong_data"])
            if mahjong_index < MAHJONG_MAX_INDEX and mahjong_control["mahjong_count"].GetValue() > 0:
                for index in range(mahjong_control["mahjong_count"].GetValue()):
                    mahjong_datas.append(mahjong_control["mahjong_data"])
                
        return mahjong_datas
    
    def UpdateMahjongTotalCount(self):
        
        mahjong_total_count = 0
        mahjong_wan_count = 0
        mahjong_suo_count = 0
        mahjong_tong_count = 0
        mahjong_zi_count = 0
        mahjong_hua_count = 0
        
        for mahjong_ctrl in self.mahjong_wan_list:
            mahjong_wan_count += mahjong_ctrl["mahjong_count"].GetValue()
            mahjong_total_count += mahjong_ctrl["mahjong_count"].GetValue()
            
        for mahjong_ctrl in self.mahjong_suo_list:
            mahjong_suo_count += mahjong_ctrl["mahjong_count"].GetValue()
            mahjong_total_count += mahjong_ctrl["mahjong_count"].GetValue()
            
        for mahjong_ctrl in self.mahjong_tong_list:
            mahjong_tong_count += mahjong_ctrl["mahjong_count"].GetValue()
            mahjong_total_count += mahjong_ctrl["mahjong_count"].GetValue()
            
        for mahjong_ctrl in self.mahjong_zi_list:
            mahjong_zi_count += mahjong_ctrl["mahjong_count"].GetValue()
            mahjong_total_count += mahjong_ctrl["mahjong_count"].GetValue()
            
        for mahjong_ctrl in self.mahjong_hua_list:
            mahjong_hua_count += mahjong_ctrl["mahjong_count"].GetValue()
            mahjong_total_count += mahjong_ctrl["mahjong_count"].GetValue()  
            
        self.check_all_mahjong_wan.Set3StateValue(wx.CHK_UNCHECKED if mahjong_wan_count == 0 else (wx.CHK_CHECKED if mahjong_wan_count == 9*4 else wx.CHK_UNDETERMINED))
        self.check_all_mahjong_suo.Set3StateValue(wx.CHK_UNCHECKED if mahjong_suo_count == 0 else (wx.CHK_CHECKED if mahjong_suo_count == 9*4 else wx.CHK_UNDETERMINED))
        self.check_all_mahjong_tong.Set3StateValue(wx.CHK_UNCHECKED if mahjong_tong_count == 0 else (wx.CHK_CHECKED if mahjong_tong_count == 9*4 else wx.CHK_UNDETERMINED))
        self.check_all_mahjong_zi.Set3StateValue(wx.CHK_UNCHECKED if mahjong_zi_count == 0 else (wx.CHK_CHECKED if mahjong_zi_count == 7*4 else wx.CHK_UNDETERMINED))
        self.check_all_mahjong_hua.Set3StateValue(wx.CHK_UNCHECKED if mahjong_hua_count == 0 else (wx.CHK_CHECKED if mahjong_hua_count == 8*4 else wx.CHK_UNDETERMINED))            
        
        self.spin_mahjong_total_count.SetValue(mahjong_total_count)
        self.parent.config.mahjong_total_count = mahjong_total_count
        
    
    def OnCheckBox(self, evt):
        
        checkbox = evt.GetEventObject()
        if checkbox is self.check_all_mahjong_wan:
            for mahjong_ctrl in self.mahjong_wan_list:
                mahjong_ctrl["mahjong_count"].SetValue(0 if checkbox.Get3StateValue() == wx.CHK_UNCHECKED else 4)            
        elif checkbox is self.check_all_mahjong_suo:
            for mahjong_ctrl in self.mahjong_suo_list:
                mahjong_ctrl["mahjong_count"].SetValue(0 if checkbox.Get3StateValue() == wx.CHK_UNCHECKED else 4)            
        elif checkbox is self.check_all_mahjong_tong:
            for mahjong_ctrl in self.mahjong_tong_list:
                mahjong_ctrl["mahjong_count"].SetValue(0 if checkbox.Get3StateValue() == wx.CHK_UNCHECKED else 4)            
        elif checkbox is self.check_all_mahjong_zi:
            for mahjong_ctrl in self.mahjong_zi_list:
                mahjong_ctrl["mahjong_count"].SetValue(0 if checkbox.Get3StateValue() == wx.CHK_UNCHECKED else 4)            
        elif checkbox is self.check_all_mahjong_hua:
            for mahjong_ctrl in self.mahjong_hua_list:
                mahjong_ctrl["mahjong_count"].SetValue(0 if checkbox.Get3StateValue() == wx.CHK_UNCHECKED else 4)
                
        self.UpdateMahjongTotalCount()
        
        
    def FindMahjongSpinCtrl(self, spin):
        
        for mahjong_ctrl in self.mahjong_wan_list:
            if spin is mahjong_ctrl["mahjong_count"]:  
                return True
        for mahjong_ctrl in self.mahjong_suo_list:
            if spin is mahjong_ctrl["mahjong_count"]:  
                return True
        for mahjong_ctrl in self.mahjong_tong_list:
            if spin is mahjong_ctrl["mahjong_count"]:  
                return True
        for mahjong_ctrl in self.mahjong_zi_list:
            if spin is mahjong_ctrl["mahjong_count"]:  
                return True
        for mahjong_ctrl in self.mahjong_hua_list:
            if spin is mahjong_ctrl["mahjong_count"]:  
                return True
            
        return False
            
        
    def OnSelectedSpinMahjongTotalCount(self, evt):
        
        spin = evt.GetEventObject()
    
        if spin is self.spin_mahjong_total_count:
            self.parent.config.mahjong_total_count = spin.GetValue()
        else:
            if self.FindMahjongSpinCtrl(spin):
                self.UpdateMahjongTotalCount()
        
    def OnChangeSpinMahjongTotalCount(self, evt):

        spin = evt.GetEventObject()

        if spin is self.spin_mahjong_total_count:
            self.parent.config.mahjong_total_count = spin.GetValue()        
        else:
            if self.FindMahjongSpinCtrl(spin):
                self.UpdateMahjongTotalCount()  
                
    def OnSelectedSpinValue(self, evt):
        
        spin = evt.GetEventObject()
    
        if spin is self.spin_mahjong_player_count:
            self.parent.config.mahjong_player_count = spin.GetValue()
            if self.parent.config.mahjong_player_count > 0:
                self.spin_mahjong_banker_seat_id.SetRange(0, self.parent.config.mahjong_player_count - 1)
                if self.spin_mahjong_banker_seat_id.GetValue() >= self.parent.config.mahjong_player_count:
                    self.spin_mahjong_banker_seat_id.SetValue(self.parent.config.mahjong_player_count - 1)
            else:
                self.spin_mahjong_banker_seat_id.SetRange(0, 0)
                self.spin_mahjong_banker_seat_id.SetValue(0)
                
            self.parent.config.mahjong_banker_seat_id = self.spin_mahjong_banker_seat_id.GetValue() 
            
        elif spin is self.spin_mahjong_banker_seat_id:
            self.parent.config.mahjong_banker_seat_id = spin.GetValue() 
            
        elif spin is self.spin_mahjong_test_count:
            self.parent.config.mahjong_test_count = spin.GetValue()               
        
    def OnChangeSpinValue(self, evt):

        spin = evt.GetEventObject()

        if spin is self.spin_mahjong_player_count:
            self.parent.config.mahjong_player_count = spin.GetValue()
            if self.parent.config.mahjong_player_count > 0:
                self.spin_mahjong_banker_seat_id.SetRange(0, self.parent.config.mahjong_player_count - 1)
                if self.spin_mahjong_banker_seat_id.GetValue() >= self.parent.config.mahjong_player_count:
                    self.spin_mahjong_banker_seat_id.SetValue(self.parent.config.mahjong_player_count - 1)
            else:
                self.spin_mahjong_banker_seat_id.SetRange(0, 0)
                self.spin_mahjong_banker_seat_id.SetValue(0)
                
            self.parent.config.mahjong_banker_seat_id = self.spin_mahjong_banker_seat_id.GetValue() 
            
        elif spin is self.spin_mahjong_banker_seat_id:
            self.parent.config.mahjong_banker_seat_id = spin.GetValue()  
            
        elif spin is self.spin_mahjong_test_count:
            self.parent.config.mahjong_test_count = spin.GetValue()       
    

class MahjongMainFrame(wx.Frame):
    
    def __init__(self):
        
        wx.Frame.__init__(self, parent = None, id = -1, title = u'麻将做牌工具', size = (960,640)) 
        
        self.SetMinClientSize((960, 640))
        
        self.config = MahjongConfig()
        self.config.Read("MahjongConfig.ini")
        #self.config.ReadJson("MahjongConfig.json") 
        
        self.panel = wx.Panel(self)
        self.canvas = DragCanvas(self)
        self.canvas.SetSize(self.GetClientSize())
        
        self.btn_setting = wx.Button(self.canvas, label=u"设置", size = (40, -1))
        
        frame_sizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.panel.SetSizer(frame_sizer)
        self.panel.SetBackgroundColour(wx.Colour(255,255,255))
        
        frame_sizer.Add(self.canvas, 1, wx.ALL|wx.EXPAND,2)
        
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_MAXIMIZE, self.OnMaxSize)
        self.Bind(wx.EVT_ICONIZE, self.OnMinSize)
        
        self.Bind(wx.EVT_BUTTON, self.OnBtnSetting, self.btn_setting)
        
    def __del__(self):
        
        self.config.Write("MahjongConfig.ini")
        self.config.WriteJson("MahjongConfig.json")
        print('save config to file')
        
    def OnSize(self, evt): 
        
        self.canvas.SetSize(self.GetClientSize())
        self.canvas.Refresh()
        
    def OnMaxSize(self, evt): 
        
        self.canvas.SetSize(self.GetClientSize())
        self.canvas.Refresh()
        
    def OnMinSize(self, evt): 
        
        self.canvas.SetSize(self.GetClientSize())
        self.canvas.Refresh()
        
        
    def OnBtnSetting(self, evt):
        
        mahjong_datas = []
        setting_dlg = MahjongSettingDlg(self)
        setting_dlg.ShowModal()
        mahjong_datas = setting_dlg.GetMahjongDatas()
        self.canvas.AdjustMahjongDatas(mahjong_datas)
        self.canvas.UpdateMahjongView()
        setting_dlg.Destroy()
        

class MahjongApp(wx.App):  

    def OnInit(self):
        frame = MahjongMainFrame()
        frame.Show(True)
        return True
    


def main():
    """software start runing """

    app = MahjongApp()  
    app.MainLoop()

    return

    
if __name__ == "__main__":
    main()

 
