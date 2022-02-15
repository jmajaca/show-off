import {readFromImagePath} from './paths';
import {ReadFromImageResponse} from './types';

async function readFromImage(image: File): Promise<ReadFromImageResponse> {
    const formData = new FormData();
    formData.set('image', image);
    const response = await fetch(readFromImagePath(), {
        method: 'POST',
        body: formData
    });
    return response.json();
}


export const showOffApi = {
    readFromImage,
}