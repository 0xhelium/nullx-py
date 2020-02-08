#ifndef __NULLX_LIBC_RAND_H__
#define __NULLX_LIBC_RAND_H__

#include <Python.h>

PyObject * libc_srand(PyObject* self, PyObject* args);
PyObject * libc_rand(PyObject* self, PyObject* args);

#endif
