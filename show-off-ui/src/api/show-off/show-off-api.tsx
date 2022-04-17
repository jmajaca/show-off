import {readFromImagePath, textCorrectionPath} from './paths';
import {ReadFromImageResponse, TextCorrection} from './types';

async function readFromImage(image: File): Promise<ReadFromImageResponse> {
    const formData = new FormData();
    formData.set('image', image);
    const response = await fetch(readFromImagePath(), {
        method: 'POST',
        body: formData
    });
    return response.json();
}

async function sendTextCorrection(textCorrection: TextCorrection): Promise<boolean> {
    const response = await fetch(textCorrectionPath(), {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(textCorrection)
    });
    return response.status == 202;
}


export const showOffApi = {
    readFromImage,
    sendTextCorrection,
}