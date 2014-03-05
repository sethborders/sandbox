
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
