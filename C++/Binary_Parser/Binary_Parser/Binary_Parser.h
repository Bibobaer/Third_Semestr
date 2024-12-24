#pragma once
#include <string>
#include <fstream>
#include <iostream>

struct DOS_HEADER {
    uint16_t e_magic;       // Magic number    маркус лох
    uint16_t e_cblp;        // Bytes on last page of file
    uint16_t e_cp;          // Pages in file
    uint16_t e_crlc;        // Relocations
    uint16_t e_cparhdr;     // Size of header in paragraphs
    uint16_t e_minalloc;    // Minimum extra paragraphs needed
    uint16_t e_maxalloc;    // Maximum extra paragraphs needed
    uint16_t e_ss;          // Initial (relative) SS
    uint16_t e_sp;          // Initial SP
    uint16_t e_csum;        // Checksum
    uint16_t e_ip;          // Initial IP
    uint16_t e_cs;          // Initial (relative) CS
    uint16_t e_lfarlc;      // File address of relocation table
    uint16_t e_ovno;        // Overlay number
    uint16_t e_res[4];      // Reserved words
    uint16_t e_oemid;       // OEM identifier (for e_oeminfo)
    uint16_t e_oeminfo;     // OEM information; e_oemid specific
    uint16_t e_res2[10];    // Reserved words
    long e_lfanew;          // File address of new exe header
};

struct DOS_FILE {
    uint16_t Machine;
    uint16_t NumberOfSections;
    uint32_t TimeDateStamp;
    uint32_t PointerToSymbolTable;
    uint32_t NumberOfSymbols;
    uint16_t SizeOfOptionalHeader;
    uint16_t Characteristics;
};

struct IMAGE_DATA_DIRECTORY {
    uint32_t   VirtualAddress;
    uint32_t   Size;
};

struct _IMAGE_OPTIONAL_HEADER {
    uint16_t   Magic;
    uint8_t    MajorLinkerVersion;
    uint8_t    MinorLinkerVersion;
    uint32_t   SizeOfCode;
    uint32_t   SizeOfInitializedData;
    uint32_t   SizeOfUninitializedData;
    uint32_t   AddressOfEntryPoint;
    uint32_t   BaseOfCode;
    uint32_t   BaseOfData;

    uint32_t   ImageBase;
    uint32_t   SectionAlignment;
    uint32_t   FileAlignment;
    uint16_t   MajorOperatingSystemVersion;
    uint16_t   MinorOperatingSystemVersion;
    uint16_t   MajorImageVersion;
    uint16_t   MinorImageVersion;
    uint16_t   MajorSubsystemVersion;
    uint16_t   MinorSubsystemVersion;
    uint32_t   Win32VersionValue;
    uint32_t   SizeOfImage;
    uint32_t   SizeOfHeaders;
    uint32_t   CheckSum;
    uint16_t   Subsystem;
    uint16_t   DllCharacteristics;
    uint32_t   SizeOfStackReserve;
    uint32_t   SizeOfStackCommit;
    uint32_t   SizeOfHeapReserve;
    uint32_t   SizeOfHeapCommit;
    uint32_t   LoaderFlags;
    uint32_t   NumberOfRvaAndSizes;
    IMAGE_DATA_DIRECTORY DataDirectory[16];
};

struct _IMAGE_IMPORT_DESCRIPTOR {
    union {
        uint32_t Characteristics;            // 0 for terminating null import descriptor
        uint32_t OriginalFirstThunk;         // RVA to original unbound IAT (PIMAGE_THUNK_DATA)
    } DUMMYUNIONNAME;

    uint32_t TimeDateStamp;                  // 0 if not bound,

    uint32_t ForwarderChain;                 // -1 if no forwarders
    uint32_t Name;
    uint32_t FirstThunk;                     // RVA to IAT (if bound this IAT has actual addresses)
};

class PE_Parser {
private:
	std::ifstream stream;
	DOS_FILE buffer;
public:
    PE_Parser() = default;
    PE_Parser(std::string filename) noexcept(false);
	void PrintData();
};