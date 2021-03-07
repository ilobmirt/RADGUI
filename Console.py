from typing import Dict

#==================================================#
#RAD GUI Console
#==================================================#
class Console():
    OutputFilter: Dict[str,int] = {}
    WriteTags: Dict[str,int] = {}

    @classmethod
    def Write(cls,Input: str) -> None:

        CanWrite: bool = False
        WriteKey: str = ""
        WriteValue: int = 0

        #Determine if message is to be written in screen
        #No filter or Tags = All Permitted
        if(cls.OutputFilter != {}) and (cls.WriteTags != {}):
            for WriteKey, WriteValue in cls.WriteTags.items():
                if (WriteKey in cls.OutputFilter):
                    if (WriteValue <= cls.OutputFilter[WriteKey]):
                        CanWrite = True
                        break
        else:
            CanWrite = True
        
        if(CanWrite == True):
            print(Input)