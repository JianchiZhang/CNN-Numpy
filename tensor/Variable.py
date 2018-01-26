import numpy as np
from util import initializer

if 'GLOBAL_VARIABLE_SCOPE' not in globals():
    # global GLOBAL_VARIABLE_SCOPE
    GLOBAL_VARIABLE_SCOPE = {}


class Variable(object):
    def __init__(self, shape=list, name=str, scope='', grad=True, learnable=False, init='MSRA'):
        if scope != '':
            self.scope = scope if scope[-1] == '/' else scope + '/'
            self.name = self.scope + name
        else:
            self.name = name
            self.scope = scope

        if self.name in GLOBAL_VARIABLE_SCOPE:
            raise Exception('Variable name: %s exists!' % self.name)
        else:
            GLOBAL_VARIABLE_SCOPE[self.name] = self

        for i in shape:
            if not isinstance(i, int):
                raise Exception("Variable name: %s shape is not list of int"%self.name)

        self.shape = shape
        self.data = initializer(shape, init)
        self.child = []
        self.parent = []

        if grad:
            self.diff = np.zeros(self.shape)
            self.wait_bp = True
            self.learnable = learnable

    def eval(self):
        for operator in self.parent:
            GLOBAL_VARIABLE_SCOPE[operator].forward()
        self.wait_bp = True
        return self.data

    def diff_eval(self):
        if self.wait_bp:
            for operator in self.child:
                GLOBAL_VARIABLE_SCOPE[operator].backward()
            self.wait_bp = False
        else:
            pass

        return self.diff

    def apply_gradient(self, learning_rate=float, decay_rate=float, method='SGD'):
        self.data *= (1 - decay_rate)
        if method == 'SGD':
            learning_rate = learning_rate
        self.data -= learning_rate*self.diff
        self.diff *= 0


def get_by_name(name):
    if 'GLOBAL_VARIABLE_SCOPE' in globals():
        try:
            return GLOBAL_VARIABLE_SCOPE[name]
        except:
            raise Exception('GLOBAL_VARIABLE_SCOPE not include name: %s'%name)
    else:
        raise Exception('No Variable')


if __name__ == "__main__":
    shape = (3, 3, 12, 24)
    a = Variable(shape, 'a')
    print a.name

