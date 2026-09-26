[app]
title = Jarvis AI Buddy
package.name = jarvisai
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,groq,edge-tts,pocketsphinx,pyjnius
orientation = portrait
osx.kivy_version = 1.9.1
fullscreen = 0
android.permissions = RECORD_AUDIO, INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, CAMERA, MODIFY_AUDIO_SETTINGS
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
