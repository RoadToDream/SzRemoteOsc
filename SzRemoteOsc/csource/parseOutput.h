#ifdef WIN32
#define LIB_EXPORT __declspec(dllexport)
#else
#define LIB_EXPORT
#endif

extern "C" LIB_EXPORT void parseOutput(char* dataRec, char* data, int dataLength);
