
#include <Python.h>
#include <stdlib.h>
#include <stdio.h>
#include <sys/socket.h>

#define SHELL_NAME "buildtcp.py"

void hexdump (char *desc, void *addr, int len)
{
	int i;
	unsigned char buff[17];
	unsigned char *pc = (unsigned char*)addr;

	if (desc != NULL)
		printf ("%s:\n", desc);

	for (i = 0; i < len; i++) {

		if ((i % 16) == 0) {
			if (i != 0)
				printf ("  %s\n", buff);

			printf ("  %04x ", i);
		}

		printf (" %02x", pc[i]);

		if ((pc[i] < 0x20) || (pc[i] > 0x7e))
			buff[i % 16] = '.';
		else
			buff[i % 16] = pc[i];
		buff[(i % 16) + 1] = '\0';
	}

	while ((i % 16) != 0) {
		printf ("   ");
		i++;
	}

	printf ("  %s\n", buff);
}

void print_dict(PyObject *dict)
{
	PyObject *key, *value;
	Py_ssize_t pos = 0;
	while (PyDict_Next(dict, &pos, &key, &value)) {
		PyObject* k_str_exc_type = PyObject_Repr(key);
		PyObject* k_pyStr = PyUnicode_AsEncodedString(k_str_exc_type, "utf-8", "Error ~");
		printf("key:%s ---> ", (const char *)PyBytes_AS_STRING(k_pyStr));

		PyObject* v_str_exc_type = PyObject_Repr(value);
		PyObject* v_pyStr = PyUnicode_AsEncodedString(v_str_exc_type, "utf-8", "Error ~");
		printf("value:%s\n", PyBytes_AsString(v_pyStr));
	}
}

int main(int argc, char **argv)
{
	Py_Initialize();

	PyRun_SimpleString("import sys");
	PyRun_SimpleString("import os");
	PyRun_SimpleString("import time");
	PyRun_SimpleString("import io");
	PyRun_SimpleString("import socket");
	//PyRun_SimpleString("print(os.getcwd())");
	PyRun_SimpleString("sys.path.append(os.getcwd())");
	PyRun_SimpleString("import buildtcp");

	//int ret =  PyRun_SimpleFile(fp, "./buildtcp.py");
	PyObject *main_module = PyImport_AddModule("__main__");
	PyObject *target = PyImport_AddModule("buildtcp");
	if(!main_module) {
		printf("failed to PyImport_AddModule()\n");
		return 0;
	}

	PyObject *g_dict = PyModule_GetDict(main_module);
	PyObject *l_dict = PyDict_New();
	if(!l_dict) {
		printf("failed to PyDict_New()\n");
		return 0;
	}

	FILE *fp = fopen("./buildtcp.py", "r");
	//PyObject *res = PyRun_File(fp, "./buildtcp.py", Py_file_input, g_dict, l_dict);
	//PyObject *res = PyRun_File(fp, "./buildtcp.py", Py_file_input, g_dict, g_dict);
	//PyObject *res = PyRun_String("buildtcp.buildtcp()", Py_file_input, g_dict, l_dict);
	printf("PyDict_Size(g_dict):%d\n", PyDict_Size(g_dict));
	print_dict(g_dict);
	printf("PyDict_Size(l_dict):%d\n", PyDict_Size(l_dict));
	print_dict(l_dict);
	//PyObject *key = PyUnicode_FromString("buildtcp");
	//PyObject *func = PyDict_GetItem(l_dict, key);
	//PyObject* f_str_exc_type = PyObject_Repr(func);
	//PyObject* f_pyStr = PyUnicode_AsEncodedString(f_str_exc_type, "utf-8", "Error ~");
	//printf("value:%s\n", PyBytes_AsString(f_pyStr));
	//res = PyObject_Call(func, PyTuple_New(), NULL);
	//res = PyObject_CallObject(func, NULL);
	PyObject *res = PyObject_CallMethodObjArgs(target, PyUnicode_FromString("buildtcp"), NULL);
	if(!res) {
		printf("failed to PyRun_File()\n");
		return 0;
	}

	if(!PyObject_CheckBuffer(res)) {
		printf("res is not Py_buffer\n");
		return 0;
	}

	Py_buffer buf;
	int ret = PyObject_GetBuffer(res, &buf, PyBUF_SIMPLE);
	if(ret == -1) {
		printf("failed to PyObject_GetBuffer()\n");
		return 0;
	}
	hexdump("return val", buf.buf, buf.len);

	fclose(fp);
	Py_Finalize();

	return 0;
}

