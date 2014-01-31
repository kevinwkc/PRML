#coding:utf-8
import numpy as np
from mlp import MultiLayerPerceptron
from sklearn.datasets import load_digits
from sklearn.preprocessing import LabelBinarizer
from sklearn.metrics import confusion_matrix, classification_report

"""
簡易手書き数字データの認識
scikit-learnのインストールが必要
http://scikit-learn.org/
"""

def train_test_split(X, y, test_rate=0.1):
    """訓練データとテストデータに分割"""
    # 訓練データと教師信号をシャッフル
    num_samples= X.shape[0]
    p = np.arange(num_samples)
    np.random.seed(0)
    np.random.shuffle(p)
    X, y = X[p], y[p]

    # 訓練データとテストデータに分ける
    num_test = int(num_samples * test_rate)
    num_train = num_samples - num_test
    X_train = X[0:num_train, :]
    X_test = X[num_train:num_samples, :]
    y_train = y[0:num_train]
    y_test = y[num_train:num_samples]

    return X_train, X_test, y_train, y_test

def draw_digits(digits):
    """数字データの最初の10サンプルを描画"""
    import pylab
    for index, (image, label) in enumerate(zip(digits.images, digits.target)[:10]):
        pylab.subplot(2, 5, index + 1)
        pylab.axis('off')
        pylab.imshow(image, cmap=pylab.cm.gray_r, interpolation='nearest')
        pylab.title('%i' % label)
    pylab.show()

if __name__ == "__main__":
    # scikit-learnの簡易数字データをロード
    # 1797サンプル, 8x8ピクセル
    digits = load_digits()

    # 数字データのサンプルを描画
#     draw_digits(digits)

    # 訓練データを作成
    X = digits.data
    y = digits.target
    # ピクセルの値を0.0-1.0に正規化
    X /= X.max()

    # 多層パーセプトロン
    mlp = MultiLayerPerceptron(64, 100, 10, act1="tanh", act2="sigmoid")

    # 訓練データ（90%）とテストデータ（10%）に分解
    X_train, X_test, y_train, y_test = train_test_split(X, y, 0.1)

    # 教師信号の数字を1-of-K表記に変換
    # 0 => [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # 1 => [0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
    # ...
    # 9 => [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
    labels_train = LabelBinarizer().fit_transform(y_train)
    labels_test = LabelBinarizer().fit_transform(y_test)

    # 訓練データを用いてニューラルネットの重みを学習
    mlp.fit(X_train, labels_train, epochs=10000)

    # テストデータを用いて予測精度を計算
    predictions = []
    for i in range(X_test.shape[0]):
        o = mlp.predict(X_test[i])
        predictions.append(np.argmax(o))
    print confusion_matrix(y_test, predictions)
    print classification_report(y_test, predictions)