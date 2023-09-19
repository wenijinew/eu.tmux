<h1 align="center">
![Glamour.Tmux](https://raw.githubusercontent.com/wenijinew/glamour.tmux/main/glamour.tmux.png)
</h1>

# What's Glamour.Tmux

Glamour.Tmux is a Tmux plugin. It aims to help Tmux user to simply configurations, especially for theme configuration.

# Installation


* Option1: Configure in .tmux.conf file as TPM plugin.

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

After installation, user can use bind-keys as follows:

* `PREFIX g` - set dynamic theme.
* `PREFIX G` - reset default theme.
* `PREFIX a` - show all themes.
* `PREFIX r` - rotate all built-in themes.

To create own theme, simply copy `dynamic.theme.yaml` to the new them file. Then, do customization in the new theme file.
To set the new theme as default theme, update `$XDG_CONFIG_HOME/tmux/glamour.yaml` file to change theme name to new theme.

# Developer Guide

Glamour.Tmux is developed with Python and Bash programming languages.

Python modules are use to generate dynamic palette, parse configuration file and theme file, generate Tmux commands to set options and bind keys.

Bash scripts are use to accept client parameters, create dynamic configuration file or theme file, run generated Tmux commands to apply configurations and theme.

# Thanks

Glamour.Tmux is derived from [catppuccin/tmux](https://github.com/catppuccin/tmux). Thanks all contributors and their great workk on [catppuccin/tmux](https://github.com/catppuccin/tmux).
