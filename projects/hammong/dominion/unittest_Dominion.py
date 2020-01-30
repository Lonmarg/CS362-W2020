from unittest import TestCase
import Dominion
import testUtility


def basicsetup(self):
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


def assertequal(thing1, thing2):
    if thing1 == thing2:
        return
    else:
        assert False

class TestCard:

    def setUp(self):
        basicsetup(self)

    def test_init(self):
        # initialize test data
        self.setUp()
        cost = 1
        buypower = 5

        # instantiate the card object
        card = Dominion.Coin_card(self.player.name, cost, buypower)

        # verify that the class variables have the expected values
        assertequal('Annie', card.name)
        assertequal(buypower, card.buypower)
        assertequal(cost, card.cost)
        assertequal("coin", card.category)
        assertequal(0, card.vpoints)

    def test_react(self):
        pass


class TestAction_Card:
    def setUp(self):
        basicsetup(self)

        # Setup test cards parameters
        self.name = 'TestCard1'
        self.cost = 2
        self.actions = 0
        self.cards = 0
        self.buys = 0
        self.coins = 4


    def test_init(self):
        self.setUp()

        # instantiate the card object
        self.card = Dominion.Action_card(self.name, self.cost, self.actions, self.cards, self.buys, self.coins)

        # verify that the class variables have the expected values
        assertequal('TestCard1', self.card.name)
        assertequal(self.cost, self.card.cost)
        assertequal(self.actions, self.card.actions)
        assertequal(self.cards, self.card.cards)
        assertequal(self.buys, self.card.buys)
        assertequal(self.coins, self.card.coins)

    # I need to setup the players Deck, Hand, discard, etc as this function will mess with all of them
    def test_use(self):
        assertequal(self.player.played, [])
        self.card.use(self.player, self.trash)
        assertequal(self.player.played, [])


    def test_augment(self):
        assert False
