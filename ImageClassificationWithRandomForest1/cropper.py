from PIL import Image
import math
class Image_Crop:
    def __init__(self,img,thres=600):
        self.gx=[[3,0,-3],
                 [10,0,-10],
                 [3,0,-3]]
        self.gy=[[3,10,3],
                 [0,0,0],
                 [-3,-10,-3]]
        self.image = Image.open(img)
        self.width,self.height=self.image.size
        self.threshold = thres
        self.min_width=50
        self.min_height=50
        self.max_width=0
        self.max_height=0
        self.crop_min_width=50
        self.crop_min_height=50
        self.crop_max_width=0
        self.crop_max_height=0
        self.path=img
        self.nonExist=0
        self.colorthreshold=30
    
    def Edge_detection(self):
        self.crop_min_width=50
        self.crop_min_height=50
        self.crop_max_width=0
        self.crop_max_height=0
        var_list=[]
        color=""
        self.down_size()
        new_img=Image.new(self.image.mode, self.image.size)
        isLimited=False
        while (isLimited==False):
            
            var_list=[]
            for x in range(0, self.width):
                
                self.min_width=50
                self.min_height=50
                self.max_width=0
                self.max_height=0
                for y in range(0, self.height):
                    sum_x = self.kernal_sum(x,y,check="gx")
                    sum_y = self.kernal_sum(x,y,check="gy")
                    sum_xy = math.sqrt(math.pow(sum_x,2) + math.pow(sum_y,2))
                    if sum_xy<self.threshold:
                        if x<self.crop_min_width:
                            self.crop_min_width=x
                        if x>self.crop_max_width:
                            self.crop_max_width=x
                        if y<self.crop_min_height:
                            self.crop_min_height=y
                        if y>self.crop_max_height:
                            self.crop_max_height=y
		    #print(str(sum_x)+","+str(sum_y)+":"+str(sum_xy))
                    white=(255,255,255)
                    black=(0,0,0)
                    if sum_xy>self.threshold:
                        new_img.putpixel((x,y),white)
                    else:
                        if x<self.min_width:
                            self.min_width=x
                        if x>self.max_width:
                            self.max_width=x
                        if y<self.min_height:
                            self.min_height=y
                        if y>self.max_height:
                            self.max_height=y
                        new_img.putpixel((x,y),black)
                        isLimited = True
                if(self.min_height==50):
                    self.min_height=0
                if(self.min_width==50):
                    self.min_width=0

                var_list.append(self.max_height-self.min_height)

            self.threshold += 20
        #new_img.show()
        self.threshold=600
        if self.max_width==self.min_width:
            self.max_width=self.width
        if self.max_height==self.max_height:
            self.max_height=self.height
        left = self.crop_min_width
        top = self.crop_min_height
        right = self.crop_max_width
        bottom = self.crop_max_height
        self.image=self.image.crop((left,top,right,bottom))
        self.width,self.height=self.image.size
        color=[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
        r=0
        g=0
        b=0
        bl=0
        w=0
        for i in range(1,5):
            for j in range(1,5):

                color[i][j]=(self.ColorDetector(self.width/2-self.width/(j*10),self.height/2-self.height/(i*10)))
                if(color[i][j]=="Red"):
                    r+=1
                if(color[i][j]=="Green"):
                    g+=1
                if(color[i][j]=="Blue"):
                    b+=1
                if(color[i][j]=="Black"):
                    bl+=1
                if(color[i][j]=="White"):
                    w+=1
                color[i][j]=(self.ColorDetector(self.width/2+self.width/(j*10),self.height/2+self.height/(i*10)))
                if(color[i][j]=="Red"):
                    r+=1
                if(color[i][j]=="Green"):
                    g+=1
                if(color[i][j]=="Blue"):
                    b+=1
                if(color[i][j]=="Black"):
                    bl+=1
                if(color[i][j]=="White"):
                    w+=1
                color[i][j]=(self.ColorDetector(self.width/2,self.height/2))
                if(color[i][j]=="Red"):
                    r+=1
                if(color[i][j]=="Green"):
                    g+=1
                if(color[i][j]=="Blue"):
                    b+=1
                if(color[i][j]=="Black"):
                    bl+=1
                if(color[i][j]=="White"):
                    w+=1
        if (r>g and r>b and r>bl and r>w):
            color="Red"
        elif(g>b and g>bl and g>w):
            color = "Green"
        elif(b>bl and b>w):
            color="Blue"
        elif(bl>w):
            color="Black"
        else:
            color="White"
        #self.image.show()
        #new_img.show()
        #var_list=self.Cal_Variance()
        #var_list.append(self.width)
        #var_list.append(self.height)
        var_list.append(color)
        return var_list

    def ColorDetector(self,width,height):
        pixel=self.image.getpixel((width,height))
        red1=pixel[0]+self.colorthreshold
        green1=pixel[1]+self.colorthreshold
        blue1=pixel[2]+self.colorthreshold
        red2=pixel[0]-self.colorthreshold
        green2=pixel[1]-self.colorthreshold
        blue2=pixel[2]-self.colorthreshold
        if ((pixel[1]>red2 and pixel[1]<red1) and (pixel[2]<red2 and pixel[2]<green2)):
            return "Red"
        if(pixel[0]>pixel[1] and pixel[0]>pixel[2]):
            return "Red"
        if ((pixel[1]>blue2 and pixel[1]<blue1) and (pixel[0]<green2 and pixel[0]<blue2)):
            return "Blue"
        if(pixel[2]>red1 and pixel[2]>green1):
            return "Blue"
        if(pixel[1]>red1 and pixel[1]>blue1):
            return "Green"
        if ((pixel[1]>red2 and pixel[1]<red1) and (pixel[1]>blue2 and pixel[1]<blue1)  and (self.gray_convert(pixel)<70)):
           return "Black"
        else:
            return "White"
        return

    def kernal_sum(self,x,y,check):
        p=[0,0,0,0,0,0,0,0,0]
        sum = 0
        if check=='gx':
            if(x-1)<0 or (y-1)<0:
                p[0]=self.nonExist*self.gx[0][0]
            else:
                p[0]= self.get_pixel(x-1,y-1)*self.gx[0][0]
            
            if(x-1)<0:
                p[1]=self.nonExist*self.gx[0][1]
            else:
                p[1]= self.get_pixel(x-1,y-1)*self.gx[0][1]
                    
            if(x-1)<0 or (y+1)>self.height:
                p[2]=self.nonExist*self.gx[0][2]
            else:
                p[2]= self.get_pixel(x-1,y-1)*self.gx[0][2]

            if(y-1)<0:
                p[3]=self.nonExist*self.gx[1][0]
            else:
                p[3]= self.get_pixel(x-1,y-1)*self.gx[1][0]

            p[4]= self.get_pixel(x-1,y-1)*self.gx[1][1]
            
            if(y+1)>self.height:
                p[5]=self.nonExist*self.gx[1][2]
            else:
                p[5]= self.get_pixel(x-1,y-1)*self.gx[1][2]

            if(x+1)>self.width or (y-1)<0:
                p[6]=self.nonExist*self.gx[2][0]
            else:
                p[6]= self.get_pixel(x-1,y-1)*self.gx[2][0]

            if(x+1)>self.width:
                p[7]=self.nonExist*self.gx[2][1]
            else:
                p[7]= self.get_pixel(x-1,y-1)*self.gx[2][1]
                    
            if(x+1)>self.width or (y+1)>self.height:
                p[8]=self.nonExist*self.gx[2][2]
            else:
                p[8]= self.get_pixel(x-1,y-1)*self.gx[2][2]
                    
        else:
            if(x-1)<0 or (y-1)<0:
                p[0]=self.nonExist*self.gy[0][0]
            else:
                p[0]= self.get_pixel(x-1,y-1)*self.gy[0][0]
            
            if(x-1)<0:
                p[1]=self.nonExist*self.gy[0][1]
            else:
                p[1]= self.get_pixel(x-1,y-1)*self.gy[0][1]
                    
            if(x-1)<0 or (y+1)>self.height:
                p[2]=self.nonExist*self.gy[0][2]
            else:
                p[2]= self.get_pixel(x-1,y-1)*self.gy[0][2]

            if(y-1)<0:
                p[3]=self.nonExist*self.gy[1][0]
            else:
                p[3]= self.get_pixel(x-1,y-1)*self.gy[1][0]

            p[4]= self.get_pixel(x-1,y-1)*self.gy[1][1]
            
            if(y+1)>self.height:
                p[5]=self.nonExist*self.gy[1][2]
            else:
                p[5]= self.get_pixel(x-1,y-1)*self.gy[1][2]

            if(x+1)>self.width or (y-1)<0:
                p[6]=self.nonExist*self.gy[2][0]
            else:
                p[6]= self.get_pixel(x-1,y-1)*self.gy[2][0]

            if(x+1)>self.width:
                p[7]=self.nonExist*self.gy[2][1]
            else:
                p[7]= self.get_pixel(x-1,y-1)*self.gy[2][1]
                    
            if(x+1)>self.width or (y+1)>self.height:
                p[8]=self.nonExist*self.gy[2][2]
            else:
                p[8]= self.get_pixel(x-1,y-1)*self.gy[2][2]

        for i in range(9):
            sum +=abs(p[i])
        sum = sum / 9
        return sum

    def get_pixel(self,x,y):
        pixel=self.image.getpixel((x,y))
        pix = self.gray_convert(pixel)

        return pix

    def gray_convert(self,pixel):

        gray = (pixel[0]+pixel[1]+pixel[2])
        gray = gray/3
        return gray
    
    def down_size(self):
        self.image = self.image.resize((50,50),Image.ANTIALIAS)
        self.width,self.height=self.image.size
        return
    def get_avrage(self,iteam_list):
        sum = 0
        count=0
        for i in iteam_list:
            sum +=i 
            count +=1
        avg=sum/count
        tem=[]
        tem.append(count)
        tem.append(sum)
        tem.append(avg)
        return tem

    def Cal_Variance(self):
        gray=[]
        sat=[]
        variances=[]
        entropy =[]
        for x in range(0,self.width):
            for y in range(0,self.height):
                gray.append(self.gray_convert(self.image.getpixel((x,y))))
                r=self.red_convert(self.image.getpixel((x,y)))+1
                g=self.green_convert(self.image.getpixel((x,y)))+3
                b=self.blue_convert(self.image.getpixel((x,y)))+1
                sat.append((max(r,g,b)-min(r,g,b))/(max(r,g,b)))
                entropy.append(self.gray_convert(self.image.getpixel((x,y)))*(math.log2(self.gray_convert(self.image.getpixel((x,y)))+1)))
   
        '''var_list_gray = self.get_avrage(gray)
        var_gray_last=0
        var_list_sat = self.get_avrage(sat)
        for x in range(0,self.width):
            for y in range(0,self.height):
               var_gray_last+=(self.gray_convert(self.image.getpixel((x,y)))-var_list_gray[2])**2
        last_gray=int(var_gray_last/(var_list_gray[0]-1))
        var_sat=int(var_list_sat[1])'''
   
        variances.append(gray)
        variances.append(sat)
        variances.append(entropy)
        return variances
    def red_convert(self,pixel):
        red = pixel[0]
        return red
    def green_convert(self,pixel):
        green = pixel[1]
        return green
    def blue_convert(self,pixel):
        blue = pixel[2]
        return blue
