class Player :
    def __init__(self, numberplayer) :
        self.numberplayer = numberplayer
        if numberplayer == 1:
            self.direction = 'right'
        else:
            self.direction = 'left'

        
    def bind(self, menu) :
        if self.numberplayer == 1 :
            menu.root.bind('<Right>', self.right)
            menu.root.bind('<Left>', self.left)
            menu.root.bind('<Up>' , self.up)
            menu.root.bind('<Down>', self.down)
        else :
            menu.root.bind('<d>', self.right)
            menu.root.bind('<q>', self.left)
            menu.root.bind('<z>' , self.up)
            menu.root.bind('<s>', self.down)

    def up(self,event):
        self.change_direction('up')
        print('up')
    def down(self,event):
        self.change_direction('down')
        print('down')
    def right(self,event):
        self.change_direction('right')
        print('right')
    def left(self,event):
        self.change_direction('left')
        print('left')

    def change_direction(self, direction_target) :
        if self.direction == 'up' and direction_target != 'down' :
            self.direction = direction_target
        elif self.direction == 'down' and direction_target != 'up' :
            self.direction = direction_target
        elif self.direction == 'left' and direction_target != 'right' :
            self.direction = direction_target
        elif self.direction == 'right' and direction_target != 'left' :
            self.direction = direction_target
        elif self.direction == '' :
            self.direction = direction_target

    def get_direction(self) :
        return self.direction
