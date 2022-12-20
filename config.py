from libqtile import bar, layout, widget, hook
from libqtile.config import Group, Key, Match, Screen
from libqtile.lazy import lazy
import os
import subprocess

# Auto start
@hook.subscribe.startup_once
def autostart():
    path = os.path.expanduser('/home/tafta/.config/qtile/autostart.sh')
    subprocess.call([path])

# Variables
mod4 = 'mod4'               # Window key
mod1 = 'mod1'               # Alt key
tab = 'Tab'                 # Tab key
ctrl = 'control'            # Control
shift = 'shift'             # Shift
up = 'Up'                   # Up arrow
down = 'Down'               # Down arrow
left = 'Left'               # Left arrow
right = 'Right'             # Right arrow
enter = 'Return'            # Character return
space = 'space'             # Space
# terminal = guess_terminal()
terminal = 'alacritty'

# Keymap
# A list of available commands that can be bound to keys can be found
# at https://docs.qtile.org/en/latest/manual/config/lazy.html
keys = [
    # Switch between windows
    Key([mod4, ctrl], left, lazy.layout.left(), desc='Move focus to left'),
    Key([mod4, ctrl], right, lazy.layout.right(), desc='Move focus to right'),
    Key([mod4, ctrl], down, lazy.layout.down(), desc='Move focus down'),
    Key([mod4, ctrl], up, lazy.layout.up(), desc='Move focus up'),

    Key([mod4], space, lazy.layout.next(), desc='Move window focus to other window'),
    Key([mod1], tab, lazy.layout.next(), desc='Move window focus to other window'),
    Key([mod1, shift], tab, lazy.layout.previous(), desc='Move window focus to other window'),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod4, shift], left, lazy.layout.shuffle_left(), desc='Move window to the left'),
    Key([mod4, shift], right, lazy.layout.shuffle_right(), desc='Move window to the right'),
    Key([mod4, shift], down, lazy.layout.shuffle_down(), desc='Move window down'),
    Key([mod4, shift], up, lazy.layout.shuffle_up(), desc='Move window up'),

    # Launch terminal
    Key([mod4], enter, lazy.spawn(terminal), desc='Launch terminal'),

    # Toggle between different layouts as defined below
    Key([mod4], 'Tab', lazy.next_layout(), desc='Toggle between layouts'),
    Key([mod4], 'q', lazy.window.kill(), desc='Kill focused window'),
    Key([mod4, ctrl], 'r', lazy.reload_config(), desc='Reload the config'),
    Key([mod4], 'r', lazy.spawncmd(), desc='Spawn a command using a prompt widget'),

    # Workspaces
    Key([mod4], left, lazy.screen.prev_group(), desc='Go to the previous workspace'),
    Key([mod4], right, lazy.screen.next_group(), desc='Go to the next workspace'),

    # Audio
    # Require 'alsa-utils' package
    Key([], 'XF86AudioMute', lazy.spawn('amixer -q set Master toggle'), desc='Mute volume'),
    Key([], 'XF86AudioRaiseVolume', lazy.spawn('amixer -c 0 sset Master 5+ unmute'), desc='Raise volume'),
    Key([], 'XF86AudioLowerVolume', lazy.spawn('amixer -c 0 sset Master 5- unmute'), desc='Lower volume'),
]

groups = [Group(i) for i in '12345678']

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod4],
                'f' + i.name,
                lazy.group[i.name].toscreen(),
                desc='Switch to group {}'.format(i.name),
            ),

            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod4, shift],
                'f' + i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc='Switch to & move focused window to group {}'.format(
                    i.name),
            ),
        ]
    )

layout_options = {
    'margin': 0,
    'border_width': 0,
    'border_focus': '#d75f5f',
    'border_normal': '#8f3d3d'
}

layouts = [
    layout.Max(**layout_options),
    layout.MonadTall(**layout_options),
    layout.MonadWide(**layout_options),
    layout.Spiral(**layout_options),
    # layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

font = "JetBrainsMono Nerd Font"
widget_defaults = dict(
    font=font,
    fontsize=12,
    padding=3,
)

extension_defaults = widget_defaults.copy()

bar_margin = 0 # [8, 8, 0, 8]
bar_border_width = 0 # [4, 16, 4, 16]
bar_background = '#1e2127'  # -- neosolarized '#292d3e',
bar_border_color = '#1e2127'  # -- neosolarized '#292d3e',
top = bar.Bar(
    [
        widget.WindowName(),

        widget.Spacer(
            length=bar.STRETCH
        ),

        widget.CurrentLayout(
            padding=16,
        ),

        widget.GroupBox(
            active='#d0d0d0',
            highlight_method='line',
            disable_drag=True,
            this_current_screen_border='#8f3d3d',
            borderwidth=2,
            padding_x=8
        ),

        widget.Prompt(
            padding=8
        ),

        widget.Spacer(
            length=bar.STRETCH

        ),

        widget.WindowCount(
            max_chars=2,
            foreground='#8f3d3d',
            fontsize=16,
            padding=16
        ),

        widget.PulseVolume(
            padding=8,
            limit_max_volume=True,
            step=5,
            volume_down_command='XF86AudioLowerVolume',
            volume_up_command='XF86AudioRaiseVolume'
        ),

        widget.Clock(
            format='%H:%M %d %B, %Y',
            padding=8
        ),
    ],
    24,
    background=bar_background,
    opacity=1,
    margin=bar_margin,
    border_width=bar_border_width,
    border_color=bar_border_color
)

screens = [
    Screen(
        top=top,
        # wallpaper='~/.config/qtile/wallpaper/20.jpg',
        # wallpaper_mode='stretch',
    ),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

wmname = "LG3D"
