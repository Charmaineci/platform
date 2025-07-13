import cv2

def predict(dataset, model, ext):
    global img_y
    # 获取图像路径和文件名
    x = dataset[0].replace('\\', '/')
    file_name = dataset[1]
    print(x)
    print(file_name)
    # 读取图像
    x = cv2.imread(x)
    # 调用模型的detect方法进行物体检测
    img_y, image_info = model.detect(x)
    # 将标记了检测结果的图像保存到临时目录
    cv2.imwrite('./tmp/draw/{}.{}'.format(file_name, ext), img_y)
    # 返回检测结果信息
    return image_info