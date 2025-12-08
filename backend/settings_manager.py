"""Settings manager for ThermoLogger configuration."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Dict, List


class SettingsManager:
    """Manages application settings including thermocouple types."""

    THERMOCOUPLE_TYPES = ['K', 'J', 'T', 'E', 'N', 'S', 'R', 'B']
    DEFAULT_TYPE = 'K'

    def __init__(self, settings_file: str | Path = "settings.json"):
        self.settings_file = Path(settings_file)
        self.channel_types: List[str] = [self.DEFAULT_TYPE] * 8
        self.load_settings()

    def load_settings(self) -> bool:
        """Load settings from JSON file."""
        if not self.settings_file.exists():
            logging.info(f"Settings file not found at {self.settings_file}, using defaults")
            return False

        try:
            with open(self.settings_file, 'r') as f:
                data = json.load(f)
                self.channel_types = data.get('channel_types', [self.DEFAULT_TYPE] * 8)
                
                # Ensure we have exactly 8 channels
                while len(self.channel_types) < 8:
                    self.channel_types.append(self.DEFAULT_TYPE)
                self.channel_types = self.channel_types[:8]
                
                logging.info(f"Settings loaded from {self.settings_file}")
                return True
        except Exception as e:
            logging.error(f"Error loading settings: {e}")
            return False

    def save_settings(self) -> bool:
        """Save settings to JSON file."""
        try:
            data = {
                'channel_types': self.channel_types
            }
            with open(self.settings_file, 'w') as f:
                json.dump(data, f, indent=2)
            logging.info(f"Settings saved to {self.settings_file}")
            print(f"[SETTINGS] Saved to {self.settings_file}")
            return True
        except Exception as e:
            logging.error(f"Error saving settings: {e}")
            return False

    def get_channel_type(self, channel: int) -> str:
        """Get thermocouple type for a specific channel (0-7)."""
        if 0 <= channel < 8:
            return self.channel_types[channel]
        return self.DEFAULT_TYPE

    def set_channel_type(self, channel: int, tc_type: str) -> bool:
        """Set thermocouple type for a specific channel (0-7)."""
        if 0 <= channel < 8 and tc_type in self.THERMOCOUPLE_TYPES:
            self.channel_types[channel] = tc_type
            return True
        return False

    def get_all_channel_types(self) -> List[str]:
        """Get all channel thermocouple types."""
        return self.channel_types.copy()

    def set_all_channel_types(self, types: List[str]) -> bool:
        """Set all channel thermocouple types."""
        if len(types) != 8:
            return False
        if not all(t in self.THERMOCOUPLE_TYPES for t in types):
            return False
        self.channel_types = types.copy()
        return True
