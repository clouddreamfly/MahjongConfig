#!/usr/bin/python
# coding: utf-8

import time
import json
import wx




class MahjongConfig:

    def __init__(self):
        
        self.config = None
        
    def getConfig(self):
        
        return self.config    
        
    def readConfig(self, path):
        """monitor config json file read"""
    
        try:
            fp = open(path, 'r', encoding='utf-8')
        except:
            print("open json file error!")
            return False
    
        with fp:
            try:
                check_bom = fp.read(3)
                if check_bom == '\xef\xbb\xbf':
                    fp.seek(3)
                else:
                    fp.seek(0)
                self.config = json.load(fp)
            except BaseException as err:
                print("json read error",err)
                return False, err
    
        return True
    
    def writeConfig(self, path):
        """table configure json file read"""

        if self.config == None or len(self.config) == 0:
            return False

        try:
            fp = open(path,'w', encoding='utf-8')
        except:
            print("open json file error!")
            return False
            
        with fp:
            try:
                json.dump(self.config,fp,indent=4,separators=(',',': '))
            except BaseException as err:
                print("json write error", err)
                return False, err
                
        return True    
    
        
#----------------------------------------------------------------------

class DragShape:
    
    def __init__(self, bmp):
        
        self.bmp = bmp
        self.pos = (0,0)
        self.shown = True
        self.text = None
        self.fullscreen = False

    def HitTest(self, pt):
        
        rect = self.GetRect()
        return rect.InsideXY(pt.x, pt.y)

    def GetRect(self):
        
        return wx.Rect(self.pos[0], self.pos[1], self.bmp.GetWidth(), self.bmp.GetHeight())

    def Draw(self, dc, op = wx.COPY):
        
        if self.bmp.Ok():
            memDC = wx.MemoryDC()
            memDC.SelectObject(self.bmp)

            dc.Blit(self.pos[0], self.pos[1],
                    self.bmp.GetWidth(), self.bmp.GetHeight(),
                    memDC, 0, 0, op, True)

            return True
        else:
            return False


class DragMahjong(DragShape):
    
    def __init__(self, card_data, mahjong_bmp):
        
        DragShape.__init__(self, mahjong_bmp)
        
        self.card_data = card_data



# 牌堆麻将        
class HeapMahjong(DragMahjong):
    
    def __init__(self, card_data, mahjong_img, mahjong_bg):
        
        mahjong_bmp = wx.EmptyBitmapRGBA(mahjong_bg.GetWidth(), mahjong_bg.GetHeight())
        memDC = wx.MemoryDC()
        memDC.SelectObject(mahjong_bmp)  
        memDC.DrawBitmap(mahjong_bg, 0, 0, True)
        memDC.DrawBitmap(mahjong_img, (mahjong_bg.GetWidth()-mahjong_img.GetWidth()) / 2, 0, True)      
        
        mahjong_bmp = mahjong_bmp.ConvertToImage().Scale(mahjong_bmp.GetWidth() - 18, mahjong_bmp.GetHeight() - 30)
        mahjong_bmp = mahjong_bmp.ConvertToBitmap()            
        
        DragMahjong.__init__(self, card_data, mahjong_bmp)
        
        
        
# 发牌麻将   
class DealMahjong(DragMahjong):
    
    def __init__(self, card_data, mahjong_img, mahjong_bg):
        
        mahjong_bmp = wx.EmptyBitmapRGBA(mahjong_bg.GetWidth(), mahjong_bg.GetHeight())
        memDC = wx.MemoryDC()
        memDC.SelectObject(mahjong_bmp)  
        
        mahjong_img = mahjong_img.ConvertToImage().Scale(mahjong_bg.GetWidth() - 8, mahjong_bg.GetHeight() - 20)
        mahjong_img = mahjong_img.ConvertToBitmap()             
        memDC.DrawBitmap(mahjong_bg, 0, 0, True)
        memDC.DrawBitmap(mahjong_img, (mahjong_bg.GetWidth()-mahjong_img.GetWidth()) / 2, 0, True)        
        
        DragMahjong.__init__(self, card_data, mahjong_bmp)
        
        
         
         
# 左边麻将    
class LeftMahjong(DragMahjong):
    
    def __init__(self, card_data, mahjong_img, mahjong_bg):
        
        mahjong_bmp = wx.EmptyBitmapRGBA(mahjong_bg.GetWidth(), mahjong_bg.GetHeight())
        memDC = wx.MemoryDC()
        memDC.SelectObject(mahjong_bmp)  
        memDC.DrawBitmap(mahjong_bg, 0, 0, True)
        memDC.DrawBitmap(mahjong_img, (mahjong_bg.GetWidth()-mahjong_img.GetWidth()) / 2, 6, True)        
        
        DragMahjong.__init__(self, card_data, mahjong_bmp)
        
        self.SeatID = 0
        
        
        
        
# 上面麻将
class TopMahjong(DragMahjong):
    
    def __init__(self, card_data, mahjong_img, mahjong_bg):
        
        mahjong_bmp = wx.EmptyBitmapRGBA(mahjong_bg.GetWidth(), mahjong_bg.GetHeight())
        memDC = wx.MemoryDC()
        memDC.SelectObject(mahjong_bmp)  
        
        mahjong_img = mahjong_img.ConvertToImage().Scale(mahjong_bg.GetWidth() - 8, mahjong_bg.GetHeight() - 20)
        mahjong_img = mahjong_img.ConvertToBitmap()        
        memDC.DrawBitmap(mahjong_bg, 0, 0, True)
        memDC.DrawBitmap(mahjong_img, (mahjong_bg.GetWidth()-mahjong_img.GetWidth()) / 2, 0, True)        
        
        DragMahjong.__init__(self, card_data, mahjong_bmp)
         
        self.SeatID = 1 
        
         
# 右边麻将  
class RightMahjong(DragMahjong):
    
    def __init__(self, card_data, mahjong_img, mahjong_bg):
        
        mahjong_bmp = wx.EmptyBitmapRGBA(mahjong_bg.GetWidth(), mahjong_bg.GetHeight())
        memDC = wx.MemoryDC()
        memDC.SelectObject(mahjong_bmp)  
        memDC.DrawBitmap(mahjong_bg, 0, 0, True)
        memDC.DrawBitmap(mahjong_img, (mahjong_bg.GetWidth()-mahjong_img.GetWidth()) / 2, 6, True)        
        
        DragMahjong.__init__(self, card_data, mahjong_bmp)
        
        self.SeatID = 2
      
      
# 底部麻将   
class BottomMahjong(DragMahjong):
    
    def __init__(self, card_data, mahjong_img, mahjong_bg):
        
        mahjong_bmp = wx.EmptyBitmapRGBA(mahjong_bg.GetWidth(), mahjong_bg.GetHeight())
        memDC = wx.MemoryDC()
        memDC.SelectObject(mahjong_bmp)         
        memDC.DrawBitmap(mahjong_bg, 0, 0, True)
        memDC.DrawBitmap(mahjong_img, (mahjong_bg.GetWidth()-mahjong_img.GetWidth()) / 2, 28, True)     
        
        mahjong_bmp = mahjong_bmp.ConvertToImage().Scale(mahjong_bmp.GetWidth() - 18, mahjong_bmp.GetHeight() - 30)
        mahjong_bmp = mahjong_bmp.ConvertToBitmap()            
        
        DragMahjong.__init__(self, card_data, mahjong_bmp)
         
        self.SeatID = 3
 
 
SeatDirection_Left = 0
SeatDirection_Top = 1
SeatDirection_Right = 2
SeatDirection_Bottom = 3

   
# 手上麻将
class HandMahjong:
    
    def __init__(self, parent, seat_id, seat_direction, hand_cards):
        
        self.parent = parent
        self.seat_id = seat_id
        self.seat_direction = seat_direction
        self.hand_cards = []  
        self.view_cards = []
        
        for data in hand_cards:
            self.hand_cards.append(data)
             
        self.InitMahjong()
            
             
    def InitMahjong(self):
        
        if self.seat_direction == SeatDirection_Left:
            self.InitLeftMahjong()
        elif self.seat_direction == SeatDirection_Top:
            self.InitTopMahjong()
        elif self.seat_direction == SeatDirection_Right:
            self.InitRightMahjong()
        else:
            self.InitBottomMahjong()
            
    
    def InitLeftMahjong(self):
        
        mahjong_bg = wx.Bitmap('images/mj_bg/mj_small_bg_l.png')
        height_space = (mahjong_bg.GetHeight() - 20 )
        width_space = (mahjong_bg.GetWidth())
        x = 20
        y = 100        
        count = 0
        for data in self.hand_cards:
            color = (((data & 0xF0) >> 4) & 0xFF)
            value = ((data & 0x0F) & 0xFF)
            file_name = 'mj.png'
            if color == 0 :
                file_name = "mj_w_%d_l" % (value)
            elif color == 1: 
                file_name = "mj_tiao_%d_l" % (value)
            elif color == 2:
                file_name = "mj_tong_%d_l" % (value)
            elif color == 3:
                if value <= 7 :
                    file_name = "mj_%02x_l" % (data)
                else:
                    file_name = "mj_h_%d_l" % (value - 7)
                
            mahjong_img = wx.Bitmap('images/mj_left/%s.png' % (file_name))
            
            shape = LeftMahjong(data, mahjong_img, mahjong_bg)
            shape.pos = (x, y + count * height_space)
            shape.fullscreen = True
            self.view_cards.append(shape) 
            self.parent.shapes.append(shape) 
            count += 1        
            
            

    def InitTopMahjong(self):                    
                   
        mahjong_bg = wx.Bitmap('images/mj_bg/mj_small_bg_t.png')
       
        height_space = (mahjong_bg.GetHeight())   
        width_space = (mahjong_bg.GetWidth() - 4)
        x = 180
        y = 100        
        count = 0
        for data in self.hand_cards:
            color = (((data & 0xF0) >> 4) & 0xFF)
            value = ((data & 0x0F) & 0xFF)
            file_name = 'mj.png'
            if color == 0 :
                file_name = "mj_w_%d_t" % (value)
            elif color == 1: 
                file_name = "mj_tiao_%d_t" % (value)
            elif color == 2:
                file_name = "mj_tong_%d_t" % (value)
            elif color == 3:
                if value <= 7 :
                    file_name = "mj_%02x_t" % (data)
                else:
                    file_name = "mj_h_%d_t" % (value - 7)
                
            mahjong_img = wx.Bitmap('images/mj_top/%s.png' % (file_name))
            
            shape = TopMahjong(data, mahjong_img, mahjong_bg)
            shape.pos = (x + count * width_space, y)
            shape.fullscreen = True
            self.view_cards.append(shape) 
            self.parent.shapes.append(shape)    
            count += 1
                
                
    def InitRightMahjong(self):
     
        mahjong_bg = wx.Bitmap('images/mj_bg/mj_small_bg_r.png')
       
        height_space = (mahjong_bg.GetHeight() - 20)
        width_space = (mahjong_bg.GetWidth())
        x = 860
        y = 100   
        count = 0
        for data in self.hand_cards:
            color = (((data & 0xF0) >> 4) & 0xFF)
            value = ((data & 0x0F) & 0xFF)
            file_name = 'mj.png'
            if color == 0 :
                file_name = "mj_w_%d_r" % (value)
            elif color == 1: 
                file_name = "mj_tiao_%d_r" % (value)
            elif color == 2:
                file_name = "mj_tong_%d_r" % (value)
            elif color == 3:
                if value <= 7 :
                    file_name = "mj_%02x_r" % (data)
                else:
                    file_name = "mj_h_%d_r" % (value - 7)
                
            mahjong_img = wx.Bitmap('images/mj_right/%s.png' % (file_name))
            
            shape = RightMahjong(data, mahjong_img, mahjong_bg)
            shape.pos = (x, y + count * height_space)
            shape.fullscreen = True
            self.view_cards.append(shape) 
            self.parent.shapes.append(shape)     
            count += 1
        
                
    def InitBottomMahjong(self):
        
            mahjong_bg = wx.Bitmap('images/mj_bg/mj_hand_bg.png')
           
            height_space = (mahjong_bg.GetHeight())   
            width_space = (mahjong_bg.GetWidth() - 17)
            x = 100
            y = 450    
            count = 0
            for data in self.hand_cards:
                color = (((data & 0xF0) >> 4) & 0xFF)
                value = ((data & 0x0F) & 0xFF)
                file_name = 'mj.png'
                if color == 0 :
                    file_name = "mj_w_%d" % (value)
                elif color == 1: 
                    file_name = "mj_tiao_%d" % (value)
                elif color == 2:
                    file_name = "mj_tong_%d" % (value)
                elif color == 3:
                    if value <= 7 :
                        file_name = "mj_%02x" % (data)
                    else:
                        file_name = "mj_h_%d" % (value - 7)
                    
                mahjong_img = wx.Bitmap('images/mj_bottom/%s.png' % (file_name))
                
                shape = BottomMahjong(data, mahjong_img, mahjong_bg)
                shape.pos = (x + count * width_space, y)
                shape.fullscreen = True
                self.view_cards.append(shape) 
                self.parent.shapes.append(shape)      
                count += 1      
                
                

#----------------------------------------------------------------------

class DragCanvas(wx.ScrolledWindow):
    
    def __init__(self, parent, ID = -1):
        
        wx.ScrolledWindow.__init__(self, parent, ID)
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
             
        self.heapMahjongList = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09,                                 
                                0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19,
                                0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x29,
                                0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x3A, 0x3B, 0x3C, 0x3D, 0x3E, 0x3F]
        
        self.dealMahjongList = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09,
                                0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19,
                                0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x29,
                                0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37]
        self.leftMahjongList = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x16, 0x17, 0x18, 0x19, 0x38, 0x39, 0x3A, 0x3B, 0x3C, 0x3D, 0x3E, 0x3F]
        self.topMahjongList = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x16, 0x17, 0x18, 0x19, 0x38, 0x39, 0x3A, 0x3B, 0x3C, 0x3D, 0x3E, 0x3F]
        self.rightMahjongList = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x16, 0x17, 0x18, 0x19]
        self.bottomMahjongList = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x16, 0x17, 0x18, 0x19]
        
        self.HandMahjongList = []
        
        
        mahjong_bg = wx.Bitmap('images/mj_bg/mj_bg.png')
        height_space = (mahjong_bg.GetHeight() - 24)   
        width_space = (mahjong_bg.GetWidth() - 20)
        x = 200
        y = 20          
        
        for data in self.heapMahjongList:
            color = (((data & 0xF0) >> 4) & 0xFF)
            value = ((data & 0x0F) & 0xFF)
            file_name = 'mj.png'
            if color == 0 :
                file_name = "mj_w_%d_t" % (value)
            elif color == 1: 
                file_name = "mj_tiao_%d_t" % (value)
            elif color == 2:
                file_name = "mj_tong_%d_t" % (value)
            elif color == 3:
                if value <= 7 :
                    file_name = "mj_%02x_t" % (data)
                else:
                    file_name = "mj_h_%d_t" % (value - 7)
                
            mahjong_img = wx.Bitmap('images/mj_top/%s.png' % (file_name))
            
            shape = HeapMahjong(data, mahjong_img, mahjong_bg)
            shape.pos = (x + value * width_space, y + color * height_space)
            shape.fullscreen = True
            self.shapes.append(shape)      
            
            
        mahjong_bg = wx.Bitmap('images/mj_bg/mj_small_bg_t.png')
        height_space = (mahjong_bg.GetHeight() - 18)   
        width_space = (mahjong_bg.GetWidth() - 4)
        x = 180
        y = 200 
        x_count = 0
        y_count = 0
        x_max_count = 13
        y_max_count = 7
        for data in self.dealMahjongList:
            color = (((data & 0xF0) >> 4) & 0xFF)
            value = ((data & 0x0F) & 0xFF)
            file_name = 'mj.png'
            if color == 0 :
                file_name = "mj_w_%d_t" % (value)
            elif color == 1: 
                file_name = "mj_tiao_%d_t" % (value)
            elif color == 2:
                file_name = "mj_tong_%d_t" % (value)
            elif color == 3:
                if value <= 7 :
                    file_name = "mj_%02x_t" % (data)
                else:
                    file_name = "mj_h_%d_t" % (value - 7)
                
            mahjong_img = wx.Bitmap('images/mj_top/%s.png' % (file_name))
            
            shape = DealMahjong(data, mahjong_img, mahjong_bg)
            shape.pos = (x + x_count * width_space, y + y_count * height_space)
            shape.fullscreen = True
            self.shapes.append(shape)  
            
            x_count += 1
            if x_count >= x_max_count:
                x_count = 0
                y_count += 1
                if y_count >= y_max_count:
                    break
            

        if len(self.leftMahjongList) > 0:
            hand_mahjong = HandMahjong(self, 0, SeatDirection_Left, self.leftMahjongList)
            self.HandMahjongList.append(hand_mahjong)
            
        if len(self.topMahjongList) > 0:
            hand_mahjong = HandMahjong(self, 0, SeatDirection_Top, self.topMahjongList)
            self.HandMahjongList.append(hand_mahjong)      
            
        if len(self.rightMahjongList) > 0:
            hand_mahjong = HandMahjong(self, 0, SeatDirection_Right, self.rightMahjongList)
            self.HandMahjongList.append(hand_mahjong)    
            
        if len(self.bottomMahjongList) > 0:
            hand_mahjong = HandMahjong(self, 0, SeatDirection_Bottom, self.bottomMahjongList)
            self.HandMahjongList.append(hand_mahjong)    
            
    
        
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
            self.dragShape.shown = False
            self.RefreshRect(self.dragShape.GetRect())
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

            if self.dragShape.text:
                self.dragImage = wx.DragString(self.dragShape.text,
                                               wx.StockCursor(wx.CURSOR_HAND))
            else:
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
        self.spin_mahjong_player_count = wx.SpinCtrl(static_box, value='108', size=(60,-1))    
        self.spin_mahjong_player_count.SetRange(2, 4)
        self.spin_mahjong_player_count.SetValue(4)
        static_box_sizer.Add(label_mahjong_player_count, 0, wx.ALIGN_CENTER_VERTICAL)
        static_box_sizer.Add(self.spin_mahjong_player_count, 0, wx.ALIGN_CENTER_VERTICAL)    
        
        
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
            self.mahjong_wan_list.append({"image": img_mahjong, "card_data": i+1, "mahjong_count": spin_mahjong_count})
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
            self.mahjong_suo_list.append({"image": img_mahjong, "card_data": 0x10+i+1, "mahjong_count": spin_mahjong_count})
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
            self.mahjong_tong_list.append({"image": img_mahjong, "card_data": 0x20+i+1, "mahjong_count": spin_mahjong_count})
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
            self.mahjong_zi_list.append({"image": img_mahjong, "card_data": 0x30+i+1, "mahjong_count": spin_mahjong_count})
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
            self.mahjong_hua_list.append({"image": img_mahjong, "card_data": 0x30+i+1, "mahjong_count": spin_mahjong_count})
            mahjong_sizer = wx.BoxSizer(orient=wx.VERTICAL)
            mahjong_sizer.Add(img_mahjong, 0, wx.CENTER)
            mahjong_sizer.Add(spin_mahjong_count, 0, wx.CENTER)
            frame_sizer1_5.Add(mahjong_sizer)
            frame_sizer1_5.AddSpacer(8)       
        
        self.UpdateMahjongTotalCount()
        
        
        # 控件事件绑定
        self.Bind(wx.EVT_SPINCTRL, self.OnSelectedSpinMahjongTotalCount, self.spin_mahjong_total_count)
        self.Bind(wx.EVT_TEXT, self.OnChangeSpinMahjongTotalCount, self.spin_mahjong_total_count)   
        self.Bind(wx.EVT_SPINCTRL, self.OnSelectedSpinMahjongTotalCount, self.spin_mahjong_player_count)
        self.Bind(wx.EVT_TEXT, self.OnChangeSpinMahjongTotalCount, self.spin_mahjong_player_count)           
        
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
    
    
    def UpdateMahjongTotalCount(self):
        
        mahjong_total_count = 0
        for mahjong_ctrl in self.mahjong_wan_list:
            mahjong_total_count += mahjong_ctrl["mahjong_count"].GetValue()
        for mahjong_ctrl in self.mahjong_suo_list:
            mahjong_total_count += mahjong_ctrl["mahjong_count"].GetValue()
        for mahjong_ctrl in self.mahjong_tong_list:
            mahjong_total_count += mahjong_ctrl["mahjong_count"].GetValue()
        for mahjong_ctrl in self.mahjong_zi_list:
            mahjong_total_count += mahjong_ctrl["mahjong_count"].GetValue()
        for mahjong_ctrl in self.mahjong_hua_list:
            mahjong_total_count += mahjong_ctrl["mahjong_count"].GetValue()  
        
        self.spin_mahjong_total_count.SetValue(mahjong_total_count)
        
        
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
            self.parent.mahjong_total_count = spin.GetValue()
        elif spin is self.spin_mahjong_player_count:
            self.parent.mahjong_player_count = spin.GetValue()
        else:
            if self.FindMahjongSpinCtrl(spin):
                self.UpdateMahjongTotalCount()
        
    def OnChangeSpinMahjongTotalCount(self, evt):

        spin = evt.GetEventObject()

        if spin is self.spin_mahjong_total_count:
            self.parent.mahjong_total_count = spin.GetValue()
        elif spin is self.spin_mahjong_player_count:
            self.parent.mahjong_player_count = spin.GetValue()            
        else:
            if self.FindMahjongSpinCtrl(spin):
                self.UpdateMahjongTotalCount()  
    

class MahjongMainFrame(wx.Frame):
    
    def __init__(self):
        
        wx.Frame.__init__(self, parent = None, id = -1, title = u'麻将做牌工具', size = (960,600)) 
        
        self.panel = wx.Panel(self)
        self.canvas = DragCanvas(self)
        self.canvas.SetSize(self.GetClientSize())
        
        self.mahjong_total_count = 0
        self.mahjong_player_count = 0
        
        self.btn_setting = wx.Button(self.canvas, label=u"设置", size = (40, -1))
        
        frame_sizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.panel.SetSizer(frame_sizer)
        self.panel.SetBackgroundColour(wx.Colour(255,255,255))
        
        frame_sizer.Add(self.canvas, 1, wx.ALL|wx.EXPAND,2)
        
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_MAXIMIZE, self.OnMaxSize)
        self.Bind(wx.EVT_ICONIZE, self.OnMinSize)
        
        self.Bind(wx.EVT_BUTTON, self.OnBtnSetting, self.btn_setting)
        
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
        
        setting_dlg = MahjongSettingDlg(self)
        setting_dlg.ShowModal()
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

 
