import React, {createRef, LegacyRef, useEffect, useState} from 'react';

import {makeStyles} from '@mui/styles';

import RecordButton from '../components/RecordButton';
import RecordBackground from '../components/RecordBackground';
import {ProcessState} from '../enums/ProcessState';
import DeleteButton from '../components/DeleteButton';
import {showOffApi} from '../api/show-off/show-off-api';
import {resizeFile} from '../utils/ImageResizer';
import TextPopup from '../components/TextPopup';
import VideoBackground from '../components/VideoBackground';

const IMAGE_HEIGHT = parseInt(process.env.REACT_APP_IMAGE_HEIGHT!);

const useStyles = makeStyles({
    container: {
        display: 'flex',
        justifyContent: 'center',
        width: '100vw',
        height: '100vh',
        position: 'relative',
    },
    recordButton: {
        position: 'absolute',
        bottom: '50px'
    },
    deleteButton: {
        position: 'absolute',
        top: '10px',
        right: '10px',
    }
});

export type TextPopupData = {
    open: boolean,
    text: string,
}

export default function MainPage() {

    const [image, setImage] = useState<File>();
    const [processState, setProcessState] = useState<ProcessState>(ProcessState.SEND);
    const [popupData, setPopupData] = useState<TextPopupData>({open: false, text: ''});
    const classes = useStyles();

    const handleTextPopupClose = (affirmative: boolean) => {
        if (affirmative) {
            console.log('process');
        }
        setPopupData({open: false, text: popupData.text});
    }

    useEffect(() => {
        if (processState === ProcessState.SENDING) {
            resizeFile(image!, IMAGE_HEIGHT).then(resizedImage => {
                showOffApi.readFromImage(resizedImage).then(response => {
                    console.log(response);
                    setProcessState(ProcessState.UPLOAD);
                    setPopupData({open: true, text: response.text});
                })
            });
        }
    }, [processState]);

    return (
        <div className={classes.container}>
            {processState === ProcessState.SEND &&
                <DeleteButton setProcessState={setProcessState} setImage={setImage} className={classes.deleteButton}/>
            }
            <RecordButton processState={processState} setProcessState={setProcessState} setImage={setImage} className={classes.recordButton}/>
            <VideoBackground image={image} setImage={setImage}/>
            <TextPopup open={popupData.open} text={popupData.text} handleClose={handleTextPopupClose}/>
        </div>
    );
}