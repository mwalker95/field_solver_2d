#!/bin/bash
ffmpeg -y -framerate 5 -i %05d.png -c:v libx264 -pix_fmt yuv420p out.mp4
