
def int_pairs(A, B, K):
    """两个整数集合A和B，返回符合下面条件的整数对(a, b)

    1. a属于A，b属于B
    2. 0 <= b - a < K （K是一个常数，如2）
    3. 每个数字只能属于一个整数对
    """
    A, B = sorted(A), sorted(B)
    pairs = []
    i, j = 0, 0
    while i < len(A) and j < len(B):
        diff = B[j] - A[i]
        if diff >= K:
            i += 1
        elif diff < 0:
            j += 1
        else:
            pairs.append((A[i], B[j]))
            i += 1
            j += 1
    return pairs


if __name__ == '__main__':
    A = [1, 7, 8, 3]
    B = [2, 10,  4, 8]
    print int_pairs(A, B, 2)
