#!/bin/bash

curl --location --request POST 'http://127.0.0.1:5555/upload_image' \
--form 'file=@"test_images/qr4.PNG"'