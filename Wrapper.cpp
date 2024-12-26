#include <llvm/IR/LLVMContext.h>
#include <llvm/IR/IRBuilder.h>
#include <llvm/IR/Module.h>
#include <llvm/IR/Function.h>
#include <llvm/IR/Verifier.h>
#include <llvm/Support/raw_ostream.h>
#include <iostream>
#include <string>

#ifdef _WIN32

#define EXPORT __declspec(dllexport) 

#else 

#define EXPORT

#endif




extern "C"{
    EXPORT llvm::LLVMContext* MakeContext(){
        return new llvm::LLVMContext();
    }


    EXPORT llvm::Module* MakeModule(const char* Name, llvm::LLVMContext& cont){
        return new llvm::Module(static_cast<llvm::StringRef>(Name), cont); 
    }

    EXPORT void DelModule(llvm::Module* mod){
        delete mod;
    }

    EXPORT llvm::IRBuilder<>* MakeBuilder(llvm::LLVMContext& cont){
        return new llvm::IRBuilder<>(cont);
    }


    EXPORT llvm::FunctionType* FuctionType_Get(llvm::Type* Res, bool IsVarArg){
        return llvm::FunctionType::get(Res, IsVarArg);
    }


    EXPORT llvm::Type* getInt32Ty_(llvm::IRBuilder<>* b){
        return b->getInt32Ty();
    }    

    EXPORT llvm::GlobalValue::LinkageTypes CreateExternalLinkage(){
        return llvm::Function::ExternalLinkage;
    }

    EXPORT llvm::Function* Function_Create(llvm::FunctionType* FT, llvm::GlobalValue::LinkageTypes Linkage, const char * Name, llvm::Module* mod){
        return llvm::Function::Create(FT, Linkage, static_cast<const llvm::Twine&>(Name), mod);
    }

    EXPORT llvm::BasicBlock* BasicBlock_Create(llvm::LLVMContext& c, const char* Name, llvm::Function* parent){
        return llvm::BasicBlock::Create(c, static_cast<const llvm::Twine&>(Name), parent);
    }

    EXPORT void IRBuildermeth_SetInsertPoint(llvm::IRBuilder<>* b, llvm::BasicBlock* bb){
        b->SetInsertPoint(bb);
    }

    EXPORT void IRBuildermeth_CreateRet(llvm::IRBuilder<>* b, llvm::Value* val){
        b->CreateRet(val);
    }

    EXPORT llvm::Value* getInt32_(llvm::IRBuilder<>* b, unsigned int num){
        return b->getInt32(num);
    }

    EXPORT std::string* MakeStdString(const char* info){
        return new std::string(info);
    }

    EXPORT void DelStdString(std::string* s){
        delete s;
    }

    EXPORT llvm::raw_string_ostream* Make_raw_string_ostream(std::string* s){
        return new llvm::raw_string_ostream(*s);
    }

    EXPORT bool VerModule(llvm::Module* mod, llvm::raw_string_ostream* errstrm){
        return verifyModule(*mod, &*errstrm);
    }

    EXPORT llvm::raw_fd_ostream *llvm_errs(){
        return &llvm::errs();
    }

    EXPORT std::string *raw_string_ostreammeth_str(llvm::raw_string_ostream* errstrm){
        return &errstrm->str();
    }

    EXPORT void modulemethdef_print(llvm::Module* mod, llvm::raw_fd_ostream &OS, llvm::AssemblyAnnotationWriter *AAW){
        mod->print(OS, AAW);
    }

    EXPORT llvm::raw_fd_ostream *llvm_outs(){
        return &llvm::outs();
    }

    EXPORT llvm::raw_ostream *AddCstr_and_llvmerr(llvm::raw_fd_ostream *s, const char* s1){
        return &(*s << s1);
    }

    EXPORT llvm::raw_ostream *Addrawos_and_stdstring(llvm::raw_ostream *s, std::string* s1){
        return &(*s << *s1);
    }

    EXPORT llvm::AssemblyAnnotationWriter *MakeNullAAW(){
        return (llvm::AssemblyAnnotationWriter *)nullptr;
    }

}


int main(){
    llvm::LLVMContext context;
    llvm::Module* mod = new llvm::Module("Main.z", context);

    llvm::IRBuilder<> builder(context);

    llvm::FunctionType* functype = llvm::FunctionType::get(builder.getInt32Ty(), false);
    llvm::Function* mainFunc = llvm::Function::Create(functype, llvm::Function::ExternalLinkage, "main", mod);
    llvm::BasicBlock* entry = llvm::BasicBlock::Create(context, "entry", mainFunc);
    builder.SetInsertPoint(entry);

    builder.CreateRet(builder.getInt32(3));

    std::string err;
    llvm::raw_string_ostream errStream(err);
    if(verifyModule(*mod, &errStream)){
        llvm::errs() << "Error: " << errStream.str();
    }

    mod->print(llvm::outs(), nullptr);
    delete mod;

    return 1;
}