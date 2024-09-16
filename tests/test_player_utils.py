"""
Test Player Utils Module

This module contains unit tests for the player utility functions from the common.player_utils module.
It verifies the correct extraction of player information from various log line formats,
including player join, leave, and spawn events.
"""

import unittest
from common.player_utils import (
    extract_player_info_from_join,
    extract_player_id_from_leave,
    extract_player_character_from_spawn,
)


class TestPlayerUtils(unittest.TestCase):
    def test_extract_player_info_from_join(self):
        """
        Test the extraction of player information from a join event log line.

        This test verifies:
        1. Correct extraction of player ID and name from a valid join event log line.
        2. Handling of an invalid username in a join event log line.
        """
        line = "Client authenticated: (KU_Xo93QaLmG1) DST_Player"
        player_id, player_name = extract_player_info_from_join(line)
        self.assertEqual(player_id, "KU_Xo93QaLmG1")
        self.assertEqual(player_name, "DST_Player")

        # Test invalid username
        line = "Client authenticated: (KU_Xo93QaLmG1) Invalid@Username"
        player_id, player_name = extract_player_info_from_join(line)
        self.assertEqual(player_id, "KU_Xo93QaLmG1")
        self.assertIsNone(player_name)

    def test_extract_player_id_from_leave(self):
        """
        Test the extraction of player information from a leave event log line.

        This test verifies:
        1. Correct extraction of player ID and name from a valid leave event log line.
        2. Handling of a leave event log line without a player name.
        """
        line = "[Shard] (KU_Xo93QaLmG1) DST_Player disconnected from [SHDMASTER](1)"
        player_id, player_name = extract_player_id_from_leave(line)
        self.assertEqual(player_id, "KU_Xo93QaLmG1")
        self.assertEqual(player_name, "DST_Player")

        # Test line without player name
        line = "[Shard] (KU_Xo93QaLmG1) disconnected from [SHDMASTER](1)"
        player_id, player_name = extract_player_id_from_leave(line)
        self.assertEqual(player_id, "KU_Xo93QaLmG1")
        self.assertIsNone(player_name)

    def test_extract_player_character_from_spawn(self):
        """
        Test the extraction of player and character information from a spawn event log line.

        This test verifies:
        1. Correct extraction of player name and character from a valid spawn event log line.
        2. Handling of an invalid username in a spawn event log line.
        """
        line = "Spawn request: wilson from DST_Player"
        player_name, character = extract_player_character_from_spawn(line)
        self.assertEqual(player_name, "DST_Player")
        self.assertEqual(character, "wilson")

        # Test invalid username
        line = "Spawn request: wilson from Invalid@Username"
        player_name, character = extract_player_character_from_spawn(line)
        self.assertIsNone(player_name)
        self.assertIsNone(character)


if __name__ == "__main__":
    unittest.main()
