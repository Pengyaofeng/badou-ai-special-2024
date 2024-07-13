import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

# 使用numpy生成200个随机点
'''
`np.linspace(-0.5, 0.5, 200)` 生成了一个在 `-0.5` 到 `0.5` 之间均匀分布的 200 个点的数组。 ->  ndarray=(200,):  [-0.5 -0.49497487 -0.48994975   ... , -0.40954774 -0.40452261 -0.39949749, ...]
`   [:, np.newaxis]` 则将这个一维数组转换为了一个二维数组，其中每个元素都是一个单列数组。       ->   ndarray=(200,1) [[-0.5       ], [-0.49497487], [-0.48994975],  ... , [-0.42964824], [-0.42462312], [-0.41959799], ...]
                    : 表示切片操作，它可以用来选择数组中的一部分元素。np.newaxis 是 NumPy 中的一个常量，它表示一个新的维度。
                    在 [:, np.newaxis] 中，: 表示选择数组中的所有行，np.newaxis 表示在列方向上添加一个新的维度。 
'''
x_data = np.linspace(-0.5, 0.5, 200)[:, np.newaxis]
'''
生成了一个与 `x_data` 形状相同的正态分布噪声数组 `noise`。
`np.random.normal(0, 0.02, x_data.shape)`：这是 NumPy 中的 `random.normal()` 函数，用于生成正态分布的随机数。
    - `0`：表示正态分布的均值。
    - `0.02`：表示正态分布的标准差。
    - `x_data.shape`：表示生成的噪声数组的形状与 `x_data` 相同。
生成的噪声数组 `noise` 将被添加到 `x_data` 中，可以模拟数据中的噪声或不确定性。这种添加噪声的操作在许多数据分析和机器学习任务中是常见的，用于模拟真实世界中的噪声情况或增加数据的多样性。
-> ndarray=(200,1)  [[-1.94065991e-02], [-1.90875956e-02], [-3.32497285e-02],  [-4.50778537e-02], [-4.12792091e-02], ... ]
'''
noise = np.random.normal(0, 0.02, x_data.shape)
'''
`y_data` 是 `x_data` 的平方加上噪声:
        `np.square(x_data)`：这部分计算 `x_data` 的平方, `+ noise`：将上一步计算得到的平方结果与噪声数组 `noise` 相加。
ndarray=(200,1)  [[ 2.75000018e-01], [ 2.45577994e-01], [ 1.90546902e-01], ... , [ 2.10356814e-01], [ 1.95916267e-01], [ 1.78977107e-01]]
'''
y_data = np.square(x_data) + noise

# 定义两个placeholder存放输入数据
'''
定义了两个占位符 x 和 y，用于在 TensorFlow 图中接收输入数据：
    tf.placeholder(tf.float32, [None, 1])：这是 TensorFlow 中的 placeholder() 函数，用于创建一个占位符。
        1. tf.float32：指定占位符的数据类型为 float32，即 32 位浮点数。
        2. [None, 1]：指定占位符的形状。None 表示该维度的大小可以是任意值，而 1 表示该维度的大小为 1。
    在 TensorFlow 中，占位符用于在计算图中表示输入数据。它们在执行计算图时将被实际的数据所填充。通过使用占位符，你可以在构建计算图时不确定输入数据的具体值，而是在运行时动态地提供数据。
'''
x = tf.placeholder(tf.float32, [None, 1])
y = tf.placeholder(tf.float32, [None, 1])


"""      
在神经网络中，通常要求输入数据具有固定的维度。将图片转换为 2 维数组可以将图像的每个像素作为一个输入特征，并且可以通过调整数组的维度来适应不同大小的图片。
具体来说，通过将图片转换为 2 维数组，可以将图像的高度和宽度作为数组的两个维度，这样神经网络就可以对每个像素进行处理和分析。
inputs -> ndarray:(200,1)      [    [-1.94065991e-02], 
                                    [-1.90875956e-02], 
                                     ...                                                                                                               
                                    [-4.12792091e-02]   ]                                          
                  
          x_data                    L1                          final_outputs      y_data(标签值)
          (200,1)                 (?, 10)                         (?, 1)             (200,1)
                                  zh1/ah1                         zo1/ao1
                   Weights_L1                  Weights_L2
                    (1, 10)                     (10, 1)
                   biases_L1                   biases_L2
                    (1, 10)                     (1, 1)
                  Wx_plus_b_L1                Wx_plus_b_L2
"""
# 定义神经网络中间层    # 权重 Weights 和偏置 biases 。在训练神经网络时，这些参数将通过反向传播算法进行优化，以提高模型的性能
'''
创建了一个名为 Weights_L1 的变量，用于存储神经网络第一层的权重。tf.random_normal([1, 10]) 表示生成一个形状为 [1, 10] 的随机正态分布的权重矩阵。
Weights_L1 =》    <tf.Variable 'Variable:0' shape=(1, 10) dtype=float32_ref>
'''
Weights_L1 = tf.Variable(tf.random_normal([1, 10]))
'''
创建了一个名为 biases_L1 的变量，用于存储神经网络第一层的偏置。tf.zeros([1, 10]) 表示生成一个形状为 [1, 10] 的全零偏置矩阵。
biases_L1 =》     <tf.Variable 'Variable_1:0' shape=(1, 10) dtype=float32_ref>
'''
biases_L1 = tf.Variable(tf.zeros([1, 10]))  # 加入偏置项
'''
wx+b: 计算了输入数据 x 与权重矩阵 Weights_L1 的矩阵乘法，并加上偏置矩阵 biases_L1。结果存储在 Wx_plus_b_L1 中。
Wx_plus_b_L1 =》  <tf.Tensor 'add:0' shape=(?, 10) dtype=float32>
'''
Wx_plus_b_L1 = tf.matmul(x, Weights_L1) + biases_L1
'''
激活函数： 应用了双曲正切（tanh）激活函数。激活函数的作用是在神经网络中引入非线性，增加模型的表达能力。
L1 =》 <tf.Tensor 'Tanh:0' shape=(?, 10) dtype=float32>
'''
L1 = tf.nn.tanh(Wx_plus_b_L1)  # 加入激活函数

# 定义神经网络输出层
Weights_L2 = tf.Variable(tf.random_normal([10, 1]))   # <tf.Variable 'Variable_2:0' shape=(10, 1) dtype=float32_ref>
biases_L2 = tf.Variable(tf.zeros([1, 1]))  # 加入偏置项   <tf.Variable 'Variable_3:0' shape=(1, 1) dtype=float32_ref>
Wx_plus_b_L2 = tf.matmul(L1, Weights_L2) + biases_L2  # <tf.Tensor 'add_1:0' shape=(?, 1) dtype=float32>
prediction = tf.nn.tanh(Wx_plus_b_L2)  # 加入激活函数     <tf.Tensor 'Tanh_1:0' shape=(?, 1) dtype=float32>

# 定义损失函数（均方差函数）
'''
计算了预测值与真实值之间的均方误差（Mean Squared Error，MSE）损失：
    1. `tf.square(y - prediction)`：这部分计算了预测值 `prediction` 与真实值 `y` 之间的差的平方。`tf.square()` 函数用于对输入的张量进行元素级的平方操作。
    2. `tf.reduce_mean()`：这是 TensorFlow 中的 `reduce_mean()` 函数，用于计算张量的平均值。在这里，它用于计算平方差的平均值，即均方误差。
均方误差是一种常用的损失函数，用于衡量预测值与真实值之间的差异。在训练神经网络时，通过最小化均方误差来优化模型的参数，以使预测值尽可能接近真实值。
'''
loss = tf.reduce_mean(tf.square(y - prediction))  # <tf.Tensor 'Mean:0' shape=() dtype=float32>

# 定义反向传播算法（使用梯度下降算法训练）
'''
训练步骤，通过梯度下降算法来最小化损失函数 `loss`:
    1. `tf.train.GradientDescentOptimizer(0.1)`：这创建了一个梯度下降优化器对象。`0.1` 是学习率（learning rate），它控制了每次迭代中参数更新的幅度。
    2. `.minimize(loss)`：这是优化器对象的 `minimize()` 方法，用于指定要最小化的目标函数，即损失函数 `loss`。
在训练神经网络时，通常会在一个循环中重复执行训练步骤，通过不断调整模型的参数来最小化损失函数。每次执行训练步骤时，都会根据当前的参数值和损失函数的梯度来更新参数，以逐步降低损失。
'''
train_step = tf.train.GradientDescentOptimizer(0.1).minimize(loss)  #  <tf.Operation 'GradientDescent' type=NoOp>

with tf.Session() as sess:  # 创建了一个 TensorFlow 会话，并将其命名为 sess。在这个会话中，将执行 TensorFlow 图的计算。
    # 变量初始化:  初始化了所有的全局变量, 在训练神经网络之前，需要先初始化变量，以便在训练过程中对其进行更新。
    sess.run(tf.global_variables_initializer())
    # 训练2000次
    for i in range(2000):
        # 在每次训练迭代中，执行训练步骤 train_step。feed_dict 参数用于提供训练数据。在这里，将 x_data 作为输入 x 的值，将 y_data 作为输入 y 的值。
        sess.run(train_step, feed_dict={x: x_data, y: y_data})

    # 获得预测值
    prediction_value = sess.run(prediction, feed_dict={x: x_data}) # [[0.23106132], [0.227212  ], [0.22337301], [0.21954514], [0.215729  ], [0.21192546], [0.208135  ], [0.20435847], [0.20059659], [0.19684997], [0.19311948], [0.1894058 ], [0.18570952], [0.18203175], [0.17837273], [0.17473327], [0.17111431], [0.16751657], [0.16394041], [0.16038695], [0.15685648], [0.15335025], [0.14986838], [0.14641215], [0.14298166], [0.13957812], [0.13620187], [0.13285407], [0.12953489], [0.12624525], [0.12298585], [0.11975718], [0.11655988], [0.11339476], [0.11026268], [0.10716382], [0.10409924], [0.10106912], [0.09807483], [0.09511615], [0.09219405], [0.08930916], [0.08646214], [0.08365341], [0.08088366], [0.07815327], [0.07546317], [0.07281363], [0.07020503], [0.06763861], [0.06511384], [0.06263224], [0.0601936 ], [0.05779885], [0.05544851], [0.05314253], [0.05088187], [0.04866666], [0.04649776], [0.0443754 ], [0.04229973], [0.04027157], [0.0382912 ], [0.03635892], [0.03447521], [0.0326403 ], [0.0308548 ], [0.02911876], [0.02743277], [0.02579683], [0.02421183], [0.02267741], [0.02119444], [0.0197628 ], [0.01838298], [0.0170552 ], [0.01577953], [0.01455639], [0.01338599], [0.01226861], [0.01120419], [0.01019317], [0.0092358 ], [0.00833185], [0.00748206], [0.0066859 ], [0.00594418], [0.00525648], [0.00462311], [0.00404418], [0.00351994], [0.00305026], [0.00263535], [0.00227499], [0.00196945], [0.00171867], [0.00152284], [0.00138163], [0.00129536], [0.00126395], [0.00128734], [0.00136524], [0.00149807], [0.00168526], [0.00192722], [0.00222337], [0.00257414], [0.00297912], [0.00343807], [0.00395117], [0.00451797], [0.00513856], [0.00581264], [0.00654006], [0.00732054], [0.00815406], [0.00904014], [0.00997877], [0.01096968], [0.01201256], [0.01310723], [0.01425331], [0.01545053], [0.01669871], [0.01799735], [0.01934626], [0.02074507], [0.02219342], [0.02369103], [0.02523732], [0.02683216], [0.028475  ], [0.03016555], [0.03190334], [0.03368786], [0.0355189 ], [0.0373957 ], [0.0393181 ], [0.04128534], [0.04329726], [0.04535306], [0.04745236], [0.04959489], [0.05177967], [0.05400643], [0.05627462], [0.05858369], [0.06093299], [0.06332204], [0.06575011], [0.06821689], [0.07072149], [0.07326344], [0.07584219], [0.0784568 ], [0.08110698], [0.08379202], [0.08651114], [0.08926363], [0.09204905], [0.09486665], [0.09771558], [0.10059536], [0.10350519], [0.1064444 ], [0.10941222], [0.11240812], [0.11543107], [0.11848065], [0.121556  ], [0.12465632], [0.12778103], [0.13092943], [0.13410051], [0.13729376], [0.1405082 ], [0.1437434 ], [0.14699832], [0.15027241], [0.15356478], [0.15687473], [0.16020148], [0.1635443 ], [0.16690223], [0.17027491], [0.17366138], [0.1770608 ], [0.18047246], [0.18389572], [0.18732965], [0.19077365], [0.19422698], [0.19768885], [0.20115826], [0.20463492], [0.20811783], [0.21160634], [0.21509974], [0.21859737], [0.22209841]]

    # 画图
    plt.figure()
    plt.scatter(x_data, y_data)  # 散点是真实值
    plt.plot(x_data, prediction_value, 'r-', lw=5)  # 曲线是预测值
    plt.show()
