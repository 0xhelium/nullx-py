#include <stdlib.h>
#include <Python.h>

#include "rand.h"

static PyMethodDef LibcMethods[] = {
	{"srand", libc_srand, METH_VARARGS,
	 "Sets its argument as the seed for a new sequence of pseudo-random integers to be returned by rand()."},
	{"rand", libc_rand, METH_VARARGS,
	 "Returns a pseudo-random integer in the range 0 to RAND_MAX inclusive (i.e., the mathematical range [0, RAND_MAX])."},
	{NULL, NULL, 0, NULL}
};

static struct PyModuleDef libcmodule = {
	PyModuleDef_HEAD_INIT,
	"nullx.libc",
	NULL,
	-1,
	LibcMethods
};

PyMODINIT_FUNC PyInit_libc(void) {
	return PyModule_Create(&libcmodule);
}
