from PIL import Image, UnidentifiedImageError
import os
import ImageMatrix

class ImageMerger():
    def __init__(self, merge_layout, flush, arrange, output_path=None) -> None:
        self.layout = merge_layout
        self.flush = flush
        self.arrange = arrange
        self.output_dirname = output_path
        self.BG_COLOR = (255,255,255,0)
    
    
    def merge(self, single_rowCol: bool, img_paths, merged_name=''):
        try:
            merge_matrix = [Image.open(img) for img in img_paths]
        except FileNotFoundError:
            print('Error: The input file(s) do not exist/unable to read.')
            exit(1)
        except UnidentifiedImageError:
            print('Unable to identify image file(s).')
            exit(1)
        merge_matrix = ImageMatrix.arranged_image_matrix(merge_matrix, self.layout, single_rowCol, self.flush, self.arrange)
                 
        default_output_name = (merged_name + '.png') if merged_name else 'merged_image.png'
        default_output_dir = os.path.dirname(img_paths[0]) if not self.output_dirname else self.output_dirname
        merged_output_path = os.path.join(default_output_dir, default_output_name)
        
        for ridx, imgs_row in enumerate(merge_matrix.img_matrix):
            for cidx, img in enumerate(imgs_row):
                filename = merge_matrix.img_matrix[ridx][cidx].filename
                offset = merge_matrix.img_matrix[ridx][cidx].offset
                merge_matrix.img_matrix[ridx][cidx] = img.resize(merge_matrix.modified_dimension_matrix[ridx][cidx], resample=Image.LANCZOS)
                merge_matrix.img_matrix[ridx][cidx].filename = filename
                merge_matrix.img_matrix[ridx][cidx].offset = offset
        
        merged_image = self.__paste(merge_matrix)
        merged_image.save(merged_output_path)

    
    def __paste(self, matrix):
        new_canvas = Image.new('RGBA', matrix.canvas_size, self.BG_COLOR)
        for imgs_row in matrix.img_matrix:
            for img in imgs_row:
                new_canvas.paste(img, img.offset)   
        return new_canvas     
    