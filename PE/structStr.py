#coding=utf-8
ImageFileHeaderStructStr = '''typedef struct _IMAGE_FILE_HEADER {
      WORD Machine;                     //这里定义的是运行平台,i386= 0x014Ch这个值，还有其他平台，看书吧。。
      WORD NumberOfSections;　　　　　　　//这个是标识区块的数目，紧跟在PE头的后面，也就是IMAGE_NT_HEADERS的后面
      DWORD TimeDateStamp;
      DWORD PointerToSymbolTable;
      DWORD NumberOfSymbols;
      WORD SizeOfOptionalHeader; 　　　　//这里表明了IMAGE_NT_HEADERS中的大小(RAW SIZE)，32位一般是0x00E0, 64位PE+一般是0x00F0
      WORD Characteristics;　　　　　　　//普通的EXE是0x010fh, DLL文件是0x210Eh
    } IMAGE_FILE_HEADER,*PIMAGE_FILE_HEADER;'''
    
ImageOptionalHeaderStructStr = '''typedef struct _IMAGE_OPTIONAL_HEADER {

      WORD Magic;
      BYTE MajorLinkerVersion;
      BYTE MinorLinkerVersion;
      DWORD SizeOfCode;　　　　　　　　　　　//这里定义了包含代码区块的大小
      DWORD SizeOfInitializedData;　　　　//这里定义了已经初始化的变量的区块的大小
      DWORD SizeOfUninitializedData;　　　//这里是未初始化的变量的区块的大小
      DWORD AddressOfEntryPoint;　　　　　//这里是程序入口的RVA（相对虚拟地址）
      DWORD BaseOfCode;　　　　　　　　　　//这里是程序代码块的起始RVA
      DWORD BaseOfData;　　　　　　　　　　//这里是数据块起始RVA
      DWORD ImageBase;　　　　　　　　　　　//这里是程序默认装入的基地址(ImageBase)
      DWORD SectionAlignment;　　　　　　 //内存中区块的对齐值，非常重要
      DWORD FileAlignment;　　　　　　　　//文件中区块的对齐值，非常重要
      WORD MajorOperatingSystemVersion;
      WORD MinorOperatingSystemVersion;
      WORD MajorImageVersion;
      WORD MinorImageVersion;
      WORD MajorSubsystemVersion;
      WORD MinorSubsystemVersion;
      DWORD Win32VersionValue;
      DWORD SizeOfImage;
      DWORD SizeOfHeaders;
      DWORD CheckSum;
      WORD Subsystem;　　　　　　　　　　//这里定义了文件的子系统，图形接口子系统，字符子系统，具体可以看具体的定义
      WORD DllCharacteristics;
      DWORD SizeOfStackReserve;
      DWORD SizeOfStackCommit;
      DWORD SizeOfHeapReserve;
      DWORD SizeOfHeapCommit;
      DWORD LoaderFlags;
      DWORD NumberOfRvaAndSizes;　　　//这里定义了数据目录表的项数，一直保持为16
      IMAGE_DATA_DIRECTORY DataDirectory[IMAGE_NUMBEROF_DIRECTORY_ENTRIES]; //这个是数据目录表，指向输入、输出表、资源块等数据，很重要
    } IMAGE_OPTIONAL_HEADER32,*PIMAGE_OPTIONAL_HEADER32;'''
    
ImageDataDirectoryStructStr = '''typedef struct _IMAGE_DATA_DIRECTORY {
      DWORD VirtualAddress;            //数据块的其实RVA，很重要
      DWORD Size;　　　　　　　　　　　　　//数据块的长度
    } IMAGE_DATA_DIRECTORY,*PIMAGE_DATA_DIRECTORY;'''
    
ImageSectionHeaderStructStr = '''        DWORD VirtualSize;  
    } Misc;                     //区块尺寸</span>  
    DWORD VirtualAddress;       //区块的RVA地址  
    DWORD SizeOfRawData;        //在文件中对齐后的尺寸  
    DWORD PointerToRawData;     //在文件中偏移  
    DWORD PointerToRelocations; //在OBJ文件中使用，重定位的偏移  
    DWORD PointerToLinenumbers; //行号表的偏移（供调试使用地）  
    WORD NumberOfRelocations;   //在OBJ文件中使用，重定位项数目  
    WORD NumberOfLinenumbers;   //行号表中行号的数目  
    DWORD Characteristics;      //区块属性如可读，可写，可执行等  
} IMAGE_SECTION_HEADER, *PIMAGE_SECTION_HEADER;  '''

ImageImportDescriptor = '''        DWORD OriginalFirstThunk;    //指向输入名称表（INT）的RVA  
    }  
    DWORD TimeDateStamp;             //一个32位的时间标志  
    DWORD ForwarderChain;            //这是一个被转向API的索引，一般为0  
    DWORD Name;                      //DLL名字,是个以00结尾的ASCII字符的RVA地址  
    DWORD FirstThunk;                //指向输入地址表（IAT）的RVA  '''