import json
from unittest import TestCase
from cartoonify import separate_channels, combine_channels, RGB2grayscale, blur_kernel, apply_kernel, \
    bilinear_interpolation, resize, rotate_90, get_edges, quantize, quantize_colored_image, add_mask
# from exercises.exercise5.ex5_helper import load_image, save_image


class TestExercise5(TestCase):
    def test_separate_channels(self):
        self.assertEqual([[[1]], [[2]]], separate_channels([[[1, 2]]]))
        self.assertEqual([
            [[0, 177, 123], [206, 167, 2]],
            [[255, 187, 124], [207, 157, 3]],
            [[200, 197, 125], [208, 147, 4]]
        ], separate_channels([
            [[0, 255, 200], [177, 187, 197], [123, 124, 125]],
            [[206, 207, 208], [167, 157, 147], [2, 3, 4]]
        ]))
        self.assertEqual([
            [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        ], separate_channels([
            [[1, 1, 1], [2, 2, 2], [3, 3, 3]],
            [[4, 4, 4], [5, 5, 5], [6, 6, 6]],
            [[7, 7, 7], [8, 8, 8], [9, 9, 9]],
        ]))

    def test_combine_channels(self):
        self.assertEqual([[[1, 2]]], combine_channels([[[1]], [[2]]]))
        self.assertEqual([
            [[0, 255, 200], [177, 187, 197], [123, 124, 125]],
            [[206, 207, 208], [167, 157, 147], [2, 3, 4]]
        ], combine_channels([
            [[0, 177, 123], [206, 167, 2]],
            [[255, 187, 124], [207, 157, 3]],
            [[200, 197, 125], [208, 147, 4]]
        ]))
        self.assertEqual([
            [[1, 1, 1], [2, 2, 2], [3, 3, 3]],
            [[4, 4, 4], [5, 5, 5], [6, 6, 6]],
            [[7, 7, 7], [8, 8, 8], [9, 9, 9]]
        ], combine_channels([
            [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            [[1, 2, 3], [4, 5, 6], [7, 8, 9]]]
        ))

    def test_channel_together(self):
        lst = [[[0, 255, 200], [177, 187, 197], [123, 124, 125]],
               [[206, 207, 208], [167, 157, 147], [2, 3, 4]]]
        self.assertEqual(lst, combine_channels(separate_channels(lst)))
        lst = [[[0, 255, 200, 233], [89, 189, 198, 98]],
               [[1, 254, 201, 232], [88, 188, 199, 99]]]
        self.assertEqual(lst, combine_channels(separate_channels(lst)))

    def test_RGB2grayscale(self):
        self.assertEqual([[163]], RGB2grayscale([[[100, 180, 240]]]))
        self.assertEqual([[20, 40, 60], [10, 30, 40]], RGB2grayscale([
            [[10, 20, 44], [30, 39, 70], [52, 60, 78]],
            [[10, 2, 50], [30, 36, 0], [27, 40, 70]]
        ]))

    def test_blur_kernel(self):
        one_to_nine = 1 / 9
        self.assertEqual([[one_to_nine] * 3] * 3, blur_kernel(3))
        one_to_tw_five = 1 / 25
        self.assertEqual([[one_to_tw_five] * 5] * 5, blur_kernel(5))
        one_to_200_squared = 1 / (200 ** 2)
        self.assertEqual([[one_to_200_squared] * 200] * 200, blur_kernel(200))
        one_to_minus_nine = 1 / (-3) ** 2
        self.assertEqual([[one_to_minus_nine] * 3] * 3, blur_kernel(-3))

    def test_apply_kernel(self):
        self.assertEqual([[14, 128, 241]], apply_kernel([[0, 128, 255]], blur_kernel(3)))
        self.assertEqual(
            [[18, 30, 40, 50, 54], [38, 46, 56, 66, 74], [68, 76, 86, 96, 104],
             [98, 106, 116, 126, 134], [130, 138, 148, 158, 166], [164, 170, 180, 190, 202],
             [198, 206, 216, 228, 236], [221, 226, 238, 251, 255]],
            apply_kernel([[10, 20, 30, 40, 50], [40, 50, 60, 70, 80], [70, 80, 90, 100, 110],
             [100, 110, 120, 130, 140], [130, 140, 150, 160, 170], [170, 180, 190, 200, 210],
             [200, 210, 220, 230, 240], [230, 240, 250, 270, 280]],
                         [[0.1, 0.2, 0.2], [0.05, 0.05, 0.1], [0.1, 0.1, 0.1]])
        )
        self.assertEqual([[0, 4, 10]], apply_kernel([[0, 5, 10]],
                                                    [[-0.1, -0.1, 0.4], [0.1, 0.2, -0.2], [0.3, 0.2, 0.2]]))
        self.assertEqual([[1, 2, 3]], apply_kernel([[1, 2, 3]], blur_kernel(1)))

    def test_bilinear_interpolation(self):
        self.assertEqual(0, bilinear_interpolation([[0, 64], [128, 255]], 0, 0))
        self.assertEqual(255, bilinear_interpolation([[0, 64], [128, 255]], 1, 1))
        self.assertEqual(64, bilinear_interpolation([[0, 64], [128, 255]], 0.5, 0))
        self.assertEqual(160, bilinear_interpolation([[0, 64], [128, 255]], 0.5, 1))
        # self.assertEqual(64, bilinear_interpolation([[0, 64], [128, 255]], -0.5, 1))
        # self.assertEqual(32, bilinear_interpolation([[0, 64], [128, 255]], -0.5, 0.5))
        # self.assertEqual(128, bilinear_interpolation([[0, 64], [128, 255]], 1, -0.5))
        # self.assertEqual(64, bilinear_interpolation([[0, 64], [128, 255]], 0.5, -0.5))
        self.assertEqual(112, bilinear_interpolation([[0, 64], [128, 255]], 0.5, 0.5))
        # self.assertEqual(160, bilinear_interpolation([[0, 64], [128, 255]], 0.5, 1.5))
        # self.assertEqual(192, bilinear_interpolation([[0, 64], [128, 255]], 1.5, 0.5))
        # self.assertEqual(255, bilinear_interpolation([[0, 64], [128, 255]], 3, 3))

    def test_resize(self):
        self.assertEqual([[0, 64], [128, 255]], resize([[0, 64], [128, 255]], 2, 2))
        self.assertEqual([[0, 32, 64], [128, 192, 255]], resize([[0, 64], [128, 255]], 2, 3))
        self.assertEqual([[0, 32, 64], [64, 112, 160], [128, 192, 255]], resize([[0, 64], [128, 255]], 3, 3))
        self.assertEqual([[0, 21, 43, 64], [43, 71, 99, 128], [85, 121, 156, 191], [128, 170, 213, 255]],
                         resize([[0, 64], [128, 255]], 4, 4))

    def test_rotate90(self):
        self.assertEqual([[4, 1], [5, 2], [6, 3]], rotate_90([[1, 2, 3], [4, 5, 6]], 'R'))
        self.assertEqual([[3, 6], [2, 5], [1, 4]], rotate_90([[1, 2, 3], [4, 5, 6]], 'L'))
        test_list = [
            [[0, 255, 132], [233, 100, 101]],
            [[1, 254, 133], [232, 101, 100]],
            [[2, 253, 134], [231, 104, 105]],
        ]
        json_list = json.dumps(test_list)
        self.assertEqual(json.loads(json_list),
                         rotate_90(rotate_90(rotate_90(rotate_90(test_list, 'R'), 'R'), 'R'), 'R'))
        self.assertEqual(json.loads(json_list),
                         rotate_90(rotate_90(rotate_90(rotate_90(test_list, 'L'), 'L'), 'L'), 'L'))
        self.assertEqual(json.loads(json_list),
                         rotate_90(rotate_90(test_list, 'R'), 'L'))
        self.assertEqual([
            [[2, 253, 134], [1, 254, 133], [0, 255, 132]],
            [[231, 104, 105], [232, 101, 100], [233, 100, 101]]
        ], rotate_90(test_list, 'R'))

    def test_get_edges(self):
        self.assertEqual([[255, 0, 255]], get_edges([[200, 50, 200]], 3, 3, 10))
        # ziggy = load_image('examples/ziggy.jpg')
        # ziggy_channels = separate_channels(ziggy)
        # new_ziggy = combine_channels([get_edges(channel, 5, 15, 17) for channel in ziggy_channels])
        # save_image(new_ziggy, 'examples/ziggy_new.jpg')

    def test_quantize(self):
        self.assertEqual([[0, 32, 96], [128, 191, 223]], quantize([[0, 50, 100], [150, 200, 250]], 8))
        self.assertEqual([[0, 42, 96], [149, 191, 244]], quantize([[0, 50, 100], [150, 200, 250]], 24))

    def test_quantize_colored_image(self):
        self.assertEqual([[[0, 32, 96], [128, 191, 223]]],
                         quantize_colored_image([[[0, 50, 100], [150, 200, 250]]], 8))

    def test_add_mask(self):
        self.assertEqual([[0, 255, 0], [255, 0, 255]],
                         add_mask([[255, 255, 255], [255, 255, 255]], [[0, 0, 0], [0, 0, 0]], [[0, 1, 0], [1, 0, 1]]))
        self.assertEqual([
                             [[13, 14], [3, 4], [17, 18]],
                             [[7, 8], [21, 22], [11, 12]]
                         ],
                         add_mask([
                             [[1, 2], [3, 4], [5, 6]],
                             [[7, 8], [9, 10], [11, 12]]
                         ], [
                             [[13, 14], [15, 16], [17, 18]],
                             [[19, 20], [21, 22], [23, 24]]
                         ], [[0, 1, 0], [1, 0, 1]]))

