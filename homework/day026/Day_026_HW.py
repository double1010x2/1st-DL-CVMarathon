# %%
'''
## 『本次練習內容』
#### 學習搭建RPN層
'''

# %%
'''
## 『本次練習目的』
  #### 了解Object Detection演算法中是如何做到分類又回歸BBOX座標
'''

# %%
from tensorflow.keras.layers import Flatten, Dense, Input, Conv2D, MaxPooling2D, Dropout
from tensorflow.keras.layers import GlobalAveragePooling2D, GlobalMaxPooling2D, TimeDistributed


input_shape_img = (1024, 1024, 3)
img_input = Input(shape=input_shape_img)
'''先過一般CNN層提取特徵'''
def nn_base(img_input):
    # Block 1
    x = Conv2D(64, (3, 3), activation='relu', padding='same', name='block1_conv1')(img_input)
    x = Conv2D(64, (3, 3), activation='relu', padding='same', name='block1_conv2')(x)
    # 縮水1/2 1024x1024 -> 512x512
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block1_pool')(x)

    # Block 2
    x = Conv2D(128, (3, 3), activation='relu', padding='same', name='block2_conv1')(x)
    x = Conv2D(128, (3, 3), activation='relu', padding='same', name='block2_conv2')(x)
    # 縮水1/2 512x512 -> 256x256
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block2_pool')(x)

    # Block 3
    x = Conv2D(256, (3, 3), activation='relu', padding='same', name='block3_conv1')(x)
    x = Conv2D(256, (3, 3), activation='relu', padding='same', name='block3_conv2')(x)
    x = Conv2D(256, (3, 3), activation='relu', padding='same', name='block3_conv3')(x)
    # 縮水1/2 256x256 -> 128x128
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block3_pool')(x)

    # Block 4
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block4_conv1')(x)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block4_conv2')(x)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block4_conv3')(x)
    # 縮水1/2 128x128 -> 64x64
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block4_pool')(x)

    # Block 5
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block5_conv1')(x)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block5_conv2')(x)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block5_conv3')(x)

    # 最後返回的x是64x64x512的feature map。
    return x

# %%
'''過RPN'''
def rpn(base_layers, num_anchors):

    x = Conv2D(512, (3,3), padding='same', activation='relu', kernel_initializer='normal', name='rpn_conv1')(base_layers)

    # rpn分類和迴歸
    x_class = Conv2D(num_anchors * 2, (1, 1), activation='softmax',name='rpn_out_class')(x)
    x_reg = Conv2D(num_anchors * 4, (1, 1), activation='linear', name='rpn_out_regress')(x)

    return x_class, x_reg, base_layers

# %%
base_layers=nn_base(img_input)

# %%
x_class, x_reg, base_layers=rpn(base_layers, 9)

# %%
print('Classification支線：',x_class) #'''確認深度是否為18'''
print('BBOX Regression 支線：',x_reg) #'''確認深度是否為36'''
print('CNN Output：',base_layers)
