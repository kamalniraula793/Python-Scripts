#!/bin/bash

# Get clipboard content using xclip
CLIPBOARD_CONTENT=$(xclip -selection clipboard -o)

# Display the clipboard content using a notification
notify-send "Clipboard Content" "$CLIPBOARD_CONTENT"
