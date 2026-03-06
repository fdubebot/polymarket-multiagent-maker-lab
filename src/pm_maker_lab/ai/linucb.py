from dataclasses import dataclass


@dataclass
class LinUCBArm:
    a: list[list[float]]
    b: list[float]


class LinUCBPolicy:
    def __init__(self, n_features: int, alphas: list[float], explore: float = 0.4):
        self.n_features = n_features
        self.alphas = alphas
        self.explore = explore
        self.arms = []
        for _ in alphas:
            ident = [[1.0 if i == j else 0.0 for j in range(n_features)] for i in range(n_features)]
            self.arms.append(LinUCBArm(a=ident, b=[0.0] * n_features))

    def _matvec(self, m: list[list[float]], v: list[float]) -> list[float]:
        return [sum(mr[i] * v[i] for i in range(self.n_features)) for mr in m]

    def _inv_diag_approx(self, m: list[list[float]]) -> list[float]:
        return [1.0 / max(1e-9, m[i][i]) for i in range(self.n_features)]

    def choose(self, x: list[float]) -> int:
        best_idx, best_score = 0, float("-inf")
        for idx, arm in enumerate(self.arms):
            inv_diag = self._inv_diag_approx(arm.a)
            theta = [inv_diag[i] * arm.b[i] for i in range(self.n_features)]
            exploit = sum(theta[i] * x[i] for i in range(self.n_features))
            explore = self.explore * sum((x[i] * x[i] * inv_diag[i]) ** 0.5 for i in range(self.n_features))
            score = exploit + explore
            if score > best_score:
                best_score = score
                best_idx = idx
        return best_idx

    def update(self, arm_idx: int, x: list[float], reward: float) -> None:
        arm = self.arms[arm_idx]
        for i in range(self.n_features):
            for j in range(self.n_features):
                arm.a[i][j] += x[i] * x[j]
        for i in range(self.n_features):
            arm.b[i] += reward * x[i]
