/* artfast: модуль расширения Python на C — быстрые целочисленные функции */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

/* gcd(a, b) */
static PyObject *artfast_gcd(PyObject *self, PyObject *args)
{
    long long a, b, t;

    if (!PyArg_ParseTuple(args, "LL", &a, &b))
        return NULL;
    if (a < 0) a = -a;
    if (b < 0) b = -b;
    while (b) {
        t = a % b;
        a = b;
        b = t;
    }
    return PyLong_FromLongLong(a);
}

/* popcount(n) - число единичных битов */
static PyObject *artfast_popcount(PyObject *self, PyObject *args)
{
    unsigned long long n;

    if (!PyArg_ParseTuple(args, "K", &n))
        return NULL;
    return PyLong_FromLong(__builtin_popcountll(n));
}

static PyMethodDef methods[] = {
    { "gcd", artfast_gcd, METH_VARARGS, "Greatest common divisor." },
    { "popcount", artfast_popcount, METH_VARARGS, "Number of set bits." },
    { NULL, NULL, 0, NULL }
};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT, "artfast", "Small integer helpers in C.", -1, methods
};

PyMODINIT_FUNC PyInit_artfast(void)
{
    return PyModule_Create(&module);
}
