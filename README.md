![Glamour.Tmux](assets/images/glamour.tmux.v2.png)

# What's Glamour.Tmux

Glamour.Tmux is a Tmux plugin(throught [TPM](https://github.com/tmux-plugins/tpm)). It aims to help Tmux user to simplify configurations, especially for theme configuration, customization, and *dynamic* theme generation.

# What's NOT Glamour.Tmux

Glamour.Tmux is not for Tmux layout or Tmux session management. Try [tmuxp](https://github.com/tmux-python/tmuxp) and [tmuxinator](https://github.com/tmuxinator/tmuxinator) instead.

# Installation


* Option1: Configure in `.tmux.conf` file as [TPM](https://github.com/tmux-plugins/tpm) plugin.

``` bash
set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-sensible'
set -g @plugin 'wenijinew/glamour.tmux'
```

And then run command `tmux source ~/.tmux.conf` and `PREFIX I ` to clone this repo to `~/.tmux/plugins/`

* Option2: Clone this repo by manually:

``` bash
git clone https://github.com/wenijinew/glamour.tmux.git
```

Go to glamour.tmux and run `./glamour.tmux`


# User Guide

After installation, user can use bind-keys as follows for theme settings:

Note: by default, PREFIX is `C-b`.

* `PREFIX g` - create and apply a dynamic theme.
* `PREFIX G` - reset to the default theme.
* `PREFIX a` - show all available themes.
* `PREFIX r` - rotate all available themes.

To create own theme, simply copy `dynamic.theme.yaml` to the new them file. Then, do customization in the new theme file.
To set the new theme as default theme, update `$XDG_CONFIG_HOME/tmux/glamour.yaml` file to change theme name to new theme.

More bind-keys are set by default as follows:

* `PREFIX C-j` - enable synchronize-panes (typing in all panes simultaneously in current windows).
* `PREFIX C-k` - disable synchronize-panes (typing in all panes simultaneously in current windows).
* `M-Left` - select the left window. (if in the first window, then go to last window)
* `M-Right` - select the right window. (if in the last window, then go to first window)
* `M-l` - select the previous working window.
* `M-j` - go to the left pane in the same horizontal level. if no more left, then go to the last pane in the same hozontal level.
* `M-k` - go to the downward pane in the same vertial level. if no more downward pane, then go to the first pane in the same vertial level.

# Developer Guide

Glamour.Tmux is developed with Python and Bash programming languages.

Python modules are use to generate dynamic palette, parse configuration file and theme file, generate Tmux commands to set options and bind keys.

Bash scripts are use to accept client parameters, create dynamic configuration file or theme file, run generated Tmux commands to apply configurations and theme.

Learn more detail by reading the flow chart below:

![Glamour Tmux Flow Chart](assets/images/glamour_tmux_flow_chart.png)

# Thanks

Glamour.Tmux is derived from [catppuccin/tmux](https://github.com/catppuccin/tmux). Thanks all contributors and their great workk on [catppuccin/tmux](https://github.com/catppuccin/tmux).
