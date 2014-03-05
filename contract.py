#################################################################################
# Copyright (c) 2014 Seth Borders
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# 
#################################################################################

def _cast_list(func_name, types, values):

    conv = []
    for t, v in zip(types, values):

        try:
            x = t(v)
        except:
            raise ValueError("%s: Cannot convert value %s to %s" % (func_name, v, t))
        else:
            conv.append(x)

        return tuple(conv)
	
def _wrap(w, f):

    w.__name__ = f.__name__
    w.__doc__  = f.__doc__

def params(*types):

    def d(f):

        def w(*args):

            args = _cast_list(f.__name__, types, args)
            return f(*args)

        _wrap(w,f)
        return w

    return d

def returns(*types):

    def d(f):

        def w(*args,**kwargs):

            ret = f(*args,**kwargs)
            ret = _cast_list(f.__name__, types, [ret] if len(types) == 1 else ret)
            return ret[0] if len(types) == 1 else ret

        _wrap(w,f)
        return w

    return d
