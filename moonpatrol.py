#!/usr/bin/env python3
'''
@author  Francesco Ciociola - https://kekko01.altervista.org/blog/
@from Michele Tomaiuolo - http://www.ce.unipr.it/people/tomamic
@license This software is free - http://www.gnu.org/licenses/gpl.html
'''

import g2d as g2d, random, webbrowser
from classes import Arena, Rover, Background, Hole, Hill, Bullet, Alien, AlienBullet, Robot, RobotBullet

ARENA_W = 480
ARENA_H = 360
arena = Arena((ARENA_W, ARENA_H))
#b1 = Ball(arena, (40, 80))
#b2 = Ball(arena, (80, 40))
#g = Ghost(arena, (120, 80))
version="2.0"
ask=False
sound=g2d.load_audio("assets/sound.mp3")
sprites = g2d.load_image("assets/moon-patrol.png")
backgroundsimage=g2d.load_image("assets/moon-patrol-bg.png")
startbackground=g2d.load_image("assets/splash.png")
backgrounds=[Background((0,0),2,(0,0),(510,257)),Background((510,0),2,(0,0),(510,257)),Background((0,180),4,(0,384),(510,127)),Background((510,180),4,(0,384),(510,127)),Background((0,300),6,(0,515),(510,127)),Background((510,300),6,(0,515),(510,127))]
holes=[]
hills=[]
bullets=[]
aliens=[]
aliensbullets=[]
robots=[]
robotsbullets=[]
spawntimer=0
game=True
writing=False
with open("assets/score","r") as target:
    highscore=target.read()
    highscore=highscore.strip()
with open("assets/nick","r") as target:
    nick=target.read()
    nick=nick.strip()
with open("assets/lang/choice","r") as target:
    for line in target:
        langset = line.strip()
message=[]
with open("assets/lang/"+langset,"r") as target:
    for text in target:
        message.append(text.strip())
score=0
level=1
difficulty=30
again=True
reset_highscore=False
def tick():
    global spawntimer,game,score,writing,level,ask,difficulty,nick,multiplayer,rover,rover1,again,highscore,reset_highscore
    if game:
        if not ask:
            g2d.draw_image(startbackground,(0,0))
            if nick=="null":
                readme=g2d.confirm(message[0])
                if readme:
                    webbrowser.open("https://github.com/Kekko01/My-Moon-Patrol/blob/master/README.md")
            while nick=="null" or not nick:
                nick=g2d.prompt(message[1])
                with open("assets/nick","w") as target:
                    target.write(nick)
                with open("assets/nick","r") as target:
                    nick=target.read()
                    nick=nick.strip()

            multiplayer=g2d.confirm(message[2])
            rover = Rover(arena, (60, 300), 1)
            if multiplayer:
                rover1 = Rover(arena, (100, 300), 2)
            ask=True
        g2d.play_audio(sound,True)
        if score % 13 == 0 and score!=0:
            score+=2
            difficulty+=3
            level+=1
        if g2d.key_pressed("ArrowUp"):
            rover.go_up()
        if g2d.key_pressed("ArrowRight"):
            rover.go_right()
    #    if g2d.key_pressed("ArrowDown"):
    #        rover.go_down()
        if g2d.key_pressed("ArrowLeft"):
            rover.go_left()
        if (g2d.key_released("ArrowUp") or
              g2d.key_released("ArrowRight") or
              g2d.key_released("ArrowDown") or
              g2d.key_released("ArrowLeft")):
            rover.stay()

        if multiplayer:
            if g2d.key_pressed("w"):
                rover1.go_up()
            if g2d.key_pressed("d"):
                rover1.go_right()
        #    if g2d.key_pressed("ArrowDown"):
        #        rover.go_down()
            if g2d.key_pressed("a"):
                rover1.go_left()
            if (g2d.key_released("w") or
                  g2d.key_released("d") or
                  g2d.key_released("s") or
                  g2d.key_released("a")):
                rover1.stay()

        arena.move_all()  # Game logic

        g2d.clear_canvas()

        if g2d.key_pressed("Spacebar"):
            bullets.append(Bullet(arena, rover.x_position(), rover.y_position(), 0))
            bullets.append(Bullet(arena, rover.x_position(), rover.y_position(), 1))
        if g2d.key_pressed("c") and multiplayer:
            bullets.append(Bullet(arena, rover1.x_position(), rover1.y_position(), 0))
            bullets.append(Bullet(arena, rover1.x_position(), rover1.y_position(), 1))

        for a in backgrounds:
            a.move()
            g2d.draw_image_clip(backgroundsimage, a.symbol(), a.position())

        for a in arena.actors():
            if a.symbol() != (0, 0, 0, 0):
                g2d.draw_image_clip(sprites, a.symbol(), a.position())
            else:
                g2d.fill_rect(a.position())

        if spawntimer==0:
            if random.randint(0,20)==0:
                holes.append(Hole(arena, (131,167), (ARENA_W,300)))
                spawntimer=120
            elif random.randint(0,20)==0:
                holes.append(Hole(arena, (159,167), (ARENA_W,300)))
                spawntimer=120
            elif random.randint(0,20)==0:
                hills.append(Hill(arena,(80,203),(13,16),1))
                spawntimer=120
            elif random.randint(0,20)==0:
                hills.append(Hill(arena,(112,199),(13,16),2))
                spawntimer=120
            elif random.randint(0,10)==0:
                aliens.append(Alien(arena))
                spawntimer=120
            elif random.randint(0,10)==0:
                robots.append(Robot(arena))
                spawntimer=120
        if spawntimer>0:
            spawntimer-=1

        for a in holes:
            if a.x_position()<=0:
                holes.remove(a)
            if a.collide(rover):
                game=False
            if multiplayer:
                if a.collide(rover1):
                    game=False

        for a in hills:
            if a.x_position()<=0:
                hills.remove(a)
                arena.remove(a)
            if a.collide(rover):
                game=False
            if multiplayer:
                if a.collide(rover1):
                    game=False
            for i in bullets:
                if a.collide(i):
                    if a.get_life()==2:
                        a.take_life()
                        bullets.remove(i)
                        arena.remove(i)
                        score+=1
                    else:
                        bullets.remove(i)
                        hills.remove(a)
                        arena.remove(i)
                        arena.remove(a)
                        score+=1
        for a in bullets:
            if a.x_position()>ARENA_W:
                bullets.remove(a)
                arena.remove(a)
            if a.y_position()<0:
                bullets.remove(a)
                arena.remove(a)
        for a in aliens:
            if a.x_position()<=0:
                aliens.remove(a)
                arena.remove(a)
            if random.randint(0,120)==0:
                aliensbullets.append(AlienBullet(arena, (a.x_position(),a.y_position())))
            for i in bullets:
                if a.collide(i):
                    bullets.remove(i)
                    a.delete()
                    #aliens.remove(a)
                    arena.remove(i)
                    arena.remove(a)
                    score+=1
        for a in robots:
            if a.x_position()<=0:
                robots.remove(a)
                arena.remove(a)
            if random.randint(0,60)==0:
                robotsbullets.append(RobotBullet(arena, (a.x_position(),a.y_position())))
            for i in bullets:
                if a.collide(i):
                    bullets.remove(i)
                    a.delete()
                    #aliens.remove(a)
                    arena.remove(i)
                    arena.remove(a)
                    score+=1
            if a.collide(rover):
                game=False
            if multiplayer:
                if a.collide(rover1):
                    game=False
        for a in aliensbullets:
            if a.y_position()>300:
                if random.randint(0,5)==0:
                    holes.append(Hole(arena, (131,167), (a.x_position(),300)))
                    aliensbullets.remove(a)
                    arena.remove(a)
            if a.collide(rover):
                game=False
            if multiplayer:
                if a.collide(rover1):
                    game=False

        for a in robotsbullets:
            if a.y_position()<=0:
                aliensbullets.remove(a)
                arena.remove(a)
            if a.collide(rover):
                game=False
            if multiplayer:
                if a.collide(rover1):
                    game=False

    else:
        g2d.pause_audio(sound)
        if again:
            again=g2d.confirm(message[5])
            if again:
                for i in bullets:
                    bullets.remove(i)
                    arena.remove(i)
                for i in holes:
                    holes.remove(i)
                    arena.remove(i)
                for i in hills:
                    hills.remove(i)
                    arena.remove(i)
                for i in aliens:
                    aliens.remove(i)
                    arena.remove(i)
                for i in aliensbullets:
                    aliensbullets.remove(i)
                    arena.remove(i)
                for i in robots:
                    robots.remove(i)
                    arena.remove(i)
                for i in robotsbullets:
                    robotsbullets.remove(i)
                    arena.remove(i)
                spawntimer=0
                level=1
                difficulty=30
                rover.reset_position()
                if multiplayer:
                    rover1.reset_position()
                if int(highscore)<score:
                    highscore=score
                    str(highscore)
                    reset_highscore=True
                score=0
                game=True
        else:
            if int(highscore)<score:
                highscore=score
                str(highscore)
                reset_highscore=True
            g2d.set_color((255,0,0))
            g2d.draw_text("Game Over",(110,170),50)
            g2d.draw_image_clip(sprites, rover.drop_symbol(), rover.position())
            rover.drop()
            rover.position()
            if multiplayer:
                g2d.draw_image_clip(sprites, rover1.drop_symbol(), rover1.position())
                rover1.drop()
                rover1.position()
            if not writing and reset_highscore:
                with open("assets/score","w") as target:
                    target.write(str(score))
                online=g2d.confirm(message[3])
                if online:
                    url="http://kekko01files.altervista.org/projects/moonpatrol_scores.php?nick="+str(nick)+"&score="+str(score)+"&version="+version
                    webbrowser.open(url)
                writing=True
            else:
                if ask:
                    online=g2d.confirm(message[4])
                    if online:
                        url="http://kekko01files.altervista.org/projects/moonpatrol_scores.php"
                        webbrowser.open(url)
                    ask=False
    g2d.draw_text("Highscore:", (20, 20), 30)
    g2d.draw_text(highscore, (170, 10), 40)
    g2d.draw_text("Score:", (330, 20), 30)
    g2d.draw_text(str(score), (420, 10), 40)
    g2d.draw_text("Level:", (20, 70), 30)
    g2d.draw_text(str(level), (100, 60), 40)

def main():
    g2d.init_canvas(arena.size())
    g2d.main_loop(tick, difficulty)

main()
