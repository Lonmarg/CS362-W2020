from unittest import TestCase
import Dominion
import testUtility


# Setup the essentials for the game of Dominion that is likely used by a lot of these tests so I don't have duplicate
# code all over
def basicsetup(self):
    # Data setup
    self.players = testUtility.getplayernames(["Annie", "*Ben", "*Carla"])
    self.nV = testUtility.setupvictorycards(self.players)
    self.nC = testUtility.setupcurses(self.players)
    self.box = testUtility.getboxes(self.nV)
    self.supply_order = testUtility.setupsupplyorder()

    # Setup essential and random supply cards
    self.supply = testUtility.getrandomsupply(self.box, 10)
    self.supply = testUtility.setupsupply(self.supply, self.players, self.nV, self.nC)
    self.trash = testUtility.setuptrash()

    # Create our human Player
    self.player = Dominion.Player('Annie')


# A helper function that tests if the two passed parameters are equal
def assertequal(thing1, thing2):
    if thing1 == thing2:
        return
    else:
        assert False


# A helper function that tests if the two passed parameters are NOT equal
def assertnotequal(thing1, thing2):
    if thing1 == thing2:
        assert False
    else:
        return


# A helper function that tests if thing1 is greater than thing2
def assertgreater(thing1, thing2):
    if thing1 > thing2:
        return
    else:
        assert False


# A test class which tests the Coin Card class in Dominion.py
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


# A test class which tests the Action Card class in Dominion.py
class TestAction_Card:
    def setUp(self):
        basicsetup(self)

        # Setup test cards parameters
        self.name = 'TestCard1'
        self.cost = 2
        self.actions = 1
        self.cards = 3
        self.buys = 2
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

    # Test the cards Use function
    def test_use(self):
        # Call init to setup the cards parameters and the games essential parameters
        self.test_init()

        # Clear the players hand to make testing easier
        self.player.hand.clear()
        # Ensure the Played list and Hand list are currently empty
        assertequal(self.player.played, [])
        assertequal(self.player.hand, [])

        # Add the created Action Card to the players hand
        self.player.hand.append(self.card)

        # Ensure the card was added to the players hand
        assertequal(self.player.played, [])
        assertequal(self.player.hand[0], self.card)

        # Call the use function on the created card
        self.card.use(self.player, self.trash)

        # Ensure the card was successfully used which removes it from the players hand and adds it to their played
        assertequal(self.player.played[0], self.card)
        assertequal(self.player.hand, [])

    # Test the cards Augment function
    def test_augment(self):
        # Call init to setup the cards parameters and the games essential parameters
        self.test_init()

        # Define the parameters on Player that the augment function changes
        self.player.actions = 1
        self.player.buys = 1
        self.player.purse = 4
        # Clear the players hand to make testing easier
        self.player.hand.clear()

        # Ensure all the players parameters that will be changed are setup correctly
        assertequal(self.player.actions, 1)
        assertequal(self.player.buys, 1)
        assertequal(self.player.purse, 4)
        assertequal(self.player.hand, [])
        assertequal(len(self.player.hand), 0)

        # Add the created card to the players hand
        self.player.hand.append(self.card)
        # Ensure the card was added to their hand
        assertequal(self.player.hand[0], self.card)
        # Ensure they don't have any other cards
        assertequal(len(self.player.hand), 1)

        # Call the augment function on the card we created
        self.card.augment(self.player)

        # Ensure all the parameters that augment changes were changed successfully
        assertequal(self.player.actions, 2)
        assertequal(self.player.buys, 3)
        assertequal(self.player.purse, 8)
        assertequal(self.player.hand[0], self.card)
        assertequal(len(self.player.hand), 4)


# A test class which tests the Player class in Dominion.py
class TestPlayer:
    # Setup the essential parameters to test Dominion
    def setUp(self):
        basicsetup(self)

    # Test the Draw function on the Player class in Dominion.py
    def test_draw(self):
        self.setUp()

        # Loop through the current hand copying the cards back into the deck as we're going to clear the hand
        for i in range(len(self.player.hand)):
            self.player.deck.append(self.player.hand[i])

        # Clear the hand to make testing easier
        self.player.hand.clear()

        # Ensure the hand is empty
        assertequal(len(self.player.hand), 0)

        # Create a tempDeck used for testing the deck after we've drawn
        tempDeck = []

        # Move everything from the players deck into their discard pile
        for i in range(len(self.player.deck)):
            tempDeck.append(self.player.deck[i])
            self.player.discard.append(self.player.deck[i])

        # Clear the decks as everything was copied to the discard
        self.player.deck.clear()

        # Ensure the discard now has all the cards from the original deck
        assertequal(self.player.discard, tempDeck)
        # Ensure the deck has been cleared
        assertequal(self.player.deck, [])

        # Call the draw function and store the card that was drawn
        drawnCard = self.player.draw()
        # Remove the drawn card from our deck copy
        tempDeck.remove(drawnCard)

        # The Draw function checks if the deck is empty, if it is it shuffles the discard and copies it all
        # into the deck. The above Draw call should have done this so the Deck should now have everything
        # that was in the discard and the discard should have been emptied
        assertequal(self.player.discard, [])

        # Used to determine if the discard was properly copied back into the deck
        decksEqual = False

        # Loop through the original deck and look for each card within the new deck that was constructed by the
        # Draw function. If the Draw function is working properly they should be identical
        for i in tempDeck:
            for j in self.player.deck:
                if i == j:
                    decksEqual = True
                    break
            if not decksEqual:
                assert False

        # The draw function should add a card to the players hand. Since the hand was previously cleared there should
        # be 1 card in the players hand. Ensure there is only 1 card and it's the card that the draw function returned
        assertequal(len(self.player.hand), 1)
        assertequal(self.player.hand[0], drawnCard)

    # Testing the action_balance function in Dominion.py
    # The function this is testing is used by NPCs to determine which list of cards they should use when purchasing
    # new cards. It considers how many actions they currently have in their deck and changes purchase options
    # accordingly
    def test_action_balance(self):
        self.setUp()

        # Clear the "stack" so we can setup the player with specific numbers of actions to make testing more clear
        self.player.deck.clear()
        self.player.hand.clear()
        self.player.played.clear()
        self.player.aside.clear()
        self.player.hold.clear()

        # Give the player a single card with 1 action to avoid a division by 0 crash in action_balance
        self.player.deck.append(Dominion.Action_card('TestCard', 1, 1, 0, 0, 0))

        # Ensure the balance is currently 0 with only 1 action
        assertequal(self.player.action_balance(), 0)

        # Clear the deck again
        self.player.deck.clear()

        # Give the player a bunch of cards with no actions
        self.player.deck.append(Dominion.Action_card('TestCard', 1, 0, 0, 0, 0))
        self.player.deck.append(Dominion.Action_card('TestCard', 1, 0, 0, 0, 0))
        self.player.deck.append(Dominion.Action_card('TestCard', 1, 0, 0, 0, 0))
        self.player.deck.append(Dominion.Card('TestCard', 'None', 1, 0, 0))
        self.player.deck.append(Dominion.Card('TestCard', 'None', 1, 0, 0))

        assertequal(self.player.action_balance(), -42)

        # Clear the deck again
        self.player.deck.clear()

        # Give the player a bunch of cards with 3 actions
        self.player.deck.append(Dominion.Action_card('TestCard', 1, 1, 0, 0, 0))
        self.player.deck.append(Dominion.Action_card('TestCard', 1, 1, 0, 0, 0))
        self.player.deck.append(Dominion.Action_card('TestCard', 1, 1, 0, 0, 0))
        self.player.deck.append(Dominion.Card('TestCard', 'None', 1, 0, 0))
        self.player.deck.append(Dominion.Card('TestCard', 'None', 1, 0, 0))

        assertequal(self.player.action_balance(), 0)

        # Clear the deck again
        self.player.deck.clear()

        # Give the player a bunch of cards with 1 action
        self.player.deck.append(Dominion.Action_card('TestCard', 1, 1, 0, 0, 0))
        self.player.deck.append(Dominion.Action_card('TestCard', 1, 0, 0, 0, 0))
        self.player.deck.append(Dominion.Action_card('TestCard', 1, 0, 0, 0, 0))
        self.player.deck.append(Dominion.Card('TestCard', 'None', 1, 0, 0))
        self.player.deck.append(Dominion.Card('TestCard', 'None', 1, 0, 0))

        assertequal(self.player.action_balance(), -28)

        # Clear the deck again
        self.player.deck.clear()

        # Give the player a bunch of cards with 500 actions
        self.player.deck.append(Dominion.Action_card('TestCard', 1, 500, 0, 0, 0))
        self.player.deck.append(Dominion.Action_card('TestCard', 1, 0, 0, 0, 0))
        self.player.deck.append(Dominion.Action_card('TestCard', 1, 0, 0, 0, 0))
        self.player.deck.append(Dominion.Card('TestCard', 'None', 1, 0, 0))
        self.player.deck.append(Dominion.Card('TestCard', 'None', 1, 0, 0))

        assertequal(self.player.action_balance(), 6958)

        # Clear the deck again
        self.player.deck.clear()

        # Give the player a bunch of nonsense cards with 300 actions
        self.player.deck.append(Dominion.Action_card('TestCard', 1, 100, 0, 0, 0))
        self.player.deck.append(Dominion.Action_card('TestCard', 1, 100, 0, 0, 0))
        self.player.deck.append(Dominion.Action_card('TestCard', 1, 100, 0, 0, 0))
        self.player.deck.append(Dominion.Card('TestCard', 'None', 1, 0, 0))
        self.player.deck.append(Dominion.Card('TestCard', 'None', 1, 0, 0))

        assertequal(self.player.action_balance(), 4158)

    def test_cardsummary(self):
        self.setUp()

        # Clear the "stack" so we can setup the player with specific numbers of actions to make testing more clear
        self.player.deck.clear()
        self.player.hand.clear()
        self.player.played.clear()
        self.player.aside.clear()
        self.player.hold.clear()

        # Add some cards to the deck so we can get a summary of them to test
        self.player.deck.append(Dominion.Action_card('TestCard1', 1, 1, 0, 0, 0))
        self.player.deck.append(Dominion.Action_card('TestCard2', 1, 1, 0, 0, 0))
        self.player.deck.append(Dominion.Action_card('TestCard3', 1, 1, 0, 0, 0))
        self.player.deck.append(Dominion.Action_card('TestCard2', 1, 1, 0, 0, 0))
        self.player.deck.append(Dominion.Action_card('TestCard2', 1, 1, 0, 0, 0))
        self.player.deck.append(Dominion.Action_card('TestCard3', 1, 1, 0, 0, 0))

        # Get a summary of the current cards in the players stack
        summary = self.player.cardsummary()

        # Confirm each key has the correct number of cards
        assertequal(summary['TestCard1'], 1)
        assertequal(summary['TestCard2'], 3)
        assertequal(summary['TestCard3'], 2)

        assertequal(summary["VICTORY POINTS"], 0)

        # Clear the deck again
        self.player.deck.clear()

        self.player.deck.append(Dominion.Card('TestCard1', 'victory', 1, 0, 5))
        self.player.deck.append(Dominion.Card('TestCard1', 'victory', 1, 0, 3))
        self.player.deck.append(Dominion.Card('TestCard1', 'victory', 1, 0, 1))
        self.player.deck.append(Dominion.Card('TestCard1', 'victory', 1, 0, 1))
        self.player.deck.append(Dominion.Card('TestCard1', 'victory', 1, 0, 4))
        self.player.deck.append(Dominion.Card('TestCard1', 'victory', 1, 0, 1))

        summary = self.player.cardsummary()

        assertequal(summary['TestCard1'], 6)
        assertequal(summary["VICTORY POINTS"], 15)


    def test_calcpoints(self):
        self.setUp()

        # Clear the "stack" so we can setup the player with specific numbers of actions to make testing more clear
        self.player.deck.clear()
        self.player.hand.clear()
        self.player.played.clear()
        self.player.aside.clear()
        self.player.hold.clear()

        # Give the player three victory cards but no Gardens
        self.player.deck.append(Dominion.Card('TestCard1', 'victory', 1, 0, 5))
        self.player.deck.append(Dominion.Card('TestCard1', 'victory', 1, 0, 3))
        self.player.deck.append(Dominion.Card('TestCard1', 'victory', 1, 0, 1))

        # Ensure they have a total of 9 victory points
        assertequal(self.player.calcpoints(), 9)

        # Clear the players deck so we can try a different set of cards
        self.player.deck.clear()

        # Give the player three victory cards, one of which is a Garden
        self.player.deck.append(Dominion.Card('TestCard1', 'victory', 1, 0, 5))
        self.player.deck.append(Dominion.Card('TestCard1', 'victory', 1, 0, 3))
        self.player.deck.append(Dominion.Card('Gardens', 'victory', 1, 0, 1))

        # Ensure they have a total of 9 victory points, the garden only gives 1 as they don't have 20+ cards total
        assertequal(self.player.calcpoints(), 9)

        # Clear the players deck so we can try a different set of cards
        self.player.deck.clear()

        # Give the player 20+ cards with 1 Garden
        self.player.deck.append(Dominion.Card('TestCard1', 'victory', 1, 0, 5))
        self.player.deck.append(Dominion.Card('TestCard1', 'victory', 1, 0, 3))
        self.player.deck.append(Dominion.Card('TestCard1', 'victory', 1, 0, 1))
        self.player.deck.append(Dominion.Card('TestCard1', 'victory', 1, 0, 1))
        self.player.deck.append(Dominion.Card('TestCard1', 'victory', 1, 0, 1))
        self.player.deck.append(Dominion.Card('TestCard1', 'victory', 1, 0, 1))
        self.player.deck.append(Dominion.Card('TestCard1', 'victory', 1, 0, 1))
        self.player.deck.append(Dominion.Card('TestCard1', 'victory', 1, 0, 1))
        self.player.deck.append(Dominion.Card('TestCard1', 'victory', 1, 0, 1))
        self.player.deck.append(Dominion.Card('TestCard1', 'victory', 1, 0, 1))
        self.player.deck.append(Dominion.Card('TestCard1', 'action', 1, 0, 0))
        self.player.deck.append(Dominion.Card('TestCard1', 'action', 1, 0, 0))
        self.player.deck.append(Dominion.Card('TestCard1', 'action', 1, 0, 0))
        self.player.deck.append(Dominion.Card('TestCard1', 'action', 1, 0, 0))
        self.player.deck.append(Dominion.Card('TestCard1', 'action', 1, 0, 0))
        self.player.deck.append(Dominion.Card('TestCard1', 'action', 1, 0, 0))
        self.player.deck.append(Dominion.Card('TestCard1', 'action', 1, 0, 0))
        self.player.deck.append(Dominion.Card('TestCard1', 'action', 1, 0, 0))
        self.player.deck.append(Dominion.Card('TestCard1', 'action', 1, 0, 0))
        self.player.deck.append(Dominion.Card('TestCard1', 'action', 1, 0, 0))
        self.player.deck.append(Dominion.Card('Gardens', 'victory', 1, 0, 1))

        # Ensure they have a total of 19 victory points, the garden should give + 2
        assertequal(self.player.calcpoints(), 19)

class TestGameOver:
    # Setup the essential parameters to test Dominion
    def setUp(self):
        basicsetup(self)

    # Test the gameover function in Dominion.py
    def test_gameover(self):
        self.setUp()

        # Ensure we have the following cards in our supply
        assertgreater(len(self.supply["Gold"]), 0)
        assertgreater(len(self.supply["Duchy"]), 0)
        assertgreater(len(self.supply["Curse"]), 0)

        # Ensure the game is setup properly to satisfy the gameover function
        assertequal(Dominion.gameover(self.supply), False)

        #Loop through our supply removing all the Gold, Duchy, and Curse cards
        for i in range(len(self.supply["Gold"])):
            self.supply["Gold"].pop()

        for i in range(len(self.supply["Duchy"])):
            self.supply["Duchy"].pop()

        for i in range(len(self.supply["Curse"])):
            self.supply["Curse"].pop()

        # Ensure we successfully removed these cards from our supply
        assertequal(len(self.supply["Gold"]), 0)
        assertequal(len(self.supply["Duchy"]), 0)
        assertequal(len(self.supply["Curse"]), 0)

        # Ensure the game successfully triggers the gameover state once 3 supply cards piles are gone
        assertequal(Dominion.gameover(self.supply), True)

        # Ensure there are Province cards in the supply
        assertequal(len(self.supply["Province"]), 12)

        # Whitebox testing lets me look at the logic in gameover and see that province is checked before anything else
        # so even if there are 3 piles missing, it will return gameover True first if Province is empty. Note, this
        # probably isn't a super great idea as a SWE could decide to change the logic for gameover which could break
        # this test

        # Remove all Province cards from the supply
        for i in range(len(self.supply["Province"])):
            self.supply["Province"].pop()

        # Ensure all Province cards have been removed
        assertequal(len(self.supply["Province"]), 0)

        # Ensure the game over state returns True
        assertequal(Dominion.gameover(self.supply), True)


