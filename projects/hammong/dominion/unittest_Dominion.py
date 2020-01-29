from unittest import TestCase
import Dominion
import testUtility

class TestCard:

    def setUp(self):
        # Data setup
        self.player = testUtility.GetPlayers()
        self.nV = testUtility.GetCurses(self.players)
        self.nC = testUtility.GetVictoryCards(self.players)
        self.box = testUtility.GetBoxes(self.nV)
        self.supply_order = testUtility.GeSupplyOrder()

        # Pick n cards from box to be in the supply
        self.supply = testUtility.GetSupply(self.box, 5, self.players, self.nV, self.nC)
        self.trash = []

    def test_react(self):
        self.fail()