from core import process, predict


def c_main(path, model, ext):
    # 调用process模块的pre_process函数处理输入图像路径
    image_data = process.pre_process(path)
    # 调用predict模块的predict函数进行物体检测
    image_info = predict.predict(image_data, model, ext)
    # 返回处理后的图像文件名和检测结果信息
    return image_data[1] + '.' + ext, image_info


if __name__ == '__main__':
    pass
