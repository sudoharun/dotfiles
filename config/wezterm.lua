-- Pull in the wezterm API
local wezterm = require 'wezterm'

-- This table will hold the configuration.
local config = {}

-- In newer versions of wezterm, use the config_builder which will
-- help provide clearer error messages
if wezterm.config_builder then
  config = wezterm.config_builder()
end

-- This is where you actually apply your config choices

-- For example, changing the color scheme:
config.color_scheme = '3024 (dark) (terminal.sexy)'
config.enable_tab_bar = false

config.font = wezterm.font 'IosevkaTerm Nerd Font'
config.font = wezterm.font_with_fallback {
  'Noto Sans CJK',
  'JetBrainsMono Nerd Font',
}
config.font_size = 16

config.window_background_opacity = 0.9
config.window_padding = {
  top = 12,
  bottom = 12,
  left = 12,
  right = 12,
}

-- and finally, return the configuration to wezterm
return config

