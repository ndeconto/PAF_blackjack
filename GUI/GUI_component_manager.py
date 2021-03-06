from time import clock, sleep
from pygame import *
from pygame.locals import *

CONTINUE                =   0
EXIT_GAME_LOOP          =   -1
CLOSE_WINDOW            =   1
REPLAY                  =   2

class GUIComponentManager:
    """
        class which controls GUIComponents, ie calls their methods update and
        manage_event
    """


    def __init__(self, component_list, frequency):
        """
            component_list :
                    list of the components which will be managed by the instance


            frequency :
                number of update per second
        """



        self.component_list     =   sorted(component_list,
                                           key = lambda c : c.display_level)
        self.period             =   1. / frequency



    def add_component(self, new_component):

        self.component_list.append(new_component)


    def argsort(seq):
        return 


    def run(self):

        running = True

        while running:

            t_start = clock()

            ev_list = event.get()
            new_component_list = []


            #manage "special" events
            for ev in ev_list:

                if ev.type == QUIT:
                    running = False
                    ret = CLOSE_WINDOW
                    break

            if not running : break

           

            for c in self.component_list:

                ret = c.manage_event(ev_list)

                if ret == EXIT_GAME_LOOP or ret == CLOSE_WINDOW or ret == REPLAY:
                    running = False
                    break
                
                l = c.update(self.component_list)
                new_component_list.extend(l)

            if not running : break

            

            #sort by display_level
            index_order = [i for i, x in sorted(enumerate(new_component_list),
                                        key = lambda x : x[1].display_level)]
            to_update = []
             
            for i in index_order :
                to_update.append(new_component_list[i].display())


            #probably not optimal, to_update should be used to refresh modified
            #parts only; here the entiere screen is refreshed
            display.flip()


            self.component_list = new_component_list


            sleep(max(0, self.period - (clock() - t_start)))


        return ret

            
