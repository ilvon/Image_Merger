# Image_Merger

A script for merging multiple images at once.

## Arguments

- `-l`: orientation of the output image, either in portrait or landscape
- `-a`: layout arrangement of the merge by row
- `-f`: merge images with resizing, no gap between images from the output
- `-s`: merge images into a single column/row output (e.g. $n\times1$ / $1\times n$ image)

## Remarks

1. layout arrangement can specify in a form as follow: `-a 1 2 3`, which overrride the setting of portrait or landascape mode
2. layout of the output image will be determined automatically by the script if not specify with `-a` flag, which preferring having a square layout (e.g. for mering 16 images, prefer in a $4\times4$ layout rather $8\times2$)
3. output image will located in the same directory of the first input image
4. with turning off flush mode, input images will not being resized, hence leaving gaps in between

