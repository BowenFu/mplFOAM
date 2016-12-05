montage -mode concatenate -tile 1x vorticity/32.0_*png -flip -geometry -100-100 -density 50 32.0.png
montage -mode concatenate -tile 1x vorticity/33.0_*png -flip -geometry -100-100 -density 50 33.0.png
montage -mode concatenate -tile 1x vorticity/34.0_*png -flip -geometry -100-100 -density 50 34.0.png
montage -mode concatenate -tile 1x vorticity/35.0_*png -flip -geometry -100-100 -density 50 35.0.png
montage -mode concatenate -tile 1x vorticity/36.0_*png -flip -geometry -100-100 -density 50 36.0.png

convert -flip 32.0.png 32.0.png
convert -flip 33.0.png 33.0.png
convert -flip 34.0.png 34.0.png
convert -flip 35.0.png 35.0.png
convert -flip 36.0.png 36.0.png

montage -mode concatenate -tile x1 3*.0.png -density 50 multi.png
