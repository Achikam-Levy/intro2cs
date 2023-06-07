# def main():
#     variabels = sys.argv
#     if len(variabels) == 8:
#         image_source = variabels[1]
#         cartoon_dest = int(variabels[2])
#         max_im_size = int(variabels[3])
#         blur_size = int(variabels[4])
#         th_block_size = int(variabels[5])
#         th_c = float(variabels[6])
#         quant_num_shades = variabels[7]
#         initial_image = ex5_helper.load_image(image_source)
#         new_small_image = resize_if_image_vivid(initial_image, max_im_size)
#         cartoon_image = cartoonify(new_small_image, blur_size, th_block_size, th_c, quant_num_shades)
#         ex5_helper.save_image(cartoon_image, cartoon_dest)
#     else:
#         print("wrong argument")
#         sys.exit()