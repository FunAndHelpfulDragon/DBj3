import aiofiles
import os


class File:
    def __init__(self):
        print("Setup file reading")

    async def ReadFile(self, filePath):
        async with aiofiles.open(filePath, 'r') as f:
            return await f.read()

    async def ReadLinesFile(self, filePath):
        async with aiofiles.open(filePath, 'r') as f:
            return await f.readlines()

    async def WriteFile(self, filePath, data):
        async with aiofiles.open(filePath, 'w') as f:
            await f.write(data)

    async def AppendFile(self, filePath, data):
        async with aiofiles.open(filePath, 'a') as f:
            await f.write(data)

    async def CheckForAdmin(self, filePath, user):
        lines = await self.ReadFile(filePath)
        lines = lines.split(",")
        for line in lines:
            if line.strip() == user:
                return True
        return False

    def CheckForFile(self, filePath):
        return os.path.exists(filePath)

    async def GetPositionInFile(self, filePath, user):
        lines = await self.ReadFile(filePath)
        lines = lines.split(",")
        Pos = 0
        for line in lines:
            if line.strip() == user:
                return Pos
            Pos = Pos + 1
        return Pos

    async def GetList(self, filePath):
        lines = await self.ReadFile(filePath)
        lines = lines.split(",")
        return lines

    def RemoveValueFromList(self, list, pos):
        list[pos] = ""
        return list

    def MakeListString(self, list):
        string = ""
        for value in list:
            if value != "":
                string = string + value.strip() + ","
        return string

    def MakeFile(self, dir, fileName, data):
        if self.CheckForFile(os.path.join(dir, fileName)):
            os.system(f"echo '{data}' > {os.path.join(dir, fileName)}")
        else:
            os.system(f"mkdir {dir}")
            os.system(f"echo '{data}' > {os.path.join(dir, fileName)}")
