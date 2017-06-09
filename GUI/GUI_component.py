from pygame import *

class GUIComponent:
    

    def __init__(self, display_level, position, size,
                 events_to_handle, events_actions,
                 background=None):

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
        """


        self.display_level      =   display_level
        self.position           =   position
        self.size               =   size
        self.events_to_handle   =   events_to_handle
        self.bg                 =   background

        


    def update(self):
        """
            prints the component on the screen
        """

        if self.background == None: return

        r = Rect(self.position, self.size)
        display.get_surface().blit(background, r)
        display.update(r)


    #---------------------------------- TODO -------------------------------#
    # the caller of this function should give extra paramters to this function
    #in order to enable it to use events_actions functions with context's
    #parameters
    def manage_event(self, event_list):
        """
            handles the events whose type is in self.events_to_handle
            ignores the others
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

    

        
        
        

        

        
