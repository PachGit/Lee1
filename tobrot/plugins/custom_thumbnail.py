#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @AnyDLBot | Other Contributors 
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/5MysterySD/Tele-LeechX >
# All Right Reserved


import os

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image
from tobrot import DOWNLOAD_LOCATION


async def save_thumb_nail(client, message):
    thumbnail_location = os.path.join(DOWNLOAD_LOCATION, "thumbnails")
    thumb_image_path = os.path.join(
        thumbnail_location, str(message.from_user.id) + ".jpg"
    )
    ismgs = await message.reply_text("<code>Processing . . . ð</code>")
    if message.reply_to_message is not None:
        if not os.path.isdir(thumbnail_location):
            os.makedirs(thumbnail_location)
        download_location = thumbnail_location + "/"
        downloaded_file_name = await client.download_media(
            message=message.reply_to_message, file_name=download_location
        )
        # https://stackoverflow.com/a/21669827/4723940
        Image.open(downloaded_file_name).convert("RGB").save(downloaded_file_name)
        metadata = extractMetadata(createParser(downloaded_file_name))
        height = 0
        if metadata.has("height"):
            height = metadata.get("height")
        # resize image
        # ref: https://t.me/PyrogramChat/44663
        img = Image.open(downloaded_file_name)
        # https://stackoverflow.com/a/37631799/4723940
        # img.thumbnail((320, 320))
        img.resize((320, height))
        img.save(thumb_image_path, "JPEG")
        # https://pillow.readthedocs.io/en/3.1.x/reference/Image.html#create-thumbnails
        os.remove(downloaded_file_name)
        await ismgs.edit(
            "<b>â¡<i>Custom Thumbnail ð¼ Saved for Next Uploads</i>â¡</b>\n\n"
            + "<b><i>âYour Photo is Set, Ready to Go ...ð¨âð¦¯</i></b>."
        )
    else:
        await ismgs.edit("<b><i>âSorryâ</i></b>\n\n" + "<b>â Reply with Image to Save Your Custom Thumbnail.â</b>")

async def clear_thumb_nail(client, message):
    thumbnail_location = os.path.join(DOWNLOAD_LOCATION, "thumbnails")
    thumb_image_path = os.path.join(
        thumbnail_location, str(message.from_user.id) + ".jpg"
    )
    ismgs = await message.reply_text("<code>Processing . . . ð</code>")
    if os.path.exists(thumb_image_path):
        os.remove(thumb_image_path)
        await ismgs.edit("<b><i>âSuccessâ</i></b>\n\n" + "<b>ð¼Custom Thumbnail Cleared Successfully As Per Your Request.</b>")
    else:
        await ismgs.edit("<b><i>âSorryâ</i></b>\n\n" + "<b>âNothing to Clear For Youâ</b>")
