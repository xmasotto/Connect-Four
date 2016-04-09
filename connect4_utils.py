import numpy as np
import json
import copy
import time

class Eval:
    def __init__(self, mask_definition):
        self.mask_definition = json.loads(mask_definition)
        self.masks = []
        for obj in self.mask_definition:
            self.masks.extend(self.json_to_masks(obj))
        
    def evaluate(self, board, flipped):
        score = 0
        for mask in self.masks:
            print(mask.count_instances(board) - mask.count_instances(flipped))*mask.weight
            score += (mask.count_instances(board) - mask.count_instances(flipped))*mask.weight
        return score
        
    def debug_evaluate(self, board, flipped, color):
        '''def print_mask(mask):
            for line in mask.mask:
                print(line)
    
        for mask in self.masks:
            print(mask.name)
            print_mask(mask)
            
        time.sleep(100);'''
        for line in board:
            print(line)
        print("")
        for mask in self.masks:
            print(mask.name, "board: ", mask.count_instances(board), "flipped: ", mask.count_instances(flipped))
        for mask in self.masks:
            if (mask.count_instances(board) > 0 or mask.count_instances(flipped) > 0):
                print("Found " + mask.name + "!");
                print(color)
                time.sleep(10)
        print("\n")
    
    def json_to_masks(self, obj):
        masks = []
        name = obj["name"]
        weight = float(obj["weight"])
        mask = [list(x) for x in obj["mask"].split()]
        original_mask = Mask(mask, name, weight)
        masks.append(original_mask)
        
        transforms = obj["transforms"]
        for transform in transforms:
            a, b = [int(x) for x in transform.split(",")]
            if a == 0 and b == 1:
                masks.append(Mask.flip_x(original_mask))
            if a != 0:
                mask = original_mask.rotate_mask(a/90)
                if b == 1:
                    mask = mask.flip_x()
                masks.append(mask)
        return masks
    
        
    

class Mask:
    def __init__(self, mask, name, weight):
        self.mask = mask
        self.name = name
        self.weight = weight
        self.pre_y = Mask.blocked_rows(self.mask)
        self.pre_x = Mask.blocked_rows(Mask.rotate_array(self.mask, times=1))
        self.post_y = Mask.blocked_rows(Mask.rotate_array(self.mask, times=2))
        self.post_x = Mask.blocked_rows(Mask.rotate_array(self.mask, times=3))
        print self.pre_y, self.pre_x, self.post_y, self.post_x
        
    def set_weight(self, weight):
        self.weight = weight
    
    @staticmethod
    def rotate_array(arr, times=1):
        return np.rot90(arr,k=times)
    
    def rotate_mask(self,times=1):
        return Mask(Mask.rotate_array(self.mask, times), self.name + "_" + str(times*90), self.weight)
        
    def flip_x(self):
        m = copy.deepcopy(self.mask)
        for i in range(len(m)):
            for j in range(len(m[i])):
                m[i][j], m[i][len(m[i])-j-1] = m[i][len(m[i])-j-1], m[i][j]
        return Mask(m, self.name + "_flipped", self.weight)
    
    @staticmethod
    def blocked_rows(arr):
        pre = 0
        for row in arr:
            all_blocked = True
            for elem in row:
                if not (elem == 'o' or elem == 'b'):
                    all_blocked = False
            if all_blocked:
                pre += 1
            else:
                break
        return pre
    
    @staticmethod
    def positions_eq(board_position, mask_position):
        if board_position == mask_position:
            return True
        if board_position == ' ' and mask_position == '-':
            return True
        return False
    
    def check_at_board_position(self, x_start, y_start, board):
        for i in range(len(self.mask)):
            for j in range(len(self.mask[i])):
                y = y_start + i
                x = x_start + j
                if (not (y < 0 or y >= len(board) or \
                        x < 0 or x >= len(board[y]))) and \
                        not Mask.positions_eq(board[y][x], self.mask[i][j]):
                    return False
        return True
        
    def count_instances(self, board):
        instances = 0
        for y_start in range(-1*self.pre_y,len(board)+self.post_y-len(self.mask)+1):
            for x_start in range(-1*self.pre_x,len(board[0])+self.post_x-len(self.mask[0])+1):
                if self.check_at_board_position(x_start, y_start, board):
                    instances += 1
        return instances

    def count_difference(self, board):
        return count_instances(board) - count_instances(board.reverse)
                            
    #returns x-symmetric, y-symmetric
    def check_symmetric(mask):
        x_sym = True
        for row in mask:
            for i in range(len(row)):
                if row[i] != row[len(row)-1-i]:
                    x_sym = False
        for i in range(len(mask)):
            for j in range(len(mask[i])):
                if mask[i][j] != mask[i][len(mask[i])-1-j]:
                    x_sym = False
                if mask[i][j] != mask[len(mask)-1-i][j]:
                    y_sym = False
        return x_sym, y_sym

j = '''[
    {
        "name": "Shape_1",
        "weight": "25",
        "mask": "-xx-",
        "transforms": [
            "0,0",
            "90,0",
            "180,0"
        ]
    },
    {
        "name": "Shape_2",
        "weight": "25",
        "mask": "xx--",
        "transforms": [
            "0,0",
            "90,0",
            "180,0"
        ]
    },
    {
        "name": "Shape_3",
        "weight": "9999",
        "mask": "xxxx",
        "transforms": [
            "0,0",
            "90,0"
        ]
    },
    {
        "name": "Shape_4",
        "weight": "50",
        "mask": "xxx-",
        "transforms": [
            "0,0",
            "90,0",
            "180,0"
            
          ]
    },
    {
        "name": "Shape_5",
        "weight": "9999",
        "mask": "x---\\n-x--\\n--x-\\n---x",
        "transforms": [
            "0,0",
            "90,0"
        ]
    }
]'''
j = Eval(j)
