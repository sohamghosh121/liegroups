import copy

import numpy as np

from liegroups import SE3

def test_bindto():
    T1 = SE3.identity()
    T2 = SE3.identity()
    T2.bindto(T1)
    assert(T1 is not T2 and T1.rot is T2.rot and T1.trans is T2.trans)

def test_identity():
    T = SE3.identity()
    assert isinstance(T, SE3)


def test_mul():
    T = np.array([[0, 0, -1, 0.1],
                  [0, 1, 0, 0.5],
                  [1, 0, 0, -0.5],
                  [0, 0, 0, 1]])
    T2 = T.dot(T)
    assert np.allclose(
        (SE3.from_matrix(T) * SE3.from_matrix(T)).as_matrix(), T2)


def test_wedge_vee():
    xi = np.array([1, 2, 3, 4, 5, 6])
    Xi = SE3.wedge(xi)
    assert np.array_equal(xi, SE3.vee(Xi))


def test_exp_log():
    T = SE3.exp(np.array([1, 2, 3, 4, 5, 6]))
    assert np.allclose(SE3.exp(SE3.log(T)).as_matrix(), T.as_matrix())


def test_perturb():
    T = SE3.exp(np.array([1, 2, 3, 4, 5, 6]))
    T_copy = copy.deepcopy(T)
    xi = np.array([0.6, 0.5, 0.4, 0.3, 0.2, 0.1])
    T.perturb(xi)
    assert np.allclose(T.as_matrix(), (SE3.exp(xi) * T_copy).as_matrix())


def test_normalize():
    T = SE3.exp(np.array([1, 2, 3, 4, 5, 6]))
    T.rot.mat += 0.1
    T.normalize()
    assert SE3.is_valid_matrix(T.as_matrix())


def test_inv():
    T = SE3.exp(np.array([1, 2, 3, 4, 5, 6]))
    assert np.allclose((T * T.inv()).as_matrix(), np.identity(4))


def test_adjoint():
    T = SE3.exp(np.array([1, 2, 3, 4, 5, 6]))
    assert T.adjoint().shape == (6, 6)
