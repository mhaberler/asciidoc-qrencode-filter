# Introduction #
This filter enables you to create create QRCodes from asciidoc documents

# Requirement #
qrencode http://fukuchi.org/works/qrencode/index.en.html
This filter has been successfully used under an Archlinux machine.
On Windows, install of QRcode library and slight modifications are probably required.

# Usage #
To use it, please just put this text block in your asciidoc document:
```
["qrcode", size=10]
-------------------------
http://google.com
-------------------------
```

The size parameter is optional and tells qrencode which pixel size to use (default = 3)