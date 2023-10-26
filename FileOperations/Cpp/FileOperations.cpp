#include <iostream>
#include <filesystem>
#include <vector>
#include <string>
#include <Windows.h>
#include <locale>
#include <fstream>
#include <map>
#include "json.hpp"
#include "pugixml.hpp"
#include <zlib.h>


std::vector<std::string> GetListOfDrives() {
    std::vector<std::string> arrayOfDrives;
    LPSTR buffer = new char[MAX_PATH]();
    GetLogicalDriveStringsA(MAX_PATH, buffer);

    for (int i = 0; i < 100; i += 4)
        if (buffer[i] != (char)0) 
            arrayOfDrives.push_back(std::string{buffer[i], buffer[i+1], buffer[i+2]});

    delete[] buffer;
    return arrayOfDrives;
}

void PrintDriveInfo()
{
    std::vector<std::string> drives = GetListOfDrives();

    for (auto drive : drives) {
        std::cout << "Drive path: " << drive << '\n';

        std::filesystem::path path = drive;
        auto space = std::filesystem::space(path);

        char volumeName[MAX_PATH];
        char fileSystemName[MAX_PATH];
        char volumePaths[MAX_PATH];

        char* currentPath = new char[std::size(drive)]();
        strcpy(currentPath, drive.c_str());

        if (GetVolumeInformationA(currentPath, volumeName, MAX_PATH, NULL,
                                    NULL, NULL, fileSystemName, MAX_PATH)) {
            std::cout << "Volume Name: " << volumeName << '\n';
            std::cout << "File System: " << fileSystemName << '\n';
            std::cout << "Space capacity: " << space.capacity << "\n\n";
        } 
        delete[] currentPath;
    }
}

void OperateFiles()
{
    std::string str{};
    std::cin >> str;

    std::fstream stream;
    stream.open("file.txt",  std::ios::out);
    stream << str;
    stream.close();

    str.clear();

    stream.open("file.txt", std::ios::in);
    stream >> str;
    stream.close();

    std::cout << str;
    
    std::remove("file.txt");
}

void OperateJson()
{
    std::cout << "Type amount of keys/values: ";
    size_t amount;
    std::cin >> amount;

    std::map<std::string, std::string> dictionary;
    for (size_t i{}; i < amount; ++i)
    {
        std::cout << "Type key: ";
        std::string key;
        std::cin >> key;

        std::cout << "Type value: ";
        std::string value;
        std::cin >> value;

        dictionary[key] = value;
    }
    
    nlohmann::json data(dictionary);
    
    std::fstream file;
    file.open("file.json", std::ios::out);
    file << data.dump();
    file.close();

    file.open("file.json", std::ios::in);
    nlohmann::json parsed;
    auto res = parsed.parse(file);
    file.close();
    
    std::cout << res.dump();

    std::remove("file.json");
}

void OperateXml()
{
    pugi::xml_document file;
    auto res = file.load_file("file.xml");
    if (!res)
    {
        std::cout << res.description();
        return;
    }

    auto node = file.child("note");

    std::cout << "to value: " << node.child("to").attribute("atr").value();
    node.child("to").append_attribute("atr3").set_value("info3");
    file.save_file("file.xml");

    std::remove("file.xml");
}

void DecompressFile(char *infilename, char *outfilename)
 {
    gzFile infile = gzopen(infilename, "rb");
    FILE *outfile = fopen(outfilename, "wb");
    if (!infile || !outfile) return;

    char buffer[128];
    int num_read = 0;
    while ((num_read = gzread(infile, buffer, sizeof(buffer))) > 0) {
       fwrite(buffer, 1, num_read, outfile);
       }

    gzclose(infile);
    fclose(outfile);
}

void CompressFile(char *infilename, char *outfilename)
{
    FILE *infile = fopen(infilename, "rb");
    gzFile outfile = gzopen(outfilename, "wb");
    if (!infile || !outfile) return;

    char inbuffer[128];
    int num_read = 0;
    unsigned long total_read = 0;
    while ((num_read = fread(inbuffer, 1, sizeof(inbuffer), infile)) > 0) {
       gzwrite(outfile, inbuffer, num_read);
    }
    fclose(infile);
    gzclose(outfile);
}

void OperateZip()
{
    char str[] = {"file.txt"};
    char str2[] = {"file.zip"};
    char str3[] = {"file2.txt"};
    CompressFile(str, str2);
    DecompressFile(str2, str3);
}

int main()
{
    SetConsoleOutputCP(1251);
    SetConsoleCP(1251);

    std::ios_base::sync_with_stdio(false);
    std::cin.tie(NULL);

    PrintDriveInfo();
    OperateFiles();
    OperateJson();
    OperateXml();
    OperateZip();
    return 0;
}