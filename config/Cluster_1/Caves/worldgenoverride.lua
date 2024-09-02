return {
  override_enabled = true,  -- Enable custom world generation for caves.

  preset = "DST_CAVE",  -- Preset should always be "DST_CAVE" for cave shards.

  overrides = {
      -- Example overrides for caves (default, never, rare, often, always):
      earthquakes = "default",  -- Frequency of earthquakes in caves.

      -- Customize as needed for your caves environment.
  }
}
