%module Wire

#define VERSION "0.22"

%include stl.i
%include "wire-enum.h"

%{
#include "WireWrapper.cc"
%}

%include "WireWrapper.cc"
