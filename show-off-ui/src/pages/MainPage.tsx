import React, {useState} from 'react';

import {makeStyles} from '@mui/styles';

import RecordButton from '../components/RecordButton';
import RecordBackground from '../components/RecordBackground';
import {ProcessState} from '../enums/ProcessState';
import DeleteButton from '../components/DeleteButton';

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

export default function MainPage() {

    const [image, setImage] = useState<File>();
    const [processState, setProcessState] = useState<ProcessState>(ProcessState.UPLOAD);
    const classes = useStyles();

    return (
        <div className={classes.container}>
            {processState === ProcessState.SEND &&
                <DeleteButton setProcessState={setProcessState} setImage={setImage} className={classes.deleteButton}/>
            }
            <RecordButton processState={processState} setProcessState={setProcessState} setImage={setImage} className={classes.recordButton}/>
            <RecordBackground image={image}/>
        </div>
    );
}