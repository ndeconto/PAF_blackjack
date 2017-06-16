from pygame import *

from GUI_component_manager import CONTINUE, EXIT_MAIN_LOOP

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
            time, GUI_component_manager.EXIT_MAIN_LOOP to quit the main loop of
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


    def manage_event(self, ev_list):
        
        ImageComponent.manage_event(self, ev_list)

        for ev in ev_list:


            if (ev.type == MOUSEBUTTONDOWN and
                Rect(self.position, self.size).collidepoint(mouse.get_pos())):

                self.click_in = True


            if ev.type == MOUSEBUTTONUP :

                if Rect(self.position, self.size).collidepoint(mouse.get_pos()):

                    if self.click_in: self.on_click()

                else :
                    self.click_in = False

        

        
