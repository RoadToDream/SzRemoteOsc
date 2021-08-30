#include "parseOutput.h"

void parseOutput(char* dataRec, char* data, int dataLength)
{
    short red_mask, green_mask, blue_mask, pixel;
    int pixLength;
    char red_value, green_value, blue_value, red, green, blue;
    int idxRaw = 0;
    
    red_mask = 0xF800;
    green_mask = 0x7E0;
    blue_mask = 0x1F;

    for(int idxData =0; idxData<int(dataLength/4);idxData++)
    {
        pixLength=*(unsigned short int*)(dataRec+idxData*4);
        pixel=dataRec[idxData*4+3]<<8|(0x00FF&dataRec[idxData*4+2]);
        red_value = (pixel & red_mask) >> 11;
        green_value = (pixel & green_mask) >> 5;
        blue_value = (pixel & blue_mask);
        red   = red_value << 3;
        green = green_value << 2;
        blue  = blue_value << 3;
        for(int idxSub=0; idxSub<pixLength; idxSub++)
        {
            data[idxRaw+idxSub*3]=red;
            data[idxRaw+idxSub*3+1]=green;
            data[idxRaw+idxSub*3+2]=blue;
        }
        idxRaw+=pixLength*3;
    }
}