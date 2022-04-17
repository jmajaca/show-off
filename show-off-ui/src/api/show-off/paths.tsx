const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

export const readFromImagePath = (): string =>
    `${BACKEND_URL}/read`;

export const textCorrectionPath = (): string =>
    `${BACKEND_URL}/correct-text`
