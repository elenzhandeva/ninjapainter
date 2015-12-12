#####CS FINAL PROJECT
####Aliaa Gouda, Elena Zhan
###FINAL COPY

from pygame import *
from pprint import *

font.init()

swid = 1024     #screen width
shei = 768      #screen height
grwh = 32       #grid width

grwid = int(swid/grwh)    #x-axis grids
grhei = int(shei/grwh)    #y-axis grids

gwid = 0
ghei = 0

screen = display.set_mode((swid,shei))
display.set_caption("Ninja Painter")

#~~~~~~~~~~~~~~~~~~#
digits = []
for i in range (0,10):
    digits.append(str(i))

direc=['up','down','left','right']    
direct = [[0,0],[0,-1],[0,1],[-1,0],[1,0]]  #still, up, down, left, right (change to coors)

corners = ["2","3","4","5"] #variables used for corners in txt files for floors
diagdirect = [[1,-1],[-1,-1],[-1,1],[1,1]]  #changes to the coor from each corner
diagdir = [[1,3],[1,4],[2,4],[2,3]]     #directions to hit corner from
diagdirrev=[[2,4],[2,3],[1,3],[1,4]]    #other directions

colvars = ["r","g","b","o"]     #used for the X colour spots
ucolvars = ["R","G","B","O"]    #used for buckets
colvals = [(255,0,0),(0,255,0),(0,0,255),(175,50,204)]  #values for each colour

#reading file for level selected; outputs starting pos, col assigned and floor plan
def rfloor(levfile,lev):
     global floor, start, onep, col1, col2, gwid, ghei

#sets start coords     
     infile = open(str(levfile)+"LEVEL"+str(lev)+".txt").readlines()
     coors = infile[0].strip()
     x, y = coors.split(",")
     start = [int(x), int(y)]
     del infile[0]

#sets colours in [p]
     if onep==False:
          if infile[0].count(", ")==1:  #if there are 2 colours for each player
               col1a, col1b = infile[0].strip().split(", ")
               col1 = [col1a, col1b]
               col2a, col2b = infile[1].strip().split(", ")
               col2 = [col2a, col2b]
          else:     #if there's only 1 per player
               col1 = [infile[0].strip()]
               col2 = [infile[1].strip()]

          infile=infile[2:] #remove 2 lines containing col info

     elif onep==True:   #if 1 player, add all colours to list
          infile[0].strip()
          n = infile[0].count(",")
          for i in range (n+1):
              col1.append(infile[0][2*i])
              
          del infile[0]     #remove line containing col info

#reads rest of file to floor plan (2-D list)
     for line in infile:
          floor.append(line.strip("\n"))
     gwid = len(floor[0])
     ghei = len(floor)

#----------------------------------------------------#
#####PICTURE FILES#######
#~~~~~screen pics~~~~~#
bg = image.load("Screens/bg1.png")

homepic = image.load("Screens/home.png")
playpic = image.load("Screens/play.png")
outpic = image.load("Screens/quit.png")
contpic = image.load("Screens/continue.png")
howpic = image.load("Screens/how.png")
scorepic = image.load("Screens/scores.png")

p1pic = image.load("Screens/1p.png")
p2pic = image.load("Screens/2p.png")
mousepic = image.load("Screens/mouse.png")
arrowpic = image.load("Screens/keys.png")

#screen display info pics + dims
p1card = image.load("Screens/p1card.png")
p1crec = Rect(10,10,80,110)
p2card = image.load("Screens/p2card.png")
p2crec = Rect(900,10,80,110)

mmbut = image.load("Backgrounds/mmbut1.png")
end = image.load("Screens/basicback.jpg")

#--------------FLOOR PICS-----------------------
#loading pics of spots of game 
picname=['floor1','wall','diagdul1','diagudr','diagdur2','diagudl','ladder']    #list of names on file 
backpics=[]
for i in range(len(picname)):
    pic = image.load("picsnew/"+picname[i]+".png")
    pic = transform.scale(pic,(grwh,grwh))
    backpics.append(pic)

#painting spots pictures 
n=['spot','buck','fill']
spots=[]
bucks=[]
fill=[]
for i in range(len(colvars)):
    for j in range(len(n)):
        pic = image.load("picsnew/"+colvars[i]+n[j]+".png")
        pic = transform.scale(pic,(grwh,grwh))
        if n[j] == 'spot':
            spots.append(pic)
        if n[j] == 'buck':
            bucks.append(pic)
        if n[j] == 'fill':
            fill.append(pic)

#----------------SPRITE LOADING----------------
#Mckenzie prog referenced, sprites of player are loaded into a 2D List
def loadsprites(folder,name,first,last):
     list1 = []
     for i in range(first,last+1):
          pic=image.load("%s/%s%03d.png" % (folder,name,i))
          pic=transform.scale(pic,(grwh,grwh))
          list1.append(pic)
     return list1

#stills are seperated into a diff list from sprites due to length
def stills(j):
    global direc
    stills =[]
    for i in range (len(direc)):
        pic = image.load("stills/still"+direc[i]+"%d.png" %(j))
        pic = transform.scale(pic,(grwh,grwh))
        stills.append(pic)
    return stills

player1=[]
player1.append(stills(1))
player1.append(loadsprites("ninja1","girlninja4",1,8)) #UP
player1.append(loadsprites("ninja1","girlninja1",1,8)) #DOWN
player1.append(loadsprites("ninja1","girlninja2",1,8)) #LEFT
player1.append(loadsprites("ninja1","girlninja3",1,8)) #RIGHT

player2=[]
player2.append(stills(2))
player2.append(loadsprites("ninja2","girlninja4",1,8)) #UP
player2.append(loadsprites("ninja2","girlninja1",1,8)) #DOWN
player2.append(loadsprites("ninja2","girlninja2",1,8)) #LEFT
player2.append(loadsprites("ninja2","girlninja3",1,8)) #RIGHT

###########SCREEN DEFINITIONS#################
def dhome():
     running = True
     screen.blit(bg,(0,0))
     dims = [Rect(340,350,383,81), Rect(340,450,383,81), Rect(340,550,383,81)]  #dims for each button
     goto = ["players", "howto", "scores"]  #pages buttons go to
     pics = [playpic, howpic, scorepic]     #pics for each button

     for rec in range(len(dims)):
          screen.blit(pics[rec],dims[rec])

     while running:
          click = False
          for evt in event.get():
               if evt.type==QUIT:
                    return "exit"
               if evt.type==MOUSEBUTTONDOWN:
                    click = True
          mx,my = mouse.get_pos()

          for rec in range(len(dims)):  #go to page clicked
               if click==True and dims[rec].collidepoint(mx,my):
                    page = goto[rec]
                    return page                   
          display.flip()

def howto():
    global page, mmbut 
    pgh = 1             #due to several how to pages, counter for which pg
    running = True
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                return "exit"
            if evt.type == MOUSEBUTTONDOWN:
                mb = mouse.get_pressed()
                mx,my = mouse.get_pos()
                if mb[0]==1:
                    #next pg # is based on current page user is on
                    if back.collidepoint(mx,my) and pgh  !=1:       
                        pgh -= 1
                    if nxt.collidepoint(mx,my) and pgh !=3:
                        pgh += 1
                    else:
                        if back.collidepoint(mx,my) and pgh == 1:
                            page = "home"
                            return page
                        if nxt.collidepoint(mx,my) and pgh == 3:
                            page = "home"
                            return page

        howpic = image.load("Backgrounds/howto"+str(pgh)+".png")
        screen.blit(howpic,(0,0))

        pbut=[image.load("Backgrounds/back.png"),image.load("Backgrounds/next.png")]
            
        back = Rect (50,650,150,51)     #previous page
        nxt = Rect (845,650,150,51)     #next page 

        #blitting next, back, main menu buttons based on current page 
        if pgh == 1 or pgh == 2:
            screen.blit(pbut[1],nxt)
        if pgh == 2 or pgh == 3:
            screen.blit(pbut[0],back)

        mmbut = transform.scale(mmbut,(150,51))

        if pgh == 1:
            screen.blit(mmbut,back)
        if pgh == 3:
            screen.blit(mmbut,nxt)

        display.flip()

def dtopscores():
    global page, mmbut
    click = False
    running = True
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                running = False
            if evt.type == MOUSEBUTTONDOWN:
                click = True

        mx,my=mouse.get_pos()
            
        back = image.load("Backgrounds/topscores1.jpg")
        screen.blit(back,(0,0))

        init()
        arialFont = font.SysFont("Silom",30)
        scores = []
        names = []
       
        x,y = 300,250           #coor of name 
        x1,y1= 600,250          #coor of score
        for line in open("Scores.txt").read().strip().split("\n"):
            n,s = line.split(", ")
            names.append(n)
            scores.append(s) 

        amt = 0         #number of entries in top score pg
        if len(names) >10:      #if scores file has more than 10, to just stop at 10
            amt=10
        else:
            amt = len(names)

        #blitting the names and scores of the top 10 
        for i in range(amt):
            namepic = arialFont.render(str(names[i]),True,(0,0,0))
            screen.blit(namepic,(x,y))
            scorepic = arialFont.render(str(scores[i]),True,(0,0,0))
            screen.blit(scorepic,(x1,y1))
            y+=50
            y1+=50

        #main menu button
        mmRect = Rect(800,650,200,70)
        mmbut = transform.scale(mmbut,(150,51))
        screen.blit(mmbut,mmRect)
        if mmRect.collidepoint(mx,my) and click == True:
                page = "home"
                return page
        

        display.flip()

#pick 1 or 2 player mode
def dplayers():
     global onep
     running = True
     screen.blit(bg,(0,0))
     dims = [Rect(300,350,203,264), Rect(550,350,203,264)]
     goto = ["dName", "levels"]
     pics = [p1pic, p2pic]

     for rec in range(len(dims)):
          screen.blit(pics[rec],dims[rec])
     
     while running:
          click = False
          for evt in event.get():
               if evt.type==QUIT:
                    return "exit"
               if evt.type==MOUSEBUTTONDOWN:
                    click = True

          mx,my = mouse.get_pos()

          for rec in range(len(dims)):
               if click==True and dims[rec].collidepoint(mx,my):
                    page = goto[rec]
                    if page=="dName": onep = True   #sends to Name page only if 1 player
                    else: onep = False              #so use as a flag change

                    return page
                    
          display.flip()     

#screen to enter player name
name = ""
def dName():
    global name, bg, page
    screen.blit(bg,(0,0))
    enpic = image.load("Screens/ename.png")
    enpic = transform.scale(enpic,(300,100))
    screen.blit(enpic,(375,350))

    #mckenzie getname() referenced 
    tFont = font.SysFont("Times New Roman", 16)
    back = screen.copy()        # copy screen so we can replace it when done
    textArea = Rect(450,400,250,100) # make changes here.
    
    typing = True
    while typing:
        for e in event.get():
            if e.type == QUIT:
                page = "home"   # puts QUIT back in event list so main quits
                return page
            if e.type == KEYDOWN:
                if e.key == K_BACKSPACE:    # remove last letter
                    if len(name)>0:
                        name = name[:-1]
                elif e.key == K_KP_ENTER or e.key == K_RETURN : 
                    typing = False
                    page = "meth"
                    return page
                elif e.key < 256:
                    name += e.unicode       # add character to ans
                    
        txtPic = tFont.render(name, True, (0,0,0))   #
        screen.blit(txtPic,(textArea.x+3,textArea.y+2))

        
        display.flip()
        screen.blit(back,(0,0))         #clears name box when backspacing 

#pick input method in 1p mode
def dmeth():
     global meth
     running = True
     screen.blit(bg,(0,0))
     dims = [Rect(300,350,203,264), Rect(550,350,203,264)]
     methods = ['mou','arr']
     pics = [mousepic, arrowpic]

     for rec in range(len(dims)):
          screen.blit(pics[rec],dims[rec])
     
     while running:
          click = False
          for evt in event.get():
               if evt.type==QUIT:
                    return "exit"
               if evt.type==MOUSEBUTTONDOWN:
                    click = True

          mx,my = mouse.get_pos()

          for rec in range(len(dims)):
               if click==True and dims[rec].collidepoint(mx,my):
                    page = "levels"
                    meth = methods[rec]     #sets input method
                    return page
                    
          display.flip()

lev = 0
levfile = "0"
#user chooses level to play (easy to difficult - 1 to 6)
def dlevels():
     global lev, levfile 
     running = True
     screen.blit(bg,(0,0))
     dims = [Rect(337,379,100,100),Rect(462,379,100,100),Rect(587,379,100,100),
             Rect(337,494,100,100),Rect(462,494,100,100),Rect(587,494,100,100)]

     levelpics=[]
     for i in range (1,7):
          pic = image.load("Backgrounds/levels"+str(i)+".png")
          pic = transform.scale(pic,(100,100))
          levelpics.append(pic)
          
     while running:
          click = False
          for evt in event.get():
               if evt.type==QUIT:
                    return "exit"
               if evt.type==MOUSEBUTTONDOWN:
                    click = True

          mx,my = mouse.get_pos()

          for rec in range(len(dims)):
               screen.blit(levelpics[rec],dims[rec])
               if click==True and dims[rec].collidepoint(mx,my):
                    if onep == True:
                        levfile = "1Player/"
                    else:
                        levfile = "2Player/"

                    lev = dims.index(dims[rec])+1

                    page = "game"
                    return page

          display.flip()

def dend():
     global end, win, score, arialFont
     running = True
     end = transform.scale(end,(1024,768))
     screen.blit(end,(0,0))

     if onep == True:
         win = "LEVEL SCORE: "+str(score)
     if onep == False:
         win = win

     init()
     arialFont = font.SysFont("Silom",70)
     
     winpic = arialFont.render(win,True,(0,0,0))
     screen.blit(winpic,(250,150))

     dims = [Rect(350,450,250,50), Rect(350,540,250,50), Rect(350,630,250,50)]
     goto = ["home", "levels", "exit"]
     pics = [image.load("Backgrounds/mmbut1.png"),image.load("Screens/continue.png"),
             image.load("Screens/quit.png")]

     for rec in range(len(dims)):
          screen.blit(pics[rec],dims[rec])
     
     while running:
          click = False
          for evt in event.get():
               if evt.type==QUIT:
                    return "exit"
               if evt.type==MOUSEBUTTONDOWN:
                    click = True

          mx,my = mouse.get_pos()

          for rec in range(len(dims)):
               if click==True and dims[rec].collidepoint(mx,my):
                    page = goto[rec]
                    return page
                    
          display.flip()

#########UTILITY DEFINITIONS########
##adds two lists
def add2(list1,list2):
     return [list1[0]+list2[0],list1[1]+list2[1]]

##gets value at grid location
def get(grid,loc):
     x,y=loc
     if 0<=y<len(grid) and 0<=x<len(grid[y]):
          return grid[y][x]
     return "neg"   #when location is at a border

##sets value at grid location
def sett(grid, loc, val):
    string = grid[loc[1]]
    str1,str2 = string[:loc[0]],string[loc[0]+1:]
    string = str1+val+str2
    floor[loc[1]]=string
    return grid

##returns a rect for given x,y coor
def rectdim(x,y):
     return (x*grwh+1,y*grwh+1,grwh-2,grwh-2)

#~~#

#returns value of something from the player's list
def f(lyst, obj):
     global pmod
     n = pmod.index(obj)
     return lyst[n]

#sets value of something in the player's list
def s(lyst,obj, val):
     global pmod
     n = pmod.index(obj)
     lyst[n]=val
     return lyst

#~~#
    
#returns T/F if new spot is a diagonal block
def diagonal(floor, nspot, digits):
     if get(floor,nspot) in digits and  2<=int(get(floor,nspot))<=5:
         return True
     return False

#returns new direction when player hits a diagonal
def changed(corn,d):
     global diagdir
     coin = corners.index(corn)        #index of corner type in lists
     if d not in diagdir[coin]:     #if hitting block from back side (not diag)
          d=0
     elif d==diagdir[coin][0]:      #else switch direction
          d=diagdirrev[coin][1]
     elif d==diagdir[coin][1]:
          d=diagdirrev[coin][0]
     return d

#changing colour of a spot (painting)
def colspot(floor, coor, col):
     global blankscreen, colvars
     screen.blit(blankscreen,(0,0))
     screen.blit(fill[colvars.index(col)],(coor[0]*grwh,coor[1]*grwh))
     blankscreen = screen.copy()        #change blankscreen to new screen
     floor = sett(floor, coor, "0")     #remove "topaint" var from floor
     return floor

#removes 1 from the num of blocks uncoloured when painted
def left(p, col):
     for c in range(len(f(p,'pcols'))):
          if f(p,'pcols')[c].lower()==col:
                f(p,'remain')[c]-=1
     return p

#returns RGB value for colour variable
def colour(collet):
     return colvals[ucolvars.index(collet.upper())]

#draws card for player w/ current colour picked
def drawcard(p):
     if f(p,'col')!='n':
         draw.rect(screen,colour(f(p,'col')),f(p,'cardrec'),0)
     screen.blit(f(p,'cardpic'),f(p,'cardrec'))
     s(p,'colchange',False) #reset flag

#draws the player colours and the # of blocks left of that col
def drawcard2(p):
     for c in range(len(f(p,'pcols'))):
          dims = rec(p,c)
          draw.rect(screen,colour(f(p,'pcols')[c]),dims,0)
          
          num = f(p,'remain')[c]
          bnum = cardFont.render(str(num),True,(0,0,0))
          screen.blit(bnum,dims)
     
     s(p,'colX',False)  #reset flag

#calcs rec dims under pcard for drawcard2 for displaying col info
def rec(p,num):
     x,y,w,h = f(p,'cardrec')
     x1 = x+(w//4)*num
     y1 = y+h
     return Rect(x1,y1,w//4,w//4)

#~~#

##blits all images for the floorplan of each level
def mplan():
     global blankscreen, spots, pspots, backpics, bucks, floor, p1, p2, onep
     ncols = [0,0,0,0] #list counter for X-spot colours in floor
     for y in range(len(floor)):
          for x in range(len(floor[y])):
               if floor[y][x] in digits:
                   screen.blit(backpics[int(floor[y][x])],(x*grwh,y*grwh))
               elif floor[y][x] in colvars:
                   screen.blit(spots[colvars.index(str(floor[y][x]))],(x*grwh,y*grwh))
                   ncols[colvars.index(str(floor[y][x]))]+=1
               elif floor[y][x] in ucolvars:
                   screen.blit(bucks[ucolvars.index(str(floor[y][x]))],(x*grwh,y*grwh))
        
     for c in range(len(f(p1,'pcols'))):    #changes col spot counters in p1's list
          f(p1,'remain')[c] = ncols[colvars.index(f(p1,'pcols')[c].lower())]
          
     if onep==False:        #changes col spot counters in p2's list
          for c in range(len(f(p2,'pcols'))):
               f(p2,'remain')[c] = ncols[colvars.index(f(p2,'pcols')[c].lower())]

     pspots = f(p1,'remain')[0]+f(p1,'remain')[1]   #used for calculating score in 1p mode
     blankscreen = screen.copy()

#controls the door where player enters/exits
def edoor():
     global onep
     doors=[]

     pic = image.load("picsnew/exitclosed.png")
     pic = transform.scale(pic,(grwh,grwh))
     doors.append(pic)
     pic = image.load("picsnew/exitopen.png")
     pic = transform.scale(pic,(grwh,grwh))
     doors.append(pic)

     
     r1,r2 = sum(f(p1,'remain')),sum(f(p2,'remain'))
     s1,s2 = f(p1,'score'),f(p2,'score')

     #open when he starts and open when done
     if onep== True:
        if r1 ==0 or s1 == 0:       #if remaining spots are 0 or he hasn't moved yet
            screen.blit(doors[1],(start[0]*grwh,start[1]*grwh))

     elif onep==False: 
         if r2 == 0 or s2 ==0 or r1 ==0 or s1 == 0:
             screen.blit(doors[1],(start[0]*grwh,start[1]*grwh))
      
     #closed while playing
     if r1>0 and s1>0:
         if onep == True:
             screen.blit(doors[0],(start[0]*grwh,start[1]*grwh))
         if onep == False and r2>0 and s2 > 0:
             screen.blit(doors[0],(start[0]*grwh,start[1]*grwh))

#----------------------------------------------------------------------------------------------
#counts sprite frame and resets drawNinja flag
def drawNinja(p):
     drawNinja2(p)
     s(p,'frame', f(p,'frame')+1)
     if f(p,'frame') >= len(f(p,'pics')[f(p,'d')-1]) or f(p,'d') == 0:
          s(p,'frame', 0)
     s(p,'dNinja', False)
     return p
    
#actually does the drawing
def drawNinja2(p):
     global floor
     if get(floor, f(p,'coor'))=="6":
          pic = f(p,'pics')[0][0]
     elif f(p,'d') != 0:
          pic = f(p,'pics')[f(p,'d')][int(f(p,'frame'))]
     elif f(p,'d') == 0 and f(p,'od')!= 0:
          pic = f(p,'pics')[0][f(p,'od')-1]
         
     screen.blit(pic,((f(p,'coor')[0]*grwh+grwh/2)-grwh//2,(f(p,'coor')[1]*grwh+grwh/2)-grwh//2))
     
#----------------------------------------------------------------------------------------------
def arrd(p):   #changes direction with arrowkey input
     global press, keys
     if press==True and f(p,'d')==0:
          if keys[K_UP]:
              s(p,'d', 1)
              s(p,'vert', True)
          elif keys[K_DOWN]:
              s(p,'d', 2)
              s(p,'vert', True)
          elif keys[K_LEFT]:
              s(p,'d', 3)
              s(p,'vert', False)
          elif keys[K_RIGHT]:
              s(p,'d', 4)
              s(p,'vert', False)
          s(p,'score',f(p,'score')+1)   #add 1 move to score
     return p

def moud(p):   #changes direction with mouse input
     global click
     if click==True and f(p,'d')==0:
          mx,my = mouse.get_pos()
          cx,cy= (f(p,'coor')[0]*grwh)+(grwh//2),(f(p,'coor')[1]*grwh)+(grwh//2)    #current pos of ninja on x-y grid

          #slope is calculated to determine quadrant in which dir is determined
          if cx != mx:
               slope = ((float(cy-my))/(float(cx-mx)))
               #up or down
               if slope > 1 or slope < -1:
                    if my < cy:
                         s(p,'d', 1)
                         s(p,'vert', True)
                    elif my > cy:
                         s(p,'d', 2)
                         s(p,'vert', True)
               #left or right 
               elif -1 < slope < 1 :
                    if mx < cx:
                         s(p,'d', 3)
                         s(p,'vert', False)
                    if mx > cx:
                         s(p,'d', 4)
                         s(p,'vert', False)

          s(p,'score',f(p,'score')+1)   #add 1 move to score
     return p

#---------------------------------------------------------------------------------------
#score calculator outputs to "Scores" file
score = 0 
def dscore():
     global pspots, name, score
     names =[]  #clears names and scores lists
     scores=[]

     #reads previous scores to add new score to file
     for line in open("Scores.txt").read().strip().split("\n"):
        n, s = line.split(", ")
        names.append(n)
        scores.append(int(s))

     #calculating score based on number of assigned spots and moves
     score = (1000 * pspots)//f(p1,"score")
     scores.append(score)
     names.append(name)

     #sorts scores
     nscores = [i for i in scores]
     nscores.sort(reverse=True)

     #rearranging names to align with sorted scores
     nnames =[]
     for i in range(len(nscores)):
         p = scores.index(nscores[i])
         nnames.append(names[p])
         names[p] = ""
         scores[p] = 0

     out = open("Scores.txt","w")
     for i in range(len(nscores)):
          if nnames[i]!="" and nscores[i]!=0:
               out.write(str(nnames[i]))
               out.write(", ")
               out.write(str(nscores[i]))
               out.write("\n")
     out.close()
     return score

###############-------------------------------------------------------------------------------
#everything that happens in a move
def PoneA(p):
     global screen, floor, press, keys, click
     global digits, direct, colvars, ucolvars, colvals, corners

#method of moving to next spot
     if f(p,'inmeth')=='arr':
           arrd(p)
     elif f(p,'inmeth')=='mou':
           moud(p)

#move a spot in direction every running loop
     nspot=add2(f(p,'coor'),direct[f(p,'d')])

#if spot is a diagonal from the box side: dir=still
     if get(floor, nspot) in corners and changed(get(floor,nspot),f(p,'d'))==0:
               s(p,'d', 0)
  #elif nspot is a block or at border, direction=still and draw ninja
     elif get(floor,nspot)=="1" or get(floor,nspot)=="neg":
          s(p,'d', 0)
          s(p,'dNinja', True)
    #^otherwise, change coor to newspot
     else: s(p,'coor', nspot)
     
#if new coor is diag, change direction
     if diagonal(floor, f(p,'coor'), digits)==True:
          s(p,'d', changed(get(floor,f(p,'coor')),f(p,'d')))

#if new coor is not a block nor diag, draw player #REGULAR MOVE 
     if get(floor, f(p,'coor'))!= "1" and get(floor, f(p,'coor')) not in corners and get(floor,f(p,'coor')) != "6" :
          s(p,'dNinja', True)
         
#if new coor is a ladder, draw player and d=0
     if get(floor, f(p,'coor'))=="6":
          s(p,'d', 0)
          s(p,'dNinja', True)
#__________________________________

#if new coor is bucket, pick colour
     if get(floor,f(p,'coor')) in f(p,'pcols'):
          s(p,'col', get(floor,f(p,'coor')))
          s(p,'colchange',True) #T flag to redraw pcard with new colour

#if new coor is X and col matches: colspot and reduce list of X's count
     if get(floor, f(p,'coor')) in colvars and f(p,'col').lower() == get(floor,f(p,'coor')):
          p = left(p, get(floor, f(p,'coor')))
          colspot(floor, f(p,'coor'), get(floor, f(p,'coor')))
          s(p,'colX',True)  #T flag to redraw counter under pcard for user info

#if moving, old direction = d (end of loop right now)
     if f(p,'d') != 0:
          s(p,'od', f(p,'d'))
         
     return p

#-------------------------------------------------------------------------------------------
#game screen
def game():
     global p1, p2, onep, meth, col1, col2, blankscreen, remain, start
     global press, click, keys, win, page
     
     if onep==True and meth=="mou":  #if only 1 player, alternative inmeth
          s(p1,'inmeth','mou')

     s(p1,'pcols',col1)
     s(p2,'pcols',col2)
     
     #background of game 
     gb = image.load("Screens/gameback.jpg")
     gb = transform.scale(gb,(1024,768))
     screen.blit(gb,(0,0))

     init()
     moveFont = font.SysFont("Silom",30)
     
     mplan()
     edoor()

     drawcard(p1)
     drawcard2(p1)
     if onep==False:
         drawcard(p2)
         drawcard2(p2)

     blankscreen = screen.copy()

     running=True
     while running:
          press=False
          click=False
          for evt in event.get():
               if evt.type==QUIT:
                    running=False
                    page = "home"
                    return page
               if evt.type==KEYDOWN:
                    press=True
                    keys=key.get_pressed()
               if evt.type==MOUSEBUTTONDOWN:
                    click = True

#calculate movements for player(s)
          p1 = PoneA(p1)
          if onep==False:
               p2 = PoneA(p2)

#blit blankscreen, add player cards, add colour info, recopy screen before blitting door and ninjas
          screen.blit(blankscreen,(0,0))
          if f(p1,'colchange')==True:
                    drawcard(p1)
          if f(p2,'colchange')==True:
                    drawcard(p2)
          if f(p1,'colX')==True:
               drawcard2(p1)
          if f(p2,'colX')==True:
               drawcard2(p2)
          blankscreen = screen.copy()
          edoor()
          
          if f(p1,'dNinja')==True:
               p1=drawNinja(p1)
          if onep==False:
               if f(p2,'dNinja')==True:
                    p2=drawNinja(p2)
                    
#if 1 player, all spots coloured and coor==start pos: end game
          if onep==True:
               moves = moveFont.render("# Moves: " + str(f(p1,'score')),True,(0,0,0))
               screen.blit(moves,(430,20))
               
               if sum(f(p1,'remain'))==0 and f(p1,"coor") == start:
                    page = "end"
                    return page

#if 2 player, either player has both: all spots coloured and coor==start pos:
    #end game, that player wins
          if onep==False:        
               if sum(f(p1,'remain'))==0 and f(p1,"coor") == start:
                    win = "PLAYER 1 WON!"
                    page = "end"
                    return page
               if sum(f(p2,'remain'))==0 and f(p2,"coor") == start:
                    win = "PLAYER 2 WON!"
                    page = "end"
                    return page
          display.flip()


##################MAIN LOOP####################
page = "home"
onep = True
meth = 'arr'

press=False
click=False
keys=[]
 
pspots =0 #counter for # of spots in level

blankscreen = screen.copy()

while page !="exit":
     for evt in event.get():
          if evt.type==QUIT:
               running=False
    
     if page == "home":
          page = dhome()
          
     if page == "howto":
          page = howto()
     
     if page == "scores":
          page = dtopscores()

     if page == "players":
          page = dplayers()

     if page == "dName":
         page = dName()
          
     if page == "meth":
          page = dmeth()

     if page == "levels":
          page = dlevels()

     if page == "game":

          #certain variables must be reseted 
          floor=[]  #2D list for floor plan
          start = [0,0] #start coords (door)
          col1 = [] #colours for p1
          col2 = [] #colours for p2
          win = ""  #mssg for winner

          rfloor(levfile,lev)
          
          init()
          cardFont = font.SysFont("Times New Roman",16,True,False)

          ##player info = [current coordinates, current direction, old direction, flag for vert/hor movement,
            ##colour player has picked, player colours, blocks remaining of each colour, input method, #of moves
              ##list of sprite pics for player, flag for drawing player, frame for sprite,
                ##flag for whether colour has changed (draw pcard), player pic for card, rect dims for pcard,
                  ##flag for colouring spot (draw colour/blocks info under pcard)]
          pmod = ['coor', 'd', 'od', 'vert', 'col', 'pcols','remain', 'inmeth', 'score',
                  'pics', 'dNinja', 'frame', 'colchange','cardpic','cardrec','colX']    #model player list
          p1 = [start, 0, 1, False, 'n', [], [0,0,0,0], 'arr', 0,
                player1, False, 0, False, p1card, p1crec, False]
          p2 = [start, 0, 1, False, 'n', [], [0,0,0,0], 'mou', 0,
                player2, False, 0, False, p2card, p2crec, False]

          page = game()


     if page == "end":
          if onep == True:    #if 1p mode, prints score
              score = dscore()
          page = dend()

quit()
