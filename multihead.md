多头注意力（Multi-Head Attention）的数学表达式如下：

$$
\text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, ..., \text{head}_h)W^O
$$

其中每个注意力头的计算为：
$$
\text{head}_i = \text{Attention}(QW_i^Q, KW_i^K, VW_i^V)
$$

而注意力机制的计算公式为：
$$
\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$

参数说明：
- $Q, K, V$：查询、键、值矩阵
- $W_i^Q, W_i^K, W_i^V$：第$i$个头对应的可学习参数矩阵
- $W^O$：输出投影矩阵
- $d_k$：键向量的维度
- $h$：注意力头的数量
