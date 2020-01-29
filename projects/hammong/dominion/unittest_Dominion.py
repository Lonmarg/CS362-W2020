from unittest import TestCase
import Dominion
import testUtility

class TestCard:

    def setUp(self):
        # Data setup
        self.players = testUtility.getplayernames(["Annie", "*Ben", "*Carla"])
        self.nV = testUtility.setupvictorycards(self.players)
        self.nC = testUtility.setupcurses(self.players)
        self.box = testUtility.getboxes(self.nV)
        self.supply_order = testUtility.setupsupplyorder()

        # Pick n cards from box to be in the supply
        self.supply = testUtility.getrandomsupply(self.box, 10)
        self.supply = testUtility.setupsupply(self.supply, self.players, self.nV, self.nC)
        self.trash = testUtility.setuptrash()
        self.player = Dominion.Player('Annie')


    def test_int(self):
        #initialize test data
        self.setUp()
        cost = 1
        buypower = 5

        #instantiate the card object
        card = Dominion.Coin_card(self.player.name, cost, buypower)

        #verify that the class variables have the expected values
        self.assertequal('Annie', card.name)
        self.assertequal(buypower, card.buypower)
        self.assertequal(cost, card.cost)
        self.assertequal("coin", card.category)
        self.assertequal(0, card.vpoints)


    def test_react(self):
        pass

    def assertequal(self, thing1, thing2):
        if thing1 == thing2:
            return True
        else:
            self.fail()