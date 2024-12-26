import cffi
import os



def GetLLvm() -> str:
    import subprocess

    result = subprocess.Popen(["llvm-config", "--bindir"], stdout=subprocess.PIPE, text=True, stderr=subprocess.PIPE)
    
    out, err = result.communicate()

    if result.returncode == 0:
        return out
    else: 
        print("it seems you do not have llvm installed please install llvm-19 and up")
        exit(1)

DLLLoaction = GetLLvm().split("\n")[0]
os.add_dll_directory(DLLLoaction)


ffi = cffi.FFI()

ffi.cdef("""
    typedef struct LLVMContext LLVMContext;
    typedef struct Module Module;
    typedef struct IRBuilder IRBuilder;
    typedef struct FunctionType FunctionType;
    typedef struct IntegerType IntegerType;
    typedef struct Function Function;
    typedef struct BasicBlock BasicBlock;
    typedef struct string string;
    typedef struct raw_string_ostream raw_string_ostream;
    typedef struct raw_fd_ostream raw_fd_ostream;
    typedef struct raw_ostream raw_ostream;
    typedef struct Type Type;
    typedef struct Value Value;
    typedef struct AssemblyAnnotationWriter AssemblyAnnotationWriter;
    

    LLVMContext* MakeContext();

    Module* MakeModule(const char* Name, LLVMContext* cont);
    void DelModule(Module* mod);
    
    IRBuilder* MakeBuilder(LLVMContext* cont);
    FunctionType* FuctionType_Get(Type* Res, bool IsVarArg);
    Type* getInt32Ty_(IRBuilder* b);
    unsigned int CreateExternalLinkage();
    Function* Function_Create(FunctionType* FT, unsigned int Linkage, const char * Name, Module* mod);
    BasicBlock* BasicBlock_Create(LLVMContext* c, const char* Name, Function* parent);
    void IRBuildermeth_SetInsertPoint(IRBuilder* b, BasicBlock* bb);
    void IRBuildermeth_CreateRet(IRBuilder* b, Value* val);
    Value* getInt32_(IRBuilder* b, unsigned int num);
    void DelStdString(string* s);
    raw_string_ostream* Make_raw_string_ostream(string* s);
    bool VerModule(Module* mod, raw_string_ostream* errstrm);
    string* MakeStdString(const char* info);
    raw_fd_ostream *llvm_errs();
    string *raw_string_ostreammeth_str(raw_string_ostream* errstrm);
    void modulemethdef_print(Module* mod, raw_fd_ostream *OS, AssemblyAnnotationWriter *AAW);
    raw_fd_ostream *llvm_outs();
    raw_ostream *AddCstr_and_llvmerr(raw_fd_ostream *s, const char* s1);
    raw_ostream *Addrawos_and_stdstring(raw_ostream *s, string* s1);
    AssemblyAnnotationWriter *MakeNullAAW();
""")


Lib = ffi.dlopen(os.getcwd()  + "/Wrapper.dll")



class LLVMContext:
    def __init__(self):
        self.Context = Lib.MakeContext()


class Module:
    def __init__(self, Name: str, c: LLVMContext):
        self.Module = Lib.MakeModule(Name.encode('utf-8'), c.Context)
        self.Del = False

    def __del__(self):
        if(self.Del == False):
            from time import sleep
            print("THE 'dispose' METHOD WAS NOT CALLED THIS WILL CAUSE A MEMORY LEAK")            
            sleep(5)
  
    def print(self, Os, AAW):
        Lib.modulemethdef_print(self.Module, Os, AAW)

    def dispose(self):

        Lib.DelModule(self.Module)
        self.Del = True

class IRBuilder:
    def __init__(self, Con: LLVMContext):
        self.IRBuilder = Lib.MakeBuilder(Con.Context)
    
    def getInt32Ty(self):
        return Lib.getInt32Ty_(self.IRBuilder)

    def SetInsertPoint(self, block):
        Lib.IRBuildermeth_SetInsertPoint(self.IRBuilder, block.Block)
    
    def CreateRet(self, value):
        Lib.IRBuildermeth_CreateRet(self.IRBuilder, value)
        
    def getInt32(self, num):
        return Lib.getInt32_(self.IRBuilder, num)

class FunctionType:
    def __init__(self):
        self.type = None

    def get(self, type, isvararg: bool):
        x = FunctionType()
        x.type = Lib.FuctionType_Get(type, isvararg)
        return x
    
class Function:
    def __init__(self):
        self.Func = None

    ExternalLinkage = Lib.CreateExternalLinkage()

    def Create(self, functype: FunctionType, Linkage, Name: str, Mod: Module):
        x = Function()
        x.Func = Lib.Function_Create(functype.type, Linkage, Name.encode('utf-8'), Mod.Module)
        return x
    
class BasicBlock:
    def __init__(self):
        self.Block = None

    def Create(self, con: LLVMContext, Name: str, Func: Function):
        x = BasicBlock()
        x.Block = Lib.BasicBlock_Create(con.Context, Name.encode('utf-8'), Func.Func)
        return x
    

class std:
    class string:
        def __init__(self, info: str):
            self.string = Lib.MakeStdString(info.encode('utf-8'))
        
        def __del__(self):
            Lib.DelStdString(self.string)

class raw_string_ostream:
    def __init__(self, strin: std.string):
        self.raw_str_os = Lib.Make_raw_string_ostream(strin.string)
    
    def str(self):
        return Lib.raw_string_ostreammeth_str()

def errs():
    return Lib.llvm_errs()

def verifyModule(mod: Module, errs: raw_string_ostream):
    return Lib.VerModule(mod.Module, errs.raw_str_os)

def Addcstr_llvmerr(err, info: str):
    return Lib.AddCstr_and_llvmerr(err, info.encode('utf-8'))

def Addrawos_string(ros, strin):
    return Lib.Addrawos_and_stdstring(ros, strin)

def outs():
    return Lib.llvm_outs()


def NullAAW():
    return Lib.MakeNullAAW()

