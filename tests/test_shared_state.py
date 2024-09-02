import unittest
from common.shared_state import Player, SharedState


class TestSharedState(unittest.TestCase):
    def setUp(self):
        self.shared_state = SharedState()

    def test_sync_player_state(self):
        player = Player(id="1", name="TestPlayer")
        self.shared_state.sync_player_state(player)
        self.assertIn("1", self.shared_state.players)
        self.assertEqual(self.shared_state.players["1"].name, "TestPlayer")

    def test_get_player_by_name(self):
        player = Player(id="1", name="TestPlayer")
        self.shared_state.sync_player_state(player)
        retrieved_player = self.shared_state.get_player_by_name("TestPlayer")
        self.assertEqual(retrieved_player.id, "1")

    def test_remove_player(self):
        player = Player(id="1", name="TestPlayer")
        self.shared_state.sync_player_state(player)
        removed_name = self.shared_state.remove_player("1")
        self.assertEqual(removed_name, "TestPlayer")
        self.assertNotIn("1", self.shared_state.players)

    def test_update_player_event(self):
        player = Player(id="1", name="TestPlayer")
        self.shared_state.sync_player_state(player)
        self.shared_state.update_player_event("1", "resume")
        self.assertTrue(self.shared_state.players["1"].resumed)


if __name__ == "__main__":
    unittest.main()
