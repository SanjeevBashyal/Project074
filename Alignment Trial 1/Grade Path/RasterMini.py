from math import floor

class RasterMini:
    def __init__(self, xres, yres, extent):
        self.xres = xres
        self.yres = yres
        self.extent = extent
    
        
    def create_points_from_path_list(self, min_cost_path):
        path_points = list(
            map(lambda row_col: self._row_col_to_point_list(row_col), min_cost_path))
        return path_points
        
    def _row_col_to_point_list(self,row_col):

        x = (row_col[1] + 0.5) * self.xres + self.extent[0]
        y = self.extent[3] - (row_col[0] + 0.5) * self.yres
        return [x,y]
        
        
