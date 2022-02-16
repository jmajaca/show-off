import React, {useEffect, useState} from 'react';

import {makeStyles} from '@mui/styles';
import {ProcessState} from '../enums/ProcessState';
import DeleteButton from '../components/DeleteButton';
import {showOffApi} from '../api/show-off/show-off-api';
import {resizeFile} from '../utils/ImageResizer';
import TextPopup from '../components/TextPopup';
import VideoBackground from '../components/VideoBackground';
import VideoButton from '../components/VideoButton';
import {ImageWrapper} from '../types/ImageWrapper';

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

    const [image, setImage] = useState<ImageWrapper | undefined>();
    const [processState, setProcessState] = useState<ProcessState>(ProcessState.UPLOAD);
    const [popupData, setPopupData] = useState<TextPopupData>({open: false, text: ''});
    const classes = useStyles();

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

    const handleTextPopupClose = (affirmative: boolean) => {
        if (affirmative) {
            console.log('process');
        }
        setPopupData({open: false, text: popupData.text});
    }

    const onVideoButtonClick = () => {
        switch (processState) {
            case ProcessState.UPLOAD:
                setProcessState(ProcessState.SEND);
                break;
            case ProcessState.SEND:
                setProcessState(ProcessState.SENDING);
                break;
            default:
                break;
        }
    }

    const onDeleteButtonClick = () => {
        setProcessState(ProcessState.UPLOAD);
        setImage(undefined);
    }

    return (
        <div className={classes.container}>
            {processState === ProcessState.SEND &&
                <DeleteButton onClick={onDeleteButtonClick} className={classes.deleteButton}/>
            }
            <VideoBackground processState={processState} setImage={setImage}/>
            <VideoButton processState={processState} onClick={onVideoButtonClick} className={classes.recordButton}/>
            <TextPopup open={popupData.open} text={popupData.text} handleClose={handleTextPopupClose}/>
        </div>
    );
}