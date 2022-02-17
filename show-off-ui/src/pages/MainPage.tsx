import React, {useEffect, useState} from 'react';

import {makeStyles} from '@mui/styles';

import {ProcessState} from '../enums/ProcessState';
import DeleteButton from '../components/buttons/DeleteButton';
import {showOffApi} from '../api/show-off/show-off-api';
import {getHeightAndWidthForImage, resizeFile} from '../utils/ImageResizer';
import TextPopup from '../components/popups/TextPopup';
import VideoBackground from '../components/backgrounds/VideoBackground';
import VideoButton from '../components/buttons/VideoButton';
import {ImageWrapper} from '../types/ImageWrapper';
import FileButton from '../components/buttons/FileButton';
import ImageBackground from '../components/backgrounds/ImageBackground';

const IMAGE_HEIGHT = parseInt(process.env.REACT_APP_IMAGE_HEIGHT!);

const useStyles = makeStyles({
    container: {
        display: 'flex',
        justifyContent: 'center',
        width: '100vw',
        height: '100vh',
        position: 'relative',
    },
    recordButtonBox: {
        position: 'absolute',
        bottom: '50px',
        display: 'flex',
        justifyContent: 'center'
    },
    fileButton: {
        position: 'relative',
        left: '10px',
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
    const [sendAnimationFlag, setSendAnimationFlag] = useState<boolean>(false);
    const classes = useStyles();

    useEffect(() => {
        if (processState === ProcessState.SENDING) {
            resizeFile(image!, IMAGE_HEIGHT).then(resizedImage => {
                showOffApi.readFromImage(resizedImage).then(response => {
                    console.log(response);
                    setPopupData({open: true, text: response.text});
                    setSendAnimationFlag(false);
                    onDeleteButtonClick();
                })
            });
        } if (processState === ProcessState.SEND) {
            setSendAnimationFlag(true);
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

    const onFileButtonClick = (inputRef:  React.RefObject<HTMLInputElement>) => {
        if (processState === ProcessState.UPLOAD) {
            inputRef.current!.click();
        } else if (processState === ProcessState.SEND) {
            setProcessState(ProcessState.SENDING);
        }
    }

    const onFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files && event.target.files.length !== 0) {
            const image = event.target.files[0];
            getHeightAndWidthForImage(image).then(dimensions => {
                setImage({image: image, width: dimensions.width, height: dimensions.height, source: 'file'});
                setProcessState(ProcessState.SEND);
            });
        }
    }

    return (
        <div className={classes.container}>
            {processState === ProcessState.SEND &&
                <DeleteButton onClick={onDeleteButtonClick} className={classes.deleteButton}/>
            }
            {image?.source !== 'file' && <VideoBackground processState={processState} image={image} setImage={setImage}/>}
            {image?.source === 'file' && <ImageBackground image={image.image}/>}
            <div className={classes.recordButtonBox}>
                <VideoButton processState={processState} sendAnimationFlag={sendAnimationFlag} onClick={onVideoButtonClick}/>
                <FileButton sendAnimationFlag={sendAnimationFlag} onFileChange={onFileChange} onClick={onFileButtonClick} className={classes.fileButton}/>
            </div>
            <TextPopup open={popupData.open} text={popupData.text} handleClose={handleTextPopupClose}/>
        </div>
    );
}