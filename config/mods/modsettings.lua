-- Use the "ForceEnableMod" function when developing a mod. This will cause the
-- game to load the mod every time no matter what, saving you the trouble of
-- re-enabling it from the main menu.
--
-- Note! You shout NOT do this for normal mod loading. Please use the Mods menu
-- from the main screen instead.
--ForceEnableMod("kioskmode_dst")
-- Use "EnableModDebugPrint()" to show extra information during startup.
--EnableModDebugPrint()
-- Use "EnableModError()" to make the game more strict and crash on bad mod practices.
--EnableModError()
-- Use "DisableModDisabling()" to make the game stop disabling your mods when the game crashes
--DisableModDisabling()
-- Use "DisableLocalModWarning()" to make the game stop warning you when enabling local mods.
--DisableLocalModWarning()

return {  
  ["workshop-375859599"] = { enabled = true }, -- Health Info
  ["workshop-378160973"] = { enabled = true }, -- Global Positions
  ["workshop-374550642"] = { enabled = true }, -- Increased Stack size
  ["workshop-3026138806"] = { enabled = true }, -- Extra Equip Slots Clean [Doom] 3.1.0
  ["workshop-3007715893"] = { enabled = true }, -- 更多物品堆叠/More Items Stack
  ["workshop-1803285852"] = { enabled = true }, -- Auto Stack and Pick Up
  ["workshop-501385076"] = { enabled = true }, -- Quick Pick
  ["workshop-1079538195"] = { enabled = true }, -- Moving Box
  ["workshop-569043634"] = { enabled = true }, -- Campfire Respawn
  ["workshop-3232213331"] = { enabled = true }, -- Automatic sorter DST (2024)
}