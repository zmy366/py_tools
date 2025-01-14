import cv2
import os
import numpy as np

def cv2_imread(file_path):
    img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)
    return img

def cv2_imwrite(file_path, img):
    cv2.imencode('.jpg',img)[1].tofile(file_path)

image1 = cv2_imread('')
image2 = cv2_imread('')

# height, width = image1.shape[0:2]

# # 定义旋转参数
# angle = 90  # 旋转角度
# center = (width // 2, height // 2)  # 旋转中心
# scale = 1.0  # 缩放比例

# # 计算旋转矩阵
# rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale)

# # 应用旋转
# rotated_image1 = cv2.warpAffine(image1, rotation_matrix, (width, height))
# rotated_image2 = cv2.warpAffine(image2, rotation_matrix, (width, height))

# 合并图像
merged_image = cv2.vconcat([image1, image2])  # 使用 cv2.vconcat 垂直合并图像

# 保存合并后的图像
# cv2.imwrite('D:\\aaa.png', merged_image)  # 保存合并后的图像

cv2_imwrite('', merged_image)
cv2.waitKey(0)  # 等待按键
cv2.destroyAllWindows()  # 关闭所有打开的窗口