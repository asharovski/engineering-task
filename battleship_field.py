'''
Created on 10 Sep 2019

@author: alex
'''
import collections
import random

SHIPS_SIZE_DICT = {"Carrier":4, "Cruiser":3, "Destroyer":2, "Submarine":1}
coordinate = collections.namedtuple( 'Coordinate', ( 'x', 'y' ) )
GAME_MATRIX_SIZE = 10


class Navy( object ):

    def __init__( self ):
        self.not_available_coordinates = set()
        self.ships = []
        self.matrix = [["-"] * GAME_MATRIX_SIZE for _ in range( GAME_MATRIX_SIZE )]
        self.columns = ["  0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    def update_not_available_coordinates( self, ship ):
        """ This method add all coordinates and neighboring coordinates of new ship to not_available_coordinates"""

        def add_not_available_neighbor_cordinates_of_horizontal_ship():
            for ship_coordinate in ship.ship_coordinates:
                x = ship_coordinate.x - 1
                if x >= 0:
                    above_coordinate = coordinate( x=x, y=ship_coordinate.y )
                    self.not_available_coordinates.add( above_coordinate )
                x = ship_coordinate.x + 1
                if x <= 9:
                    below_coordinate = coordinate( x=x, y=ship_coordinate.y )
                    self.not_available_coordinates.add( below_coordinate )
            y = ship.start.y - 1
            if y >= 0:
                left_coordinate = coordinate( ship.start.x, y )
                self.not_available_coordinates.add( left_coordinate )
                x = left_coordinate.x - 1
                if x >= 0:
                    left_above = coordinate( x, left_coordinate.y )
                    self.not_available_coordinates.add( left_above )
                x = left_coordinate.x + 1
                if x <= 9:
                    left_bolow = coordinate( x, left_coordinate.y )
                    self.not_available_coordinates.add( left_bolow )
            y = ship.end.y + 1
            if y <= 9:
                right_coordinate = coordinate( ship.end.x, y )
                self.not_available_coordinates.add( right_coordinate )
                x = right_coordinate.x - 1
                if x >= 0:
                    right_above = coordinate( x, right_coordinate.y )
                    self.not_available_coordinates.add( right_above )
                x = right_coordinate.x + 1
                if x <= 9:
                    right_bolow = coordinate( x, right_coordinate.y )
                    self.not_available_coordinates.add( right_bolow )

        def add_not_available_neighbor_cordinates_of_vertical_ship():
            for ship_coordinate in ship.ship_coordinates:
                y = ship_coordinate.y - 1
                if y >= 0:
                    left_coordinate = coordinate( x=ship_coordinate.x, y=y )
                    self.not_available_coordinates.add( left_coordinate )
                y = ship_coordinate.y + 1
                if y <= 9:
                    right_coordinate = coordinate( x=ship_coordinate.x, y=y )
                    self.not_available_coordinates.add( right_coordinate )
            x = ship.start.x - 1
            if x >= 0:
                above_coordinate = coordinate( x=x, y=ship.start.y )
                self.not_available_coordinates.add( above_coordinate )
                y = above_coordinate.y - 1
                if y >= 0:
                    above_left = coordinate( x=above_coordinate.x, y=y )
                    self.not_available_coordinates.add( above_left )
                y = above_coordinate.y + 1
                if y <= 9:
                    above_right = coordinate( x=above_coordinate.x, y=y )
                    self.not_available_coordinates.add( above_right )
            x = ship.end.x + 1
            if x <= 9:
                below_coordinate = coordinate( x=x, y=ship.end.y )
                self.not_available_coordinates.add( below_coordinate )
                y = below_coordinate.y - 1
                if y >= 0:
                    below_left = coordinate( x=below_coordinate.x, y=y )
                    self.not_available_coordinates.add( below_left )
                y = below_coordinate.y + 1
                if y <= 9:
                    below_right = coordinate( x=below_coordinate.x, y=y )
                    self.not_available_coordinates.add( below_right )

        if ship.direction == "horizontal":
            add_not_available_neighbor_cordinates_of_horizontal_ship()
        else:
            add_not_available_neighbor_cordinates_of_vertical_ship()

        self.not_available_coordinates = self.not_available_coordinates.union( ship.ship_coordinates )

    def add_ship( self, ship ):
        self.ships.append( ship )

    def add_ship_to_matrix( self, ship ):
        for coordinate in ship.ship_coordinates:
            x = coordinate.x
            y = coordinate.y
            row = self.matrix[x]
            row[y] = 'X'

    def print_navy( self ):
        row_num = 0
        print "\t\t", "   ".join( self.columns )
        for row in self.matrix:
            print "\t\t", row_num, "   ".join( row )
            row_num += 1


class Ship( object ):

    def __init__( self, ship_name, ship_size ):
        self.name = ship_name
        self.ship_size = ship_size
        self.ship_coordinates = set()

    def create_ship( self , not_available_coordinates ):
        """
        This method create ship with random coordinates,if any coordinate is in not_available_coordinates,
        then method will rty again create.
        """
        while True:
            direction = random.choice( ["horizontal", "vertical"] )
            start = random.randint( 0, GAME_MATRIX_SIZE )
            end = start + self.ship_size
            if end <= GAME_MATRIX_SIZE :
                for i in range( start, end ):
                    if direction == "horizontal":
                        xy = coordinate( x=start, y=i )
                    else:
                        xy = coordinate( x=i, y=start )
                    self.ship_coordinates.add( xy )

                if not not_available_coordinates.intersection( self.ship_coordinates ):
                    self.end = xy
                    break
                else:
                    self.ship_coordinates = set()
        self.direction = direction
        if self.direction == "horizontal":
            self.start = coordinate( x=self.end.x, y=self.end.y - self.ship_size + 1 )
        else:
            self.start = coordinate( x=self.end.x - self.ship_size + 1 , y=self.end.y )
        return self.ship_coordinates


def create_ship_and_add_to_navy( ship, navy ):
    ship.create_ship( navy.not_available_coordinates )
    navy.update_not_available_coordinates( ship )
    navy.add_ship( ship )
    navy.add_ship_to_matrix( ship )


def placeSubmarine( navy ):
    ship_size = SHIPS_SIZE_DICT.get( "Submarine" )
    if ship_size is not None:
        ship = Ship( ship_name="Submarine", ship_size=ship_size )
        create_ship_and_add_to_navy( ship, navy )


def placeDestroyer( navy ):
    ship_size = SHIPS_SIZE_DICT.get( "Destroyer" )
    if ship_size is not None:
        ship = Ship( ship_name="Destroyer", ship_size=ship_size )
        create_ship_and_add_to_navy( ship, navy )


def placeCruiser( navy ):
    ship_size = SHIPS_SIZE_DICT.get( "Cruiser" )
    if ship_size is not None:
        ship = Ship( ship_name="Cruiser", ship_size=ship_size )
        create_ship_and_add_to_navy( ship, navy )


def placeCarrier( navy ):
    ship_size = SHIPS_SIZE_DICT.get( "Carrier" )
    if ship_size is not None:
        ship = Ship( ship_name="Carrier", ship_size=ship_size )
        create_ship_and_add_to_navy( ship, navy )


if __name__ == "__main__":
    navy = Navy()
    placeCarrier( navy )
    placeCruiser( navy )
    placeDestroyer( navy )
    placeSubmarine( navy )
    navy.print_navy()

