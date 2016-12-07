montage -mode concatenate -tile 1x vorticity/32.0_*png -flip -geometry -150-150 -density 50 32.0.png
montage -mode concatenate -tile 1x vorticity/34.0_*png -flip -geometry -150-150 -density 50 34.0.png
montage -mode concatenate -tile 1x vorticity/36.0_*png -flip -geometry -150-150 -density 50 36.0.png

convert -flip 32.0.png 32.0.png
convert -flip 34.0.png 34.0.png
convert -flip 36.0.png 36.0.png

montage -mode concatenate -tile x1 3*.0.png -geometry -150-150 -density 150 multi.png
