from Image_Merger import ImageMerger
import argparse
from tkinter.filedialog import askopenfilenames, askdirectory

IMG_FORMATS = [('Image', '*.png;*.jpg;*.jpeg;*.gif;*.webp;*.bmp;*.raw;*.tiff;*.tif;*.svg;*.ico')]

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', type=str, metavar='',nargs='*', required=False,
                    help='File paths of images that being merged')
parser.add_argument('-a', '--arrange', type=int, metavar='',nargs='*', required=False,
                    help='Layout arrangement of the merge by row')
parser.add_argument('-l', '--layout', type=str, default='l', metavar='',
                    help='Merging layout (Default=\'l\', landscape), (\'l\'=landscape, \'p\'=portrait)')
parser.add_argument('-f', '--flush', default=True, action='store_false',
                    help='Disable merging images in flush mode (Default=True)')
parser.add_argument('-s', '--single', default=False, action='store_true',
                    help='Merge images into single row/column (Default=False)')
parser.add_argument('-o', '--out', default=False, action='store_true',
                    help='Select custom output path (Default=Off)')
parser.add_argument('-n', '--name', type=str, default='', metavar='',
                    help='Name of output image (Exclude file extension) (Default=\'merged_image\')')
args = parser.parse_args()  

if 0 in args.arrange:
    print('Invalid layout arrangement!')
    exit(1)

if args.layout not in ['l', 'landscape', 'p', 'portrait']:
    print('Invalid choice for image arrangment')
    exit(1)
        
if args.out:
    output_dir = askdirectory(title='Select your custom output directory')
else:
    output_dir = None

src_imgs = askopenfilenames(title='Select images to be merged', filetypes=IMG_FORMATS) if not args.input else args.input
if (src_imgs == ''):
    print('Invalid images selected!')
    exit(1)
    
try:    
    merger = ImageMerger(args.layout, args.flush, args.arrange,output_dir)
    merger.merge(args.single, src_imgs, args.name)
except Exception as err:
    print(f'Error occured! Error: {str(err)}')
