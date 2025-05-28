# -*- coding: utf-8 -*-
import sys
import os
import re
import xbmcplugin
import xbmcgui

handle = int(sys.argv[1])
base_path = xbmc.translatePath("special://home/addons/plugin.video.bl4z3_streamhub/")
m3u_path = os.path.join(base_path, "resources", "IPTV_Italia.m3u")

def parse_m3u(filepath):
    channels = []
    with open(filepath, encoding="utf-8") as file:
        lines = file.readlines()

    current = {}
    for line in lines:
        line = line.strip()
        if line.startswith("#EXTINF"):
            match = re.search(r'tvg-logo="([^"]+)"', line)
            logo = match.group(1) if match else ""

            match = re.search(r'group-title="([^"]+)"', line)
            group = match.group(1) if match else "Altro"

            title = line.split(",")[-1]
            current = {"title": title, "logo": logo, "group": group}
        elif line and not line.startswith("#"):
            current["url"] = line
            channels.append(current)
            current = {}
    return channels

def list_channels():
    channels = parse_m3u(m3u_path)
    for channel in channels:
        li = xbmcgui.ListItem(label=channel["title"])
        li.setArt({'thumb': channel["logo"], 'icon': channel["logo"]})
        li.setInfo('video', {'title': channel["title"], 'genre': channel["group"]})
        xbmcplugin.addDirectoryItem(handle=handle, url=channel["url"], listitem=li, isFolder=False)
    xbmcplugin.endOfDirectory(handle)

if __name__ == "__main__":
    list_channels()