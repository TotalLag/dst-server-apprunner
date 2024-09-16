"""
Test Shared State Module

This module contains unit tests for the SharedState class from the common.shared_state module.
It verifies the correct functionality of various methods in the SharedState class,
including player synchronization, retrieval, removal, and event updating.
"""

import unittest
from common.shared_state import Player, SharedState


class TestSharedState(unittest.TestCase):
    def setUp(self):
        """
        Set up a fresh SharedState instance before each test.
        """
        self.shared_state = SharedState()

    def test_sync_player_state(self):
        """
        Test the sync_player_state method of SharedState.

        This test verifies that:
        1. A new player can be added to the shared state.
        2. The player's information is correctly stored.
        """
        player = Player(id="1", name="TestPlayer")
        self.shared_state.sync_player_state(player)
        self.assertIn("1", self.shared_state.players)
        self.assertEqual(self.shared_state.players["1"].name, "TestPlayer")

    def test_get_player_by_name(self):
        """
        Test the get_player_by_name method of SharedState.

        This test verifies that:
        1. A player can be retrieved by their name.
        2. The correct player information is returned.
        """
        player = Player(id="1", name="TestPlayer")
        self.shared_state.sync_player_state(player)
        retrieved_player = self.shared_state.get_player_by_name("TestPlayer")
        self.assertEqual(retrieved_player.id, "1")

    def test_remove_player(self):
        """
        Test the remove_player method of SharedState.

        This test verifies that:
        1. A player can be removed from the shared state.
        2. The correct player name is returned upon removal.
        3. The player is no longer in the shared state after removal.
        """
        player = Player(id="1", name="TestPlayer")
        self.shared_state.sync_player_state(player)
        removed_name = self.shared_state.remove_player("1")
        self.assertEqual(removed_name, "TestPlayer")
        self.assertNotIn("1", self.shared_state.players)

    def test_update_player_event(self):
        """
        Test the update_player_event method of SharedState.

        This test verifies that:
        1. A player's event status can be updated.
        2. The 'resumed' flag is correctly set after a 'resume' event.
        """
        player = Player(id="1", name="TestPlayer")
        self.shared_state.sync_player_state(player)
        self.shared_state.update_player_event("1", "resume")
        self.assertTrue(self.shared_state.players["1"].resumed)


if __name__ == "__main__":
    unittest.main()
