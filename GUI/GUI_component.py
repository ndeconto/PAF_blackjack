from pygame import *

from time import clock

from GUI_component_manager import CONTINUE, EXIT_GAME_LOOP

class GUIComponent:
    

    def __init__(self, display_level, position, size,
                 events_to_handle, events_actions,
                 background=None, identifier=""):

        """
            parameters description :

            display_level :
                the more the display_level is high, the more the component is in
                foreground. display_level is not directly used by this class,
                but by the function which calls the method update() (the
                GUI_ComponentManager)

            position :
                the position of the component; must be a tuple (x, y)

            size :
                the size of the component; must be a tuple (width, height)

            events_to_handle :
                list of pygame.event.EventType.type which describes which
                eventtypes have an effect on the component

            events_actions :
                list of functions which respectively describes which action is
                done when an event is handled. More precisely, events_actions[i]
                is called when events_to_handle[i] is handled.
                As far as the parameters of those functions are concerned, they
                must respect an given format. See GUI_component_manager.py

            background (optionnal):
                background of the component

            identifier (optionnal):
                just to reconize the component easily
        """


        self.display_level      =   display_level
        self.position           =   position
        self.size               =   size
        self.events_to_handle   =   events_to_handle
        self.background         =   background
        self.id                 =   identifier

        self.alive              =   True

        self.todo               =   []


    def do_in_x_seconds(self, x, function):
        """
            x seconds after calling this method, function() will be called

            NB : if the component is killed, the function won't be called
        """

        self.todo.append((clock(), x, function))


    def update(self, other_components):
        """
            this method is called periodically, and can modify the component

            this function returns a list.
            This is a list of components which can contain :
                self if this component is still "alive" ; if self is not present
                    in that list, this component will be removed by the manager
                new components which just have been created by this function
        
        """

        if self.alive:

            t = clock()
            l = []
            for t2, x, f in self.todo:
                if t - t2 > x:
                    f()
                else: l.append((t2, x, f))
            self.todo = l
            
            return [self]

        return []


    def die(self):
        """
            removes proprely the component
        """
        
        self.alive = False

        


    def display(self):
        """
            prints the component on the screen
            must return the area which has to be refresh on screen
            if nothing has been displayed, it can return Rect(0, 0, 0, 0)
        """

        if self.background == None: return

        r = Rect(self.position, self.size)
        display.get_surface().blit(self.background, r)

        return r


    #---------------------------------- TODO -------------------------------#
    # the caller of this function should give extra parameters to this function
    #in order to enable it to use events_actions functions with context's
    #parameters
    def manage_event(self, event_list):
        """
            handles the events whose type is in self.events_to_handle
            ignores the others

            this function must return GUI_component_manager.CONTINUE most of the
            time, GUI_component_manager.EXIT_GAME_LOOP to quit the main loop of
            the component manager
        """

        #NB : loop's complexity is maybe not optimal...
        for ev in event_list:

            try :
                i = event_list.index(ev.type)
            except ValueError:  #ev.type is not in the list
                continue        #event is ignored

            # ------------------------------ TODO ----------------------------#
            # see commentar above for the parameters
            self.events_actions[i]()


        return CONTINUE

    

        
class ImageComponent(GUIComponent):
    """
        for components which are images
    """

    def __init__(self, display_level, position, img, events_to_handle=[],
                 events_actions=[], identifier=""):
        """
            for display_level, position, events_to_handle, events_actions, and
            identifier, see GUIComponent

            img :
                will be the background of the GUIComponent
                can be a string (= path to an image file) or a surface
        """

        if isinstance(img, str):
            img = image.load(img).convert_alpha()

        GUIComponent.__init__(self, display_level, position, img.get_size(),
                              events_to_handle, events_actions, background=img,
                              identifier=identifier)
                              


class FlashingImageComponent(GUIComponent):

    def __init__(self, display_level, position, l_img, period,
                 events_to_handle=[], events_actions=[], identifier=""):
        """
            same as ImageComponent, but displays alternatively different
            images
            l_img is the list of images
            period is the time (in second) between the image change
            NB : this period cannot be smaller than game manager's period
            so you can set period to 0, it means "change as fast as possible"

            all images must have the same size
        """

        self.l_img = []
        self.cpt = 0
        self.last_change = clock()

        for img in l_img:
            if isinstance(img, str):
                self.l_img.append(image.load(img).convert_alpha())
            else :
                self.l_img.append(img)


        self.period = period

            
        GUIComponent.__init__(self, display_level, position, img.get_size(),
                              events_to_handle, events_actions, background=img,
                              identifier=identifier)


    def update(self, other_comp):

        r = GUIComponent.update(self, other_comp)

        if (clock() - self.last_change > self.period):

            self.cpt = (self.cpt + 1) % len(self.l_img)
            self.background = self.l_img[self.cpt]

            self.last_change = clock()

        return r
                     
    
             
        
class Bouton(ImageComponent):

    def __init__(self, display_level, position, img, on_click, identifier=""):
        """
            represente un bouton d'image img.
            onClick doit etre une fonction sans parametre qui est appelee
            quand on clique sur le bouton
        """

        ImageComponent.__init__(self, display_level, position, img,
                                identifier=identifier)

        self.on_click = on_click

        self.click_in = False

        self.enable = True



    def activer(self):
        """
            quand le bouton est actif, on peut cliquer dessus
            quand il est inactif, ca ne fait rien
        """
        self.enable = True

    def desactiver(self):
        self.enable = False


    def manage_event(self, ev_list):
        
        ImageComponent.manage_event(self, ev_list)

        for ev in ev_list:


            if (ev.type == MOUSEBUTTONDOWN and
                Rect(self.position, self.size).collidepoint(mouse.get_pos())):

                self.click_in = True


            if ev.type == MOUSEBUTTONUP :

                if Rect(self.position, self.size).collidepoint(mouse.get_pos()):

                    if self.click_in and self.enable:
                        self.on_click()

                else :
                    self.click_in = False

        return CONTINUE

        
class PauseComponent(GUIComponent):
    """
        invisible component which waits that one specified key is pressed
        then sends a signal to the GameManager
    """

    def __init__(self, pressed_key, signal):
        """
            pressed_key :
                descripbes the key one wich the component will react
                must be a keyboard constant, ie K_RETURN, K_a, ...
                (cf pygame documentation for an exhaustive list)
        """

        GUIComponent.__init__(self, 0, (0, 0), (0, 0), [], [])
        self.signal = signal
        self.pressed_key = pressed_key

    def manage_event(self, ev_list):

        for ev in ev_list:

            if ev.type == KEYDOWN and ev.key == self.pressed_key:
                return self.signal

        return CONTINUE




class Mise(GUIComponent):
    """
        objet graphique de la mise
    """

    DISPLAY_LEVEL = 4
    FONT = "font/321impact.ttf"
    X_FACTOR = 1.2
    Y_FACTOR = 1.2

    #decalage relatif du txt
    OFFSET_TXT_X = 0.05
    OFFSET_TXT_Y = 0.1

    def __init__(self, x, position, font_size, font_color=(255, 255, 255),
                 background_color=(0, 0, 0)):
        
        self.x = x
        self.font = font.Font(self.FONT, font_size)

        self.background_color = background_color
        self.font_color = font_color

        self.render_txt()

        x, y = self.txt.get_size()
        bg = Surface((x * self.X_FACTOR, y * self.Y_FACTOR))
        bg.fill(self.background_color)
        GUIComponent.__init__(self, self.DISPLAY_LEVEL, position, bg.get_size(),
                              [], [], background=bg)

    def render_txt(self):
        self.txt = self.font.render("Mise : " + str(self.x), 1, self.font_color)

    def display(self):

        s = display.get_surface()
        #s.blit(self.background, self.position)
        self.render_txt()
        s.blit(self.txt, (self.position[0] + self.size[0] * self. OFFSET_TXT_X,
                          self.position[1] + self.size[1] * self. OFFSET_TXT_Y))

        return Rect(self.position, self.size)

    def doubler(self):
        self.x *= 2

        

    
        
