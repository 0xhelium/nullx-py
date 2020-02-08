#include <stdlib.h>
#include <Python.h>

#include "rand.h"

PyObject * libc_srand(PyObject* self, PyObject* args) {
	unsigned int seed;
	if (!PyArg_ParseTuple(args, "I", &seed))
		return NULL;
	srand(seed);
	return Py_BuildValue("");
}

PyObject * libc_rand(PyObject* self, PyObject* args) {
	return PyLong_FromLong(rand());
}
