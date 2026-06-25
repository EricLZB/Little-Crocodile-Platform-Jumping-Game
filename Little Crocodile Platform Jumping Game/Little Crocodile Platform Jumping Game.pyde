add_library('minim')

def setup():
    global player_x, player_y, player_vy, player_size, music1, music2, minim
    player_x=270
    player_y=700
    player_vy=0
    player_size=60
    
    minim=Minim(this)
    music1=minim.loadFile("start.mp3")
    music2=minim.loadFile("fail.MP3")
    
    global begin_platform_x, begin_platform_y, begin_platform_w, begin_platform_h
    begin_platform_w=100
    begin_platform_h=20
    begin_platform_x=width/2-begin_platform_w/2
    begin_platform_y=height-begin_platform_h-30
    
    global score, platforms_x, platforms_y, platforms_w, platforms_h, grav, jump_force, scroll_speed, game_over
    score=0
    platforms_x=[]
    platforms_y=[]
    platforms_w=60
    platforms_h=20
    grav=0.2
    jump_force=-8
    scroll_speed=6
    game_over=False
    
    global bombs, candies, crocodile, sky, Candy, visible_candy, a
    bombs=[]
    candy=[]
    visible_candy=[]
    
    global bombs_probability, candies_probability
    bombs_probability=[]
    candies_probability=[]
    a=0
    size(600, 900)
    Candy=loadImage("Candy.png")
    crocodile=loadImage("little_crocodile.jpg")
    sky=loadImage("sky.jpg")
    for i in range(10):
        platforms_x.append(random(0,width-platforms_w))
        platforms_y.append(height-i*80-200)
        bombs_probability.append(random(0,1))
        candies_probability.append(random(0,1))
        visible_candy.append(1)
    
def generate():
    global platforms_x, platforms_y, bombs_probability, candies_probability
    global begin_platform_x, begin_platform_y, begin_platform_w, begin_platform_h
    begin_platform_w=100
    begin_platform_h=20
    begin_platform_x=width/2-begin_platform_w/2
    begin_platform_y=height-begin_platform_h-30
    
    for i in range(10):
        platforms_x[i]=random(0,width-platforms_w)
        platforms_y[i]=height-i*80-200
        bombs_probability[i]=random(0,1)
        candies_probability[i]=random(0,1)
        visible_candy[i]=1
        
def draw_platforms():
    fill(100, 200, 100)
    rect(begin_platform_x, begin_platform_y, begin_platform_w, begin_platform_h)
    for i in range(10):
        fill(100, 200, 100)
        rect(platforms_x[i], platforms_y[i], platforms_w, platforms_h)
        update_platforms()
        if bombs_probability[i]<0.1:
            fill(255, 0, 0)
            ellipse(platforms_x[i]+platforms_w/2, platforms_y[i]-platforms_h/2, 20, 20)
        else:
            if candies_probability[i]<0.17:
                if visible_candy[i]==1:
                    image(Candy, platforms_x[i]+platforms_w/2-25, platforms_y[i]-platforms_h/2-25, 50, 50)

def update_platforms():
    for i in range(10):
        if platforms_y[i]>height:
            platforms_y[i]=20
            platforms_x[i]=random(0,width-platforms_w)
            bombs_probability[i]=random(0,1)
            candies_probability[i]=random(0,1)

def check_platform_collision():
    global player_vy, game_over, score, visble_candy
    if (player_x+player_size>begin_platform_x and 
            player_x<begin_platform_x+begin_platform_w and 
            player_y+player_size>begin_platform_y and 
            player_y+player_size<begin_platform_y+begin_platform_h and 
            player_vy>0):
            player_vy=jump_force
    for i in range(10):
        if (player_x+player_size>platforms_x[i] and 
            player_x<platforms_x[i]+platforms_w and 
            player_y+player_size>platforms_y[i] and 
            player_y+player_size<platforms_y[i]+platforms_h and 
            player_vy>0):
            player_vy=jump_force
            
        if bombs_probability[i]<0.1:
            if (player_x+player_size>platforms_x[i]+platforms_w/2-10 and 
                player_x<platforms_x[i]+platforms_w/2+10 and 
                player_y+player_size>platforms_y[i]-10 and 
                player_y<platforms_y[i]):
                game_over=True
                
        if candies_probability[i]<0.17:
            if (player_x+player_size>platforms_x[i]+platforms_w/2-25 and 
                player_x<platforms_x[i]+platforms_w/2+25 and 
                player_y+player_size>platforms_y[i]-25 and 
                player_y<platforms_y[i]):
                if visible_candy[i]==1:
                    visible_candy[i]=0
                    score+=20

def update_player():
    global player_vy, player_y, player_x, game_over, score
    
    player_vy+=grav
    player_y+=player_vy

    if keyPressed:
        if keyCode==LEFT:
            player_x-=5
        elif keyCode==RIGHT:
            player_x+=5
    
    if player_x<0: 
        player_x=width
    if player_x>width: 
        player_x=0
    if player_y>height+player_size:
        game_over=True
    
    if (begin_platform_y-player_y-player_size)//10>score:
        score=int((begin_platform_y-player_y-player_size)//10)
        
def scrolling():
    global player_y, begin_platform_y
    if player_y<height/3:
        scroll=height/3-player_y
        player_y+=scroll
        begin_platform_y+=scroll
        for i in range(10):
            platforms_y[i]+=scroll
            
def draw():
    global a, score
    image(sky, 0, 0, width, height)
    
    if a==1:
        if game_over:
            music1.pause() 
            music1.rewind()
            music2.play()
            draw_game_over()
        else:
            music2.rewind()
            music1.play()
            update_player()
            check_platform_collision()
            draw_platforms()
            scrolling()
            image(crocodile, player_x, player_y, player_size, player_size)
            textSize(24)
            fill(255,0,0)
            text('Score:'+str(score), 65, 30)
    else:
        draw_start_screen()

def mousePressed():
    global a
    if a==0:
        a=1
    elif game_over:
        if dist(mouseX, mouseY, 150, 150) < 75:
            exit()
        elif dist(mouseX, mouseY, 450, 150) < 75:
            restart_game()

def draw_game_over():
    textSize(32)
    textAlign(CENTER)
    fill(255, 0, 0)
    text("Game Over!", width/2, height/2)
    text("You got Score:"+str(score),width/2, height/2+30)
    fill(255, 0, 0)
    ellipse(150, 150, 150, 150)
    textSize(32)
    fill(0)
    text("Close", 150, 155)
    fill(100, 200, 100)
    ellipse(450, 150, 150, 150)
    fill(0)
    text("Restart", 450, 155)

def draw_start_screen():
    textSize(48)
    textAlign(CENTER)
    fill(255, 0, 0)
    text("Press mouse to start", width/2, height/2)
    textSize(36)
    text("instructions:", 120, 32)
    textSize(24)
    text("Press the keyboard left and right keys to control", 315, 64)
    text("the little crocodile move and on the stages", 285, 96)
    text("if the little crocodile can get a candy,",252, 150)
    text("it can get extra 20 score.",181, 180)
    text("if the little crocodile get the red bomb",257,230) 
    text("or fall down to the bottom, the game is over",290,260)
    textSize(26)
    text("(score: depend on the height of the crocidle)",296, 620)

def restart_game():
    global game_over, a
    global player_x, player_y, player_vy, score
    player_x=270
    player_y=700
    player_vy=0
    score=0    
    generate()
    game_over=False
    a=1
    
