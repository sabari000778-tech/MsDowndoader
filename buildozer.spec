[app]
title = Ms Downloader
package.name = msdownloader
package.domain = org.sabari
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,yt-dlp,certifi,urllib3
orientation = portrait
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.api = 33
android.sdk_path = /home/runner/android-sdk
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1
