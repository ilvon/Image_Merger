import math

#* image_num_x = col, image_num_y = row

def arranged_image_matrix(img_obj_list: list, orientation, single_rowCol: bool, flush: bool, arrange: list):    
    image_num = len(img_obj_list)
    
    if arrange:
        if sum(arrange) != image_num:
            print('Invalid layout arrangement!')
            exit(1)
        row_start_idx = 0
        matrix = []
        for x in arrange:
            row_end_idx = row_start_idx + x
            matrix.append(img_obj_list[row_start_idx:row_end_idx])
            row_start_idx = row_end_idx
        return ImageMatrix(arrange, matrix, flush)
               
    if single_rowCol:
        if orientation == 'p' or orientation == 'portrait':
            matrix = [[img] for img in img_obj_list]
            return ImageMatrix([1]*len(img_obj_list), matrix, flush)
        else:
            matrix = [img_obj_list]
            return ImageMatrix([len(img_obj_list)], matrix, flush)
    search_range = int(math.sqrt(image_num))
    smaller_divisor = 1
    for i in range(search_range, 0, -1):
        if image_num % i == 0:
            smaller_divisor = i
            break
    if orientation == 'p' or orientation == 'portrait':
        image_num_x = smaller_divisor
        image_num_y = int(image_num/smaller_divisor)
    else:
        image_num_x = int(image_num/smaller_divisor)
        image_num_y = smaller_divisor
           
    matrix = [img_obj_list[i : i+image_num_x] for i in range(0, len(img_obj_list), image_num_x)] 
    
    return ImageMatrix([image_num_x]*image_num_y, matrix, flush)


class ImageMatrix():
    def __init__(self, arrangement, matrix, flush):
        self.array = arrangement
        self.flush = flush
        self.MARGIN = 20
        self.img_matrix = matrix
        self.dimension_matrix = self.__get_dimension_matrix(self.array, self.img_matrix)
        self.modified_dimension_matrix, self.canvas_size = self.__get_resized_matrix(self.array, self.dimension_matrix)
        self.__get_pasting_offset(self.modified_dimension_matrix)

    class utils():
        @staticmethod
        def geometric_mean(values: list):
            avg_height = math.exp(sum(math.log(v) for v in values) / len(values))
            return round(avg_height)

        @staticmethod
        def get_row_element_sum(list_2d: list, list_index: int) -> list:
            return [sum(col[list_index] for col in row) for row in list_2d]
        
        @staticmethod
        def create_2D_matrix(array, filler) -> list:
            return [[filler]*ele_cnt for ele_cnt in array]
                 
        @staticmethod
        def extract_row_elements(row, ele_idx) -> list:
            extracted = []
            for ele in row:
                if ele:
                    extracted.append(ele[ele_idx])
            return extracted
        
        @staticmethod
        def get_row_max_element(matrix_2d: list, idx, value_only: bool) -> list:
            maxima = [max(r, key=lambda x: x[idx]) for r in matrix_2d]
            if value_only:
                maxima = [x[idx] for x in maxima]
            return maxima


    def __get_dimension_matrix(self, dm_array, m):
        dm = self.utils.create_2D_matrix(dm_array, None)
        for ridx, r in enumerate(m):
            for cidx, c in enumerate(r):
                dm[ridx][cidx] = (c.width, c.height)
            dm[ridx] = list(filter(None, dm[ridx]))
        return dm
    
    
    def __get_resized_matrix(self, array, dimension_matrix: list):
        final_matrix = self.utils.create_2D_matrix(array, None)
        
        if not self.flush:
            row_width_maxima = self.utils.get_row_element_sum(dimension_matrix, 0)
            final_canvas_width = self.MARGIN * (max(array) + 1) + max(row_width_maxima)
            row_height_maxima = self.utils.get_row_max_element(dimension_matrix, 1, True)
            final_canvas_height = sum(row_height_maxima) + self.MARGIN * (len(array) + 1)
            return dimension_matrix, (final_canvas_width, final_canvas_height)
        
        # 1st resizing
        for ridx, r in enumerate(dimension_matrix):
            temp_new_height = self.utils.geometric_mean(self.utils.extract_row_elements(r, 1))
            for cidx, c in enumerate(r):
                temp_new_width = c[0] * (temp_new_height / c[1])
                final_matrix[ridx][cidx] = (temp_new_width, temp_new_height)
           
        total_width = [sum(self.utils.extract_row_elements(row, 0)) for row in final_matrix]
        final_canvas_width = self.utils.geometric_mean(total_width)
        # 2nd resizing
        for ridx, r in enumerate(final_matrix):
            resizing_multiplier = final_canvas_width / total_width[ridx]
            for cidx, c in enumerate(r):
                occupied_percentage = final_matrix[ridx][cidx][0] / total_width[ridx]
                final_matrix[ridx][cidx] = (round(final_canvas_width * occupied_percentage),
                                            round(final_matrix[ridx][cidx][1] * resizing_multiplier))  
        final_matrix_size = (final_canvas_width, sum([r[0][1] for r in final_matrix]))
        
        return final_matrix, final_matrix_size
    
    
    def __get_pasting_offset(self, dmatrix):
        print(f'Merged image dimension = {self.canvas_size[0]}x{self.canvas_size[1]}')
        if not self.flush:
            self.__get_pasting_offset_nonflush(dmatrix)
            return
        for ridx, row in enumerate(dmatrix):
            for cidx, _ in enumerate(row):
                offset_x = 0 if cidx == 0 else sum([i[0] for i in dmatrix[ridx][:cidx]])
                offset_y = 0 if ridx == 0 else sum([i[0][1] for i in dmatrix[:ridx]])
                self.img_matrix[ridx][cidx].offset = (int(offset_x), int(offset_y))
       
                
    def __get_pasting_offset_nonflush(self, dmatrix):
        self.MARGIN = 20
        row_tallest_img = self.utils.get_row_max_element(dmatrix, 1, True)
        row_widths = self.utils.get_row_element_sum(dmatrix, 0)
        widest_row_width = max(row_widths)
        for ridx, row in enumerate(dmatrix):
            for cidx, col in enumerate(row):
                offset_y = self.MARGIN * (ridx + 1) + sum(row_tallest_img[:ridx])
                if dmatrix[ridx][cidx][1] != row_tallest_img[ridx]:
                    offset_y = offset_y + 0.5 * (row_tallest_img[ridx] - col[1])
                    
                offset_x = self.MARGIN * (cidx + 1) + sum([c[0] for c in row[:cidx]])
                if dmatrix[ridx][cidx][0] != widest_row_width:
                    offset_x = offset_x + 0.5 * (widest_row_width - row_widths[ridx])
                    
                self.img_matrix[ridx][cidx].offset = (int(offset_x), int(offset_y))
                