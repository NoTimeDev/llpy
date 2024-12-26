import llpy as llvm
from llpy import std, verifyModule

Context: llvm.LLVMContext = llvm.LLVMContext()
Module: llvm.Module = llvm.Module("Main.z", Context)
Builder: llvm.IRBuilder = llvm.IRBuilder(Context)

functype: llvm.FunctionType = llvm.FunctionType.get(llvm.FunctionType, Builder.getInt32Ty(), False)
mainFunc: llvm.Function = llvm.Function.Create(llvm.Function, functype, llvm.Function.ExternalLinkage, "main", Module)
entry: llvm.BasicBlock = llvm.BasicBlock.Create(llvm.BasicBlock, Context, "entry", mainFunc)

Builder.SetInsertPoint(entry)
Builder.CreateRet(Builder.getInt32(69))

err: std.string = std.string("")
errStream: llvm.raw_string_ostream = llvm.raw_string_ostream(err)
if(verifyModule(Module, errStream)):
    llvm.Addrawos_string(llvm.Addcstr_llvmerr(llvm.errs(), "Errors: "), errStream.str())

Module.print(llvm.outs(), llvm.NullAAW())
Module.dispose() 
