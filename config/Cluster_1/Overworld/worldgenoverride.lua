return {
  override_enabled = true,  -- Set to true to enable custom world generation settings.

  -- Preset world generation settings.
  -- Common options:
  --   SURVIVAL_TOGETHER - Balanced world suitable for survival.
  --   DARKNESS - A world with permanent night.
  preset = "SURVIVAL_TOGETHER",

  overrides = {
      -- Example overrides (default, never, rare, often, always):
      berrybush = "default",  -- Frequency of berry bushes.
      carrots = "default",    -- Frequency of carrots.
      rabbits = "default",    -- Frequency of rabbit holes.

      -- Season start options (default, spring, summer, autumn, winter):
      season_start = "default",  -- Season in which the game starts.

      -- Day length options (default, longday, longdusk, longnight):
      day = "default",  -- Length of day and night cycles.

      -- Add more customizations as needed.
  }
}
